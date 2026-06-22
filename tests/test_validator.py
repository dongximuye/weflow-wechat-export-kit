import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "skill" / "weflow-export-wechat" / "scripts" / "validate_weflow_export.py"
SPEC = importlib.util.spec_from_file_location("validator", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def make_export(self, root: Path) -> Path:
        texts = root / "texts"
        images = root / "images"
        texts.mkdir(parents=True)
        images.mkdir(parents=True)
        (images / "one.png").write_bytes(b"png")
        records = [
            {"_type": "header", "chatlab": {}, "meta": {}},
            {"_type": "member", "platformId": "u1", "accountName": "成员", "avatar": ""},
            {
                "_type": "message", "sender": "u1", "accountName": "成员",
                "timestamp": 1_700_000_000, "type": 25, "content": "../images/one.png",
                "platformMessageId": "m1",
            },
        ]
        jsonl = texts / "chat.jsonl"
        jsonl.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in records), encoding="utf-8")
        return jsonl

    def test_valid_export_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            jsonl = self.make_export(Path(folder))
            result = validator.validate_file(jsonl)
            self.assertTrue(result["passed"])
            self.assertEqual(result["messages"], 1)
            self.assertEqual(result["existing_media_references"], 1)

    def test_missing_media_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            jsonl = self.make_export(root)
            (root / "images" / "one.png").unlink()
            result = validator.validate_file(jsonl)
            self.assertFalse(result["passed"])
            self.assertEqual(len(result["missing_media"]), 1)

    def test_invalid_json_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            jsonl = self.make_export(Path(folder))
            with jsonl.open("a", encoding="utf-8") as handle:
                handle.write("\n{broken")
            result = validator.validate_file(jsonl)
            self.assertFalse(result["passed"])
            self.assertEqual(len(result["invalid_json_lines"]), 1)


if __name__ == "__main__":
    unittest.main()

