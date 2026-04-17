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
              <p class="console-greeting-kicker">控制台</p>
              <h1 class="console-greeting-title">
                <span class="console-greeting-emoji">你好</span>
                <span>欢迎回来，{{ authStore.user?.name ?? "用户" }}</span>
              </h1>
              <p>
                当前已连接 {{ mailboxRows.length }} 个信箱，已加载 {{ totalLoadedMessages }} 封信件。
              </p>
            </div>
            <n-space>
              <n-button type="primary" :loading="dashboardRefreshing" @click="refreshDashboard">
                刷新数据
              </n-button>
              <n-button
                secondary
                type="primary"
                :disabled="!mailStore.selectedMailbox"
                @click="handleOpenSelectedMailbox"
              >
                查看当前信箱
              </n-button>
            </n-space>
          </section>

          <n-grid class="console-metrics" cols="1 s:2 l:4" responsive="screen" x-gap="18" y-gap="18">
            <n-gi v-for="card in statCards" :key="card.key">
              <n-card class="glass-card metric-card" :bordered="false">
                <div class="metric-card-head">
                  <div class="metric-card-badge">
                    <n-avatar
                      round
                      class="metric-avatar"
                      :color="card.avatarColor"
                      :style="{ color: card.avatarTextColor }"
                    >
                      {{ card.symbol }}
                    </n-avatar>
                    <n-statistic class="metric-value" :label="card.title" :value="card.value" :precision="card.precision">
                      <template v-if="card.suffix" #suffix>{{ card.suffix }}</template>
                    </n-statistic>
                  </div>
                  <n-tag round :bordered="false" :color="{ color: card.tagBg, textColor: card.tagText }">
                    {{ card.tag }}
                  </n-tag>
                </div>
                <p class="metric-note">{{ card.note }}</p>
              </n-card>
            </n-gi>
          </n-grid>

          <div class="console-main-grid">
            <section ref="insightsSectionRef" class="console-main-column">
              <n-card class="glass-card console-analytics-card" :bordered="false">
                <template #header>
                  <div class="card-title-row">
                    <span>每日信件趋势</span>
                    <n-tag round type="info">Canvas / {{ trendModeLabel }}</n-tag>
                  </div>
                </template>

                <div class="analytics-toolbar">
                  <div class="analytics-toolbar-copy">
                    <strong>每日总信件数量</strong>
                  <div class="analytics-toolbar-meta">{{ chartSummary }}</div>
                  </div>
                  <div class="analytics-toolbar-side">
                    <n-space :size="8" class="analytics-toolbar-controls">
                      <n-button
                        size="small"
                        round
                        class="analytics-mode-button"
                        :type="trendMode === 'line' ? 'primary' : 'default'"
                        :secondary="trendMode === 'line'"
                        @click="trendMode = 'line'"
                      >
                        折线图
                      </n-button>
                      <n-button
                        size="small"
                        round
                        class="analytics-mode-button"
                        :type="trendMode === 'bar' ? 'primary' : 'default'"
                        :secondary="trendMode === 'bar'"
                        @click="trendMode = 'bar'"
                      >
                        柱状图
                      </n-button>
                    </n-space>
                  </div>
                </div>

                <div class="analytics-chart-shell" :class="{ 'is-empty': !dailyMessageTrend.length }">
                  <canvas
                    v-if="dailyMessageTrend.length"
                    ref="trendCanvasRef"
                    class="analytics-chart analytics-canvas"
                  />
                  <n-empty v-else description="当前还没有可统计的信件数据" />
                </div>
              </n-card>
            </section>

            <aside class="console-side-column">
              <n-card class="glass-card" :bordered="false">
                <template #header>
                  <div class="card-title-row">
                    <span>分享 / API 信息</span>
                    <n-tag round type="warning">{{ mailStore.selectedMailbox ? "已就绪" : "待选择" }}</n-tag>
                  </div>
                </template>

                <div v-if="mailStore.selectedMailbox" class="share-info-panel">
                  <n-descriptions bordered label-placement="top" :column="1" size="small">
                    <n-descriptions-item label="当前信箱">
                      {{ mailStore.selectedMailbox.box_name }}
                    </n-descriptions-item>
                    <n-descriptions-item label="信箱标题">
                      {{ mailStore.selectedMailbox.title || "未设置标题" }}
                    </n-descriptions-item>
                    <n-descriptions-item label="分享 Token">
                      {{ mailStore.selectedMailbox.share_token }}
                    </n-descriptions-item>
                  </n-descriptions>
                  <div class="share-link-box">
                    {{ publicDeliveryLink || "当前信箱暂无公开投递链接" }}
                  </div>
                  <n-space wrap>
                    <n-button type="primary" secondary @click="copyShareToken(mailStore.selectedMailbox)">
                      复制 Token
                    </n-button>
                    <n-button secondary type="info" :disabled="!publicDeliveryLink" @click="copyPublicLink">
                      复制链接
                    </n-button>
                  </n-space>
                </div>
                <n-empty v-else description="暂无 API 信息" />
              </n-card>
            </aside>
          </div>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { computed, defineComponent, h, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useMessage, type MenuOption } from "naive-ui";
