import assert from "node:assert/strict";
import {
  cpSync,
  existsSync,
  mkdtempSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
  rmSync,
  renameSync,
} from "node:fs";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
const root = resolve(import.meta.dirname, "..");
const p = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));
const t = mkdtempSync(join(tmpdir(), "suite-ts-assets-"));
try {
  if (process.argv[2] === "pack") {
    const rows = JSON.parse(
      execFileSync(
        "npm",
        ["pack", "--ignore-scripts", "--json", "--pack-destination", t],
        { cwd: root, encoding: "utf8" },
      ),
    );
    const consumer = join(t, "consumer");
    mkdirSync(consumer);
    writeFileSync(
      join(consumer, "package.json"),
      JSON.stringify({ private: true, type: "module" }),
    );
    execFileSync(
      "npm",
      [
        "install",
        "--offline",
        "--ignore-scripts",
        "--no-audit",
        "--no-fund",
        join(t, rows[0].filename),
      ],
      { cwd: consumer, stdio: "pipe" },
    );
    execFileSync(
      process.execPath,
      [
        "--input-type=module",
        "-e",
        `import {component} from '${p.name}'; if(component!=='__COMPONENT_NAME__') throw Error('wrong import');`,
      ],
      { cwd: consumer, stdio: "inherit" },
    );
    writeFileSync(
      join(consumer, "check.ts"),
      `import {component} from '${p.name}'; const value: string = component; void value;`,
    );
    execFileSync(
      process.execPath,
      [
        join(root, "node_modules/typescript/bin/tsc"),
        "--noEmit",
        "--strict",
        "--module",
        "NodeNext",
        "--moduleResolution",
        "NodeNext",
        "check.ts",
      ],
      { cwd: consumer, stdio: "inherit" },
    );
  } else if (process.argv[2] === "conda") {
    const prefix = join(t, "prefix"),
      target = join(prefix, "share", "__COMPONENT_NAME__");
    mkdirSync(target, { recursive: true });
    cpSync(join(root, "dist"), join(target, "dist"), { recursive: true });
    for (const name of ["LICENSE", "README.md"])
      cpSync(join(root, name), join(target, name));
    const metadata = {
      name: p.name,
      version: p.version,
      type: p.type,
      license: p.license,
      exports: p.exports,
      types: p.types,
    };
    writeFileSync(join(target, "package.json"), JSON.stringify(metadata));
    const names = [
      "LICENSE",
      "README.md",
      "package.json",
      ...readdirSync(join(target, "dist")).map((n) => `dist/${n}`),
    ].sort();
    const files = names.map((path) => ({
      path,
      sha256: createHash("sha256")
        .update(readFileSync(join(target, path)))
        .digest("hex"),
    }));
    writeFileSync(
      join(target, "asset-manifest.json"),
      JSON.stringify({
        schemaVersion: 1,
        package: "__COMPONENT_NAME__",
        version: p.version,
        files,
      }),
    );
    const moved = join(t, "moved");
    renameSync(prefix, moved);
    const installed = join(moved, "share", "__COMPONENT_NAME__");
    for (const row of files)
      assert.equal(
        createHash("sha256")
          .update(readFileSync(join(installed, row.path)))
          .digest("hex"),
        row.sha256,
      );
    assert.equal(
      (await import(pathToFileURL(join(installed, "dist/index.js")).href))
        .component,
      "__COMPONENT_NAME__",
    );
    if (process.argv[3]) {
      const output = resolve(process.argv[3]);
      assert.equal(
        existsSync(output),
        false,
        "Refuse an existing receiver output.",
      );
      cpSync(moved, output, { recursive: true });
    }
  } else throw new Error("Select pack or conda receiving.");
  console.log(
    "Independent asset consumer passed; no public or Conda archive qualification claimed.",
  );
} finally {
  rmSync(t, { recursive: true, force: true });
}
