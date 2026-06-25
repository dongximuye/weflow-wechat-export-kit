# WeFlow 微信聊天导出套件

这套资料用于帮助不熟悉技术的同事，在 Codex 引导下导出和验收微信聊天资料。

- Windows：使用 WeFlow，支持 ChatLab JSONL 与媒体目录验收。
- Mac：使用 ExportWeChat，支持导出目录验收、增量状态和脱敏处理。

## 同事使用入口

请优先把下面两份材料发给同事：

1. [`docs/WeFlow安装与导出截图教程.html`](docs/WeFlow安装与导出截图教程.html)
2. [`docs/给Codex的完整启动提示词.md`](docs/给Codex的完整启动提示词.md)

HTML 教程是给 Windows/WeFlow 用户看的“照着点”说明，已内嵌截图，单独下载也能看到配图；启动提示词是复制给 Codex 的短入口。细节由 Codex 阅读本仓库文档，不放进提示词里。

## 下载地址

- 发布页：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/tag/v1.0.0>
- 完整工具包：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/download/v1.0.0/WeFlow.zip>

## Codex 应阅读的文件

Codex 收到启动提示词后，应先阅读：

1. `README.md`
2. `SECURITY.md`
3. Windows/WeFlow：`skill/weflow-export-wechat/SKILL.md`、`skill/weflow-export-wechat/references/WeFlow操作教程.md`、`docs/WeFlow安装与导出截图教程.html`
4. Mac/ExportWeChat：`docs/ExportWeChat-Mac导出与处理.md`
5. 安装脚本：`安装Skill.ps1`

## Windows / WeFlow 最短使用路径

1. 同事先打开 `WeFlow安装与导出截图教程.html`。
2. 同事把 `给Codex的完整启动提示词.md` 全文复制给 Codex。
3. Codex 先做权限预检，再从 GitHub Release 下载 `WeFlow.zip`。
4. Codex 安装 `weflow-export-wechat` Skill，并提醒用户重启 Codex。
5. Codex 引导用户安装 WeFlow、配置数据库目录、自动获取密钥、创建导出任务和完整性检查。

## Mac / ExportWeChat 最短使用路径

1. 同事把 `给Codex的完整启动提示词.md` 全文复制给 Codex。
2. Codex 阅读 `docs/ExportWeChat-Mac导出与处理.md`。
3. Codex 指导用户从 ExportWeChat 官网下载 macOS 客户端。
4. 若 macOS 提示“文件已损坏”，Codex 指导用户复制官网提供的终端代码并执行。
5. 导出后，用户提供完整导出目录，Codex 做完整性检查、增量状态和脱敏版处理。

## 推荐导出格式

- Windows / WeFlow：**ChatLab JSONL**。
- Mac / ExportWeChat：优先 JSON；免费版若只能 TXT，则按半结构化文本处理。
- 媒体：按分析需要选择图片、文件、语音、视频和表情包。
- 交给 Codex：提供完整导出目录，不要只提供单个文本文件。

## 增量导出与批量导出建议

已完成首次配置后，可以把 WeFlow 用作每日或定期增量导出入口。实测一个当天增量群聊从启动 WeFlow、搜索目标群、创建导出任务到任务中心完成，约 8 分钟；其中真正导出任务通常为 1–2 分钟级，剩余时间主要用于界面自动化、等待和完整性检查。

批量导出时不建议统一选择“全部时间”。推荐为每个会话保留 `export_integrity_report.md` 或状态文件，记录上次成功导出的末条时间；下次优先选择“今天”或“从上次导出日期到今天”。如果 WeFlow 只能按日期选择，允许多导一天，再由 Codex 按 `platformMessageId`、时间和内容结构去重合并。

粗略耗时预估：

- 已配置好、只导出当天增量：约 2–5 分钟/群。
- 媒体较多的群：约 5–15 分钟/群。
- 5 个群：约 15–35 分钟。
- 10 个群：约 30–70 分钟。

## 文件说明

- `docs/WeFlow安装与导出截图教程.html`：发给同事看的独立 HTML 教程，不放进 `WeFlow.zip`。
- `docs/给Codex的完整启动提示词.md`：发给同事复制给 Codex 的短入口，不要求同事研究 GitHub。
- `docs/ExportWeChat-Mac导出与处理.md`：Mac / ExportWeChat 详细流程，给 Codex 阅读。
- `skill/weflow-export-wechat`：Codex Skill。
- `安装Skill.ps1`：将本地 Skill 安装到当前用户的 Codex Skills 目录。
- `SECURITY.md`：隐私和安装器安全说明。

## 第三方软件说明

WeFlow 和 ExportWeChat 都是第三方工具，不属于本仓库。WeFlow 安装器随 `WeFlow.zip` 内部分发；ExportWeChat 请从其官网下载。不要从不明软件下载站获取安装器。

## 维护者发布

准备好 `dist` 后，安装并登录 GitHub CLI，再运行：

```powershell
.\scripts\publish-github.ps1
```

`WeFlow.zip` 只作为 Codex 下载的工具包，不包含同事版 HTML 教程；HTML 教程和启动提示词作为独立 Release 附件或仓库文档分发。
