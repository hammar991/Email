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
        <n-button circle quaternary :loading="pageRefreshing" @click="refreshCurrentView">
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
              <p class="console-greeting-kicker">Mailboxes</p>
              <h1 class="console-greeting-title">
                <span class="console-greeting-emoji">📮</span>
                <span>信箱管理</span>
              </h1>
              <p>{{ summaryText }}</p>
            </div>
            <n-tag round type="info">{{ displayedMailboxes.length }} 个信箱</n-tag>
          </section>

          <section class="console-main-column" style="margin-top: 18px;">
            <n-card class="glass-card console-analytics-card" :bordered="false">
              <template #header>
                <div class="card-title-row">
                  <span>信箱列表</span>
                  <n-tag round type="warning">{{ queryMode ? "精确查询" : "全部信箱" }}</n-tag>
                </div>
              </template>

              <div class="analytics-toolbar">
                <div class="analytics-toolbar-copy">
                  <strong>按信箱名称精确查询</strong>
                  <p>查询使用现有接口字段 `box_name`，操作列支持查看信件、复制 Token 和删除邮箱。</p>
                </div>
                <n-space class="analytics-toolbar-controls" align="end">
                  <n-input
                    v-model:value="searchBoxName"
                    clearable
                    placeholder="请输入 box_name"
                    style="width: min(320px, 100%);"
                    @keydown.enter.prevent="handleSearch"
                  />
                  <n-button type="primary" :loading="mailStore.loadingMailboxes" @click="handleSearch">
                    查询
                  </n-button>
                  <n-button secondary :disabled="!queryMode && !searchBoxName" @click="handleReset">
                    重置
                  </n-button>
                  <n-button type="primary" secondary @click="openCreateModal">
                    新增信箱
                  </n-button>
                </n-space>
              </div>

              <n-data-table
                class="console-data-table"
                :columns="columns"
                :data="displayedMailboxes"
                :loading="tableLoading"
                :bordered="false"
                :pagination="{ pageSize: 8 }"
                :row-key="rowKey"
              />
            </n-card>
          </section>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </n-layout>

  <n-modal v-model:show="showCreateModal" @after-leave="resetCreateForm">
    <n-card
      class="reset-password-modal"
      title="新增信箱"
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
        @submit.prevent="handleCreateMailbox"
      >
        <n-form-item path="name" label="信箱名称" class="auth-form-item">
          <n-input
            v-model:value="createForm.name"
            class="auth-field-input"
            placeholder="请输入信箱名称"
            @keydown.enter.prevent="handleCreateMailbox"
          />
        </n-form-item>

        <n-form-item path="title" label="标题" class="auth-form-item">
          <n-input
            v-model:value="createForm.title"
            class="auth-field-input"
            placeholder="请输入标题"
            @keydown.enter.prevent="handleCreateMailbox"
          />
        </n-form-item>

        <div class="reset-modal-actions">
          <n-button attr-type="button" secondary @click="closeCreateModal">
            取消
          </n-button>
          <n-button type="primary" :loading="createMailboxSubmitting" attr-type="submit">
            创建
          </n-button>
        </div>
      </n-form>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { computed, defineComponent, h, onMounted, reactive, ref } from "vue";
import { NButton, NPopconfirm, NSpace, useMessage, type DataTableColumns, type FormInst, type FormRules, type MenuOption } from "naive-ui";
import { useRouter } from "vue-router";
import type { MailboxInfo, MailboxPayload } from "@/api/types";
import { useAuthStore } from "@/stores/auth";
import { useMailStore } from "@/stores/mail";

type RailKey = "overview" | "mailboxes" | "messages" | "settings";

const router = useRouter();
const message = useMessage();
const authStore = useAuthStore();
const mailStore = useMailStore();

