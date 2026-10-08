"""Build the standalone HTML and ZIP using only the Python standard library."""

import base64
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "downloads"


def svg_data_uri(relative_path: str) -> str:
    path = (ROOT / relative_path).resolve()
    if not path.is_relative_to(ROOT / "assets") or path.suffix != ".svg":
        raise ValueError(f"Unsupported asset: {relative_path}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def build() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    javascript = (ROOT / "script.js").read_text(encoding="utf-8")

    css = re.sub(
        r'url\("(assets/[^"\n]+\.svg)"\)',
        lambda match: f'url("{svg_data_uri(match[1])}")',
        css,
    )
    html, style_count = re.subn(
        r'<link\b[^>]*\bhref="styles\.css"[^>]*>',
        lambda _: f"<style>\n{css}\n</style>",
        html,
    )
    html, script_count = re.subn(
        r'[ \t]*<script\b[^>]*\bsrc="script\.js"[^>]*>\s*</script>',
        "",
        html,
    )
    if style_count != 1 or script_count != 1:
        raise ValueError("Expected exactly one stylesheet and one script")
    html = re.sub(
        r'\b(src|href)="(assets/[^"\n]+\.svg)"',
        lambda match: f'{match[1]}="{svg_data_uri(match[2])}"',
        html,
    )
    if re.search(r'(?:src|href)="assets/|url\(["\']?assets/', html):
        raise ValueError("An asset reference was not embedded")
    # The DOM must exist when the original deferred script runs.
    html = html.replace("</body>", f"<script>\n{javascript}\n</script>\n</body>", 1)
    if "</body>" not in html:
        raise ValueError("Missing body end tag")

    instructions = (
        "Namaste Cinema — はじめてのインド映画と音楽\n\n"
        "1. ZIPをダウンロードし、展開（解凍）してください。\n"
        "2. namaste-cinema.html をChrome、Edge、Safariなどのブラウザーで開いてください。\n"
        "画像・デザイン・操作機能はHTMLに含まれています。追加インストールは不要です。\n"
        "映画や音楽の外部リンクを開くときはインターネット接続が必要です。\n\n"
        "ブラウザーがローカルHTMLを制限している場合、展開したフォルダーで\n"
        "python3 -m http.server 8000\n"
        "を実行し、ブラウザーで http://localhost:8000/namaste-cinema.html を開いてください。\n"
    )
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "namaste-cinema.html").write_text(html, encoding="utf-8")
    # Fixed timestamps make rebuilds reproducible without unnecessary binary diffs.
    with ZipFile(OUTPUT / "Namaste-Cinema.zip", "w") as archive:
        for filename, contents in [
            ("Namaste-Cinema/namaste-cinema.html", html),
            ("Namaste-Cinema/はじめに.txt", instructions),
        ]:
            entry = ZipInfo(filename, date_time=(2026, 10, 8, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, contents.encode("utf-8"))
    print(f"Created {OUTPUT / 'namaste-cinema.html'}")
    print(f"Created {OUTPUT / 'Namaste-Cinema.zip'}")


if __name__ == "__main__":
    build()
