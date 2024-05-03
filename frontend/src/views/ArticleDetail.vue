<template>
  <BlogHeader />

  <div v-if="article !== null" class="grid-container">
    <div>
      <h1 id="title">{{ article.title }}</h1>
      <p id="subtitle">
        本文由 {{ article.author.username }} 发布于
        {{ formatted_time(article.created) }}
        <span v-if="isSuperuser">
          <router-link
            :to="{ name: 'ArticleEdit', params: { id: article.id } }"
          >
            更新与删除
          </router-link>
        </span>
      </p>
      <div v-html="article.body_html" class="article-body"></div>
    </div>

    <div class="content">
      <h3>目録 Contens</h3>
      <div v-html="article.toc_html" class="toc"></div>
    </div>
  </div>

  <Comments :article="article" />

  <BlogFooter />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';
import Comments from '@/components/Comments.vue';
import formattedTime from '../composables/formattedTime';

import axios from 'axios';

const route = useRoute();

const article = ref(null);

onMounted(() =>
  axios
    .get('/api/article/' + route.params.id)
    .then(response => (article.value = response.data))
);

const isSuperuser = computed(() => {
  return localStorage.getItem('isSuperuser.myblog') === 'true';
});

const formatted_time = formattedTime;
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: 3fr 1fr;
}

#title {
  text-align: center;
  font-size: x-large;
}

#subtitle {
  text-align: center;
  color: gray;
  font-size: small;
}

.article-body {
  width: 90%;
  border-radius: 1rem;
  box-shadow: gray 0 0 0.6rem;
  border: 1px solid lightcyan;
  padding: 1rem;
  margin-top: 3rem;
}

.toc ul {
  list-style-type: none;
}

.toc a {
  color: gray;
}
@media screen and (max-width: 768px) {
  .content {
    display: none;
  }
  .grid-container {
    grid-template-columns: auto; /* 在小于768px的屏幕下，自动调整为单列显示 */
  }
}
</style>
