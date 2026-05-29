#!/usr/bin/env python3
# eng_editor.py

import os
import re


def get_folder():
    return os.path.dirname(os.path.abspath(__file__))


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    # 1. simple replace
    txt = txt.replace("AR-примерка полотна", "View in AR")

    # 2. remove AR catalog block and replace with BACK button
    pattern = re.compile(
        r"Полотна в AR для примерки\..*?ARABIC STYLE",
        re.S
    )

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
    ]

    if not files:
        print("No files found")
        return

    for f in files:
        process_file(os.path.join(folder, f))


if __name__ == "__main__":
    main()