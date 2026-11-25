from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class DocumentLinksTest(unittest.TestCase):
    def test_repository_links_resolve(self):
        documents = sorted(ROOT.glob("README*.md"))
        for folder in ("projects", "labs", "media"):
            documents.extend(sorted((ROOT / folder).rglob("*.md")))
        for page in documents:
            text = page.read_text("utf8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                address = urlsplit(target.strip("<>"))
                if address.scheme or not address.path:
                    continue
                file = (page.parent / unquote(address.path)).resolve()
                with self.subTest(page=page.relative_to(ROOT), target=target):
                    self.assertTrue(file.is_relative_to(ROOT))
                    self.assertTrue(file.exists())

    def test_published_demo_slots_have_an_origin_label(self):
        for page in (ROOT / "projects").glob("*.md"):
            text = page.read_text("utf8")
            self.assertEqual(text.count("<!-- demo:start -->"), text.count("<!-- demo:end -->"))
            for block in re.findall(r"<!-- demo:start -->(.*?)<!-- demo:end -->", text, re.S):
                with self.subTest(page=page.name):
                    self.assertTrue("제작" in block or "촬영" in block)
