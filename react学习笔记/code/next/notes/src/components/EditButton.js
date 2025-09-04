/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-08-20 14:45:56
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-20 14:46:09
 * @FilePath: \notes\src\components\EditButton.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
// components/EditButton.js
import Link from "next/link";

export default function EditButton({ noteId, children }) {
  const isDraft = noteId == null;
  return (
    <Link href={`/edit/${noteId || ""}`} className="link--unstyled">
      <button
        className={[
          "edit-button",
          isDraft ? "edit-button--solid" : "edit-button--outline",
        ].join(" ")}
        role="menuitem"
      >
        {children}
      </button>
    </Link>
  );
}
