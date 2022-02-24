import { createApp } from 'vue'
import App from './App.vue'
// import 'bootstrap/dist/css/bootstrap.min.css'

import luckyUi from './package/index';

const app = createApp(App)

// import Dropdown from "./package/Dropdown/Dropdown.vue";
// import DropdownItem from "./package/Dropdown/DropdownItem.vue";

// app.component('Dropdown',Dropdown)
// app.component('DropdownItem',DropdownItem)


app.use(luckyUi);

app.mount('#app')
