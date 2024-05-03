<template>
  <BlogHeader ref="headerRef" />
  <div id="user-center">
    <h3>更新资料信息</h3>
    <form>
      <div class="form-elem">
        <span>用户名：</span>
        <input v-model="username" type="text" placeholder="输入用户名" />
      </div>

      <div class="form-elem">
        <span>新密码：</span>
        <input v-model="password" type="password" placeholder="输入密码" />
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="changeInfo">更新</button>
      </div>

      <div class="form-elem">
        <button
          v-on:click.prevent="showingDeleteAlert = true"
          class="delete-btn"
        >
          删除用户
        </button>
        <div :class="{ shake: showingDeleteAlert }">
          <button
            v-if="showingDeleteAlert"
            class="confirm-btn"
            @click.prevent="confirmDelete"
          >
            确定？
          </button>
        </div>
      </div>

      <div class="form-back">
        <router-link :to="{ name: 'BlogHome' }">返回博客首页</router-link>
      </div>
    </form>
  </div>
  <BlogFooter />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';

import authorization from '@/utils/authorization';

const storage = localStorage;

const username = ref('');
const password = ref('');
const token = ref('');
const showingDeleteAlert = ref(false);
const headerRef = ref(null);

const router = useRouter();

onMounted(() => {
  // 从本地存储中获取用户名，并赋值给组件的 username 数据
  username.value = storage.getItem('username.myblog');
});

const confirmDelete = () => {
  authorization().then(function (response) {
    if (response[0]) {
      // 获取令牌
      token.value = storage.getItem('access.myblog');
      axios
        .delete('/api/user/' + username.value + '/', {
          headers: { Authorization: 'Bearer ' + token.value },
        })
        .then(function () {
          storage.clear();
          router.push({ name: 'BlogHome' });
        });
    }
  });
};
const changeInfo = () => {
  // 验证登录状态
  authorization().then(function (response) {
    // 检查登录状态
    // 若登录已过期则不执行后续操作
    if (!response[0]) {
      alert('登录已过期，请重新登录。');
      return;
    }
    // 如果登录状态有效，则在控制台输出日志，表示开始更改信息
    console.log('change info start.');
    // 密码不能小于6位
    if (password.value.length > 0 && password.value.length < 6) {
      alert('パスワードは短いです。');
      return;
    }
    // 旧的 username 用于接口发送请求
    const oldName = storage.getItem('username.myblog');
    // 获取已填写的表单数据
    let data = {};
    if (username.value !== '') {
      data.username = username.value;
    }
    if (password.value !== '') {
      data.password = password.value;
    }
    // 获取令牌
    token.value = storage.getItem('access.myblog');
    // 发送更新数据到接口
    axios
      .patch('/api/user/' + oldName + '/', data, {
        headers: { Authorization: 'Bearer ' + token.value },
      })
      .then(function (response) {
        // 从响应中获取更新后的用户名
        const name = response.data.username;
        // 将更新后的用户名存储到本地存储中
        storage.setItem('username.myblog', name);
        // 使用路由器跳转到用户中心页面，并传递更新后的用户名作为参数
        router.push({
          name: 'UserCenter',
          params: { username: name },
        });
        headerRef.value.refresh;
      });
  });
};
</script>

<style scoped>
#user-center {
  text-align: center;
  margin-top: 3rem;
}
.form-elem {
  padding: 0.6rem;
}
input {
  height: 1.5rem;
  padding-left: 0.9rem;
  width: 12em;
  margin-left: 0.3rem;
  border-radius: 0.3rem;
}
button {
  height: 2.1rem;
  background: steelblue;
  width: 6rem;
  cursor: pointer;
  border: none;
  outline: none;
  color: whitesmoke;
  border-radius: 0.3rem;
}

.confirm-btn {
  height: 2.1rem;
  width: 6rem;
  background-color: darkorange;
  margin-top: 1.2rem;
}
.delete-btn {
  background-color: red;
  margin-bottom: 0.9re m;
}
.shake {
  animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 3rem;
}
@keyframes shake {
  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }
  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }
  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }
  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}
</style>
