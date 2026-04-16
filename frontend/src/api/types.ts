export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  status_code: number;
  name: string;
  detail: string;
}

export interface ResetPasswordPayload {
  name: string;
  email: string;
  password: string;
  ensure_password: string;
}

export interface UserInfo {
  id: number;
  name: string;
  email: string;
}

export interface UpdateUserPayload {
  email: string;
}

export interface MailboxPayload {
  name: string;
  title: string;
}

export interface MailboxInfo {
  id: number;
  box_name: string;
  title: string;
  share_token: string;
}

export interface MessagePayload {
  headline: string;
  context: string;
  box_id: number;
}

export interface MessageInfo {
  id: number;
  headline: string;
  context: string | null;
  box_id: number;
  created_at: string;
}

export interface PublicMessagePayload {
  headline: string;
  context: string;
}