import type { MessageInfo } from "@/api/types";
import { useAuthStore } from "@/stores/auth";
import { useMailStore } from "@/stores/mail";

type RailKey = "overview" | "mailboxes" | "messages" | "settings";
type TrendMode = "line" | "bar";

interface DailyMessagePoint {
  dateKey: string;
  label: string;
  count: number;
}

interface TrendCoordinate {
  x: number;
  y: number;
  count: number;
  label: string;
}

interface ChartPadding {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

const router = useRouter();
const message = useMessage();
const authStore = useAuthStore();
const mailStore = useMailStore();

const dashboardRefreshing = ref(false);
const sidebarCollapsed = ref(false);
const activeTopMenu = ref("dashboard");
const activeRail = ref<RailKey>("overview");
const trendMode = ref<TrendMode>("line");
const overviewSectionRef = ref<HTMLElement | null>(null);
const insightsSectionRef = ref<HTMLElement | null>(null);
const trendCanvasRef = ref<HTMLCanvasElement | null>(null);
let trendFrameHandle: number | null = null;

function createIcon(nodes: Array<{ tag: string; attrs: Record<string, string | number> }>) {
  return defineComponent({
    name: "ConsoleIcon",
    render: () => h(
      "svg",
      {
        viewBox: "0 0 24 24",
        fill: "none",
        xmlns: "http://www.w3.org/2000/svg",
        stroke: "currentColor",
        "stroke-width": "1.8",
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
      },
      nodes.map((node) => h(node.tag, node.attrs)),
    ),
  });
}

const MailIcon = createIcon([
  { tag: "rect", attrs: { x: 3, y: 5, width: 18, height: 14, rx: 3 } },
  { tag: "path", attrs: { d: "M6 8.5L12 13l6-4.5" } },
]);
const DashboardIcon = createIcon([
  { tag: "rect", attrs: { x: 4, y: 4, width: 7, height: 7, rx: 1.5 } },
  { tag: "rect", attrs: { x: 13, y: 4, width: 7, height: 5, rx: 1.5 } },
  { tag: "rect", attrs: { x: 13, y: 11, width: 7, height: 9, rx: 1.5 } },
  { tag: "rect", attrs: { x: 4, y: 13, width: 7, height: 7, rx: 1.5 } },
]);
const BoxIcon = createIcon([
  { tag: "path", attrs: { d: "M4 8.5L12 4l8 4.5-8 4.5-8-4.5Z" } },
  { tag: "path", attrs: { d: "M4 8.5V16l8 4 8-4V8.5" } },
  { tag: "path", attrs: { d: "M12 13v7" } },
]);
const MessageIcon = createIcon([
  {
    tag: "path",
    attrs: { d: "M5 6.5A2.5 2.5 0 0 1 7.5 4h9A2.5 2.5 0 0 1 19 6.5v6A2.5 2.5 0 0 1 16.5 15H11l-4 4v-4H7.5A2.5 2.5 0 0 1 5 12.5v-6Z" },
  },
  { tag: "path", attrs: { d: "M8.5 8.5h7" } },
  { tag: "path", attrs: { d: "M8.5 11.5h5" } },
]);
const SettingIcon = createIcon([
  { tag: "circle", attrs: { cx: 12, cy: 12, r: 3.2 } },
  {
    tag: "path",
    attrs: { d: "M19.4 15a1 1 0 0 0 .2 1.1l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1 1 0 0 0-1.1-.2 1 1 0 0 0-.6.9V20a2 2 0 1 1-4 0v-.2a1 1 0 0 0-.7-.9 1 1 0 0 0-1.1.2l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1 1 0 0 0 .2-1.1 1 1 0 0 0-.9-.6H4a2 2 0 1 1 0-4h.2a1 1 0 0 0 .9-.7 1 1 0 0 0-.2-1.1l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1 1 0 0 0 1.1.2H9a1 1 0 0 0 .6-.9V4a2 2 0 1 1 4 0v.2a1 1 0 0 0 .7.9 1 1 0 0 0 1.1-.2l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1 1 0 0 0-.2 1.1V9c0 .4.2.7.6.8H20a2 2 0 1 1 0 4h-.2a1 1 0 0 0-.4 1.2Z" },
  },
]);
const RefreshIcon = createIcon([
  { tag: "path", attrs: { d: "M20 11a8 8 0 1 0 2 5.3" } },
  { tag: "path", attrs: { d: "M20 4v7h-7" } },
]);

const topMenuOptions: MenuOption[] = [
  { label: "首页", key: "home" },
  { label: "控制台", key: "dashboard" },
  { label: "文档", key: "docs" },
];

const railActions = [
  { key: "overview", label: "总览", icon: DashboardIcon },
  { key: "mailboxes", label: "信箱", icon: BoxIcon },
  { key: "messages", label: "信件", icon: MessageIcon },
  { key: "settings", label: "设置", icon: SettingIcon },
] as const;

const primaryRailActions = railActions.filter((item) => item.key !== "settings");
const secondaryRailActions = railActions.filter((item) => item.key === "settings");

const userInitial = computed(() => authStore.user?.name?.slice(0, 1).toUpperCase() || "U");
const mailboxRows = computed(() => [...mailStore.mailboxes].sort((a, b) => b.id - a.id));
const totalLoadedMessages = computed(() => Object.values(mailStore.messages).reduce((sum, items) => sum + items.length, 0));
const sharedMailboxCount = computed(() => mailboxRows.value.filter((item) => Boolean(item.share_token)).length);
const shareCoverage = computed(() => {
  if (!mailboxRows.value.length) {
    return 0;
  }

  return Math.round((sharedMailboxCount.value / mailboxRows.value.length) * 100);
});
const averageMessagesPerMailbox = computed(() => {
  if (!mailboxRows.value.length) {
    return 0;
  }

  return Number((totalLoadedMessages.value / mailboxRows.value.length).toFixed(1));
});
const publicDeliveryLink = computed(() => {
  if (!mailStore.selectedMailbox?.share_token || typeof window === "undefined") {
    return "";
  }

  return `${window.location.origin}/public/${mailStore.selectedMailbox.share_token}`;
});
const allMessages = computed<MessageInfo[]>(() => Object.values(mailStore.messages).flat());
const trendModeLabel = computed(() => trendMode.value === "line" ? "折线图" : "柱状图");

const dailyMessageTrend = computed<DailyMessagePoint[]>(() => {
  const totals = new Map<string, number>();

  allMessages.value.forEach((item) => {
    const dateKey = normalizeDateKey(item.created_at);
    totals.set(dateKey, (totals.get(dateKey) ?? 0) + 1);
  });

  return [...totals.entries()]
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([dateKey, count]) => ({
      dateKey,
      label: formatTrendDateLabel(dateKey),
      count,
    }));
});

