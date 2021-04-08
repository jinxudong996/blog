// import Vue from "vue";
// import App from "./App.vue";
// import router from "./router";
// import store from "./store";

// Vue.config.productionTip = false;

// new Vue({
//   router,
//   store,
//   render: (h) => h(App),
// }).$mount("#app");

import Vue from "vue"

var app = new Vue({
  el: '#app',
  mounted:function() {
    console.log(this.message)
    console.log(this._data.message)
  },
  data() {
    return {
      message: 'Hello Vue'
    }
  }
})