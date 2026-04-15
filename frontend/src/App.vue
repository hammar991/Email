<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <router-view />
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { dateZhCN, zhCN, type GlobalThemeOverrides } from "naive-ui";

const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: "#d15b2f",
    primaryColorHover: "#e27145",
    primaryColorPressed: "#b84b22",
    infoColor: "#2f6ea6",
    successColor: "#3b7a57",
    warningColor: "#d79125",
    errorColor: "#c74848",
    borderRadius: "18px",
    fontFamily: '"Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif',
  },
  Card: {
    borderRadius: "24px",
  },
  Input: {
    borderRadius: "16px",
  },
  Button: {
    borderRadiusMedium: "14px",
  },
};
</script>
