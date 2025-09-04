# DynamicTableEditor - Vue3 动态表格编辑器

一个基于 Vue3 + Element Plus 的动态表格编辑器组件，支持根据 JSON 配置动态渲染不同类型的表单控件，并提供增删行、数据验证等功能。

## 功能特性

- ✅ **动态列配置**：通过 JSON 配置表格列
- ✅ **多种控件类型**：支持 input、select、input-number 等
- ✅ **数据验证**：支持必填、长度、自定义验证规则
- ✅ **增删行操作**：支持添加行、删除行、删除指定行
- ✅ **双向绑定**：支持 v-model 双向数据绑定
- ✅ **事件回调**：提供 change、validation-error 等事件
- ✅ **方法暴露**：提供验证、获取数据等方法

## 安装依赖

```bash
npm install vue@^3.0.0 element-plus@^2.0.0 @element-plus/icons-vue
```

## 基本使用

### 1. 引入组件

```vue
<template>
  <DynamicTableEditor
    :columns="tableColumns"
    v-model="tableData"
    @change="handleChange"
  />
</template>

<script setup>
import DynamicTableEditor from "./DynamicTableEditor.vue";

const tableColumns = ref([
  {
    type: "input",
    label: "参数名称",
    prop: "paramName",
    rules: [{ required: true, message: "请输入参数名称", trigger: "blur" }],
  },
  {
    type: "select",
    label: "参数类型",
    prop: "paramType",
    options: [
      { label: "字符串", value: "string" },
      { label: "数字", value: "number" },
    ],
  },
]);

const tableData = ref([]);
</script>
```

### 2. 列配置说明

#### 基础配置

```javascript
{
  type: 'input',           // 控件类型：input | select | input-number
  label: '参数名称',        // 列标题
  prop: 'paramName',       // 数据字段名
  placeholder: '请输入',    // 占位符
  width: '200px',          // 列宽度（可选）
  defaultValue: '',        // 默认值（可选）
  rules: []                // 验证规则（可选）
}
```

#### 控件类型配置

**Input 输入框**

```javascript
{
  type: 'input',
  label: '参数名称',
  prop: 'paramName',
  placeholder: '请输入参数名称',
  rules: [
    { required: true, message: '请输入参数名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在2-20个字符之间', trigger: 'blur' }
  ]
}
```

**Select 选择框**

```javascript
{
  type: 'select',
  label: '参数类型',
  prop: 'paramType',
  options: [
    { label: '字符串', value: 'string' },
    { label: '数字', value: 'number' },
    { label: '布尔值', value: 'boolean' }
  ],
  defaultValue: 'string',
  rules: [
    { required: true, message: '请选择参数类型', trigger: 'change' }
  ]
}
```

**InputNumber 数字输入框**

```javascript
{
  type: 'input-number',
  label: '默认值',
  prop: 'defaultValue',
  min: 0,                  // 最小值
  max: 999999,            // 最大值
  step: 1,                // 步长
  precision: 0,           // 精度
  defaultValue: 0
}
```

#### 验证规则配置

```javascript
rules: [
  // 必填验证
  { required: true, message: "字段不能为空", trigger: "blur" },

  // 长度验证
  { min: 2, max: 20, message: "长度在2-20个字符之间", trigger: "blur" },

  // 自定义验证
  {
    validator: (value, row) => {
      if (value === "test") {
        return "不能使用test作为值";
      }
      return true;
    },
    trigger: "blur",
  },
];
```

## API 文档

### Props

| 参数        | 类型  | 必填 | 默认值 | 说明       |
| ----------- | ----- | ---- | ------ | ---------- |
| columns     | Array | 是   | []     | 表格列配置 |
| initialData | Array | 否   | []     | 初始数据   |

### Events

| 事件名            | 参数            | 说明           |
| ----------------- | --------------- | -------------- |
| update:modelValue | (data: Array)   | 数据变化时触发 |
| change            | (data: Array)   | 数据变化时触发 |
| validation-error  | (errors: Array) | 验证错误时触发 |

### Methods

通过 ref 可以调用以下方法：

| 方法名            | 参数            | 返回值  | 说明         |
| ----------------- | --------------- | ------- | ------------ |
| addRow            | -               | -       | 添加一行     |
| removeRow         | -               | -       | 删除最后一行 |
| removeSpecificRow | (index: number) | -       | 删除指定行   |
| validateAll       | -               | boolean | 验证所有数据 |
| getTableData      | -               | Array   | 获取表格数据 |
| setTableData      | (data: Array)   | -       | 设置表格数据 |

### 使用示例

```vue
<template>
  <div>
    <DynamicTableEditor
      ref="tableEditorRef"
      :columns="columns"
      v-model="tableData"
      @change="handleChange"
      @validation-error="handleError"
    />

    <el-button @click="validate">验证数据</el-button>
    <el-button @click="getData">获取数据</el-button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import DynamicTableEditor from "./DynamicTableEditor.vue";

const tableEditorRef = ref(null);
const tableData = ref([]);

const columns = ref([
  {
    type: "input",
    label: "参数名称",
    prop: "paramName",
    rules: [{ required: true, message: "请输入参数名称" }],
  },
]);

const handleChange = (data) => {
  console.log("数据变化:", data);
};

const handleError = (errors) => {
  console.log("验证错误:", errors);
};

const validate = () => {
  const isValid = tableEditorRef.value.validateAll();
  console.log("验证结果:", isValid);
};

const getData = () => {
  const data = tableEditorRef.value.getTableData();
  console.log("表格数据:", data);
};
</script>
```

## 完整示例

参考 `Example.vue` 文件，包含了一个完整的使用示例，展示了：

- 多种控件类型的使用
- 数据验证规则配置
- 事件处理
- 方法调用
- 数据导出功能

## 样式定制

组件使用 scoped 样式，可以通过以下方式定制：

```vue
<style scoped>
/* 自定义表格样式 */
:deep(.el-table) {
  border-radius: 8px;
}

/* 自定义输入框样式 */
:deep(.el-input__wrapper) {
  border-radius: 4px;
}
</style>
```

## 注意事项

1. **Element Plus 版本**：确保使用 Element Plus 2.x 版本
2. **Vue 版本**：需要 Vue 3.x 版本
3. **图标依赖**：需要安装 `@element-plus/icons-vue`
4. **数据格式**：表格数据为对象数组格式
5. **验证规则**：支持 Element Plus 的验证规则格式

## 更新日志

### v1.0.0

- 初始版本发布
- 支持动态列配置
- 支持多种控件类型
- 支持数据验证
- 支持增删行操作

## 许可证

MIT License
