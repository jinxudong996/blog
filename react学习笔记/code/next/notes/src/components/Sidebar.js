/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-06-03 10:40:33
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-20 14:47:00
 * @FilePath: \notes\src\components\Sidebar.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import React from "react";
import Link from "next/link";
import { getAllNotes } from "@/lib/redis";
import SidebarNoteList from "@/components/SidebarNoteList";
import EditButton from "@/components/EditButton";

export default async function Sidebar() {
  const notes = await getAllNotes();
  return (
    <>
      <section className="col sidebar">
        <Link href={"/"} className="link--unstyled">
          <section className="sidebar-header">
            <img
              className="logo"
              src="/logo.svg"
              width="22px"
              height="20px"
              alt=""
              role="presentation"
            />
            <strong>React Notes</strong>
          </section>
        </Link>
        <section className="sidebar-menu" role="menubar">
          <EditButton noteId={null}>New</EditButton>
        </section>
        <nav>
          <SidebarNoteList notes={notes} />
        </nav>
      </section>
    </>
  );
}
