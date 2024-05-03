// main.js 在 Vue 初始化时必然会执行
// 把后续要写的 Vue 组件挂载到刚才那个 index.html 中。
import { createApp } from "vue";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import router from "./router";

URLSearchParams.prototype.appendIfExists = function (key, value) {
  if (value !== null && value !== undefined) {
    this.append(key, value);
  }
};

const app = createApp(App);
app.use(ElementPlus);
// 挂载路由功能,用前端路由的方式来实现页面跳转
app.use(router).mount("#app");
