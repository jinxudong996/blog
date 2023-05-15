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