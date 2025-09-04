/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-06-12 17:18:20
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-20 15:12:10
 * @FilePath: \notes\src\components\Note.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import dayjs from "dayjs";
import NotePreview from "@/components/NotePreview";
import EditButton from "@/components/EditButton";
export default function Note({ noteId, note }) {
  const { title, content, updateTime } = note;

  return (
    <div className="note">
      <div className="note-header">
        <h1 className="note-title">{title}</h1>
        <div className="note-menu" role="menubar">
          <small className="note-updated-at" role="status">
            Last updated on {dayjs(updateTime).format("YYYY-MM-DD hh:mm:ss")}
          </small>
          <EditButton noteId={noteId}>Edit</EditButton>
        </div>
      </div>
      <NotePreview>{content}</NotePreview>
    </div>
  );
}
