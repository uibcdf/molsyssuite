import { readFileSync, lstatSync, realpathSync } from "node:fs";
import { resolve, relative, isAbsolute } from "node:path";
import ts from "typescript";
const root = resolve(import.meta.dirname, "..");
const selector = process.argv[2] ?? "";
if (!/^tests\/(?:[a-zA-Z0-9_-]+\/)*[a-zA-Z0-9_-]+\.test\.mjs$/.test(selector))
  throw new Error("Use one safe tests/*.test.mjs module selector.");
const path = resolve(root, selector);
if (
  isAbsolute(relative(root, path)) ||
  relative(root, path).startsWith("..") ||
  realpathSync(path) !== path ||
  !lstatSync(path).isFile() ||
  lstatSync(path).isSymbolicLink()
)
  throw new Error("Guard must be a regular local module.");
const source = ts.createSourceFile(
  path,
  readFileSync(path, "utf8"),
  ts.ScriptTarget.Latest,
  true,
  ts.ScriptKind.JS,
);
if (source.parseDiagnostics.length) throw new Error("Guard cannot be parsed.");
const names = new Set();
for (const statement of source.statements) {
  if (
    !ts.isImportDeclaration(statement) ||
    statement.moduleSpecifier.text !== "node:test"
  )
    continue;
  if (statement.importClause?.name) names.add(statement.importClause.name.text);
  for (const element of statement.importClause?.namedBindings?.elements ?? [])
    if ((element.propertyName?.text ?? element.name.text) === "test")
      names.add(element.name.text);
}
let count = 0;
for (const statement of source.statements) {
  if (
    !ts.isExpressionStatement(statement) ||
    !ts.isCallExpression(statement.expression)
  )
    continue;
  const call = statement.expression;
  if (
    ts.isIdentifier(call.expression) &&
    names.has(call.expression.text) &&
    ts.isStringLiteral(call.arguments[0]) &&
    call.arguments.length >= 2
  )
    count++;
}
if (!count) throw new Error("No statically declared node:test guard resolves.");
console.log(
  `Addressable Node module: ${count} static declarations; relevance/execution remain separate.`,
);
