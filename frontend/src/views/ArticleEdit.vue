<template>
  <BlogHeader />

  <div class="article-delete">
    <h3>更新文章</h3>
    <form>
      <div class="form-elem">
        <span>标 题: </span>
        <input
          v-model="title"
          type="text"
          placeholder="タイトルを入力する..."
        />
      </div>

      <div class="form-elem">
        <span>分 類: </span>
        <span v-for="category in categories" :key="category.id">
          <button
            class="category-btn"
            :style="categoryStyle(category)"
            @click.prevent="chooseCategory(category)"
          >
            {{ category.title }}
          </button>
        </span>
      </div>

      <div class="form-elem">
        <span>ラベル: </span>
        <input v-model="tags" type="text" placeholder="ラベルを入力する..." />
      </div>

      <div class="form-elem">
        <span>正 文: </span>
        <textarea
          v-model="body"
          placeholder="正文を入力する..."
          rows="24"
          cols="64"
        ></textarea>
      </div>

      <div class="form-elem">
        <button v-on:click.prevent="submit">提交</button>
      </div>

      <div class="form-elem">
        <button
          @click.prevent="deleteArticle"
          style="
            background-image: linear-gradient(to top left, #e52a5a, #ff585f);
          "
        >
          消除
        </button>
      </div>
    </form>
  </div>

  <BlogFooter />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BlogHeader from '@/components/BlogHeader.vue';
import BlogFooter from '@/components/BlogFooter.vue';
import axios from 'axios';
import authorization from '@/utils/authorization';

const title = ref('');
const body = ref('');

// 所有分类
const categories = ref([]);
// 选定的分类
const selectedCategory = ref(null);
// 标签
const tags = ref('');

// Article id
const articleID = ref(null);

const route = useRoute();
const router = useRouter();

onMounted(() => {
  // 页面初始化时获取所有分类
  axios
    .get('/api/category/')
    .then(response => (categories.value = response.data));
});

onMounted(() => {
  // 页面初始化时获取所有分类
  axios
    .get('/api/category/')
    .then(response => (categories.value = response.data));

  // 如果不希望非管理员用户也能获取原始 Markdown 数据
  // 那么必须在后端进行鉴权
  // 根据用户身份选用不同的序列化器

  axios.get('/api/article/' + route.params.id + '/').then(function (response) {
    const data = response.data;
    title.value = data.title;
    body.value = data.body;
    selectedCategory.value = data.category;
    tags.value = data.tags.join(',');

    articleID.value = data.id;
  });
});

// 根据分类是否被选中，按钮的颜色发生变化
const categoryStyle = category => {
  if (
    selectedCategory.value !== null &&
    category.id === selectedCategory.value.id
  ) {
    return {
      backgroundColor: 'black',
    };
  }
  return {
    backgroundColor: 'lightgrey',
    color: 'black',
  };
};
// 选取分类
const chooseCategory = category => {
  // 如果点击已选取的分类，则将 selectedCategory 置空
  if (
    selectedCategory.value !== null &&
    selectedCategory.value.id === category.id
  ) {
    selectedCategory.value = null;
  } else {
    selectedCategory.value = category;
  }
};

const submit = () => {
  authorization().then(function (response) {
    if (response[0]) {
      let data = {
        title: title.value,
        body: body.value,
      };

      data.category_id = selectedCategory.value
        ? selectedCategory.value.id
        : null;

      data.tags = tags.value
        .split(/[,，]/)
        .map(x => x.trim())
        .filter(x => x.charAt(0) !== '');

      const token = localStorage.getItem('access.myblog');
      axios
        .put('/api/article/' + articleID.value + '/', data, {
          headers: { Authorization: 'Bearer ' + token },
        })
        .then(function (response) {
          router.push({
            name: 'ArticleDetail',
            params: { id: response.data.id },
          });
        });
    } else {
      alert('令牌过期，请重新登录。');
    }
  });
};

const deleteArticle = () => {
  const token = localStorage.getItem('access.myblog');
  authorization().then(function (response) {
    if (response[0]) {
      axios
        .delete('/api/article/' + articleID.value + '/', {
          headers: { Authorization: 'Bearer ' + token },
        })
        .then(() => router.push({ name: 'BlogHome' }));
    } else {
      alert('令牌过期，请重新登录。');
    }
  });
};
</script>

<style scoped>
.category-btn {
  margin-right: 1rem;
  margin-left: 1rem;
  width: fit-content;
}
#article-create {
  text-align: center;
  font-size: large;
}
form {
  text-align: left;
  padding-left: 3rem;
  padding-right: 0.9rem;
}
.form-elem {
  padding: 0.6rem;
}

input {
  height: 1.8rem;
  padding-left: 0.9rem;
  width: 21rem;
  border-radius: 0.3rem;
  margin-left: 0.9rem;
}
button {
  height: 2.1rem;
  background: steelblue;
  width: 3.9rem;
  cursor: pointer;
  border: none;
  outline: none;
  color: whitesmoke;
  border-radius: 0.3rem;
}
textarea {
  margin-left: 0.9rem;
}
@media screen and (max-width: 768px) {
  .form-elem {
    font-size: 0.9rem;
  }
  form {
    padding: 0;
    font-size: 0.9rem;
  }

  textarea {
    width: 90%;
  }
  input {
    width: 75%;
  }
}
</style>
