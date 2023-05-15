

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { devPlugin } from "./plugins/devPlugin";

export default defineConfig({
  plugins: [devPlugin(), vue()],
});
