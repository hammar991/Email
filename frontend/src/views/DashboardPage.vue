<template>
  <div class="page-shell">
    <header class="hero">
      <div>
        <p class="eyebrow">Dashboard</p>
        <h1>信箱总览控制台</h1>
        <p class="hero-copy">
          这里集中展示当前账号下的全部信箱。表格最后一列为操作列，支持查看所有信件和生成分享 token
          按钮，点击生成分享 token 即复制。
        </p>
      </div>
      <n-space vertical :size="12" align="end">
        <n-tag round type="success">{{ authStore.user?.name ?? "未登录" }}</n-tag>
        <n-button tertiary type="primary" @click="handleLogout">退出登录</n-button>
      </n-space>
    </header>

    <main class="dashboard-stack">
      <section class="dashboard-top-grid">
        <n-card class="glass-card" :bordered="false">
          <template #header>
            <div class="card-title-row">
              <span>用户信息</span>
              <n-tag round type="info">DTO: UserUpdate.email</n-tag>
            </div>
          </template>

          <div class="user-panel">
            <div>
              <p class="mini-label">当前账号</p>
              <strong>{{ authStore.user?.name ?? "未知用户" }}</strong>
              <p class="muted">{{ authStore.user?.email ?? "暂无邮箱信息" }}</p>
            </div>
            <n-space vertical :size="12" class="profile-form-block">
              <n-input v-model:value="profileForm.email" placeholder="更新 email" />
              <n-button type="primary" secondary @click="handleUpdateProfile">
                保存邮箱
              </n-button>
            </n-space>
          </div>
        </n-card>

        <n-card class="glass-card" :bordered="false">
          <template #header>
            <div class="card-title-row">
              <span>新建信箱</span>
              <n-tag round type="warning">DTO: MailboxMsg</n-tag>
            </div>
          </template>

          <n-form :model="mailboxForm" @submit.prevent="handleCreateMailbox">
            <n-space vertical :size="16">
              <n-form-item label="name">
                <n-input v-model:value="mailboxForm.name" placeholder="请输入 name" />
              </n-form-item>
              <n-form-item label="title">
                <n-input v-model:value="mailboxForm.title" placeholder="请输入 title" />
              </n-form-item>
              <n-button block type="primary" attr-type="submit">
                创建信箱
              </n-button>
            </n-space>
          </n-form>
        </n-card>
      </section>

      <n-card class="glass-card" :bordered="false">
        <template #header>
          <div class="card-title-row">
            <span>信箱信息表</span>
            <n-space>
              <n-button secondary type="primary" @click="refreshMailboxes">刷新表格</n-button>
              <n-tag round type="info">操作列已启用</n-tag>
            </n-space>
          </div>
        </template>

        <n-data-table
          :columns="columns"
          :data="mailStore.mailboxes"
          :loading="mailStore.loadingMailboxes"
          :bordered="false"
          :pagination="{ pageSize: 8 }"
          :row-key="rowKey"
        />
      </n-card>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, h, onMounted, reactive, watch } from "vue";
import type { DataTableColumns } from "naive-ui";
import { NButton, NPopconfirm, NSpace, NTag, useMessage } from "naive-ui";
import { useRouter } from "vue-router";
import type { MailboxInfo } from "@/api/types";
import { useAuthStore } from "@/stores/auth";
import { useMailStore } from "@/stores/mail";

const router = useRouter();
const message = useMessage();
const authStore = useAuthStore();
const mailStore = useMailStore();

const profileForm = reactive({
  email: "",
});

const mailboxForm = reactive({
  name: "",
  title: "",
});

const columns = computed<DataTableColumns<MailboxInfo>>(() => [
  {
    title: "信箱名称",
    key: "box_name",
  },
  {
    title: "标题",
    key: "title",
    render: (row) => row.title || "未命名信箱",
  },
  {
    title: "分享 Token",
    key: "share_token",
    ellipsis: {
      tooltip: true,
    },
  },
  {
    title: "操作",
    key: "actions",
    width: 340,
    render: (row) =>
      h(
        NSpace,
        { wrap: false },
        {
          default: () => [
            h(
              NButton,
              {
                size: "small",
                type: "primary",
                secondary: true,
                onClick: () => handleViewMessages(row),
              },
              { default: () => "查看所有信件" },
            ),
            h(
              NButton,
              {
                size: "small",
                type: "info",
                secondary: true,
                onClick: () => copyShareToken(row),
              },
              { default: () => "生成分享 token" },
            ),
            h(
              NPopconfirm,
              {
                onPositiveClick: () => handleDeleteMailbox(row.id),
              },
              {
                trigger: () =>
                  h(
                    NButton,
                    {
                      size: "small",
                      type: "error",
                      tertiary: true,
                    },
                    { default: () => "删除" },
                  ),
                default: () => "确认删除该信箱？",
              },
            ),
          ],
        },
      ),
  },
]);

function rowKey(row: MailboxInfo) {
  return row.id;
}

async function refreshMailboxes() {
  try {
    await mailStore.fetchMailboxes();
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

async function handleCreateMailbox() {
  try {
    const mailbox = await mailStore.createMailbox({
      name: mailboxForm.name,
      title: mailboxForm.title,
    });
    mailboxForm.name = "";
    mailboxForm.title = "";
    message.success(`信箱 ${mailbox.box_name} 创建成功`);
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

async function handleDeleteMailbox(boxId: number) {
  try {
    await mailStore.deleteMailbox(boxId);
    message.success("信箱已删除");
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

function handleViewMessages(row: MailboxInfo) {
  void router.push({
    name: "mailbox-messages",
    params: {
      boxId: String(row.id),
    },
    query: {
      title: row.title || "",
      boxName: row.box_name,
    },
  });
}

async function copyShareToken(row: MailboxInfo) {
  try {
    await navigator.clipboard.writeText(row.share_token);
    message.success(`分享 token 已复制: ${row.share_token}`);
  } catch {
    message.warning("复制失败，请手动复制该 token");
  }
}

async function handleUpdateProfile() {
  try {
    await authStore.updateUser({ email: profileForm.email });
    message.success("用户邮箱已更新");
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

async function handleLogout() {
  authStore.logout();
  mailStore.reset();
  await router.push("/login");
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "操作失败";
}

watch(
  () => authStore.user,
  (value) => {
    profileForm.email = value?.email ?? "";
  },
  { immediate: true },
);

onMounted(async () => {
  try {
    await authStore.fetchUser();
    await mailStore.fetchMailboxes();
  } catch (error) {
    message.error(getErrorMessage(error));
  }
});
</script>
