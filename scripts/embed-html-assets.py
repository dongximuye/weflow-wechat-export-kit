from __future__ import annotations

import base64
import mimetypes
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "docs" / "WeFlow安装与导出截图教程.html"


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    base = HTML_PATH.parent

    for rel in sorted(set(re.findall(r'<img src="([^"]+)"', html))):
        if rel.startswith("data:"):
            continue
        image_path = base / rel
        data = base64.b64encode(image_path.read_bytes()).decode("ascii")
        mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
        html = html.replace(f'src="{rel}"', f'src="data:{mime};base64,{data}"')

    html = html.replace(
        "真正的工具包由 Codex 从 GitHub Release 下载。",
        "真正的工具包由 Codex 从 GitHub Release 下载。本 HTML 已内嵌截图，单独打开也能看到配图。",
    )

    html = html.replace(
        '<a href="#finish">6. 完成后交给 Codex 验收</a>',
        '<a href="#finish">6. 完成后交给 Codex 验收</a>\n'
        '        <a href="#autopilot">7. 不建议让 Codex 代操安装</a>',
    )

    html = html.replace(
        "  </main>\n\n  <footer>",
        '    <section id="autopilot" class="card step">\n'
        '      <h2><span class="step-number">7</span>不建议让 Codex 代操安装配置</h2>\n'
        "      <p>默认做法是：Codex 负责读教程、判断下一步、提醒风险和验收结果；人负责点击 WeFlow、微信和系统弹窗。</p>\n"
        '      <div class="notice warn">不建议让 Codex 直接接管鼠标键盘完成安装配置。安装器、微信、密钥获取和系统弹窗会频繁切换窗口；如果这时使用其他软件，会影响 Codex 截屏和判断，容易点错、卡住或变慢。</div>\n'
        "      <p>只有在操作者愿意全程盯着电脑、不切换窗口、随时处理弹窗，并明确接受效率较低的情况下，才考虑让 Codex 辅助操作局部步骤。团队复现时，推荐人工点击 + Codex 指导。</p>\n"
        "    </section>\n"
        "  </main>\n\n  <footer>",
    )

    HTML_PATH.write_text(html, encoding="utf-8")
    count = html.count("data:image/")
    print(f"embedded images: {count}")


if __name__ == "__main__":
    main()
