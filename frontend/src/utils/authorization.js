import axios from 'axios';

// async 表示函数里含有异步操作
async function authorization() {
  const storage = localStorage;

  let hasLogin = false;
  let username = storage.getItem('username.myblog');

  // 过期时间
  const expiredTime = Number(storage.getItem('expiredTime.myblog'));
  // 当前时间
  const current = new Date().getTime();
  // 刷新令牌
  const refreshToken = storage.getItem('refresh.myblog');

  // 初始 TOken 未过期
  if (expiredTime > current) {
    hasLogin = true;
    console.log('authorization access');
  }
  // 初始 Token 过期
  // 如果有刷新令牌则申请新的token
  else if (refreshToken !== null) {
    try {
      // await 表示紧跟在后面的表达式需要等待结果
      // await 关键字只能用在 async 函数中，并且由于它返回的 Promise 对象运行的结果可能是 rejected ，所以最好放到 try...catch 语句中。
      // 使用 axios.post 方法发送异步 POST 请求，向 /api/token/refresh/ 发送刷新令牌
      let response = await axios.post('/api/token/refresh/', {
        refresh: refreshToken,
      });

      // 计算新的 Token 过期时间，并将其存储在 localStorage 中
      const nextExpiredTime = Date.parse(response.headers.date) + 60000;

      storage.setItem('access.myblog', response.data.access);
      storage.setItem('expiredTime.myblog', nextExpiredTime);
      storage.removeItem('refresh.myblog');

      hasLogin = true;

      console.log('authorization refresh');
    } catch (err) {
      storage.clear();
      hasLogin = false;

      console.log('authorization err');
    }
  }
  // 无任何有效 token
  else {
    storage.clear();
    hasLogin = false;
    console.log('authorization exp');
  }
  console.log('authorization done');

  return [hasLogin, username];
}

export default authorization;
