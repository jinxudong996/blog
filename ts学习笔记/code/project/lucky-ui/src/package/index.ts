import 'bootstrap/dist/css/bootstrap.min.css'

//导入组件
import Dropdown from "./Dropdown/Dropdown.vue";
import DropdownItem from "./Dropdown/DropdownItem.vue";

const components = [
  Dropdown,
  DropdownItem
]

const install = (Vue: any) => {
  components.forEach((_: any) => {
    Vue.component(_.name, _);
  });
};

export default {
  install
};