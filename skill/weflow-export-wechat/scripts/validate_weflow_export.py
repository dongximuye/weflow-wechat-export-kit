#!/usr/bin/env python3
"""Validate WeFlow ChatLab JSONL exports without printing chat content."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


REQUIRED_MESSAGE_FIELDS = {"sender", "timestamp", "type", "content", "platformMessageId"}
MEDIA_PREFIXES = ("../images/", "../file/", "../videos/", "../emojis/")


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def iso_timestamp(value: Any) -> str | None:
    try:
        number = float(value)
        if number > 10_000_000_000:
            number /= 1000
        return datetime.fromtimestamp(number, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError, OverflowError):
        return None


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_file(path: Path) -> dict[str, Any]:
    export_root = path.parent.parent.resolve() if path.parent.name.lower() == "texts" else path.parent.resolve()
    result: dict[str, Any] = {
        "file": str(path), "lines": 0, "valid_json_lines": 0,
        "invalid_json_lines": [], "record_types": Counter(), "message_types": Counter(),
        "messages": 0, "members": 0, "headers": 0,
        "missing_message_fields": [], "duplicate_message_ids": [],
        "media_references": 0, "existing_media_references": 0,
        "missing_media": [], "unsafe_media_paths": [],
        "timestamp_start_utc": None, "timestamp_end_utc": None,
    }
    seen_ids: set[str] = set()
    timestamps: list[float] = []

    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                continue
            result["lines"] += 1
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                result["invalid_json_lines"].append({"line": line_number, "error": exc.msg})
                continue

            result["valid_json_lines"] += 1
            record_type = str(record.get("_type", "unknown"))
            result["record_types"][record_type] += 1
            if record_type == "header":
                result["headers"] += 1
            elif record_type == "member":
                result["members"] += 1
            elif record_type == "message":
                result["messages"] += 1
                result["message_types"][str(record.get("type", "unknown"))] += 1
                missing = sorted(REQUIRED_MESSAGE_FIELDS - record.keys())
                if missing:
                    result["missing_message_fields"].append({"line": line_number, "fields": missing})
                message_id = record.get("platformMessageId")
                if message_id is not None:
                    message_id = str(message_id)
                    if message_id in seen_ids:
                        result["duplicate_message_ids"].append({"line": line_number, "id": message_id})
                    seen_ids.add(message_id)
                try:
                    timestamps.append(float(record.get("timestamp")))
                except (TypeError, ValueError):
                    pass

            for text in iter_strings(record):
                normalized = text.replace("\\", "/")
                if not normalized.startswith(MEDIA_PREFIXES):
                    continue
                result["media_references"] += 1
                resolved = (path.parent / Path(normalized)).resolve()
                if not inside(resolved, export_root):
                    result["unsafe_media_paths"].append({"line": line_number, "path": normalized})
                elif resolved.is_file():
                    result["existing_media_references"] += 1
                else:
                    result["missing_media"].append({"line": line_number, "path": normalized})

    if timestamps:
        result["timestamp_start_utc"] = iso_timestamp(min(timestamps))
        result["timestamp_end_utc"] = iso_timestamp(max(timestamps))
    result["record_types"] = dict(result["record_types"])
    result["message_types"] = dict(result["message_types"])
    result["passed"] = not any((result["invalid_json_lines"], result["missing_message_fields"],
        result["duplicate_message_ids"], result["missing_media"], result["unsafe_media_paths"])) \
        and result["messages"] > 0 and result["headers"] == 1
    return result


def discover(target: Path) -> list[Path]:
    if target.is_file() and target.suffix.lower() == ".jsonl":
        return [target.resolve()]
    if target.is_dir():
        return sorted(path.resolve() for path in target.rglob("*.jsonl") if path.is_file())
    return []


def printable_summary(results: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for result in results:
        lines.extend([
            f"文件: {result['file']}",
            f"状态: {'通过' if result['passed'] else '未通过'}",
            f"JSONL: {result['valid_json_lines']}/{result['lines']} 行有效",
            f"消息: {result['messages']} 条；成员: {result['members']}；头记录: {result['headers']}",
            f"时间(UTC): {result['timestamp_start_utc']} 至 {result['timestamp_end_utc']}",
            f"媒体: {result['existing_media_references']}/{result['media_references']} 个引用存在；"
            f"缺失 {len(result['missing_media'])}；越界 {len(result['unsafe_media_paths'])}",
            f"重复消息标识: {len(result['duplicate_message_ids'])}", "",
        ])
    return "\n".join(lines).rstrip()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="校验 WeFlow ChatLab JSONL 与媒体相对路径。")
    parser.add_argument("target", type=Path, help="WeFlow 导出目录或单个 .jsonl 文件")
    parser.add_argument("--json-report", type=Path, help="保存不含聊天正文的 JSON 验收报告")
    args = parser.parse_args()
    files = discover(args.target.expanduser())
    if not files:
        print("未找到 .jsonl 文件。请提供完整 WeFlow 导出目录或 JSONL 文件。", file=sys.stderr)
        return 2
    results = [validate_file(path) for path in files]
    print(printable_summary(results))
    if args.json_report:
        report = {"validator": "weflow-export-wechat", "generated_at_utc": datetime.now(tz=timezone.utc).isoformat(),
                  "target": str(args.target), "passed": all(item["passed"] for item in results), "files": results}
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())

