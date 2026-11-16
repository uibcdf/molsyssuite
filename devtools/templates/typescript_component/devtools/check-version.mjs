import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
const root = new URL("../", import.meta.url);
const p = JSON.parse(readFileSync(new URL("package.json", root), "utf8"));
const l = JSON.parse(readFileSync(new URL("package-lock.json", root), "utf8"));
assert.match(p.version, /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/);
assert.equal(l.version, p.version);
assert.equal(l.packages[""].version, p.version);
if (process.env.GITHUB_REF_TYPE === "tag")
  assert.equal(process.env.GITHUB_REF_NAME, p.version);
