# WeFlow 微信聊天导出套件

这套资料用于帮助不熟悉技术的同事，在 Codex 引导下使用 WeFlow 导出微信聊天文字、图片、文件、语音和视频，并在分析前检查资料是否完整。

## 同事使用入口

请优先把下面两份材料发给同事：

1. [`docs/WeFlow安装与导出截图教程.html`](docs/WeFlow安装与导出截图教程.html)
2. [`docs/给Codex的完整启动提示词.md`](docs/给Codex的完整启动提示词.md)

HTML 教程是给人看的“照着点”说明；启动提示词是复制给 Codex 的。Codex 会根据提示词访问本公共仓库并下载 Release。

## 下载地址

- 发布页：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/tag/v1.0.0>
- 完整工具包：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/download/v1.0.0/WeFlow.zip>
- 单独安装器：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/download/v1.0.0/WeFlow-4.5.1-x64-Setup.exe>

## 最短使用路径

1. 同事先打开 `WeFlow安装与导出截图教程.html`。
2. 同事把 `给Codex的完整启动提示词.md` 全文复制给 Codex。
3. Codex 先做权限预检，再从 GitHub Release 下载 `WeFlow.zip`。
4. Codex 安装 `weflow-export-wechat` Skill，并提醒用户重启 Codex。
5. Codex 引导用户安装 WeFlow、配置数据库目录、自动获取密钥、创建导出任务和完整性检查。

## 推荐导出格式

- 对话文本：**ChatLab JSONL**。
- 媒体：按分析需要选择图片、文件、语音、视频和表情包。
- 交给 Codex：提供完整导出目录，不要只提供 JSONL。

## 文件说明

- `docs/WeFlow安装与导出截图教程.html`：发给同事看的独立 HTML 教程，不放进 `WeFlow.zip`。
- `docs/给Codex的完整启动提示词.md`：发给同事复制给 Codex 的启动提示词，不要求同事研究 GitHub。
- `skill/weflow-export-wechat`：Codex Skill。
- `安装Skill.ps1`：将本地 Skill 安装到当前用户的 Codex Skills 目录。
- `SECURITY.md`：隐私和安装器安全说明。

## 第三方软件说明

WeFlow 是第三方工具，不属于本仓库。Release 中如提供安装器，应同时提供 SHA-256 校验值；不要从不明软件下载站获取安装器。

## 维护者发布

准备好 `dist` 后，安装并登录 GitHub CLI，再运行：

```powershell
.\scripts\publish-github.ps1
```

`WeFlow.zip` 只作为 Codex 下载的工具包，不包含同事版 HTML 教程；HTML 教程和启动提示词作为独立 Release 附件或仓库文档分发。
