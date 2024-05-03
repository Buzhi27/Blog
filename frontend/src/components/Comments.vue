<template>
  <br /><br />
  <hr />
  <h3>发表评论</h3>
  <!-- 评论多行文本输入控件 -->
  <textarea
    v-model="message"
    :placeholder="placeholder"
    name="comment"
    id="comment-area"
    cols="60"
    rows="10"
  ></textarea>
  <div>
    <button @click="submit" class="submitBtn">发布</button>
  </div>

  <br />
  <p>已有 {{ comments.length }} 条评论</p>
  <hr />

  <!-- 渲染所有评论内容 -->
  <div v-for="comment in comments" :key="comment.id">
    <div class="comments">
      <div>
        <span class="username">
          {{ comment.author.username }}
        </span>
        于
        <span class="created">
          {{ formatted_time(comment.created) }}
        </span>
        <span v-if="comment.parent">
          对
          <span class="parent">
            {{ comment.parent.author.username }}
          </span>
        </span>
        说道：
      </div>
      <div class="content">
        {{ comment.content }}
      </div>
      <div>
        <button class="commentBtn" @click="replyTo(comment)">回复</button>
      </div>
    </div>
    <hr />
  </div>
</template>

<script setup>
import axios from 'axios';
import authorization from '@/utils/authorization';
import formattedTime from '../composables/formattedTime';
import { ref, watchEffect } from 'vue';

const props = defineProps({
  article: Object,
});

// 所有评论
const comments = ref([]);
// 评论控件绑定的文本和占位符
const message = ref('');
const placeholder = ref('Say something ...');
// 评论的评论
const parentID = ref(null);

// 监听 article 对象， 以便实时更新评论
watchEffect(() => {
  comments.value = props.article !== null ? props.article.comments : [];
});

const submit = () => {
  authorization().then(response => {
    if (response[0]) {
      axios
        .post(
          '/api/comment/',
          {
            content: message.value,
            article_id: props.article.id,
            parent_id: parentID.value,
          },
          {
            headers: {
              Authorization: 'Bearer ' + localStorage.getItem('access.myblog'),
            },
          }
        )
        .then(response => {
          comments.value.unshift(response.data);
          message.value = '';
          alert('Comment submitted successfully!');
        });
    } else {
      alert('Please login before commenting!');
    }
  });
};
// 对某条评论进行评论， 即二级评论
const replyTo = comment => {
  parentID.value = comment.id;
  placeholder.value = 'Say to ' + comment.author.username;
};
// 修改日期显示格式
const formatted_time = formattedTime;
</script>

<style scoped>
#comment-area {
  width: 80%; /* 设置宽度为容器的80% */
  max-width: 100%; /* 设置最大宽度为100% */
  height: 6rem; /* 设置初始高度 */
  resize: vertical; /* 设置垂直调整大小 */
}
@media screen and (max-width: 500px) {
  .responsive-textarea {
    width: 100%; /* 在小屏幕上设置宽度为100% */
  }
}
button {
  cursor: pointer;
  border: none;
  outline: none;
  color: whitesmoke;
  border-radius: 0.3rem;
}
.submitBtn {
  height: 2.1rem;
  background: steelblue;
  width: 3.9rem;
  margin-top: 0.9rem;
}
.commentBtn {
  height: 1.5rem;
  background: lightslategray;
  width: 2.7rem;
}
.comments {
  padding-top: 0.9rem;
}
.username {
  font-weight: bold;
  color: darkorange;
}
.created {
  font-weight: bold;
  color: darkblue;
}
.parent {
  font-weight: bold;
  color: orangered;
}
.content {
  font-size: large;
  padding: 0.9rem;
}
</style>
