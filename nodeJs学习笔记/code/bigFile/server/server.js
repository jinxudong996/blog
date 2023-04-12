const http = require("http");
const path = require("path");
const fse = require("fs-extra");

const server = http.createServer();
const UPLOAD_DIR = path.resolve(__dirname, "..", "target");

const resolvePost = req =>
  new Promise(resolve => {
    let chunk = "";
    req.on("data", data => {
      chunk += data;
    });
    req.on("end", () => {
      resolve(JSON.parse(chunk));
    });
  });

// 写入文件流
const pipeStream = (path, writeStream) =>
  new Promise(resolve => {
    const readStream = fse.createReadStream(path);
    readStream.on("end", () => {
      fse.unlinkSync(path);
      resolve();
    });
    readStream.pipe(writeStream);
  });

// 合并切片
const mergeFileChunk = async (filePath, filename, size) => {
  const chunkDir = path.resolve(UPLOAD_DIR, 'chunkDir' + filename);
  const chunkPaths = await fse.readdir(chunkDir);
  // 根据切片下标进行排序
  // 否则直接读取目录的获得的顺序会错乱
  chunkPaths.sort((a, b) => a.split("-")[1] - b.split("-")[1]);
  // 并发写入文件
  await Promise.all(
    chunkPaths.map((chunkPath, index) =>
      pipeStream(
        path.resolve(chunkDir, chunkPath),
        // 根据 size 在指定位置创建可写流
        fse.createWriteStream(filePath, {
          start: index * size,
        })
      )
    )
  );
  // 合并后删除保存切片的目录
  fse.rmdirSync(chunkDir);
};

server.on("request", async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  if (req.method === "OPTIONS") {
    res.status = 200;

    res.end();
    return;
  }

  if (req.url === "/merge") {
    const data = await resolvePost(req);
    const { filename, size } = data;
    const filePath = path.resolve(UPLOAD_DIR, `${filename}`);
    await mergeFileChunk(filePath, filename);
    res.end(
      JSON.stringify({
        code: 0,
        message: "file merged success"
      })
    );
  }

});

server.listen(3000, () => console.log("listening port 3000"));
