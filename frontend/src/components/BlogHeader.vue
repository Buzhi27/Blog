<template>
  <el-affix>
    <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false">
      <div>
        <el-menu-item index="0">
          <router-link :to="{ name: 'BlogHome' }">
            <h1>酿夏的博客</h1>
          </router-link>
        </el-menu-item>
      </div>

      <div class="flex-grow" />
      <SearchButton />

      <el-sub-menu index="2" v-if="hasLogin">
        <template #title>欢迎, {{ username }}!</template>

        <el-menu-item index="2-1">
          <div>
            <router-link
              :to="{ name: 'UserCenter', params: { username: username } }"
              >用户中心</router-link
            >
          </div>
        </el-menu-item>

        <el-menu-item index="2-2">
          <router-link :to="{ name: 'ArticleCreate' }" v-if="isSuperuser">
            发表文章
          </router-link>
        </el-menu-item>

        <el-menu-item index="3" v-if="hasLogin">
          <LogoutButton />
        </el-menu-item>
      </el-sub-menu>

      <el-menu-item index="3" v-else
        ><router-link to="/login" class="login-link"
          >登录</router-link
        ></el-menu-item
      >
    </el-menu>
  </el-affix>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import SearchButton from '@/components/SearchButton.vue';
import LogoutButton from '@/components/LogoutButton.vue';
import authorization from '@/utils/authorization';

const username = ref('');
const hasLogin = ref(false);
const isSuperuser = ref(JSON.parse(localStorage.getItem('isSuperuser.myblog')));

onMounted(() => {
  authorization().then(data => {
    hasLogin.value = data[0];
    username.value = data[1];
  });
});
</script>

<style scoped>
.flex-grow {
  flex-grow: 1;
}

.el-menu-item {
  padding: 0.3rem;
}

a {
  color: black;
  margin-right: 0.6rem;
  margin-left: 0.6rem;
  text-decoration: none;
  display: block;
  cursor: pointer;
}
</style>
