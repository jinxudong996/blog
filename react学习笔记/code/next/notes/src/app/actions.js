/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-08-20 15:16:42
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-20 15:16:54
 * @FilePath: \notes\src\app\actions.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
"use server";

import { redirect } from "next/navigation";
import { addNote, updateNote, delNote } from "@/lib/redis";

export async function saveNote(noteId, title, body) {
  const data = JSON.stringify({
    title,
    content: body,
    updateTime: new Date(),
  });

  if (noteId) {
    updateNote(noteId, data);
    redirect(`/note/${noteId}`);
  } else {
    const res = await addNote(data);
    redirect(`/note/${res}`);
  }
}

export async function deleteNote(noteId) {
  delNote(noteId);
  redirect("/");
}
