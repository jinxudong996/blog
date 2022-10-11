<template>
  <div class="about">
    <h1>This is an about page</h1>
    
    <slotText :src="data1.src">
      <!-- <template v-slot="d">{{d.slotData}}</template> -->
      <template v-slot:a>aaaa</template>
      <template v-slot:b>bbbb</template>
    </slotText>
    <div>下面是name</div>
    <div>______________________</div>
    <div>{{name}}:{{city}}</div>
  </div>
</template>


<script>

import slotText from '../components/slotText.vue'
import m from "../minxins/index.js"

export default {
  components:{
    slotText
  },
  mixins:[m],
  data(){
    return {
      data1:{
        src:'www.baidu.com',
        name:'father'
      },
      name:'金旭东'
    }
  }
}
</script>