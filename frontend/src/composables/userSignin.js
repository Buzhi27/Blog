import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const signinName = ref('');
const signinPwd = ref('');
const signinError = ref('');

export default function userSignin() {
  const router = useRouter();
  const signin = () => {
    if (!signinName.value.trim() || !signinPwd.value.trim()) {
      alert('请输入用户名或密码');
      return;
    }

    axios
      // 向 /api/token/ 路径发送了一个包含用户名和密码的请求体。
      .post('/api/token/', {
        username: signinName.value,
        password: signinPwd.value,
      })
      .then(function (response) {
        const storage = localStorage;
        // Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
        // Token 被设置成100分钟，因此这里加上 6000000 毫秒
        const expiredTime = Date.parse(response.headers.date) + 6000000;
        // 设置 localStorage， 获取数据
        // 将从服务器响应中获取的访问令牌存储在本地存储中
        storage.setItem('access.myblog', response.data.access);
        // 将从服务器响应中获取的刷新令牌存储在本地存储中
        storage.setItem('refresh.myblog', response.data.refresh);
        // 将计算出的过期时间存储在本地存储中
        storage.setItem('expiredTime.myblog', expiredTime);
        // 将用户登录的用户名存储在本地存储中
        storage.setItem('username.myblog', signinName.value);

        // 是否为管理员
        axios
          .get('/api/user/' + signinName.value + '/')
          .then(function (response) {
            storage.setItem('isSuperuser.myblog', response.data.is_superuser);
            // 路由跳转
            router.push({ name: 'BlogHome' });
          });
      })
      .catch(function (error) {
        signinError.value = '登录失败：用户名或密码错误' + error.message;
      });
  };
  return { signin, signinName, signinPwd, signinError };
}
