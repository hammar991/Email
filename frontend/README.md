# Frontend

这个目录是信箱项目的独立前端，技术栈为 `bun + vue3 + naive ui + pinia + vite`。

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

当前仓库已经提供了本地测试用的 `frontend/.env`，前端会直接请求你的本地后端。

3. 启动开发环境

```bash
bun run dev
```

默认前端地址是 `http://127.0.0.1:3000`，这与后端当前 CORS 配置兼容。

## API 适配

- 默认优先请求 `VITE_API_ORIGIN + /api/v1`
- 如果返回 `404`，会自动回退到 `VITE_API_ORIGIN`
- 也可以直接用 `VITE_API_BASE_URL` 指定完整后端基址
- 当前本地联调已固定为 `http://127.0.0.1:8003/api/v1`，与后端 `Settings.api_v1_str` 保持一致

## 页面能力

- 登录
- 注册
- 重置密码
- 用户邮箱信息更新
- 信箱创建、查看、删除
- 信件创建、查看、删除
- 公开投递页 `/public/:shareToken`
