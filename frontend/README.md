# Frontend

这个目录是邮箱项目的独立前端，技术栈为 `bun + Vue 3 + Naive UI + Pinia + Vite`。

## 启动

1. 安装依赖

```bash
bun install
```

2. 可选：复制环境变量

```bash
cp .env.example .env
```

本地联调默认使用：

```env
VITE_API_BASE_URL=http://127.0.0.1:8003/api/v1
```

仓库已经提供 `frontend/.env`，默认会直接请求本地后端。

3. 启动开发环境

```bash
bun run dev
```

默认前端地址是 `http://127.0.0.1:3000`。如果你使用 `http://localhost:3000` 打开页面，本地后端的 CORS 也已兼容这两个来源：

- `http://127.0.0.1:3000`
- `http://localhost:3000`

## API 适配

- 默认优先请求 `VITE_API_ORIGIN + /api/v1`
- 如果返回 `404`，会自动回退到 `VITE_API_ORIGIN`
- 也可以直接用 `VITE_API_BASE_URL` 指定完整后端地址
- 当前本地联调固定为 `http://127.0.0.1:8003/api/v1`，与后端 `Settings.api_v1_str` 保持一致

## 页面能力

- 登录
- 注册
- 重置密码
- 用户邮箱信息更新
- 信箱创建、查看、删除
- 信件创建、查看、删除
- 公开投递页 `/public/:shareToken`
