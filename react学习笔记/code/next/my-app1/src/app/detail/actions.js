/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-08-20 15:56:41
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-09-02 14:19:18
 * @FilePath: \my-app1\src\app\detail\actions.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
"use server";

import { revalidatePath } from "next/cache";

const data = ["阅读", "写作", "冥想"];

export async function findToDos() {
  return data;
}

export async function createToDo(formData) {
  const todo = formData.get("todo");
  data.push(todo);
  revalidatePath("/detail");
}
