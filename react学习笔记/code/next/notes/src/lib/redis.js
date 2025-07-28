import Redis from "ioredis";

// 修改: 添加 Redis 数据库连接配置
const redis = new Redis({
  host: process.env.REDIS_HOST || "127.0.0.1", // Redis 主机地址，默认为本地
  port: process.env.REDIS_PORT || 6379, // Redis 端口，默认为 6379
  password: process.env.REDIS_PASSWORD || null, // Redis 密码，默认为空
  db: process.env.REDIS_DB || 0, // Redis 数据库索引，默认为 0
});

const initialData = {
  1702459181837:
    '{"title":"sunt aut","content":"quia et suscipit suscipit recusandae","updateTime":"2023-12-13T09:19:48.837Z"}',
  1702459182837:
    '{"title":"qui est","content":"est rerum tempore vitae sequi sint","updateTime":"2023-12-13T09:19:48.837Z"}',
  1702459188837:
    '{"title":"ea molestias","content":"et iusto sed quo iure","updateTime":"2023-12-13T09:19:48.837Z"}',
};

export async function getAllNotes() {
  const data = await redis.hgetall("notes");
  if (Object.keys(data).length == 0) {
    await redis.hset("notes", initialData);
  }
  return await redis.hgetall("notes");
}

export async function addNote(data) {
  const uuid = Date.now().toString();
  await redis.hset("notes", [uuid], data);
  return uuid;
}

export async function updateNote(uuid, data) {
  await redis.hset("notes", [uuid], data);
}

export async function getNote(uuid) {
  return JSON.parse(await redis.hget("notes", uuid));
}

export async function delNote(uuid) {
  return redis.hdel("notes", uuid);
}

export default redis;