const chartSummary = computed(() => {
  if (!dailyMessageTrend.value.length) {
    return "当前还没有可绘制的趋势数据。";
  }

  const latest = dailyMessageTrend.value[dailyMessageTrend.value.length - 1];
  const peak = dailyMessageTrend.value.reduce((currentMax, item) => item.count > currentMax.count ? item : currentMax);
  return `最近一天 ${latest.label} 共 ${latest.count} 封，峰值出现在 ${peak.label}，共 ${peak.count} 封。`;
});

const statCards = computed(() => [
  {
    key: "mailboxes",
    symbol: "箱",
    title: "信箱总数",
    value: mailboxRows.value.length,
    precision: 0,
    suffix: "个",
    note: "当前账号下已创建的信箱总数",
    tag: "总览",
    tagBg: "#eff6ff",
    tagText: "#2563eb",
    avatarColor: "#dbeafe",
    avatarTextColor: "#2563eb",
  },
  {
    key: "messages",
    symbol: "信",
    title: "已加载信件",
    value: totalLoadedMessages.value,
    precision: 0,
    suffix: "封",
    note: "当前已拉取到前端的数据量",
    tag: "实时",
    tagBg: "#ecfdf5",
    tagText: "#059669",
    avatarColor: "#d1fae5",
    avatarTextColor: "#059669",
  },
  {
    key: "shared",
    symbol: "享",
    title: "可分享信箱",
    value: sharedMailboxCount.value,
    precision: 0,
    suffix: "个",
    note: `分享覆盖率 ${shareCoverage.value}%`,
    tag: "公开",
    tagBg: "#fff7ed",
    tagText: "#c2410c",
    avatarColor: "#ffedd5",
    avatarTextColor: "#ea580c",
  },
  {
    key: "average",
    symbol: "均",
    title: "平均每箱信件",
    value: averageMessagesPerMailbox.value,
    precision: 1,
    suffix: "封",
    note: "按当前已加载数据计算的平均值",
    tag: "聚焦",
    tagBg: "#f5f3ff",
    tagText: "#7c3aed",
    avatarColor: "#ede9fe",
    avatarTextColor: "#7c3aed",
  },
]);

