import type {
  MailboxInfo,
  MailboxPayload,
  MessageInfo,
  MessagePayload,
  PublicMessagePayload,
  RegisterPayload,
  RegisterResponse,
  ResetPasswordPayload,
  TokenResponse,
  UpdateUserPayload,
  UserInfo,
} from "@/api/types";

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

interface RequestOptions {
  method?: HttpMethod;
  token?: string | null;
  query?: Record<string, string | number | undefined>;
  body?: BodyInit | null;
  headers?: Record<string, string>;
}

const API_BASE_STORAGE_KEY = "email-api-base-url";

function trimSlash(value: string) {
  return value.replace(/\/+$/, "");
}

function buildUrl(baseUrl: string, path: string, query?: RequestOptions["query"]) {
  const normalizedBase = trimSlash(baseUrl);
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const url = new URL(`${normalizedBase}${normalizedPath}`);

  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.set(key, String(value));
      }
    });
  }

  return url;
}

function getCandidates() {
  const explicitBase = import.meta.env.VITE_API_BASE_URL?.trim();
  if (explicitBase) {
    return [trimSlash(explicitBase)];
  }

  const origin = trimSlash(import.meta.env.VITE_API_ORIGIN?.trim() || window.location.origin);
  const remembered = window.localStorage.getItem(API_BASE_STORAGE_KEY);
  const candidates = [remembered, `${origin}/api/v1`, origin].filter(
    (value): value is string => Boolean(value),
  );

  return [...new Set(candidates.map(trimSlash))];
}

async function parseError(response: Response) {
  try {
    const payload = await response.json();
    if (typeof payload?.detail === "string") {
      return payload.detail;
    }
    return JSON.stringify(payload);
  } catch {
    return `请求失败: ${response.status}`;
  }
}

async function request<T>(path: string, options: RequestOptions = {}) {
  const candidates = getCandidates();
  let lastError: Error | null = null;

  for (const [index, candidate] of candidates.entries()) {
    try {
      const isFormBody = options.body instanceof FormData || options.body instanceof URLSearchParams;
      const hasExplicitContentType = Object.keys(options.headers ?? {}).some(
        (header) => header.toLowerCase() === "content-type",
      );

      const response = await fetch(buildUrl(candidate, path, options.query), {
        method: options.method ?? "GET",
        headers: {
          ...(options.body && !isFormBody && !hasExplicitContentType
            ? { "Content-Type": "application/json" }
            : {}),
          ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}),
          ...options.headers,
        },
        body: options.body ?? null,
      });

      if (response.status === 404 && index < candidates.length - 1) {
        continue;
      }

      if (!response.ok) {
        throw new Error(await parseError(response));
      }

      window.localStorage.setItem(API_BASE_STORAGE_KEY, candidate);
      if (response.status === 204) {
        return undefined as T;
      }
      return (await response.json()) as T;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error("请求失败");
    }
  }

  throw lastError ?? new Error("未找到可用的后端地址");
}

export const apiClient = {
  login(username: string, password: string) {
    const formData = new URLSearchParams();
    formData.set("username", username);
    formData.set("password", password);
    return request<TokenResponse>("/login/access-token", {
      method: "POST",
      body: formData,
    });
  },
  
  register(payload: RegisterPayload) {
    return request<RegisterResponse>("/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  resetPassword(payload: ResetPasswordPayload) {
    return request<{ status: number; detail: string }>("/login/reset", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  getUserInfo(token: string) {
    return request<UserInfo>("/user/userinfo", {
      token,
    });
  },

  updateUser(token: string, payload: UpdateUserPayload) {
    return request<UserInfo>("/user/userinfo", {
      method: "PUT",
      token,
      body: JSON.stringify(payload),
    });
  },

  getMailboxes(token: string) {
    return request<MailboxInfo[]>("/box/mailbox", {
      token,
    });
  },

  getMailboxByName(token: string, boxName: string) {
    return request<MailboxInfo | null>(`/box/mailbox/${encodeURIComponent(boxName)}`, {
      token,
    });
  },

  createMailbox(token: string, payload: MailboxPayload) {
    return request<MailboxInfo>("/box/mailbox", {
      method: "POST",
      token,
      body: JSON.stringify(payload),
    });
  },

  deleteMailbox(token: string, boxId: number) {
    return request<MailboxInfo>("/box/mailbox", {
      method: "DELETE",
      token,
      query: {
        box_id: boxId,
      },
    });
  },

  getMailboxByShareToken(shareToken: string) {
    return request<MailboxInfo>(`/box/share_mailbox/${shareToken}`);
  },

  getMessages(token: string, boxId: number) {
    return request<MessageInfo[]>("/message/mail", {
      token,
      query: {
        box_id: boxId,
      },
    });
  },
  
  createMessage(token: string, payload: MessagePayload) {
    return request<MessageInfo>("/message/mail", {
      method: "POST",
      token,
      body: JSON.stringify(payload),
    });
  },

  deleteMessage(token: string, messageId: number, boxId: number) {
    return request<MessageInfo>("/message/mail", {
      method: "DELETE",
      token,
      query: {
        message_id: messageId,
        box_id: boxId,
      },
    });
  },
  
  submitPublicMessage(shareToken: string, payload: PublicMessagePayload) {
    return request<MessageInfo>(`/message/public/mailbox/${shareToken}/message`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
