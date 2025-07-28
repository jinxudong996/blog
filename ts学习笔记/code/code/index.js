import * as parser from "@babel/parser";

const code = `function square(n) {
  return n * n;
}`;

try {
  const ast = parser.parse(code, { sourceType: "module" });
  console.log(ast);
} catch (e) {
  console.error("解析失败:", e.message);
}
