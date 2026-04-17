<template>
  <n-layout class="console-shell">
    <n-layout-header class="console-header">
      <div class="console-header-left">
        <div class="console-brand">
          <n-avatar class="console-brand-logo" round color="#111827">
            <n-icon size="18"><MailIcon /></n-icon>
          </n-avatar>
          <div class="console-brand-copy">
            <strong>Quiet Inbox</strong>
          </div>
        </div>

        <n-menu
          mode="horizontal"
          class="console-top-menu"
          :value="activeTopMenu"
          :options="topMenuOptions"
          @update:value="handleTopMenuSelect"
        />
      </div>

      <n-space align="center" :size="12" class="console-header-actions">
        <n-button circle quaternary :loading="pageRefreshing" @click="refreshMessages">
          <n-icon size="16"><RefreshIcon /></n-icon>
        </n-button>
        <n-button quaternary @click="handleLogout">退出登录</n-button>
        <div class="console-user-pill">
          <n-avatar round color="#60a5fa">{{ userInitial }}</n-avatar>
          <div class="console-user-copy">
            <strong>{{ authStore.user?.name ?? "未登录" }}</strong>
            <span>{{ authStore.user?.email ?? "暂无邮箱" }}</span>
          </div>
        </div>
      </n-space>
    </n-layout-header>

    <n-layout has-sider class="console-body">
      <n-layout-sider
        v-model:collapsed="sidebarCollapsed"
        bordered
        collapse-mode="width"
        :collapsed-width="88"
        :width="220"
        show-trigger="bar"
        class="console-sider"
      >
        <div class="console-sider-inner">
          <div class="console-side-section">
            <p v-if="!sidebarCollapsed" class="console-side-section-title">控制台</p>
            <n-space vertical :size="10" class="console-rail">
              <n-tooltip v-for="item in primaryRailActions" :key="item.key" placement="right">
                <template #trigger>
                  <n-button
                    quaternary
                    class="console-rail-button"
                    :class="{ 'is-active': activeRail === item.key, 'is-collapsed': sidebarCollapsed }"
                    @click="handleRailAction(item.key)"
                  >
                    <template #icon>
                      <n-icon size="18"><component :is="item.icon" /></n-icon>
                    </template>
                    <span v-if="!sidebarCollapsed">{{ item.label }}</span>
                  </n-button>
                </template>
                {{ item.label }}
              </n-tooltip>
            </n-space>
          </div>

          <div class="console-side-section console-side-section-secondary">
            <p v-if="!sidebarCollapsed" class="console-side-section-title">个人中心</p>
            <n-space vertical :size="10" class="console-rail">
              <n-tooltip v-for="item in secondaryRailActions" :key="item.key" placement="right">
                <template #trigger>
                  <n-button
                    quaternary
                    class="console-rail-button"
                    :class="{ 'is-active': activeRail === item.key, 'is-collapsed': sidebarCollapsed }"
                    @click="handleRailAction(item.key)"
                  >
                    <template #icon>
                      <n-icon size="18"><component :is="item.icon" /></n-icon>
                    </template>
                    <span v-if="!sidebarCollapsed">{{ item.label }}</span>
                  </n-button>
                </template>
                {{ item.label }}
              </n-tooltip>
            </n-space>
          </div>
        </div>
      </n-layout-sider>

      <n-layout class="console-main">
        <n-layout-content class="console-content">
          <section class="console-welcome">
            <div>
              <p class="console-greeting-kicker">Messages</p>
              <h1 class="console-greeting-title">
                <span class="console-greeting-emoji">✉️</span>
                <span>{{ currentMailboxTitle }}</span>
              </h1>
              <p>{{ summaryText }}</p>
            </div>
            <n-tag round type="info">{{ messages.length }} 封信件</n-tag>
          </section>

          <section class="console-main-column" style="margin-top: 18px;">
            <n-card class="glass-card console-analytics-card" :bordered="false">
              <template #header>
                <div class="card-title-row">
                  <span>信件列表</span>
                  <n-tag round type="warning">{{ currentMailbox?.box_name ?? "未选择信箱" }}</n-tag>
                </div>
              </template>

              <div class="analytics-toolbar">
                <div class="analytics-toolbar-copy">
                  <strong>支持切换信箱并维护信件</strong>
                  <p>先选择信箱，再在当前信箱下新增、查看和删除信件。</p>
                </div>
                <n-space class="analytics-toolbar-controls" align="end">
                  <n-select
                    :value="selectedBoxId ?? undefined"
                    :options="mailboxOptions"
                    placeholder="请选择信箱"
                    style="width: min(320px, 100%);"
                    @update:value="handleMailboxChange"
                  />
                  <n-button type="primary" secondary :disabled="!selectedBoxId" @click="openCreateModal">
                    新增信件
                  </n-button>
                </n-space>
              </div>

              <n-spin :show="mailStore.loadingMessages || pageRefreshing">
                <n-empty
                  v-if="!mailStore.mailboxes.length"
                  description="当前还没有可用信箱，请先创建信箱。"
                />
                <n-empty
                  v-else-if="!selectedBoxId"
                  description="请选择一个信箱以查看信件。"
                />
                <n-empty
                  v-else-if="!messages.length"
                  description="当前信箱还没有信件。"
                />

                <template v-else>
                  <div class="message-list">
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
                          确认删除这封信件吗？
                        </n-popconfirm>
                      </div>
                      <p class="message-body">{{ item.context || "这封信暂时没有填写正文内容。" }}</p>
                    </article>
                  </div>

                  <div class="pagination-wrap">
                    <n-pagination
                      v-model:page="page"
                      :page-size="pageSize"
                      :item-count="messages.length"
                      show-size-picker
                      :page-sizes="[4, 8, 12]"
                      @update:page-size="handlePageSizeChange"
                    />
                  </div>
                </template>
              </n-spin>
            </n-card>
          </section>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </n-layout>

  <n-modal v-model:show="showCreateModal" @after-leave="resetCreateForm">
    <n-card
      class="reset-password-modal"
      title="新增信件"
      :bordered="false"
      size="huge"
      role="dialog"
      aria-modal="true"
      closable
      @close="closeCreateModal"
    >
      <n-form
        ref="createFormRef"
        class="auth-form auth-modal-form"
        :model="createForm"
        :rules="createRules"
        label-placement="top"
        require-mark-placement="right-hanging"
        @submit.prevent="handleCreateMessage"
      >
        <n-form-item path="headline" label="信件标题" class="auth-form-item">
          <n-input
            v-model:value="createForm.headline"
            class="auth-field-input"
            placeholder="请输入信件标题"
            @keydown.enter.prevent="handleCreateMessage"
          />
        </n-form-item>

        <n-form-item path="context" label="正文内容" class="auth-form-item">
          <n-input
            v-model:value="createForm.context"
            class="auth-field-input"
            type="textarea"
            placeholder="请输入正文内容"
          />
        </n-form-item>

        <div class="reset-modal-actions">
          <n-button attr-type="button" secondary @click="closeCreateModal">
            取消
          </n-button>
          <n-button type="primary" :loading="createMessageSubmitting" attr-type="submit">
            创建
          </n-button>
        </div>
      </n-form>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { computed, defineComponent, h, onMounted, reactive, ref, watch } from "vue";
