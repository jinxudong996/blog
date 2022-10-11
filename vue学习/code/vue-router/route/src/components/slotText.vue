<template>
  <div>
    <a :href="src" >
      <!-- <slot :slotData="data1">{{data1.name}}</slot> -->
      <slot name="a"></slot>
      <div>**************</div>
      <slot name="b"></slot>
    </a>
    
  </div>
</template>

<script>
export default {
  name:'slotText',
  props:{
    src:String
  },
  data(){
    return {
      data1:{
        src:'qqqqqqqq',
        name:'child'
      }
    }
  }
}
</script>