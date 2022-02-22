<template>
  <div id="#app">
    <img src="./assets/logo.png" alt="">
    <h1>{{count}}</h1>
    <button @click="increase">+1</button>
    <div>..............................................</div>
    <h1 v-if="loading">loading.....</h1>
    <img v-if="loaded" :src="result.message" alt="">
    <dia-log/>
  </div>
</template>

<script lang="ts">
import {ref,watch} from 'vue'
import useURLLoader from './hooks/useURLLoader'
import diaLog from './components/diaLog.vue'

interface DogResult {
  message: string;
  status: string;
}

export default {
  name: 'App',
  components:{
    diaLog
  },
  setup() {
    const { result, loading, loaded } = useURLLoader<DogResult>('https://dog.ceo/api/breeds/image/random')
    console.log('loaded',loaded.value)
    console.log(result.value)
    watch(result, () => {
      if (result.value) {
        console.log('value', result.value.message)
      }
    })
    const count = ref(0)
    const increase = () => {
      count.value++
    }
    return {
      count,
      increase,
      result,
      loading,
      loaded
    }
  }
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
