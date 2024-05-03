module.exports = {
  lintOnSave: false,
  devServer: {
    proxy: {
      // 给前端服务器设置了代理，即将 /api 地址的前端请求转发到 8000 端口的后端服务器去，从而规避跨域问题。
      '/api': {
        target: `http://127.0.0.1:8000/api`,
        changeOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
      },
    },
  },
};
