<template>
  <div>
    <div class="dropdown">
      <!-- 测试dropdown -->
      <dropdown :title="`你好啊`">
        <dropdown-item><a href="#">王大</a> </dropdown-item>
        <dropdown-item>
          <a href="#">王二</a>
        </dropdown-item>
        <dropdown-item disabled
          ><a href="#" class="dropdown-item">王三</a></dropdown-item
        >
        <dropdown-item
          ><a href="#" class="dropdown-item">王四</a></dropdown-item
        >
      </dropdown>
    </div>
  </div>
</template>

<script lang="ts">
// import "bootstrap/dist/css/bootstrap.min.css";
import { defineComponent } from "vue";

import Dropdown from "./package/Dropdown/Dropdown.vue";
import DropdownItem from "./package/Dropdown/DropdownItem.vue";

export default defineComponent({
  name: "App",
  components: {
    // Dropdown,
    // DropdownItem,
  },
});
</script>

<style scoped>
.dropdown {
  margin: 0 auto;
  width: 200px;
  border: 1px solid red;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
