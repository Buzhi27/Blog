import { ref } from 'vue';

import axios from 'axios';

const signupName = ref('');
const signupPwd = ref('');
const confirmPwd = ref('');
const signupResponse = ref(null);
const signupError = ref('');
const passwordsNotMatch = ref(false);

export default function userSignup() {
  const signup = () => {
    if (!signupName.value.trim() || !signupPwd.value.trim()) {
      alert('请输入用户名或密码');
      return;
    }

    if (signupPwd.value !== confirmPwd.value) {
      passwordsNotMatch.value = true;
      return; // 密码不匹配时停止注册流程
    }

    axios
      .post('/api/user/', {
        username: signupName.value,
        password: signupPwd.value,
      })
      .then(function (response) {
        signupResponse.value = response.data;
        alert('用户注册成功，快去登录吧！');
      })
      .catch(function (error) {
        // 在这里处理请求失败的情况，显示错误提示给用户
        signupError.value = '注册失败：' + error.message;
      });
  };
  return {
    signup,
    signupName,
    signupPwd,
    confirmPwd,
    signupResponse,
    signupError,
    passwordsNotMatch,
  };
}
