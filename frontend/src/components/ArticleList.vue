<template>
  <div v-for="article in info.results" :key="article.url" id="articles">
    <div class="grid" :style="gridStyle(article)">
      <div class="image-container">
        <img :src="imageIfExists(article)" alt="" class="image" />
      </div>

      <div class="simple-info">
        <div>
          <span v-if="article.category !== null" class="category">
            {{ article.category.title }}
          </span>
          <span v-for="tag in article.tags" v-bind:key="tag" class="tag">{{
            tag
          }}</span>
        </div>
        <div class="a-title-container">
          <router-link
            :to="{ name: 'ArticleDetail', params: { id: article.id } }"
            class="article-title"
          >
            {{ article.title }}
          </router-link>
        </div>

        <div class="time">{{ formatted_time(article.created) }}</div>

        <div class="read-more">
          <router-link
            :to="{ name: 'ArticleDetail', params: { id: article.id } }"
          >
            <span class="icon-wrapper">
              <el-icon><Reading /></el-icon>
            </span>
            Read More
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <div id="paginator">
    <span v-if="is_page_exists('previous')">
      <router-link :to="get_path('previous')"> Prev </router-link>
    </span>
    <span class="current-page">
      {{ get_page_param('current') }}
    </span>
    <span v-if="is_page_exists('next')">
      <router-link :to="get_path('next')"> Next </router-link>
    </span>
  </div>
</template>

<!-- <script>
import axios from "axios";

export default {
  name: "ArticleList",
  data: function () {
    return {
      info: "",
    };
  },
  mounted() {
    this.get_article_data();
  },
  methods: {
    imageIfExists(article) {
      if (article.avatar) {
        return article.avatar.content;
      }
    },

    gridStyle(article) {
      if (article.avatar) {
        return {
          display: "grid",
          gridTemplateColumns: "1fr 4fr",
        };
      }
    },

    formatted_time: function (iso_date_string) {
      const date = new Date(iso_date_string);
      return date.toLocaleDateString();
    },
    // 判断页面是否存在
    is_page_exists(direction) {
      //检查是否存在下一页
      if (direction === "next") {
        // 存在下一页
        return this.info.next !== null;
      }
      // 存在上一页
      return this.info.previous !== null;
    },
    // 获取页码
    get_page_param(direction) {
      // 使用 try-catch 来捕获可能发生的异常
      try {
        let url_string;

        // 根据 direction 选择不同的 URL
        switch (direction) {
          case "next":
            // 如果 direction 为 "next"， 则获取下一页的 URL
            url_string = this.info.next;
            break;
          case "previous":
            // 如果 direction 为 "previous"， 则获取上一页的 URL
            url_string = this.info.previous;
            break;
          default:
            // 如果 direction 既不是 "next" 也不是 "previous"，则返回当前页码的查询参数
            return this.$route.query.page;
        }
        // 解析 URL 字符串为 URL 对象
        const url = new URL(url_string);
        // 返回 URL 中名为 "page"的查询参数的值
        return url.searchParams.get("page");
      } catch (err) {
        // 如果发生错误，返回 undefined
        return;
      }
    },
    get_path(direction) {
      let url = "";

      try {
        switch (direction) {
          case "next":
            if (this.info.next !== undefined) {
              // 如果下一页的 URL 存在，则将其查询部分追加到 url 中
              url += new URL(this.info.next).search;
            }
            break;
          case "previous":
            if (this.info.previous !== undefined) {
              url += new URL(this.info.previous).search;
            }
            break;
        }
      } catch {
        // 如果发生异常，则返回当前存储的 URL
        return url;
      }

      // 返回最终得到的 URL
      return url;
    },
    // 获取文章列表数据
    get_article_data() {
      let url = "/api/article";

      let params = new URLSearchParams();
      params.appendIfExists("page", this.$route.query.page);
      params.appendIfExists("search", this.$route.query.search);

      const paramsString = params.toString();
      if (paramsString.charAt(0) !== "") {
        url += "/?" + paramsString;
      }

      axios.get(url).then((response) => (this.info = response.data));
    },
  },
  watch: {
    // 监听路由是否有变化
    $route() {
      this.get_article_data();
    },
  },
};
</script> -->

<script setup>
// Vue 执行 setup() 的时机非常早，此时 Vue 的实例都尚未生成，因此在 setup 中没有 this。这意味着除了 props 之外，你将无法访问组件中的任何属性：比如数据、计算属性或方法。
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import getArticleData from '@/composables/getArticleData.js';
import pagination from '@/composables/pagination.js';
import articleGrid from '@/composables/articleGrid.js';
import formattedTime from '@/composables/formattedTime.js';
import { Reading } from '@element-plus/icons-vue';

// 不能像 let info = '' 这样声明状态，这不是响应式的，而只是个普通的字符串。因此用 ref 将其包装成一个响应式的对象，和旧的 data 中的数据一样。
const info = ref('');

// 创建路由
const route = useRoute();

getArticleData(info, route);

// 翻页
const { is_page_exists, get_page_param, get_path } = pagination(info, route);

// 调整页面外观
const { imageIfExists, gridStyle } = articleGrid();

// 日期格式化
const formatted_time = formattedTime;
</script>

<!-- "scoped" 使样式仅在当前组件生效 -->

<style scoped>
.simple-info {
  margin-left: 3rem;
}
.image {
  width: 100%;
  border-radius: 0.9rem;
  box-shadow: darkslategrey 0 0 0.9rem;
}
.image-container {
  padding: 0.3rem;
}

.category {
  padding: 0.3rem 0.6rem;
  margin: 0.3rem;
  font-family: Georgia, Arial, sans-serif;
  font-size: small;
  background-image: linear-gradient(to top left, #76cce3, #2d98c2);
  color: whitesmoke;
  border-radius: 0.6rem;
}

#articles {
  padding: 0.9rem;
  margin-top: 2.1rem;
  margin-left: 20%;
  border-radius: 0.9rem;
  box-shadow: gray 0 0 0.6rem;
  font-size: 1.2rem;
  width: 60%;
}

.article-title {
  font-size: large;
  font-weight: bolder;
  color: black;
  text-decoration: none;
}

.a-title-container {
  padding: 0.6rem 0.3rem;
}

.tag {
  padding: 0.3rem 0.6rem;
  margin: 0.3rem;
  font-size: small;
  background-image: linear-gradient(to top left, #39b385, #9be15d);
  color: whitesmoke;
  border-radius: 0.6rem;
}

#paginator {
  text-align: center;
  padding-top: 3rem;
}

a {
  color: black;
  text-decoration: none;
}
a:hover {
  text-decoration: underline; /* 鼠标移动到链接上时显示下划线 */
  color: lightblue;
}

.current-page {
  font-size: x-large;
  font-weight: bold;
  padding-left: 0.6rem;
  padding-right: 0.6rem;
}
.time {
  font-size: 1rem;
}
.read-more {
  margin-top: 12%;
  font-size: 100%;
  font-weight: bold;
}
.icon-wrapper {
  vertical-align: middle;
  display: inline-block;
}

@media screen and (max-width: 768px) {
  #articles {
    font-size: 0.6rem;
    margin-left: 0;
    width: 90%;
  }
  .tag {
    font-size: 0.6rem;
  }
  .category {
    font-size: 0.6rem;
  }
  .article-title {
    font-size: 0.9rem;
  }
  .time {
    font-size: 0.66rem;
  }
  .read-more {
    margin-top: 12%;
    font-size: 0.9rem;
  }
}
</style>
