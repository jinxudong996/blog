/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-06-03 10:35:00
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-07 11:22:24
 * @FilePath: \notes\src\app\[id]\page.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import Note from "@/components/Note";
import { getNote } from "@/lib/redis";

export default async function Page({ params }) {
  // 动态路由 获取笔记 id
  const { id: noteId } = await params;
  const note = await getNote(noteId);

  // 为了让 Suspense 的效果更明显
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  await sleep(1000);
  debugger;
  if (note == null) {
    return (
      <div className="note--empty-state">
        <span className="note-text--empty-state">
          Click a note on the left to view something! 🥺
        </span>
      </div>
    );
  }

  return <Note noteId={noteId} note={note} />;
}