import { useMessage, type FormInst, type FormRules, type MenuOption } from "naive-ui";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useMailStore } from "@/stores/mail";

type RailKey = "overview" | "mailboxes" | "messages" | "settings";

const router = useRouter();
const message = useMessage();
const authStore = useAuthStore();
const mailStore = useMailStore();

const sidebarCollapsed = ref(false);
const activeTopMenu = ref("dashboard");
const activeRail = ref<RailKey>("messages");
const pageRefreshing = ref(false);
const showCreateModal = ref(false);
const createMessageSubmitting = ref(false);
const selectedBoxId = ref<number | null>(null);
const page = ref(1);
const pageSize = ref(4);
const createFormRef = ref<FormInst | null>(null);
const createForm = reactive({
  headline: "",
  context: "",
});

function createIcon(nodes: Array<{ tag: string; attrs: Record<string, string | number> }>) {
  return defineComponent({ name: "ConsoleIcon", render: () => h("svg", { viewBox: "0 0 24 24", fill: "none", xmlns: "http://www.w3.org/2000/svg", stroke: "currentColor", "stroke-width": "1.8", "stroke-linecap": "round", "stroke-linejoin": "round" }, nodes.map((node) => h(node.tag, node.attrs))) });
}

const MailIcon = createIcon([{ tag: "rect", attrs: { x: 3, y: 5, width: 18, height: 14, rx: 3 } }, { tag: "path", attrs: { d: "M6 8.5L12 13l6-4.5" } }]);
const DashboardIcon = createIcon([{ tag: "rect", attrs: { x: 4, y: 4, width: 7, height: 7, rx: 1.5 } }, { tag: "rect", attrs: { x: 13, y: 4, width: 7, height: 5, rx: 1.5 } }, { tag: "rect", attrs: { x: 13, y: 11, width: 7, height: 9, rx: 1.5 } }, { tag: "rect", attrs: { x: 4, y: 13, width: 7, height: 7, rx: 1.5 } }]);
const BoxIcon = createIcon([{ tag: "path", attrs: { d: "M4 8.5L12 4l8 4.5-8 4.5-8-4.5Z" } }, { tag: "path", attrs: { d: "M4 8.5V16l8 4 8-4V8.5" } }, { tag: "path", attrs: { d: "M12 13v7" } }]);
const MessageIcon = createIcon([{ tag: "path", attrs: { d: "M5 6.5A2.5 2.5 0 0 1 7.5 4h9A2.5 2.5 0 0 1 19 6.5v6A2.5 2.5 0 0 1 16.5 15H11l-4 4v-4H7.5A2.5 2.5 0 0 1 5 12.5v-6Z" } }, { tag: "path", attrs: { d: "M8.5 8.5h7" } }, { tag: "path", attrs: { d: "M8.5 11.5h5" } }]);
const SettingIcon = createIcon([{ tag: "circle", attrs: { cx: 12, cy: 12, r: 3.2 } }, { tag: "path", attrs: { d: "M19.4 15a1 1 0 0 0 .2 1.1l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1 1 0 0 0-1.1-.2 1 1 0 0 0-.6.9V20a2 2 0 1 1-4 0v-.2a1 1 0 0 0-.7-.9 1 1 0 0 0-1.1.2l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1 1 0 0 0 .2-1.1 1 1 0 0 0-.9-.6H4a2 2 0 1 1 0-4h.2a1 1 0 0 0 .9-.7 1 1 0 0 0-.2-1.1l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1 1 0 0 0 1.1.2H9a1 1 0 0 0 .6-.9V4a2 2 0 1 1 4 0v.2a1 1 0 0 0 .7.9 1 1 0 0 0 1.1-.2l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1 1 0 0 0-.2 1.1V9c0 .4.2.7.6.8H20a2 2 0 1 1 0 4h-.2a1 1 0 0 0-.4 1.2Z" } }]);
const RefreshIcon = createIcon([{ tag: "path", attrs: { d: "M20 11a8 8 0 1 0 2 5.3" } }, { tag: "path", attrs: { d: "M20 4v7h-7" } }]);

