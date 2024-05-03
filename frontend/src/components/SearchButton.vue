<template>
  <div class="container">
    <el-input
      v-model="searchText"
      placeholder="Search something..."
      clearable
      @keyup.enter="searchArticles"
    >
      <template #prefix>
        <el-icon class="el-input__icon" @click="searchArticles"
          ><search
        /></el-icon> </template
    ></el-input>
  </div>
</template>

<script setup>
// export default {
//   name: "SearchButton",
//   data() {
//     return {
//       searchText: "",
//     };
//   },
//   methods: {
//     searchArticles() {
//       // 获取用户搜索文本，去除首尾
//       const text = this.searchText.trim();
//       // 检查文本是否为空
//       if (text.charAt(0) !== "") {
//         //this.$router 代表路由器对象
//         // 如果搜索文本不为空，则使用 $router.push 方法导航到 "BlogHome" 路由
//         // 通过 query 参数传递搜索文本作为查询参数
//         this.$router.push({ name: "BlogHome", query: { search: text } });
//       }
//     },
//   },
// };
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Search } from '@element-plus/icons-vue';

const searchText = ref('');
const router = useRouter();

const searchArticles = () => {
  const text = searchText.value.trim();
  if (text.charAt(0) !== '') {
    router.push({ name: 'BlogHome', query: { search: text } });
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-right: 2.1rem;
}
@media screen and (max-width: 768px) {
  .container {
    display: none;
  }
}
</style>
