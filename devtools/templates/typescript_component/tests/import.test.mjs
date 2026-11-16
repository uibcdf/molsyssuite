import test from "node:test";
import assert from "node:assert/strict";
import { component } from "../dist/index.js";
test("public module has the declared source identity", () => {
  assert.equal(component, "__COMPONENT_NAME__");
});
