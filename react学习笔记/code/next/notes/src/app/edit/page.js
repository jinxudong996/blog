/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-06-03 10:35:59
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-20 14:59:22
 * @FilePath: \notes\src\app\edit\page.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import NoteEditor from "@/components/NoteEditor";

export default async function EditPage() {
  return <NoteEditor note={null} initialTitle="Untitled" initialBody="" />;
}