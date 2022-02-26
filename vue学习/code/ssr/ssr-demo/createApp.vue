import Vue from 'vue';
import App from './App';

export default function createApp (context) {
    const app = new Vue({
        render: h => h(App)
    });
  	return {
      	app
    };
};