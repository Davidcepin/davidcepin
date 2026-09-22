import os
import re

PHOTOS_DIR = "photos"
README = "README.md"
IMG_HEIGHT = "400px"
VALID_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp")

START = "<!-- PHOTOS:START -->"
END = "<!-- PHOTOS:END -->"

def build_gallery_markdown():
    if not os.path.isdir(PHOTOS_DIR):
        return ""
    files = sorted(f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith(VALID_EXT))
    if not files:
        return ""

    tags = []
    for f in files:
        path = f"{PHOTOS_DIR}/{f}"
        name = os.path.splitext(f)[0].replace("_", " ").replace("-", " ")
        tags.append(
            f'<a href="{path}" target="_blank">'
            f'<img src="{path}" alt="{name}" height="{IMG_HEIGHT}"></a>'
        )
    return "\n".join(tags)

def update_readme():
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    gallery = build_gallery_markdown()
    block = f"{START}\n{gallery}\n{END}"

    pattern = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    if not pattern.search(content):
        raise SystemExit(f"Markers {START} / {END} not found in {README}")

    new_content = pattern.sub(block, content)

    with open(README, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()
