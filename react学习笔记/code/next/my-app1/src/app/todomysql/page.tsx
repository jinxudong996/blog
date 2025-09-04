/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-01-27
 * @Description: MySQL 版本的 Todo 页面
 */

import { findToDos, createToDo } from './actions';

export default async function Page() {
  const todos = await findToDos();
  
  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        Todo List (MySQL版)
      </h1>
      
      {/* 添加新待办事项的表单 */}
      <form action={createToDo} className="mb-6">
        <div className="flex gap-2">
          <input 
            type="text" 
            name="todo" 
            placeholder="输入新的待办事项..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
          <button 
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          >
            添加
          </button>
        </div>
      </form>

      {/* 待办事项列表 */}
      <div className="space-y-2">
        <h2 className="text-lg font-semibold text-gray-700 mb-3">
          待办事项列表 ({todos.length} 项)
        </h2>
        
        {todos.length === 0 ? (
          <p className="text-gray-500 text-center py-4">
            暂无待办事项，添加一个开始吧！
          </p>
        ) : (
          <ul className="space-y-2">
            {todos.map((todo, i) => (
              <li 
                key={i} 
                className="flex items-center p-3 bg-gray-50 rounded-md border border-gray-200"
              >
                <span className="flex-1 text-gray-800">{todo}</span>
                <span className="text-sm text-gray-500 ml-2">
                  #{i + 1}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* 说明信息 */}
      <div className="mt-6 p-3 bg-blue-50 rounded-md border border-blue-200">
        <p className="text-sm text-blue-700">
          <strong>MySQL版本特性：</strong>
          <br />
          • 数据持久化存储在远程 MySQL 数据库
          <br />
          • 自动创建 text 数据库和 todolist 表
          <br />
          • 防止重复添加相同的待办事项
        </p>
      </div>
    </div>
  );
}
