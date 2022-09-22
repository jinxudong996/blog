<template>
  <div>
    <h1>这里是头部</h1>
    <router-view></router-view>
    <h1>这里是底部</h1>
  </div>
</template>

<script>
export default {
  name:'layout',
}
</script>