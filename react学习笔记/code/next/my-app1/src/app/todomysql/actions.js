/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-01-27
 * @Description: MySQL 版本的 Todo Server Actions
 */
"use server";

import { revalidatePath } from "next/cache";
import { getConnection } from "../../lib/mysql";

// 获取所有待办事项
export async function findToDos() {
  try {
    const connection = await getConnection();
    const [rows] = await connection.execute(
      "SELECT id, text, created_at, updated_at FROM todolist ORDER BY created_at DESC"
    );

    // 返回文本数组，保持与原版本兼容
    return rows.map((row) => row.text);
  } catch (error) {
    console.error("获取待办事项失败:", error);
    // 返回默认数据，避免页面崩溃
    return ["阅读", "写作", "冥想"];
  }
}

// 创建新的待办事项
export async function createToDo(formData) {
  try {
    const todo = formData.get("todo");

    // 验证输入
    if (!todo || todo.trim() === "") {
      console.error("待办事项不能为空");
      return;
    }

    const connection = await getConnection();

    // 检查是否已存在相同的待办事项
    const [existing] = await connection.execute(
      "SELECT id FROM todolist WHERE text = ? LIMIT 1",
      [todo.trim()]
    );

    if (existing.length > 0) {
      console.log("待办事项已存在:", todo);
      return;
    }

    // 插入新的待办事项
    await connection.execute("INSERT INTO todolist (text) VALUES (?)", [
      todo.trim(),
    ]);

    console.log("成功添加待办事项:", todo);

    // 重新验证页面缓存
    revalidatePath("/todomysql");
  } catch (error) {
    console.error("创建待办事项失败:", error);
  }
}

// 获取详细的待办事项信息（包含ID和时间戳）
export async function getToDosWithDetails() {
  try {
    const connection = await getConnection();
    const [rows] = await connection.execute(
      "SELECT id, text, created_at, updated_at FROM todolist ORDER BY created_at DESC"
    );

    return rows.map((row) => ({
      id: row.id,
      text: row.text,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    }));
  } catch (error) {
    console.error("获取详细待办事项失败:", error);
    return [];
  }
}

// 删除待办事项
export async function deleteToDo(id) {
  try {
    const connection = await getConnection();
    await connection.execute("DELETE FROM todolist WHERE id = ?", [id]);

    console.log("成功删除待办事项 ID:", id);
    revalidatePath("/todomysql");
  } catch (error) {
    console.error("删除待办事项失败:", error);
  }
}
