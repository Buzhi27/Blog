<template>
  <div>
    <a @click="logout">登出</a>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  const storage = localStorage;
  // 清除本地存储中的访问令牌
  storage.removeItem('access.myblog');
  // 清除本地存储中的刷新令牌
  storage.removeItem('refresh.myblog');
  // 清除本地存储中的过期时间
  storage.removeItem('expiredTime.myblog');
  // 清除本地存储中的用户名
  storage.removeItem('username.myblog');

  // 路由跳转
  // 登出后回到登录页面
  router.push({ name: 'Login' });
};
</script>

<style scoped>
a {
  color: black;
  margin-right: 0.6rem;
  margin-left: 0.6rem;
  text-decoration: none;
  display: block;

  cursor: pointer;
}
</style>