const topMenuOptions: MenuOption[] = [{ label: "首页", key: "home" }, { label: "控制台", key: "dashboard" }, { label: "文档", key: "docs" }];
const railActions = [{ key: "overview", label: "总览", icon: DashboardIcon }, { key: "mailboxes", label: "信箱", icon: BoxIcon }, { key: "messages", label: "信件", icon: MessageIcon }, { key: "settings", label: "设置", icon: SettingIcon }] as const;
const primaryRailActions = railActions.filter((item) => item.key !== "settings");
const secondaryRailActions = railActions.filter((item) => item.key === "settings");

const createRules: FormRules = {
  headline: [
    {
      required: true,
      message: "请输入信件标题",
      trigger: ["input", "blur"],
    },
  ],
};

const userInitial = computed(() => (authStore.user?.name?.slice(0, 1).toUpperCase() || "U"));
const currentMailbox = computed(() => mailStore.mailboxes.find((item) => item.id === selectedBoxId.value) ?? null);
const currentMailboxTitle = computed(() => currentMailbox.value?.title || currentMailbox.value?.box_name || "信件管理");
const mailboxOptions = computed(() => mailStore.mailboxes.map((item) => ({
  label: item.title ? `${item.box_name} (${item.title})` : item.box_name,
  value: item.id,
})));
const messages = computed(() => {
  if (!selectedBoxId.value) {
    return [];
  }

  return [...(mailStore.messages[selectedBoxId.value] ?? [])].sort((a, b) => b.id - a.id);
});
const pagedMessages = computed(() => {
  const start = (page.value - 1) * pageSize.value;
  return messages.value.slice(start, start + pageSize.value);
});
const summaryText = computed(() => {
  if (!mailStore.mailboxes.length) {
    return "当前账号下还没有信箱，请先去信箱页创建一个信箱。";
  }

  if (!currentMailbox.value) {
    return "请选择一个信箱后查看该信箱下的信件。";
  }

  return `当前正在查看 ${currentMailbox.value.box_name} 的信件，可直接新增或删除。`;
});

