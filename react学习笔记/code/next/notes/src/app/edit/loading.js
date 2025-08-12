/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-08-08 10:26:47
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-08 10:26:59
 * @FilePath: \notes\src\app\edit\loading.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
export default function EditSkeleton() {
  return (
    <div
      className="note-editor skeleton-container"
      role="progressbar"
      aria-busy="true"
    >
      <div className="note-editor-form">
        <div className="skeleton v-stack" style={{ height: '3rem' }} />
        <div className="skeleton v-stack" style={{ height: '100%' }} />
      </div>
      <div className="note-editor-preview">
        <div className="note-editor-menu">
          <div
            className="skeleton skeleton--button"
            style={{ width: '8em', height: '2.5em' }}
          />
          <div
            className="skeleton skeleton--button"
            style={{ width: '8em', height: '2.5em', marginInline: '12px 0' }}
          />
        </div>
        <div
          className="note-title skeleton"
          style={{ height: '3rem', width: '65%', marginInline: '12px 1em' }}
        />
        <div className="note-preview">
          <div className="skeleton v-stack" style={{ height: '1.5em' }} />
          <div className="skeleton v-stack" style={{ height: '1.5em' }} />
          <div className="skeleton v-stack" style={{ height: '1.5em' }} />
          <div className="skeleton v-stack" style={{ height: '1.5em' }} />
          <div className="skeleton v-stack" style={{ height: '1.5em' }} />
        </div>
      </div>
    </div>
  )
}