function normalizeDateKey(value: string) {
  const directMatch = value.match(/^\d{4}-\d{2}-\d{2}/)?.[0];
  if (directMatch) {
    return directMatch;
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value.slice(0, 10);
  }

  const year = parsed.getFullYear();
  const month = `${parsed.getMonth() + 1}`.padStart(2, "0");
  const day = `${parsed.getDate()}`.padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatTrendDateLabel(dateKey: string) {
  return /^\d{4}-\d{2}-\d{2}$/.test(dateKey) ? dateKey.slice(5).replace("-", "/") : dateKey;
}

function getNiceAxisMax(maxValue: number) {
  if (maxValue <= 5) {
    return 5;
  }

  const magnitude = 10 ** Math.floor(Math.log10(maxValue));
  const normalized = maxValue / magnitude;

  if (normalized <= 1) {
    return magnitude;
  }
  if (normalized <= 2) {
    return 2 * magnitude;
  }
  if (normalized <= 5) {
    return 5 * magnitude;
  }
  return 10 * magnitude;
}

function drawTrendAxes(
  context: CanvasRenderingContext2D,
  cssWidth: number,
  padding: ChartPadding,
  chartHeight: number,
  yAxisMax: number,
  yAxisSteps: number,
) {
  context.font = '12px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif';
  context.textBaseline = "middle";

  for (let step = 0; step <= yAxisSteps; step += 1) {
    const ratio = step / yAxisSteps;
    const y = padding.top + chartHeight * ratio;
    const value = Math.round(yAxisMax * (1 - ratio));

    context.beginPath();
    context.moveTo(padding.left, y);
    context.lineTo(cssWidth - padding.right, y);
    context.strokeStyle = "rgba(203, 213, 225, 0.72)";
    context.lineWidth = step === yAxisSteps ? 1.4 : 1;
    context.stroke();

    context.fillStyle = "#7b8494";
    context.textAlign = "right";
    context.fillText(String(value), padding.left - 10, y);
  }
}

function buildLineCoordinates(
  points: DailyMessagePoint[],
  padding: ChartPadding,
  chartWidth: number,
  chartHeight: number,
  yAxisMax: number,
) {
  return points.map((item, index) => {
    const x = points.length === 1
      ? padding.left + chartWidth / 2
      : padding.left + (chartWidth * index) / (points.length - 1);
    const y = padding.top + chartHeight - (item.count / yAxisMax) * chartHeight;

    return {
      x,
      y,
      count: item.count,
      label: item.label,
    };
  });
}

function buildBarLayout(
  points: DailyMessagePoint[],
  padding: ChartPadding,
  chartWidth: number,
  chartHeight: number,
  yAxisMax: number,
) {
  const slotWidth = points.length ? chartWidth / points.length : chartWidth;
  const barWidth = Math.max(16, Math.min(slotWidth * 0.62, 56));
  const coordinates = points.map((item, index) => {
    const x = padding.left + slotWidth * index + slotWidth / 2;
    const y = padding.top + chartHeight - (item.count / yAxisMax) * chartHeight;

    return {
      x,
      y,
      count: item.count,
      label: item.label,
    };
  });

  return { coordinates, barWidth };
}

function drawTrendXAxisLabels(
  context: CanvasRenderingContext2D,
  coordinates: TrendCoordinate[],
  axisY: number,
) {
  const xLabelStep = Math.max(1, Math.ceil(coordinates.length / 6));
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillStyle = "#7b8494";

  coordinates.forEach((point, index) => {
    if (index % xLabelStep !== 0 && index !== coordinates.length - 1) {
      return;
    }

    context.fillText(point.label, point.x, axisY);
  });
}

function drawTrendLatestValue(
  context: CanvasRenderingContext2D,
  cssWidth: number,
  latestPoint: TrendCoordinate,
  color: string,
) {
  const latestCountLabel = `${latestPoint.count} 封`;

  context.fillStyle = color;
  context.font = '600 12px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif';
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(
    latestCountLabel,
    Math.max(32, Math.min(cssWidth - 32, latestPoint.x)),
    Math.max(18, latestPoint.y - 16),
  );
}

function drawLineTrend(
  context: CanvasRenderingContext2D,
  coordinates: TrendCoordinate[],
  cssWidth: number,
  padding: ChartPadding,
  chartHeight: number,
) {
  const areaGradient = context.createLinearGradient(0, padding.top, 0, padding.top + chartHeight);
  areaGradient.addColorStop(0, "rgba(47, 110, 166, 0.28)");
  areaGradient.addColorStop(1, "rgba(47, 110, 166, 0.04)");

  context.beginPath();
  context.moveTo(coordinates[0].x, padding.top + chartHeight);
  coordinates.forEach((point) => {
    context.lineTo(point.x, point.y);
  });
  context.lineTo(coordinates[coordinates.length - 1].x, padding.top + chartHeight);
  context.closePath();
  context.fillStyle = areaGradient;
  context.fill();

  const lineGradient = context.createLinearGradient(padding.left, 0, cssWidth - padding.right, 0);
  lineGradient.addColorStop(0, "#2f6ea6");
  lineGradient.addColorStop(1, "#d15b2f");

  context.beginPath();
  coordinates.forEach((point, index) => {
    if (index === 0) {
      context.moveTo(point.x, point.y);
      return;
    }

    context.lineTo(point.x, point.y);
  });
  context.strokeStyle = lineGradient;
  context.lineWidth = 3;
  context.lineJoin = "round";
  context.lineCap = "round";
  context.stroke();

  coordinates.forEach((point, index) => {
    context.beginPath();
    context.arc(point.x, point.y, index === coordinates.length - 1 ? 5.5 : 4, 0, Math.PI * 2);
    context.fillStyle = index === coordinates.length - 1 ? "#d15b2f" : "#2f6ea6";
    context.fill();
    context.strokeStyle = "#ffffff";
    context.lineWidth = 2;
    context.stroke();
  });

  drawTrendLatestValue(context, cssWidth, coordinates[coordinates.length - 1], "#2f6ea6");
}

function drawBarTrend(
  context: CanvasRenderingContext2D,
  coordinates: TrendCoordinate[],
  barWidth: number,
  cssWidth: number,
  padding: ChartPadding,
  chartHeight: number,
) {
  const chartBottom = padding.top + chartHeight;
  const barGradient = context.createLinearGradient(0, padding.top, 0, chartBottom);
  barGradient.addColorStop(0, "rgba(47, 110, 166, 0.92)");
  barGradient.addColorStop(1, "rgba(47, 110, 166, 0.44)");

  coordinates.forEach((point, index) => {
    const top = point.y;
    const left = point.x - barWidth / 2;
    const right = point.x + barWidth / 2;
    const height = chartBottom - top;
    const radius = Math.min(10, barWidth / 3, height / 2);

    context.beginPath();
    context.moveTo(left, chartBottom);
    context.lineTo(left, top + radius);
    context.quadraticCurveTo(left, top, left + radius, top);
    context.lineTo(right - radius, top);
    context.quadraticCurveTo(right, top, right, top + radius);
    context.lineTo(right, chartBottom);
    context.closePath();
    context.fillStyle = index === coordinates.length - 1 ? "#d15b2f" : barGradient;
    context.fill();
  });

  drawTrendLatestValue(context, cssWidth, coordinates[coordinates.length - 1], "#d15b2f");
}

function scheduleTrendDraw() {
  if (typeof window === "undefined") {
    return;
  }

  if (trendFrameHandle !== null) {
    window.cancelAnimationFrame(trendFrameHandle);
  }

  trendFrameHandle = window.requestAnimationFrame(() => {
    trendFrameHandle = null;
    drawTrendChart();
  });
}

function drawTrendChart() {
  const canvas = trendCanvasRef.value;
  const points = dailyMessageTrend.value;
  if (!canvas || !points.length) {
    return;
  }

  const rect = canvas.getBoundingClientRect();
  const cssWidth = Math.floor(rect.width);
  const cssHeight = Math.floor(rect.height);
  if (cssWidth <= 0 || cssHeight <= 0) {
    return;
  }

  const context = canvas.getContext("2d");
  if (!context) {
    return;
  }

  const devicePixelRatio = window.devicePixelRatio || 1;
  canvas.width = cssWidth * devicePixelRatio;
  canvas.height = cssHeight * devicePixelRatio;
  context.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
  context.clearRect(0, 0, cssWidth, cssHeight);

  const padding: ChartPadding = {
    top: 24,
    right: 18,
    bottom: 42,
    left: 48,
  };
  const chartWidth = cssWidth - padding.left - padding.right;
  const chartHeight = cssHeight - padding.top - padding.bottom;
  const yAxisMax = getNiceAxisMax(Math.max(...points.map((item) => item.count), 1));
  const yAxisSteps = 4;

  drawTrendAxes(context, cssWidth, padding, chartHeight, yAxisMax, yAxisSteps);

  if (trendMode.value === "bar") {
    const { coordinates, barWidth } = buildBarLayout(points, padding, chartWidth, chartHeight, yAxisMax);
    drawBarTrend(context, coordinates, barWidth, cssWidth, padding, chartHeight);
    drawTrendXAxisLabels(context, coordinates, padding.top + chartHeight + 24);
    return;
  }

  const coordinates = buildLineCoordinates(points, padding, chartWidth, chartHeight, yAxisMax);
  drawLineTrend(context, coordinates, cssWidth, padding, chartHeight);
  drawTrendXAxisLabels(context, coordinates, padding.top + chartHeight + 24);
}

function scrollToSection(target: HTMLElement | null) {
  target?.scrollIntoView({ behavior: "smooth", block: "start" });
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
    activeRail.value = "overview";
    scrollToSection(overviewSectionRef.value);
    return;
  }

  message.info("当前暂未单独实现文档页。");
  activeTopMenu.value = "dashboard";
}