function normalizePage() {
  const maxPage = Math.max(1, Math.ceil(messages.value.length / pageSize.value));
  if (page.value > maxPage) {
    page.value = maxPage;
  }
}

function resetCreateForm() {
  createForm.headline = "";
  createForm.context = "";
  createFormRef.value?.restoreValidation();
}

function openCreateModal() {
  if (!selectedBoxId.value) {
    message.warning("请先选择一个信箱");
    return;
  }

  resetCreateForm();
  showCreateModal.value = true;
}

function closeCreateModal() {
  showCreateModal.value = false;
}

async function initializePage() {
  pageRefreshing.value = true;
  try {
    await authStore.fetchUser();
    await mailStore.fetchMailboxes();
    selectedBoxId.value = mailStore.selectedMailboxId ?? mailStore.mailboxes[0]?.id ?? null;

    if (selectedBoxId.value) {
      await mailStore.fetchMessages(selectedBoxId.value);
    }

    normalizePage();
  } catch (error) {
    message.error(getErrorMessage(error));
  } finally {
    pageRefreshing.value = false;
  }
}

async function handleMailboxChange(value: number | null) {
  if (value === null) {
    selectedBoxId.value = null;
    return;
  }

  selectedBoxId.value = value;
  page.value = 1;

  try {
    await mailStore.fetchMessages(value);
    normalizePage();
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

async function refreshMessages() {
  if (!selectedBoxId.value) {
    await initializePage();
    return;
  }

  pageRefreshing.value = true;
  try {
    await authStore.fetchUser();
    await mailStore.fetchMessages(selectedBoxId.value);
    normalizePage();
  } catch (error) {
    message.error(getErrorMessage(error));
  } finally {
    pageRefreshing.value = false;
  }
}

async function handleCreateMessage() {
  if (!selectedBoxId.value) {
    message.warning("请先选择一个信箱");
    return;
  }

  try {
    await createFormRef.value?.validate();
    createMessageSubmitting.value = true;
    await mailStore.createMessage({
      headline: createForm.headline.trim(),
      context: createForm.context.trim(),
      box_id: selectedBoxId.value,
    });
    page.value = 1;
    closeCreateModal();
    normalizePage();
    message.success("信件创建成功");
  } catch (error) {
    if (error instanceof Error) {
      message.error(error.message);
    }
  } finally {
    createMessageSubmitting.value = false;
  }
}

async function handleDeleteMessage(messageId: number) {
  if (!selectedBoxId.value) {
    return;
  }

  try {
    await mailStore.deleteMessage(messageId, selectedBoxId.value);
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

function handleTopMenuSelect(key: string) {
  activeTopMenu.value = key;
  if (key === "docs") {
    if (typeof window !== "undefined") {
      const openedWindow = window.open("http://127.0.0.1:8003/docs", "_blank", "noopener,noreferrer");
      if (!openedWindow) {
        window.location.href = "http://127.0.0.1:8003/docs";
      }
    }
    activeTopMenu.value = "dashboard";
    return;
  }

  if (key === "home" || key === "dashboard") {
    void router.push({ name: "dashboard" });
    return;
  }

  message.info("当前仓库暂未单独实现文档页。");
  activeTopMenu.value = "dashboard";
}

function handleRailAction(key: RailKey) {
  activeRail.value = key;

  if (key === "messages") {
    return;
  }

  if (key === "mailboxes") {
    void router.push({ name: "mailboxes" });
    return;
  }

  if (key === "settings") {
    void router.push({ name: "settings" });
    return;
  }

  void router.push({ name: "dashboard" });
}

async function handleLogout() {
  authStore.logout();
  mailStore.reset();
  await router.push("/login");
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "操作失败";
}

watch(messages, () => {
  normalizePage();
});

onMounted(() => {
  void initializePage();
});
</script>
