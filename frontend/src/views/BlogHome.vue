<template>
  <BlogHeader />

  <ArticleList />

  <BlogFooter />
</template>

<script setup>
// 在Vue中，@符号是一个别名，用于表示项目根目录。通常情况下，@会被Webpack或Vue CLI解析为项目的src目录。
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';
import ArticleList from '@/components/ArticleList.vue';
</script>
