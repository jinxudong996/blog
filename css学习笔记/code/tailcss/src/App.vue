<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  <div>
    <div class="bg-blue-500 p-4">
      <p class="text-white">Hello, Tailwind CSS!</p>
    </div>

    <button class="border-2 bg-black text-white hover:bg-white hover:text-black">
        按钮
      </button>

    <input
      type="text"
      class="px-2 outline focus:outline-2 focus:outline-sky-500"
      placeholder="请聚焦这里..."
    />

  </div>
  
  
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  // components: {
  //   HelloWorld
  // }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
