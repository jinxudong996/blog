/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-06-16 11:27:41
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-06-16 15:44:21
 * @FilePath: \cursor\001.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/**
 * 深拷贝工具方法
 * @param source 需要拷贝的源数据
 * @returns 拷贝后的新数据
 */
export function deepClone<T>(source: T): T {
  // 处理 null 和 undefined
  if (source == null) {
    return source;
  }

  // 处理日期对象
  if (source instanceof Date) {
    return new Date(source.getTime()) as any;
  }

  // 处理正则表达式
  if (source instanceof RegExp) {
    return new RegExp(source.source, source.flags) as any;
  }

  // 处理数组
  if (Array.isArray(source)) {
    return source.map((item) => deepClone(item)) as any;
  }

  // 处理对象
  if (typeof source === "object") {
    const target = {} as any;
    for (const key in source) {
      if (Object.prototype.hasOwnProperty.call(source, key)) {
        target[key] = deepClone(source[key]);
      }
    }
    return target;
  }

  // 处理基本类型
  return source;
}

// 使用示例
const example = {
  name: "test",
  age: 25,
  date: new Date(),
  arr: [1, 2, { a: 1 }],
  obj: {
    foo: "bar",
    nested: {
      value: 123,
    },
  },
};

const cloned = deepClone(example);
console.log(cloned);
