<template>
  <div class="auth-shell">
    <div class="auth-layout">
      <section class="auth-copy">
        <p class="eyebrow">Mailbox Access</p>
        <h1>登录或注册后进入信箱控制台</h1>
        <p class="hero-copy">
          使用 Vue 3、Vite 与 Naive UI 构建的认证入口。右侧卡片保留参考图那种简洁排版，
          但表单结构完全使用 Naive UI Form。
        </p>
      </section>

      <n-card class="glass-card auth-card" :bordered="false" content-style="padding: 0;">
        <div class="auth-card-inner">
          <div class="auth-card-header">
            <h2>欢迎登陆信箱系统!</h2>
            <p>字段与后端 DTO 保持一致，登录成功后自动进入 Dashboard。</p>
          </div>

          <n-tabs v-model:value="authMode" class="auth-card-tabs" type="segment" animated>
            <n-tab-pane name="login" tab="登录">
              <n-form
                ref="loginFormRef"
                class="auth-form"
                :model="loginForm"
                :rules="loginRules"
                label-placement="top"
                require-mark-placement="right-hanging"
                @submit.prevent="handleLogin"
              >
                <n-form-item path="username" label="用户名" class="auth-form-item">
                  <n-input
                    v-model:value="loginForm.username"
                    class="auth-field-input"
                    placeholder="Please Input"
                    @keydown.enter.prevent="handleLogin"
                  />
                </n-form-item>

                <n-form-item path="password" label="密码" class="auth-form-item">
                  <n-input
                    v-model:value="loginForm.password"
                    class="auth-field-input"
                    type="password"
                    show-password-on="click"
                    placeholder="Please Input"
                    @keydown.enter.prevent="handleLogin"
                  />
                </n-form-item>

                <div class="auth-actions">
                  <n-button
                    class="auth-action-button"
                    type="primary"
                    :loading="authStore.loading"
                    attr-type="submit"
                  >
                    登录
                  </n-button>
                  <n-button class="auth-action-button" secondary @click="authMode = 'register'">
                    注册
                  </n-button>
                </div>
              </n-form>
            </n-tab-pane>

            <n-tab-pane name="register" tab="注册">
              <n-form
                ref="registerFormRef"
                class="auth-form"
                :model="registerForm"
                :rules="registerRules"
                label-placement="top"
                require-mark-placement="right-hanging"
                @submit.prevent="handleRegister"
              >
                <n-form-item path="name" label="用户名" class="auth-form-item">
                  <n-input
                    v-model:value="registerForm.name"
                    class="auth-field-input"
                    placeholder="Please Input"
                    @keydown.enter.prevent="handleRegister"
                  />
                </n-form-item>

                <n-form-item path="email" label="邮箱" class="auth-form-item">
                  <n-input
                    v-model:value="registerForm.email"
                    class="auth-field-input"
                    placeholder="Please Input"
                    @keydown.enter.prevent="handleRegister"
                  />
                </n-form-item>

                <n-form-item path="password" label="密码" class="auth-form-item">
                  <n-input
                    v-model:value="registerForm.password"
                    class="auth-field-input"
                    type="password"
                    show-password-on="click"
                    placeholder="Please Input"
                    @keydown.enter.prevent="handleRegister"
                  />
                </n-form-item>

                <div class="auth-actions">
                  <n-button
                    class="auth-action-button"
                    type="primary"
                    :loading="authStore.loading"
                    attr-type="submit"
                  >
                    注册
                  </n-button>
                  <n-button class="auth-action-button" secondary @click="authMode = 'login'">
                    返回登录
                  </n-button>
                </div>
              </n-form>
            </n-tab-pane>
          </n-tabs>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useMessage, type FormInst, type FormRules } from "naive-ui";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
const message = useMessage();
const authStore = useAuthStore();

const loginFormRef = ref<FormInst | null>(null);
const registerFormRef = ref<FormInst | null>(null);
const authMode = ref<"login" | "register">("login");

const loginForm = reactive({
  username: "",
  password: "",
});

const registerForm = reactive({
  name: "",
  email: "",
  password: "",
});

const redirectPath = computed(() => {
  const redirect = route.query.redirect;
  return typeof redirect === "string" && redirect.length > 0 ? redirect : "/dashboard";
});

const loginRules: FormRules = {
  username: [
    {
      required: true,
      message: "username 不能为空",
      trigger: ["input", "blur"],
    },
  ],
  password: [
    {
      required: true,
      message: "password 不能为空",
      trigger: ["input", "blur"],
    },
  ],
};

const registerRules: FormRules = {
  name: [
    {
      required: true,
      message: "name 不能为空",
      trigger: ["input", "blur"],
    },
  ],
  email: [
    {
      required: true,
      message: "email 不能为空",
      trigger: ["input", "blur"],
    },
    {
      type: "email",
      message: "email 格式不正确",
      trigger: ["input", "blur"],
    },
  ],
  password: [
    {
      required: true,
      message: "password 不能为空",
      trigger: ["input", "blur"],
    },
  ],
};

async function handleLogin() {
  try {
    await loginFormRef.value?.validate();
    await authStore.login(loginForm.username, loginForm.password);
    message.success("登录成功");
    await router.push(redirectPath.value);
  } catch (error) {
    if (error instanceof Error) {
      message.error(error.message);
    }
  }
}

async function handleRegister() {
  try {
    await registerFormRef.value?.validate();
    const response = await authStore.register({
      name: registerForm.name,
      email: registerForm.email,
      password: registerForm.password,
    });
    message.success(response.detail || "注册成功，请登录");
    loginForm.username = registerForm.name;
    registerForm.password = "";
    authMode.value = "login";
  } catch (error) {
    if (error instanceof Error) {
      message.error(error.message);
    }
  }
}
</script>
