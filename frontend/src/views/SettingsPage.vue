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
        <n-button circle quaternary :loading="pageRefreshing" @click="refreshSettings">
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
              <p class="console-greeting-kicker">Settings</p>
              <h1 class="console-greeting-title">
                <span class="console-greeting-emoji">⚙️</span>
                <span>账户设置</span>
              </h1>
              <p>在这里维护当前账号的邮箱地址。这个页面只复用现有的用户信息和更新接口，不改动其他接口行为。</p>
            </div>
          </section>

          <section class="console-main-column" style="max-width: 420px; margin-top: 18px;">
            <n-card class="glass-card" :bordered="false">
              <template #header>
                <div class="card-title-row">
                  <span>账户设置</span>
                  <n-tag round type="info">UserUpdate.email</n-tag>
                </div>
              </template>

              <div class="user-summary">
                <n-avatar round size="large" color="#60a5fa">{{ userInitial }}</n-avatar>
                <div>
                  <strong>{{ authStore.user?.name ?? "未知用户" }}</strong>
                  <p class="muted">{{ authStore.user?.email ?? "暂无邮箱信息" }}</p>
                </div>
              </div>

              <n-form :model="profileForm" label-placement="top" @submit.prevent="handleUpdateProfile">
                <n-form-item label="邮箱地址">
                  <n-input v-model:value="profileForm.email" placeholder="请输入新的邮箱地址" />
                </n-form-item>
                <n-button block type="primary" :disabled="!canSubmitProfile" :loading="authStore.loading" attr-type="submit">
                  保存邮箱
                </n-button>
              </n-form>
            </n-card>
          </section>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { computed, defineComponent, h, onMounted, reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useMessage, type MenuOption } from "naive-ui";
import { useAuthStore } from "@/stores/auth";
import { useMailStore } from "@/stores/mail";

type RailKey = "overview" | "mailboxes" | "messages" | "settings";

const router = useRouter();
const message = useMessage();
const authStore = useAuthStore();
const mailStore = useMailStore();

const sidebarCollapsed = ref(false);
const activeTopMenu = ref("dashboard");
const activeRail = ref<RailKey>("settings");
const pageRefreshing = ref(false);
const profileForm = reactive({ email: "" });

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

const userInitial = computed(() => (authStore.user?.name?.slice(0, 1).toUpperCase() || "U"));
const canSubmitProfile = computed(() => {
  const email = profileForm.email.trim();
  return Boolean(email) && email !== (authStore.user?.email ?? "");
});

async function initializePage() {
  pageRefreshing.value = true;
  try {
    await authStore.fetchUser();
  } catch (error) {
    message.error(getErrorMessage(error));
  } finally {
    pageRefreshing.value = false;
  }
}

async function refreshSettings() {
  await initializePage();
}

async function handleUpdateProfile() {
  if (!canSubmitProfile.value) {
    message.warning("请输入新的邮箱地址");
    return;
  }

  try {
    await authStore.updateUser({ email: profileForm.email.trim() });
    message.success("用户邮箱已更新");
  } catch (error) {
    message.error(getErrorMessage(error));
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

  if (key === "settings") {
    return;
  }

  if (key === "mailboxes") {
    void router.push({ name: "mailboxes" });
    return;
  }

  if (key === "messages") {
    void router.push({ name: "messages" });
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

watch(() => authStore.user, (value) => {
  profileForm.email = value?.email ?? "";
}, { immediate: true });

onMounted(() => {
  void initializePage();
});
</script>
