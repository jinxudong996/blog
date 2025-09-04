/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-01-27
 * @Description: MySQL 数据库连接配置
 */

import mysql from "mysql2/promise";

// MySQL 连接配置
const dbConfig = {
  host: "118.31.222.50",
  port: 3307,
  user: "root",
  password: "my-mysql",
  database: "text", // 默认连接到 text 数据库
};

// 创建连接池以提高性能
const pool = mysql.createPool({
  ...dbConfig,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// 初始化数据库和表
export async function initDatabase() {
  let connection;

  try {
    // 先连接到 MySQL 服务器（不指定数据库）
    connection = await mysql.createConnection({
      host: dbConfig.host,
      port: dbConfig.port,
      user: dbConfig.user,
      password: dbConfig.password,
    });

    // 检查并创建 text 数据库
    await connection.execute(`
      CREATE DATABASE IF NOT EXISTS text 
      CHARACTER SET utf8mb4 
      COLLATE utf8mb4_unicode_ci
    `);

    console.log("数据库 text 检查/创建完成");

    // 选择 text 数据库
    await connection.execute("USE text");

    // 创建 todolist 表
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS todolist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    `);

    console.log("表 todolist 检查/创建完成");

    return true;
  } catch (error) {
    console.error("数据库初始化失败:", error);
    throw error;
  } finally {
    if (connection) {
      await connection.end();
    }
  }
}

// 获取数据库连接
export async function getConnection() {
  try {
    // 确保数据库和表已初始化
    await initDatabase();
    return pool;
  } catch (error) {
    console.error("获取数据库连接失败:", error);
    throw error;
  }
}

export default pool;
