from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from tools.register_demo import START, END, register


class DemoSlotTest(unittest.TestCase):
    def test_recording_is_copied_and_slot_replaced_idempotently(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp); (root/"projects").mkdir()
            page=root/"projects/navigation.md"
            page.write_text(f"Intro\n{START}\noriginal example\n{END}\nAfter\n","utf8")
            source=root/"sample.mp4";source.write_bytes(b"test file, never published")
            args=dict(kind="recorded",when=date(2026,1,2),caption="회전 후 정지")
            register(root,"navigation",source,preview=True,**args)
            self.assertFalse((root/"media").exists())
            target=register(root,"navigation",source,**args)
            self.assertEqual((page.parent/target).read_bytes(),source.read_bytes())
            once=page.read_text("utf8")
            self.assertIn("직접 촬영",once);self.assertNotIn("original example",once)
            self.assertTrue(once.startswith("Intro"));self.assertTrue(once.endswith("After\n"))
            register(root,"navigation",source,**args)
            self.assertEqual(page.read_text("utf8"),once)

    def test_invalid_markers_leave_document_unchanged(self):
        with TemporaryDirectory() as tmp:
            root=Path(tmp);(root/"projects").mkdir()
            page=root/"projects/perception.md";page.write_text(START,"utf8")
            with self.assertRaises(ValueError):
                register(root,"perception",root/"poster.png",kind="generated",when=date.today(),caption="합성 영상")
            self.assertEqual(page.read_text("utf8"),START)
