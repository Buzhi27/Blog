// 导入Vue Router库中的createWebHistory和createRouter函数。
import { createWebHistory, createRouter } from 'vue-router';
// 导入组件
import BlogHome from '@/views/BlogHome.vue';
import ArticleDetail from '@/views/ArticleDetail.vue';
import Login from '@/views/Login.vue';
import UserCenter from '@/views/UserCenter.vue';
import ArticleCreate from '@/views/ArticleCreate.vue';
import ArticleEdit from '@/views/ArticleEdit.vue';
import SignUp from '@/views/SignUp.vue';

// 定义路由配置数组
const routes = [
  {
    //表示这个路由规则匹配的路径是根路径
    path: '/',
    name: 'BlogHome',
    component: BlogHome,
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: ArticleDetail,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp,
  },
  {
    path: '/user/:username',
    name: 'UserCenter',
    component: UserCenter,
  },
  {
    path: '/article/create',
    name: 'ArticleCreate',
    component: ArticleCreate,
  },
  {
    path: '/article/edit/:id',
    name: 'ArticleEdit',
    component: ArticleEdit,
  },
];

const router = createRouter({
  // 用 createWebHistory() 创建 HTML5 模式
  history: createWebHistory(),
  routes,
});

// 导出创建的路由实例，以便在应用的其他部分中使用。
export default router;
