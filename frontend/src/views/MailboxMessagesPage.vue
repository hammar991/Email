<template>
  <div class="page-shell">
    <header class="hero compact">
      <div>
        <p class="eyebrow">Quiet Inbox</p>
        <h1>{{ mailboxHeading }}</h1>
        <p class="hero-copy">
          这个页面由 DashboardPage.vue 跳转进入。列表中一个 card 包含一份信件，并支持分页浏览。
        </p>
      </div>
      <n-space>
        <n-button secondary type="primary" @click="goBack">返回 Quiet Inbox</n-button>
        <n-button tertiary type="info" @click="refreshMessages">刷新信件</n-button>
      </n-space>
    </header>

    <n-card class="glass-card" :bordered="false">
      <template #header>
        <div class="card-title-row">
          <span>信件列表</span>
          <n-tag round type="warning">分页卡片模式</n-tag>
        </div>
      </template>

      <n-spin :show="mailStore.loadingMessages">
        <n-empty v-if="!messages.length" description="当前信箱还没有信件" />
        <div v-else class="message-list">
          <article v-for="item in pagedMessages" :key="item.id" class="message-card">
            <div class="message-head">
              <div>
                <h3>{{ item.headline }}</h3>
                <p class="muted">信件 ID: {{ item.id }}</p>
              </div>
              <n-popconfirm @positive-click="handleDeleteMessage(item.id)">
                <template #trigger>
                  <n-button text type="error">删除</n-button>
                </template>
                确认删除这封信件？
              </n-popconfirm>
            </div>
            <p class="message-body">{{ item.context || "这封信没有填写内容。" }}</p>
          </article>
        </div>

        <div v-if="messages.length" class="pagination-wrap">
          <n-pagination
            v-model:page="page"
            :page-size="pageSize"
            :item-count="messages.length"
            show-size-picker
            :page-sizes="[4, 8, 12]"
            @update:page-size="handlePageSizeChange"
          />
        </div>
      </n-spin>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useMessage } from "naive-ui";
import { useRoute, useRouter } from "vue-router";
import { useMailStore } from "@/stores/mail";

const route = useRoute();
const router = useRouter();
const message = useMessage();
const mailStore = useMailStore();

const page = ref(1);
const pageSize = ref(4);

const boxId = computed(() => Number(route.params.boxId));

const currentMailbox = computed(() => {
  return mailStore.mailboxes.find((item) => item.id === boxId.value) ?? null;
});

const mailboxHeading = computed(() => {
  const title = currentMailbox.value?.title || String(route.query.title || "");
  const boxName = currentMailbox.value?.box_name || String(route.query.boxName || "");
  return title || boxName || `信箱 #${boxId.value}`;
});

const messages = computed(() => mailStore.messages[boxId.value] ?? []);

const pagedMessages = computed(() => {
  const start = (page.value - 1) * pageSize.value;
  return messages.value.slice(start, start + pageSize.value);
});

async function loadPageData() {
  try {
    if (!mailStore.mailboxes.length) {
      await mailStore.fetchMailboxes();
    }
    await mailStore.fetchMessages(boxId.value);
    normalizePage();
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

function normalizePage() {
  const maxPage = Math.max(1, Math.ceil(messages.value.length / pageSize.value));
  if (page.value > maxPage) {
    page.value = maxPage;
  }
}

async function refreshMessages() {
  await loadPageData();
}

async function handleDeleteMessage(messageId: number) {
  try {
    await mailStore.deleteMessage(messageId, boxId.value);
    normalizePage();
    message.success("信件已删除");
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

function handlePageSizeChange(value: number) {
  pageSize.value = value;
  page.value = 1;
}

function goBack() {
  void router.push("/dashboard");
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "操作失败";
}

watch(
  () => route.params.boxId,
  () => {
    page.value = 1;
    void loadPageData();
  },
);

watch(messages, () => {
  normalizePage();
});

onMounted(() => {
  void loadPageData();
});
</script>
