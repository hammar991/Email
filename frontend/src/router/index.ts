import { createRouter, createWebHistory } from "vue-router";
import DashboardPage from "@/views/DashboardPage.vue";
import LoginPage from "@/views/LoginPage.vue";
import MailboxMessagesPage from "@/views/MailboxMessagesPage.vue";
import PublicDeliveryPage from "@/views/PublicDeliveryPage.vue";

const TOKEN_STORAGE_KEY = "email-access-token";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/login",
    },
    {
      path: "/login",
      name: "login",
      component: LoginPage,
      meta: {
        guestOnly: true,
      },
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: DashboardPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/mailboxes/:boxId/messages",
      name: "mailbox-messages",
      component: MailboxMessagesPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/public/:shareToken",
      name: "public-delivery",
      component: PublicDeliveryPage,
    },
  ],
});

router.beforeEach((to) => {
  const token = window.localStorage.getItem(TOKEN_STORAGE_KEY);

  if (to.meta.requiresAuth && !token) {
    return {
      name: "login",
      query: {
        redirect: to.fullPath,
      },
    };
  }

  if (to.meta.guestOnly && token) {
    return {
      name: "dashboard",
    };
  }

  return true;
});

export default router;
