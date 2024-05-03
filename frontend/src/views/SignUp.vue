<template>
  <BlogHeader />

  <div class="signup">
    <h3>注册账号</h3>
    <form>
      <div class="form-elem">
        <span>账号：</span>
        <input v-model="signupName" type="text" placeholder="输入用户名" />
      </div>
      <div class="form-elem">
        <span>密码：</span>
        <input v-model="signupPwd" type="password" placeholder="输入密码" />
      </div>
      <div class="form-elem">
        <span>确认密码：</span>
        <input
          v-model="confirmPwd"
          type="password"
          placeholder="再次输入密码"
        />
      </div>
      <!-- 显示密码不匹配的错误消息 -->
      <div v-if="passwordsNotMatch" class="error-message">
        密码不匹配，请重新输入。<br />

        {{ signupError }}
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="signup">提交</button>
      </div>
    </form>
  </div>

  <BlogFooter />
</template>

<script setup>
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';
import userSignup from '../composables/userSignup';

const {
  signup,
  signupName,
  signupPwd,
  confirmPwd,
  signupResponse,
  signupError,
  passwordsNotMatch,
} = userSignup();
</script>

<style scoped>
.signup {
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
  font-size: 0.9rem;
}
.error-message {
  color: red;
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

@media screen and (max-width: 540px) {
  .signup {
    width: 100%;
    margin-left: 0;
  }
  input {
    width: 9rem;
  }
}
</style>
