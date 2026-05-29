#!/usr/bin/env python3
# eng_editor.py

import os
import re


def get_folder():
    return os.path.dirname(os.path.abspath(__file__))


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    # Replace malformed links: eng_https:// -> https://
    txt = txt.replace("eng_https://", "https://")

    # Extra safety regex (covers any eng_https variants)
    txt = re.sub(r"eng_(https://)", r"\1", txt)

    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)

    print(f"OK: {os.path.basename(path)}")


def main():
    folder = get_folder()

    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".html")
        and os.path.isfile(os.path.join(folder, f))
    ]

    if not files:
        print("No files found")
        return

    for f in files:
        process_file(os.path.join(folder, f))


if __name__ == "__main__":
    main()