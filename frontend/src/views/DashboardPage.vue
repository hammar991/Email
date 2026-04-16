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
        <n-button circle quaternary :loading="dashboardRefreshing" @click="refreshDashboard">
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
        <section ref="overviewSectionRef" class="console-welcome">
          <div>
            <p class="console-greeting-kicker">Dashboard</p>
            <h1 class="console-greeting-title">
              <span class="console-greeting-emoji">👋</span>
              <span>早上好，{{ authStore.user?.name ?? "欢迎回来" }}</span>
            </h1>
            <p>当前已连接 {{ mailboxRows.length }} 个信箱，已加载 {{ totalLoadedMessages }} 条信件。</p>
          </div>
          <n-space>
            <n-button type="primary" :loading="dashboardRefreshing" @click="refreshDashboard">刷新数据</n-button>
            <n-button secondary type="primary" :disabled="!mailStore.selectedMailbox" @click="handleOpenSelectedMailbox">
              当前信箱
            </n-button>
          </n-space>
        </section>

        <n-grid class="console-metrics" cols="1 s:2 l:4" responsive="screen" x-gap="18" y-gap="18">
          <n-gi v-for="card in statCards" :key="card.key">
            <n-card class="glass-card metric-card" :bordered="false">
              <div class="metric-card-head">
                <div class="metric-card-badge">
                  <n-avatar round class="metric-avatar" :color="card.avatarColor" :style="{ color: card.avatarTextColor }">
                    {{ card.symbol }}
                  </n-avatar>
                  <n-statistic class="metric-value" :label="card.title" :value="card.value" :precision="card.precision">
                    <template v-if="card.suffix" #suffix>{{ card.suffix }}</template>
                  </n-statistic>
                </div>
                <n-tag round :bordered="false" :color="{ color: card.tagBg, textColor: card.tagText }">{{ card.tag }}</n-tag>
              </div>
              <p class="metric-note">{{ card.note }}</p>
            </n-card>
          </n-gi>
        </n-grid>

        <div class="console-main-grid">
          <section ref="analysisSectionRef" class="console-main-column">
            <n-card class="glass-card console-analytics-card" :bordered="false">
              <template #header>
                <div class="card-title-row">
                  <span>信箱分析</span>
                  <n-tag round type="info">Naive UI</n-tag>
                </div>
              </template>

              <n-tabs v-model:value="analysisTab" animated>
                <n-tab-pane name="mailboxes" tab="信箱列表">
                  <n-data-table
                    class="console-data-table"
                    :columns="columns"
                    :data="mailboxRows"
                    :loading="mailStore.loadingMailboxes || dashboardRefreshing"
                    :bordered="false"
                    :pagination="{ pageSize: 6 }"
                    :row-key="rowKey"
                  />
                </n-tab-pane>

                <n-tab-pane name="messages" tab="最近信件">
                  <div class="message-tab-head">
                    <div>
                      <p class="mini-label">当前聚焦</p>
                      <h3>{{ mailStore.selectedMailbox?.box_name ?? "未选择信箱" }}</h3>
                    </div>
                    <n-button secondary type="primary" :disabled="!mailStore.selectedMailbox" @click="handleOpenSelectedMailbox">查看全部</n-button>
                  </div>

                  <n-empty v-if="!selectedMessages.length" description="当前信箱还没有信件" />
                  <n-list v-else hoverable clickable class="recent-message-list">
                    <n-list-item v-for="item in selectedMessages.slice(0, 6)" :key="item.id">
                      <n-thing :title="item.headline" :description="`消息 ID: ${item.id}`">{{ item.context || "这封信暂时没有填写正文内容。" }}</n-thing>
                    </n-list-item>
                  </n-list>
                </n-tab-pane>
              </n-tabs>
            </n-card>
          </section>

          <aside ref="settingsSectionRef" class="console-side-column">
            <n-card class="glass-card" :bordered="false">
              <template #header>
                <div class="card-title-row">
                  <span>分享 / API 信息</span>
                  <n-tag round type="warning">{{ mailStore.selectedMailbox ? "已就绪" : "待创建" }}</n-tag>
                </div>
              </template>

              <div v-if="mailStore.selectedMailbox" class="share-info-panel">
                <n-descriptions bordered label-placement="top" :column="1" size="small">
                  <n-descriptions-item label="当前信箱">{{ mailStore.selectedMailbox.box_name }}</n-descriptions-item>
                  <n-descriptions-item label="信箱标题">{{ mailStore.selectedMailbox.title || "未设置标题" }}</n-descriptions-item>
                  <n-descriptions-item label="分享 Token">{{ mailStore.selectedMailbox.share_token }}</n-descriptions-item>
                </n-descriptions>
                <div class="share-link-box">{{ publicDeliveryLink || "当前信箱暂无公开投递链接" }}</div>
                <n-space wrap>
                  <n-button type="primary" secondary @click="copyShareToken(mailStore.selectedMailbox)">复制 Token</n-button>
                  <n-button secondary type="info" :disabled="!publicDeliveryLink" @click="copyPublicLink">复制链接</n-button>
                </n-space>
              </div>
              <n-empty v-else description="暂无 API 信息" />
            </n-card>

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
                <n-button block type="primary" :disabled="!canSubmitProfile" :loading="authStore.loading" attr-type="submit">保存邮箱</n-button>
              </n-form>
            </n-card>
          </aside>
        </div>
      </n-layout-content>
    </n-layout>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { computed, defineComponent, h, onMounted, reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";
import type { DataTableColumns, MenuOption } from "naive-ui";
import { NButton, NPopconfirm, NSpace, NTag, useMessage } from "naive-ui";
import type { MailboxInfo, MessageInfo } from "@/api/types";
import { useAuthStore } from "@/stores/auth";
import { useMailStore } from "@/stores/mail";

interface DashboardMailboxRow extends MailboxInfo { messageCount: number; shared: boolean }
type RailKey = "overview" | "mailboxes" | "messages" | "settings";

const router = useRouter();
const message = useMessage();
const authStore = useAuthStore();
const mailStore = useMailStore();

const dashboardRefreshing = ref(false);
const sidebarCollapsed = ref(false);
const activeTopMenu = ref("dashboard");
const analysisTab = ref<"mailboxes" | "messages">("mailboxes");
const activeRail = ref<RailKey>("overview");
const overviewSectionRef = ref<HTMLElement | null>(null);
const analysisSectionRef = ref<HTMLElement | null>(null);
const settingsSectionRef = ref<HTMLElement | null>(null);
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
const mailboxRows = computed<DashboardMailboxRow[]>(() => [...mailStore.mailboxes].map((item) => ({ ...item, messageCount: mailStore.messages[item.id]?.length ?? 0, shared: Boolean(item.share_token) })).sort((a, b) => b.id - a.id));
const totalLoadedMessages = computed(() => Object.values(mailStore.messages).reduce((sum, items) => sum + items.length, 0));
const selectedMessages = computed<MessageInfo[]>(() => mailStore.selectedMailboxId ? [...(mailStore.messages[mailStore.selectedMailboxId] ?? [])].sort((a, b) => b.id - a.id) : []);
const sharedMailboxCount = computed(() => mailboxRows.value.filter((item) => item.shared).length);
const shareCoverage = computed(() => mailboxRows.value.length ? Math.round((sharedMailboxCount.value / mailboxRows.value.length) * 100) : 0);
const averageMessagesPerMailbox = computed(() => mailboxRows.value.length ? Number((totalLoadedMessages.value / mailboxRows.value.length).toFixed(1)) : 0);
const publicDeliveryLink = computed(() => mailStore.selectedMailbox?.share_token ? `${window.location.origin}/public/${mailStore.selectedMailbox.share_token}` : "");
const canSubmitProfile = computed(() => { const email = profileForm.email.trim(); return Boolean(email) && email !== (authStore.user?.email ?? ""); });

const statCards = computed(() => [
  { key: "mailboxes", symbol: "箱", title: "信箱总数", value: mailboxRows.value.length, precision: 0, suffix: "个", note: "当前账号下的信箱总数", tag: "总览", tagBg: "#eff6ff", tagText: "#2563eb", avatarColor: "#dbeafe", avatarTextColor: "#2563eb" },
  { key: "messages", symbol: "信", title: "已加载信件", value: totalLoadedMessages.value, precision: 0, suffix: "封", note: "已拉取到本地的信件数量", tag: "实时", tagBg: "#ecfdf5", tagText: "#059669", avatarColor: "#d1fae5", avatarTextColor: "#059669" },
  { key: "shared", symbol: "享", title: "分享入口", value: sharedMailboxCount.value, precision: 0, suffix: "个", note: `分享覆盖率 ${shareCoverage.value}%`, tag: "公开", tagBg: "#fff7ed", tagText: "#c2410c", avatarColor: "#ffedd5", avatarTextColor: "#ea580c" },
  { key: "average", symbol: "均", title: "平均每箱信件", value: averageMessagesPerMailbox.value, precision: 1, suffix: "封", note: "按当前已加载数据统计", tag: "聚焦", tagBg: "#f5f3ff", tagText: "#7c3aed", avatarColor: "#ede9fe", avatarTextColor: "#7c3aed" },
]);

const columns = computed<DataTableColumns<DashboardMailboxRow>>(() => [
  { title: "信箱名称", key: "box_name", ellipsis: { tooltip: true } },
  { title: "标题", key: "title", render: (row) => row.title || "未设置标题" },
  { title: "信件数", key: "messageCount", width: 100 },
  { title: "分享状态", key: "shared", width: 110, render: (row) => h(NTag, { round: true, type: row.shared ? "success" : "default" }, { default: () => row.shared ? "已开启" : "未开启" }) },
  {
    title: "操作",
    key: "actions",
    width: 320,
    render: (row) => h(NSpace, { wrap: false }, {
      default: () => [
        h(NButton, { size: "small", type: "primary", secondary: true, onClick: () => handleViewMessages(row) }, { default: () => "查看信件" }),
        h(NButton, { size: "small", type: "info", secondary: true, onClick: () => copyShareToken(row) }, { default: () => "复制 Token" }),
        h(NPopconfirm, { onPositiveClick: () => handleDeleteMailbox(row.id) }, {
          trigger: () => h(NButton, { size: "small", type: "error", tertiary: true }, { default: () => "删除" }),
          default: () => "确认删除这个信箱吗？",
        }),
      ],
    }),
  },
]);

function rowKey(row: MailboxInfo) { return row.id; }
function scrollToSection(target: HTMLElement | null) { target?.scrollIntoView({ behavior: "smooth", block: "start" }); }
function focusMailboxTable() { activeRail.value = "mailboxes"; analysisTab.value = "mailboxes"; scrollToSection(analysisSectionRef.value); }
function handleTopMenuSelect(key: string) { activeTopMenu.value = key; if (key === "home" || key === "dashboard") { activeRail.value = "overview"; scrollToSection(overviewSectionRef.value); return; } message.info("当前仓库暂未单独实现文档页。"); activeTopMenu.value = "dashboard"; }
function handleRailAction(key: RailKey) { activeRail.value = key; if (key === "overview") { scrollToSection(overviewSectionRef.value); return; } if (key === "mailboxes" || key === "messages") { analysisTab.value = key === "mailboxes" ? "mailboxes" : "messages"; scrollToSection(analysisSectionRef.value); return; } scrollToSection(settingsSectionRef.value); }

async function hydrateMailboxMessages() { const currentSelectedId = mailStore.selectedMailboxId; for (const mailbox of mailStore.mailboxes) await mailStore.fetchMessages(mailbox.id); mailStore.selectedMailboxId = currentSelectedId ?? mailStore.mailboxes[0]?.id ?? null; }
async function refreshDashboard() { dashboardRefreshing.value = true; try { await authStore.fetchUser(); await mailStore.fetchMailboxes(); await hydrateMailboxMessages(); } catch (error) { message.error(getErrorMessage(error)); } finally { dashboardRefreshing.value = false; } }
async function handleSelectMailbox(boxId: number) { try { await mailStore.fetchMessages(boxId); analysisTab.value = "messages"; } catch (error) { message.error(getErrorMessage(error)); } }
async function handleDeleteMailbox(boxId: number) { try { await mailStore.deleteMailbox(boxId); message.success("信箱已删除"); } catch (error) { message.error(getErrorMessage(error)); } }
function handleViewMessages(row: MailboxInfo) { void router.push({ name: "mailbox-messages", params: { boxId: String(row.id) }, query: { title: row.title || "", boxName: row.box_name } }); }
function handleOpenSelectedMailbox() { if (!mailStore.selectedMailbox) { message.warning("请先选择一个信箱"); return; } handleViewMessages(mailStore.selectedMailbox); }

async function copyShareToken(row: MailboxInfo) { try { await navigator.clipboard.writeText(row.share_token); message.success("分享 Token 已复制"); } catch { message.warning("复制失败，请手动复制该 Token"); } }

async function copyPublicLink() { if (!publicDeliveryLink.value) { message.warning("当前没有可复制的公开投递链接"); return; } try { await navigator.clipboard.writeText(publicDeliveryLink.value); message.success("公开投递链接已复制"); } catch { message.warning("复制失败，请手动复制链接"); } }

async function handleUpdateProfile() { if (!canSubmitProfile.value) { message.warning("请输入新的邮箱地址"); return; } try { await authStore.updateUser({ email: profileForm.email.trim() }); message.success("用户邮箱已更新"); } catch (error) { message.error(getErrorMessage(error)); } }

async function handleLogout() 
{ 
  authStore.logout(); 
  mailStore.reset(); 
  await router.push("/login"); 
}
function getErrorMessage(error: unknown) { return error instanceof Error ? error.message : "操作失败"; }

watch(() => authStore.user, (value) => { profileForm.email = value?.email ?? ""; }, { immediate: true });
onMounted(async () => { await refreshDashboard(); focusMailboxTable(); });
</script>
