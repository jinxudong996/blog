const path = require('path');
const serverBundle = path.resolve(process.cwd(), 'serverDist', 'vue-ssr-server-bundle.json');
const {createBundleRenderer} = require('vue-server-renderer');
const clientManifestPath = path.resolve(process.cwd(), 'dist', 'vue-ssr-client-manifest.json');
const clientManifest = require(clientManifestPath);

const template = fs.readFileSync(path.resolve(__dirname, 'index.html'), 'utf-8');
const renderer = createBundleRenderer(serverBundle, {
    template,  // 使用HTML模板
    clientManifest // 将客户端的构建结果清单传入
});