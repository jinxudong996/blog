<template>
  <div id="app">

    <div>这里显示message{{message}}</div>
    <div>这里显示value{{value}}</div>
    <div>
      <input type="text" v-model="value">
    </div>
    <div>
      <button @click="onClick">点击按钮</button>
    </div>
    <ul>
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/about">About</router-link>
      </li>
      <li>
        <router-link to="/posts">Posts</router-link>
      </li>
    </ul>

    <!-- 路由出口 -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name:'App',
  data(){ 
    return{
      message:'第一个ssr1',
      value:1234
    }
  },
  methods:{
    onClick(){
      console.log('hello world')
      this.value ++
    }
  }
}
</script>

<style>

</style>