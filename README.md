# WeFlow 微信聊天导出套件

这套资料帮助不熟悉技术的同事，在 Codex 引导下使用 WeFlow 导出微信聊天文字、图片、文件、语音和视频，并在分析前自动检查资料是否完整。

## 下载地址

- 发布页：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/tag/v1.0.0>
- 完整交付包：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/download/v1.0.0/WeFlow.zip>
- 单独安装器：<https://github.com/dongximuye/weflow-wechat-export-kit/releases/download/v1.0.0/WeFlow-4.5.1-x64-Setup.exe>

当前仓库为私有仓库，下载者需要登录 GitHub 并获得仓库访问权限。

## 最短使用路径

1. 从上方 GitHub Release 下载“完整交付包”。
2. 解压到空间充足的位置。
3. 打开 Codex，把 [Codex完整启动提示词.md](prompts/Codex完整启动提示词.md) 全文复制进去。
4. 按 Codex 指引安装 Skill，并重启 Codex。
5. 按提示完成 WeFlow 安装、导出和完整性检查。

详细操作见 [WeFlow操作教程.md](skill/weflow-export-wechat/references/WeFlow操作教程.md)。

## 推荐导出格式

- 对话文本：**ChatLab JSONL**。
- 媒体：按分析需要选择图片、文件、语音、视频和表情包。
- 交给 Codex：提供整个导出目录，不要只提供 JSONL。

## 文件说明

- `skill/weflow-export-wechat`：Codex Skill。
- `prompts/Codex完整启动提示词.md`：同事首次使用时复制给 Codex 的完整提示词。
- `安装Skill.ps1`：将本地 Skill 安装到当前用户的 Codex。
- `SECURITY.md`：隐私和安装器安全说明。

## 第三方软件说明

WeFlow 是第三方工具，不属于本仓库。源代码仓库不包含安装器；如获得合法再分发授权，可在版本 Release 中单独提供安装器及 SHA-256 校验值。

## 维护者发布

准备好 `dist` 后，安装并登录 GitHub CLI，再运行：

```powershell
.\scripts\publish-github.ps1
```

脚本默认创建私有仓库并发布 `v1.0.0`，不会把安装器写入 Git 历史。

