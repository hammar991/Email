<template>
  <div class="page-shell public-page">
    <header class="hero compact">
      <div>
        <p class="eyebrow">Quiet Inbox</p>
        <h1>匿名投递入口</h1>
        <p class="hero-copy">任何拿到分享令牌的人都可以通过这里提交信件，不需要登录。</p>
      </div>
      <router-link class="plain-link" to="/">返回工作台</router-link>
    </header>

    <n-card class="glass-card public-card" :bordered="false">
      <template #header>
        <div class="card-title-row">
          <span>公开信箱</span>
          <n-tag round type="info">{{ route.params.shareToken }}</n-tag>
        </div>
      </template>

      <n-spin :show="loading">
        <n-empty v-if="!mailStore.publicMailbox" description="没有查询到这个公开信箱" />
        <div v-else class="public-mailbox">
          <div class="public-mailbox-header">
            <div>
              <p class="mini-label">信箱标题</p>
              <strong>{{ mailStore.publicMailbox.title || "未命名信箱" }}</strong>
              <p class="muted">{{ mailStore.publicMailbox.box_name }}</p>
            </div>
            <n-tag type="success" round>可匿名投递</n-tag>
          </div>

          <n-divider />

          <n-form :model="form" @submit.prevent="handleSubmit">
            <n-space vertical :size="16">
              <n-input v-model:value="form.headline" placeholder="输入信件标题" />
              <n-input
                v-model:value="form.context"
                type="textarea"
                :autosize="{ minRows: 6, maxRows: 12 }"
                placeholder="输入信件内容"
              />
              <n-button type="primary" attr-type="submit">
                匿名投递
              </n-button>
            </n-space>
          </n-form>
        </div>
      </n-spin>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useMessage } from "naive-ui";
import { useMailStore } from "@/stores/mail";

const route = useRoute();
const message = useMessage();
const mailStore = useMailStore();
const loading = ref(false);

const form = reactive({
  headline: "",
  context: "",
});

async function loadMailbox() {
  const shareToken = String(route.params.shareToken || "");
  if (!shareToken) {
    return;
  }

  loading.value = true;
  try {
    await mailStore.fetchPublicMailbox(shareToken);
  } catch (error) {
    message.error(getErrorMessage(error));
  } finally {
    loading.value = false;
  }
}

async function handleSubmit() {
  const shareToken = String(route.params.shareToken || "");
  if (!shareToken) {
    message.error("缺少分享令牌");
    return;
  }

  try {
    await mailStore.submitPublicMessage(shareToken, { ...form });
    form.headline = "";
    form.context = "";
    message.success("匿名信件已投递");
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "操作失败";
}

watch(
  () => route.params.shareToken,
  () => {
    void loadMailbox();
  },
);

onMounted(() => {
  void loadMailbox();
});
</script>
