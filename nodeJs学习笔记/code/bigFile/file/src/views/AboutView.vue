<template>
  <div class="about">
    <input type="file" @change="handleFileChange" />
    <el-button @click="handleUpload">upload</el-button>
  </div>
</template>

<script>
import axios from 'axios';

const SIZE = 10 * 1024 * 1024;

export default {
  name: "file",
  data: () => ({
    container: {
      file: null,
    },
  }),
  methods: {
    handleFileChange(e) {
      debugger
      const [file] = e.target.files;
      if (!file) return;
      this.container.file = file;
    },
    // 生成文件切片
    createFileChunk(file, size = SIZE) {
      debugger
      const fileChunkList = [];
      let cur = 0;
      while (cur < file.size) {
        fileChunkList.push({ file: file.slice(cur, cur + size) });
        cur += size;
      }
      return fileChunkList;
    },
    // 上传切片
    async uploadChunks() {
      const requestList = this.data
        .map(({ chunk, hash }) => {
          const formData = new FormData();
          formData.append("chunk", chunk);
          formData.append("hash", hash);
          formData.append("filename", this.container.file.name || hash);
          return { formData };
        })
        .map(({ formData }) =>
          axios({
            url: "http://localhost:3000/upload",
            data: formData,
            method:'POST'
          })
        );
      // 并发请求
      await Promise.all(requestList);
    },
    async handleUpload() {
      debugger
      if (!this.container.file) return;
      const fileChunkList = this.createFileChunk(this.container.file);
      this.data = fileChunkList.map(({ file }, index) => ({
        chunk: file,
        // 文件名  数组下标
        hash: this.container.file.name + "-" + index,
      }));
      console.log(this.data)
      debugger
      await this.uploadChunks();
    },

    // await this.uploadChunks();
  },
};
</script>
