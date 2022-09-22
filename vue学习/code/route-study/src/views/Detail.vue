<template>
  <div class="about">
    <span>当前路由id：{{$route.params.id}}</span>
    <h2>{{id}}</h2>
    <h1>This is Detail</h1>
  </div>
</template>

<script>
export default {
  props:['id'],
  name:'Detail'
}
</script>