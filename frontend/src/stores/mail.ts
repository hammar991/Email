import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { apiClient } from "@/api/client";
import type { MailboxInfo, MailboxPayload, MessageInfo, MessagePayload, PublicMessagePayload } from "@/api/types";
import { useAuthStore } from "@/stores/auth";

export const useMailStore = defineStore("mail", () => {
  const mailboxes = ref<MailboxInfo[]>([]);
  const messages = ref<Record<number, MessageInfo[]>>({});
  const selectedMailboxId = ref<number | null>(null);
  const loadingMailboxes = ref(false);
  const loadingMessages = ref(false);
  const publicMailbox = ref<MailboxInfo | null>(null);

  const selectedMailbox = computed(
    () => mailboxes.value.find((item) => item.id === selectedMailboxId.value) ?? null,
  );

  function requireToken() {
    const authStore = useAuthStore();
    if (!authStore.token) {
      throw new Error("当前未登录");
    }
    return authStore.token;
  }

  async function fetchMailboxes() {
    loadingMailboxes.value = true;
    try {
      const token = requireToken();
      mailboxes.value = await apiClient.getMailboxes(token);

      if (mailboxes.value.length > 0) {
        const stillSelected = mailboxes.value.some((item) => item.id === selectedMailboxId.value);
        selectedMailboxId.value = stillSelected
          ? selectedMailboxId.value
          : (mailboxes.value[0]?.id ?? null);
      } else {
        selectedMailboxId.value = null;
      }

      if (selectedMailboxId.value) {
        await fetchMessages(selectedMailboxId.value);
      }

      return mailboxes.value;
    } finally {
      loadingMailboxes.value = false;
    }
  }

  async function createMailbox(payload: MailboxPayload) {
    const token = requireToken();
    const mailbox = await apiClient.createMailbox(token, payload);
    mailboxes.value = [mailbox, ...mailboxes.value];
    selectedMailboxId.value = mailbox.id;
    messages.value[mailbox.id] = [];
    return mailbox;
  }

  async function deleteMailbox(boxId: number) {
    const token = requireToken();
    await apiClient.deleteMailbox(token, boxId);
    mailboxes.value = mailboxes.value.filter((item) => item.id !== boxId);
    delete messages.value[boxId];

    if (selectedMailboxId.value === boxId) {
      selectedMailboxId.value = mailboxes.value[0]?.id ?? null;
    }

    if (selectedMailboxId.value) {
      await fetchMessages(selectedMailboxId.value);
    }
  }

  async function fetchMessages(boxId: number) {
    const token = requireToken();
    loadingMessages.value = true;
    selectedMailboxId.value = boxId;
    try {
      const response = await apiClient.getMessages(token, boxId);
      messages.value[boxId] = response;
      return response;
    } finally {
      loadingMessages.value = false;
    }
  }

  async function createMessage(payload: MessagePayload) {
    const token = requireToken();
    const message = await apiClient.createMessage(token, payload);
    const currentMessages = messages.value[payload.box_id] ?? [];
    messages.value[payload.box_id] = [message, ...currentMessages];
    return message;
  }

  async function deleteMessage(messageId: number, boxId: number) {
    const token = requireToken();
    await apiClient.deleteMessage(token, messageId, boxId);
    messages.value[boxId] = (messages.value[boxId] ?? []).filter((item) => item.id !== messageId);
  }

  async function fetchPublicMailbox(shareToken: string) {
    publicMailbox.value = await apiClient.getMailboxByShareToken(shareToken);
    return publicMailbox.value;
  }

  async function submitPublicMessage(shareToken: string, payload: PublicMessagePayload) {
    return apiClient.submitPublicMessage(shareToken, payload);
  }

  function reset() {
    mailboxes.value = [];
    messages.value = {};
    selectedMailboxId.value = null;
    publicMailbox.value = null;
  }

  return {
    mailboxes,
    messages,
    selectedMailboxId,
    selectedMailbox,
    loadingMailboxes,
    loadingMessages,
    publicMailbox,
    fetchMailboxes,
    createMailbox,
    deleteMailbox,
    fetchMessages,
    createMessage,
    deleteMessage,
    fetchPublicMailbox,
    submitPublicMessage,
    reset,
  };
});
