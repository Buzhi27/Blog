module.exports = {
  lintOnSave: false,
  devServer: {
    proxy: {
      "/api": {
        target: `http://47.97.196.12/api`,
        changeOrigin: true,
        pathRewrite: {
          "^/api": "",
        },
      },
    },
  },
};
