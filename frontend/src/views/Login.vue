<template>
  <BlogHeader />

  <div class="signin">
    <h3>登录账号</h3>
    <form>
      <div class="form-elem">
        <span>账号：</span>
        <input v-model="signinName" type="text" placeholder="输入用户名" />
      </div>

      <div class="form-elem">
        <span>密码：</span>
        <input v-model="signinPwd" type="password" placeholder="输入密码" />
      </div>

      <div v-if="signinError !== ''" class="error-message">
        {{ signinError }}
      </div>

      <div class="to-signin">
        <router-link :to="{ name: 'SignUp' }">
          如果你愿意的话，请点我注册。🤗
        </router-link>
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="signin">登录</button>
      </div>
    </form>
  </div>

  <BlogFooter />
</template>

<script setup>
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';
import userSignin from '../composables/userSignin';

const { signin, signinName, signinPwd, signinError } = userSignin();
</script>

<style scoped>
.signin {
  padding-bottom: 0.9rem;
  text-align: center;
  margin-top: 3rem;
  border: 1px solid lightblue;
  border-radius: 0.6rem;
  box-shadow: gray 0 0 0.3rem;
  width: 30%;
  margin-left: 35%;
}

.form-elem {
  padding: 0.6rem;
}
.error-message {
  color: red;
}
.to-signin {
  margin-top: 1.2rem;
}
.to-signin a {
  text-decoration: none;
}
input {
  height: 1.5rem;
  padding-left: 0.9rem;
  margin-left: 0.3rem;
  border-radius: 0.3rem;
  width: 48%;
}
button {
  height: 2.1rem;
  background: rgb(86, 188, 86);
  width: 3.9rem;
  cursor: pointer;
  border: none;
  outline: none;
  color: whitesmoke;
  border-radius: 0.3rem;
  margin-top: 1.2rem;
}
@media screen and (max-width: 600px) {
  .signin {
    width: 100%;
    margin-left: 0;
  }
  input {
    width: 9rem;
  }
}
</style>
