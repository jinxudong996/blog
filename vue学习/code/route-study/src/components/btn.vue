<template>
  <div>
    <button @click="goPageA">跳转pageA</button>
  </div>
</template>

<script>
export default {
  name:'btn',
  methods:{
    goPageA:function(){
      // this.$router.push('/pageA')
      // this.$router.push({name:'Detail',params:{
      //   id:15
      // }})
      // this.$router.replace('/pageA')
      // this.$router.go(-1)
      this.$router.back()
    }
  }
}
</script>