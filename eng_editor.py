#!/usr/bin/env python3
# eng_editor.py

import os
import re


def get_folder():
    return os.path.dirname(os.path.abspath(__file__))


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    # 1. AR text replacement
    txt = txt.replace("AR-примерка полотна", "View in AR")

    # 2. main catalog title replacement
    txt = txt.replace("Полотна в AR для примерки.", "View all tapestries in AR")

    # 3. system/browser note replacement
    txt = txt.replace(
        "Для корректного отображения используйте Google Chrome для Android либо Safari для iPhone.",
        "For correct display, use Google Chrome on Android or Safari on iPhone."
    )

    # 4. replace block from catalog section to BACK button
    pattern = re.compile(r"Полотна в AR для примерки\..*?ARABIC STYLE", re.S)

    back_button = '''
<div style="margin:20px 0;">
  <button onclick="history.back()" style="
    padding:10px 18px;
    border:none;
    border-radius:8px;
    cursor:pointer;
    background:#222;
    color:#fff;
    font-size:14px;
  ">
    BACK
  </button>
</div>
'''

    txt = pattern.sub(back_button, txt)

    # 5. fix internal links to eng_
    def repl(match):
        url = match.group(1)
        if url.startswith("eng_"):
            return match.group(0)
        return f'href="eng_{url}"'

    txt = re.sub(r'href="([^"]+\.html)"', repl, txt)

    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)

    print(f"OK: {os.path.basename(path)}")


def main():
    folder = get_folder()

    files = [
        f for f in os.listdir(folder)
        if f.startswith("eng_")
        and f.endswith(".html")
        and f != "eng_index.html"
        and os.path.isfile(os.path.join(folder, f))
    ]

    if not files:
        print("No files found")
        return

    for f in files:
        process_file(os.path.join(folder, f))


if __name__ == "__main__":
    main()