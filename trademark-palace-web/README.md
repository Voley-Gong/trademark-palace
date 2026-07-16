# 商标馆记忆宫殿 · 网页 MVP

手机可访问的碎片化训练页：四列门牌走廊、30 秒口述 + **法条原文（含关联）**、数字桩、五问办案。

## 本地启动

```bash
cd trademark-palace-web
npm install
npm run dev
```

- 本机：http://localhost:5177/
- 手机：同一局域网下使用终端打印的 Network 地址

更新法条数据：

```bash
npm run sync-data
```

（会重写 `docs/data/trademark-palace.json` 并同步到 `public/data/`）

## 五问办案

馆门或底栏进入后先选题（现共 7 案）：

| 类型 | 案件 |
|------|------|
| 侵权救济向 | 电商销售近似标 / 撕标换标 / 字号攀附转反法 |
| 程序向 | 初审异议与抢注无效 / 驳回复审与绝对无效 / 撤三攻防 / 驰名跨类攀附 |

## 地下室 · 发霉 · 搜索

- **B0 司法解释补丁**：民事近似、驰名、确权恶意、惩罚性、证据、网络、禁令、三年使用
- **发霉复习**：按发霉次数过门，可除霉或进走廊揭晓
- **全馆搜索**：条号 / 门牌 / 关键词 / 案例名
- 房间详情含 **经典案例** 卡片（案名 · 钩子 · 一句话收获）


## 通勤听过（PWA）

- 底栏 **听过**：选楼层 → 系统中文语音朗读房间口述 + 人话解释
- 可调节语速；支持安装到主屏幕（需 HTTPS / GitHub Pages）
- `manifest.webmanifest` + `sw.js` 已配置；首次打开后可「添加到主屏幕」

本地验证 PWA 需用 `npm run build && npm run preview`（`dev` 下 SW 路径一般可用，但安装体验以 preview/生产为准）。


## GitHub Pages 部署

本仓库已含工作流：`.github/workflows/deploy-trademark-palace.yml`。

### 一次性设置

1. 仓库 **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**
2. 推送到 `main`/`master`（或手动 Run workflow）
3. 站点地址一般为：`https://<user>.github.io/<repo>/`

若仓库名不是站点子路径，可在仓库 **Settings → Secrets and variables → Actions → Variables** 增加：

- `BASE_PATH` = `/你的子路径/`（首尾带 `/`）

本地模拟 Pages 构建：

```bash
# Windows PowerShell
$env:BASE_PATH="/你的仓库名/"
npm run build
npm run preview
```

默认 `vite.config.js` 使用相对路径 `base: './'`，无 env 时也可直接打开 `dist`；CI 会注入 `BASE_PATH` 以适配 project site 绝对根路径资源。

### 设计取舍（便于 Pages）

- 无前端路由深链，刷新不 404
- 静态 JSON 放在 `public/data/`，构建时原样拷贝
- 资源通过 `import.meta.env.BASE_URL` 拼接，避免硬编码 `/`
