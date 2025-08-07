/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-08-07 11:21:28
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-07 11:21:50
 * @FilePath: \notes\src\app\[id]\loading.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
export default function NoteSkeleton() {
  return (
    <div
      className="note skeleton-container"
      role="progressbar"
      aria-busy="true"
    >
      <div className="note-header">
        <div
          className="note-title skeleton"
          style={{ height: "3rem", width: "65%", marginInline: "12px 1em" }}
        />
        <div
          className="skeleton skeleton--button"
          style={{ width: "8em", height: "2.5em" }}
        />
      </div>
      <div className="note-preview">
        <div className="skeleton v-stack" style={{ height: "1.5em" }} />
        <div className="skeleton v-stack" style={{ height: "1.5em" }} />
        <div className="skeleton v-stack" style={{ height: "1.5em" }} />
        <div className="skeleton v-stack" style={{ height: "1.5em" }} />
        <div className="skeleton v-stack" style={{ height: "1.5em" }} />
      </div>
    </div>
  );
}