function handleRailAction(key: RailKey) {
  if (key === "mailboxes") {
    void router.push({ name: "mailboxes" });
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

  activeRail.value = "overview";
  scrollToSection(overviewSectionRef.value);
}

async function hydrateMailboxMessages() {
  const currentSelectedId = mailStore.selectedMailboxId;
  for (const mailbox of mailStore.mailboxes) {
    await mailStore.fetchMessages(mailbox.id);
  }
  mailStore.selectedMailboxId = currentSelectedId ?? mailStore.mailboxes[0]?.id ?? null;
}

async function refreshDashboard() {
  dashboardRefreshing.value = true;
  try {
    await authStore.fetchUser();
    await mailStore.fetchMailboxes();
    await hydrateMailboxMessages();
  } catch (error) {
    message.error(getErrorMessage(error));
  } finally {
    dashboardRefreshing.value = false;
  }
}

function handleOpenSelectedMailbox() {
  if (!mailStore.selectedMailbox) {
    message.warning("请先选择一个信箱。");
    return;
  }

  void router.push({
    name: "mailbox-messages",
    params: { boxId: String(mailStore.selectedMailbox.id) },
    query: {
      title: mailStore.selectedMailbox.title || "",
      boxName: mailStore.selectedMailbox.box_name,
    },
  });
}

async function copyShareToken(row: { share_token: string }) {
  try {
    await navigator.clipboard.writeText(row.share_token);
    message.success("分享 Token 已复制。");
  } catch {
    message.warning("复制失败，请手动复制 Token。");
  }
}

async function copyPublicLink() {
  if (!publicDeliveryLink.value) {
    message.warning("当前选中的信箱没有公开投递链接。");
    return;
  }

  try {
    await navigator.clipboard.writeText(publicDeliveryLink.value);
    message.success("公开链接已复制。");
  } catch {
    message.warning("复制失败，请手动复制链接。");
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

watch([dailyMessageTrend, trendMode], () => {
  void nextTick().then(() => {
    scheduleTrendDraw();
  });
});

watch(sidebarCollapsed, () => {
  void nextTick().then(() => {
    scheduleTrendDraw();
  });
});

onMounted(async () => {
  await refreshDashboard();
  await nextTick();
  scheduleTrendDraw();
  window.addEventListener("resize", scheduleTrendDraw);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", scheduleTrendDraw);
  if (trendFrameHandle !== null) {
    window.cancelAnimationFrame(trendFrameHandle);
  }
});
</script>