const sidebarCollapsed = ref(false);
const activeTopMenu = ref("dashboard");
const activeRail = ref<RailKey>("mailboxes");
const pageRefreshing = ref(false);
const showCreateModal = ref(false);
const createMailboxSubmitting = ref(false);
const searchBoxName = ref("");
const queryMode = ref(false);
const queriedMailboxes = ref<MailboxInfo[]>([]);
const createFormRef = ref<FormInst | null>(null);
const createForm = reactive<MailboxPayload>({
  name: "",
  title: "",
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
  name: [
    {
      required: true,
      message: "请输入信箱名称",
      trigger: ["input", "blur"],
    },
  ],
};

const userInitial = computed(() => (authStore.user?.name?.slice(0, 1).toUpperCase() || "U"));
const sortedMailboxes = computed(() => [...mailStore.mailboxes].sort((a, b) => b.id - a.id));
const displayedMailboxes = computed(() => queryMode.value ? queriedMailboxes.value : sortedMailboxes.value);
const tableLoading = computed(() => pageRefreshing.value || mailStore.loadingMailboxes || createMailboxSubmitting.value);
const summaryText = computed(() => {
  if (queryMode.value) {
    if (!displayedMailboxes.value.length) {
      return `当前没有查询到名称为 ${searchBoxName.value.trim() || "指定值"} 的信箱。`;
    }
    return `当前按 box_name 精确查询：${searchBoxName.value.trim()}。`;
  }

  return `当前账号下共有 ${sortedMailboxes.value.length} 个信箱，可直接在表格中查看、复制 Token 或进入信件页。`;
});

const columns = computed<DataTableColumns<MailboxInfo>>(() => [
  { title: "ID", key: "id", width: 72 },
  { title: "信箱名称", key: "box_name", ellipsis: { tooltip: true } },
  { title: "标题", key: "title", render: (row) => row.title || "未设置标题", ellipsis: { tooltip: true } },
  {
    title: "分享 Token",
    key: "share_token",
    minWidth: 220,
    ellipsis: { tooltip: true },
    render: (row) => h("code", { style: { fontSize: "12px" } }, row.share_token),
  },
  {
    title: "操作",
    key: "actions",
    width: 290,
    render: (row) => h(NSpace, { wrap: false }, {
      default: () => [
        h(NButton, { size: "small", type: "primary", secondary: true, onClick: () => handleViewMessages(row) }, { default: () => "查看信件" }),
        h(NButton, { size: "small", type: "info", secondary: true, onClick: () => copyShareToken(row) }, { default: () => "复制 Token" }),
        h(NPopconfirm, { onPositiveClick: () => handleDeleteMailbox(row) }, {
          trigger: () => h(NButton, { size: "small", type: "error", tertiary: true }, { default: () => "删除邮箱" }),
          default: () => "确认删除这个信箱吗？",
        }),
      ],
    }),
  },
]);

function rowKey(row: MailboxInfo) {
  return row.id;
}

function clearQueryState() {
  queryMode.value = false;
  queriedMailboxes.value = [];
  searchBoxName.value = "";
}

function resetCreateForm() {
  createForm.name = "";
  createForm.title = "";
  createFormRef.value?.restoreValidation();
}

function openCreateModal() {
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
  } catch (error) {
    message.error(getErrorMessage(error));
  } finally {
    pageRefreshing.value = false;
  }
}

async function handleSearch() {
  const keyword = searchBoxName.value.trim();
  if (!keyword) {
    message.warning("请输入信箱名称");
    return;
  }

  queryMode.value = true;
  try {
    const mailbox = await mailStore.fetchMailboxByName(keyword);
    queriedMailboxes.value = mailbox ? [mailbox] : [];
    if (!mailbox) {
      message.error("未查询到对应信箱");
    }
  } catch (error) {
    queriedMailboxes.value = [];
    message.error(getErrorMessage(error));
  }
}

async function handleReset() {
  clearQueryState();
  pageRefreshing.value = true;
  try {
    await mailStore.fetchMailboxes();
  } catch (error) {
    message.error(getErrorMessage(error));
  } finally {
    pageRefreshing.value = false;
  }
}

async function refreshCurrentView() {
  pageRefreshing.value = true;
  try {
    await authStore.fetchUser();
    if (queryMode.value && searchBoxName.value.trim()) {
      const mailbox = await mailStore.fetchMailboxByName(searchBoxName.value.trim());
      queriedMailboxes.value = mailbox ? [mailbox] : [];
    } else {
      await mailStore.fetchMailboxes();
    }
  } catch (error) {
    if (queryMode.value) {
      queriedMailboxes.value = [];
    }
    message.error(getErrorMessage(error));
  } finally {
    pageRefreshing.value = false;
  }
}

async function handleCreateMailbox() {
  try {
    await createFormRef.value?.validate();
    createMailboxSubmitting.value = true;
    await mailStore.createMailbox({
      name: createForm.name.trim(),
      title: createForm.title.trim(),
    });
    message.success("信箱创建成功");
    closeCreateModal();
    clearQueryState();
    await mailStore.fetchMailboxes();
  } catch (error) {
    if (error instanceof Error) {
      message.error(error.message);
    }
  } finally {
    createMailboxSubmitting.value = false;
  }
}

async function handleDeleteMailbox(row: MailboxInfo) {
  try {
    await mailStore.deleteMailbox(row.id);
    message.success("信箱已删除");

    if (queryMode.value && searchBoxName.value.trim() === row.box_name) {
      clearQueryState();
      await mailStore.fetchMailboxes();
    }
  } catch (error) {
    message.error(getErrorMessage(error));
  }
}

function handleViewMessages(row: MailboxInfo) {
  void router.push({
    name: "mailbox-messages",
    params: { boxId: String(row.id) },
    query: { title: row.title || "", boxName: row.box_name },
  });
}

async function copyShareToken(row: MailboxInfo) {
  try {
    await navigator.clipboard.writeText(row.share_token);
    message.success("分享 Token 已复制");
  } catch {
    message.warning("复制失败，请手动复制该 Token");
  }
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
  if (key === "mailboxes") {
    return;
  }

  if (key === "messages") {
    void router.push({ name: "messages" });
    return;
  }

  if (key === "settings") {
    void router.push({ name: "settings" });
    return;
  }

  void router.push({
    name: "dashboard",
    query: key === "overview" ? {} : { rail: key },
  });
}

async function handleLogout() {
  authStore.logout();
  mailStore.reset();
  await router.push("/login");
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "操作失败";
}

onMounted(() => {
  void initializePage();
});
</script>
