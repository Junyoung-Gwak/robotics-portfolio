"""Attach a recorded or generated demo to a project page without changing lab results."""
import argparse
import hashlib
import html
import os
from datetime import date
from pathlib import Path
from shutil import copyfile
import tempfile

CASES = ("navigation", "localization", "perception", "integration", "robot-cells")
START, END = "<!-- demo:start -->", "<!-- demo:end -->"
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
MEDIA = IMAGES | {".mp4"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def destination(root, case, source, kind, when, *, poster=False):
    suffix = source.suffix.lower()
    if not source.is_file() or suffix not in (IMAGES if poster else MEDIA):
        raise ValueError("Choose an existing MP4 or supported image (poster must be an image)")
    folder = "recordings" if kind == "recorded" else "generated-demos"
    slug = f"{case}-{when.isoformat()}-{'poster-' if poster else ''}{digest(source)[:12]}{suffix}"
    return root / "media" / folder / slug


def write_asset(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if digest(source) != digest(target):
            raise ValueError(f"Existing asset has different contents: {target.name}")
        return
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as tmp:
        temporary = Path(tmp.name)
    try:
        copyfile(source, temporary)
        if digest(temporary) != digest(source):
            raise OSError("Source changed during copy")
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def register(root, case, source, *, kind, when, caption, poster=None, preview=False):
    if case not in CASES or kind not in {"recorded", "generated"}:
        raise ValueError("Unknown project or media origin")
    if not caption.strip() or any(c in caption for c in "\r\n"):
        raise ValueError("Provide one line describing the scene")
    page = root / "projects" / (case + ".md")
    before = page.read_text("utf8")
    if before.count(START) != before.count(END) or before.count(START) > 1:
        raise ValueError("Project page has ambiguous demo markers")
    target = destination(root, case, source, kind, when)
    image = destination(root, case, poster, kind, when, poster=True) if poster else None
    caption = html.escape(caption.strip()).replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    label = "직접 촬영한 영상·사진" if kind == "recorded" else "새로 제작한 설명용 미디어"
    rel = lambda p: "../" + p.relative_to(root).as_posix()
    if image:
        display = f"[![{caption}]({rel(image)})]({rel(target)})"
    elif target.suffix in IMAGES:
        display = f"![{caption}]({rel(target)})"
    else:
        display = f"[MP4 영상 열기]({rel(target)})"
    block = f"{START}\n## 프로젝트 시연\n\n{display}\n\n**{label} · {when.isoformat()}**　{caption}\n{END}"
    if START in before:
        a, b = before.index(START), before.index(END)
        if b < a:
            raise ValueError("Demo end marker precedes its start")
        after = before[:a] + block + before[b+len(END):]
    else:
        after = before.rstrip() + "\n\n" + block + "\n"
    if preview:
        return block
    write_asset(source, target)
    if poster:
        write_asset(poster, image)
    if before != after:
        with tempfile.NamedTemporaryFile(dir=page.parent, mode="w", encoding="utf8", newline="\n", delete=False) as f:
            f.write(after)
            tmp = Path(f.name)
        try:
            if page.read_text("utf8") != before:
                raise RuntimeError("Project page changed during the update")
            os.replace(tmp, page)
        finally:
            tmp.unlink(missing_ok=True)
    return rel(target)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("case", choices=CASES)
    p.add_argument("file", type=Path)
    p.add_argument("--kind", required=True, choices=("recorded","generated"))
    p.add_argument("--date", required=True, type=date.fromisoformat, help="Recording or creation date, YYYY-MM-DD")
    p.add_argument("--caption", required=True)
    p.add_argument("--poster", type=Path)
    p.add_argument("--preview", action="store_true")
    args=p.parse_args()
    print(register(Path(__file__).resolve().parents[1], args.case, args.file, kind=args.kind,
                   when=args.date, caption=args.caption, poster=args.poster, preview=args.preview))

if __name__=="__main__":
    main()
