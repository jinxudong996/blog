const express = require("express");
const fse = require("fs-extra");

const fs = require('fs').promises; // 确保导入了 fs.promises
const path = require('path');
const formidable = require('formidable');

const app = express();
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

const pipeStream = (path, writeStream) =>
  new Promise(resolve => {
    const readStream = fse.createReadStream(path);
    readStream.on("end", () => {
      fse.unlinkSync(path);
      resolve();
    });
    readStream.pipe(writeStream);
  });

const mergeFileChunk = async (filePath, filename, size) => {
  const chunkDir = path.resolve(UPLOAD_DIR, 'chunkDir' + filename);
  const chunkPaths = await fse.readdir(chunkDir);
  chunkPaths.sort((a, b) => a.split("-")[1] - b.split("-")[1]);
  await Promise.all(
    chunkPaths.map((chunkPath, index) =>
      pipeStream(
        path.resolve(chunkDir, chunkPath),
        fse.createWriteStream(filePath, {
          start: index * size,
        })
      )
    )
  );
  fse.rmdirSync(chunkDir);
};

app.use(express.json());

app.options("*", (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  res.status(200).end();
});

app.post("/upload", async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  const form = new formidable.IncomingForm();
  form.parse(req, async (err, fields, files) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ message: "Internal Server Error" });
    }

    const chunk = Array.isArray(files.chunk) ? files.chunk[0] : files.chunk;
    if (!chunk) {
      return res.status(400).json({ message: "File chunk is missing" });
    }

    const chunkPath = chunk.path;
    const hash = Array.isArray(fields.hash) ? fields.hash[0] : fields.hash; // 检查hash是否是数组
    const filename = fields.filename;
    const chunkDir = path.resolve(UPLOAD_DIR, "chunkDir" + filename);

    try {
      await fs.mkdir(chunkDir, { recursive: true });

      const filePath = path.resolve(chunkDir, hash); // 使用字符串类型的hash
      await fs.rename(chunkPath, filePath);

      res.json({ message: "Received file chunk" });
    } catch (fileErr) {
      console.error(fileErr);
      return res.status(500).json({ message: "Error processing file chunk" });
    }
  });
});

app.post("/merge", async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "*");
  const data = await resolvePost(req);
  const { filename, size } = data;
  const filePath = path.resolve(UPLOAD_DIR, `${filename}`);
  await mergeFileChunk(filePath, filename, size);
  res.json({
    code: 0,
    message: "file merged success"
  });
});

app.listen(3000, () => console.log("listening port 3000"));
