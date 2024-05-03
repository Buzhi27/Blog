<template>
  <BlogHeader />

  <div id="article-creat">
    <h3>发表文章 (文章を発表する)</h3>
    <form id="image_form">
      <div class="form-elem">
        <span>图 片 (写 真): </span>
        <input
          @change="onFileChange"
          type="file"
          id="file"
          accept="image/gif, image/jpeg"
        />
      </div>
    </form>
    <form>
      <div class="form-elem">
        <span>标 题 (タイトル):</span>
        <input v-model="title" type="text" placeholder="タイトルを入力する：" />
      </div>

      <div class="form-elem">
        <span>分 类 (分 類):</span>
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
    </form>
  </div>

  <div class="form-elem">
    <span>正 文: </span>
    <textarea
      v-model="body"
      placeholder="输入正文"
      rows="20"
      cols="80"
    ></textarea>
  </div>

  <div class="form-elem">
    <button @click.prevent="submit">提交 (提出する)</button>
  </div>

  <BlogFooter />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
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

// 标题图
const avatarID = ref(null);

const router = useRouter();

onMounted(() => {
  // 页面初始化时获取所有分类
  axios
    .get('/api/category/')
    .then(response => (categories.value = response.data));
});

const onFileChange = e => {
  const file = e.target.files[0];
  // this.imageUrl = URL.createObjectURL(file);

  let formData = new FormData();
  formData.append('content', file);

  // 省去鉴权和错误处理的部分
  axios
    .post('/api/avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: 'Bearer ' + localStorage.getItem('access.myblog'),
      },
    })
    .then(response => (avatarID.value = response.data.id));
};

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
// 点击提交按钮
const submit = () => {
  authorization().then(function (response) {
    if (response[0]) {
      let data = {
        title: title.value,
        body: body.value,
      };

      // 添加标题图
      data.avatar_id = avatarID.value;

      // 添加分类
      if (selectedCategory.value) {
        data.category_id = selectedCategory.value.id;
      }
      // 预处理并添加标签
      // 逗号分隔标签并剔除无效标签
      data.tags = tags.value
        .split(/[,，]/)
        .map(x => x.trim())
        .filter(x => x.charAt(0) !== '');

      // 发送发表文章请求
      // 成功后前往详情页面
      const token = localStorage.getItem('access.myblog');
      axios
        .post('/api/article/', data, {
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
