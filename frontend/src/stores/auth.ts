import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { apiClient } from "@/api/client";
import type { RegisterPayload, ResetPasswordPayload, UpdateUserPayload, UserInfo } from "@/api/types";

const TOKEN_STORAGE_KEY = "email-access-token";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(window.localStorage.getItem(TOKEN_STORAGE_KEY));
  const user = ref<UserInfo | null>(null);
  const loading = ref(false);

  const isAuthenticated = computed(() => Boolean(token.value));

  function persistToken(value: string | null) {
    token.value = value;
    if (value) {
      window.localStorage.setItem(TOKEN_STORAGE_KEY, value);
    } else {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
  }

  async function login(username: string, password: string) {
    loading.value = true;
    try {
      const response = await apiClient.login(username, password);
      persistToken(response.access_token);
      await fetchUser();
      return response;
    } finally {
      loading.value = false;
    }
  }

  async function register(payload: RegisterPayload) {
    console.log("注册请求载荷:", payload);
    loading.value = true;
    try {
      return await apiClient.register(payload);
    } finally {
      loading.value = false;
    }
  }

  async function resetPassword(payload: ResetPasswordPayload) {
    loading.value = true;
    try {
      return await apiClient.resetPassword(payload);
    } finally {
      loading.value = false;
    }
  }

  async function fetchUser() {
    if (!token.value) {
      user.value = null;
      return null;
    }

    loading.value = true;
    try {
      user.value = await apiClient.getUserInfo(token.value);
      return user.value;
    } catch (error) {
      persistToken(null);
      user.value = null;
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function updateUser(payload: UpdateUserPayload) {
    if (!token.value) {
      throw new Error("当前未登录");
    }

    loading.value = true;
    try {
      user.value = await apiClient.updateUser(token.value, payload);
      return user.value;
    } finally {
      loading.value = false;
    }
  }

  function logout() {
    persistToken(null);
    user.value = null;
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    login,
    register,
    resetPassword,
    fetchUser,
    updateUser,
    logout,
  };
});
