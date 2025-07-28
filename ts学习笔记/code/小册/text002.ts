type ReturnType1<func extends (...args: any) => any> = func extends (
  ...args
) => infer R
  ? R
  : any;
// type ReturnType1<T> = T extends (...args: any) => infer R ? R : never;
function getRandom(): number {
  return Math.random();
}
// 结果：number
type result1 = ReturnType1<typeof getRandom>;

type Tree = [
  {
    label: string;
    children?: Tree[];
  }
];

let treeData = ref<Tree[]>([]);
