import os

# ===== Настройки =====
NAME = "fullprint_liberty_cap"
SEO_NAME = NAME
SIZE = ""  # или оставь пустую строку ""
# =====================

script_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(script_dir, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    full_html = f.read()

# Находим закрывающий тег </header>
header_end = full_html.find("</header>")
if header_end == -1:
    raise ValueError("Не найден закрывающий тег </header> в index.html")

# Оставляем всё до </header>
before_header_close = full_html[: header_end + len("</header>")]

# Находим открывающий тег <footer
footer_start = full_html.find("<footer", header_end)
if footer_start == -1:
    raise ValueError("Не найден тег <footer> в index.html")

# Оставляем footer и всё после него
after_footer = full_html[footer_start:]

output_dir = script_dir
output_filename = f"{SEO_NAME}.html"

# Формируем AR секцию с model-viewer
ar_section = f"""

<section class="u-clearfix u-section-1" id="block-1" style="padding: 20px;">
  <div class="u-sheet u-valign-middle u-sheet-1" style="max-width: 700px; margin: 0 auto;">
    <h4 style="text-align: center; margin-bottom: 30px;">
      3D/AR MODEL {NAME} {SIZE}
    </h4>

    <model-viewer
      src="images/FULLPRINT/{NAME}.glb"
      ios-src="images/FULLPRINT/{NAME}.usdz"
      alt="{SEO_NAME}"
      ar
      ar-modes="scene-viewer quick-look webxr"
      camera-controls
      style="width: 100%; height: 600px; background: #000;">
    </model-viewer>

    <p style="text-align:center; font-size:14px; color:#ccc; margin-top:10px;">
      Для корректного отображения используйте Google Chrome для Android либо Safari для iPhone.
    </p>
  </div>
</section>
"""

# Полностью очищаем содержимое между </header> и <footer>
# и вставляем новую AR-секцию
page_html = before_header_close + ar_section + after_footer

# Записываем файл
with open(os.path.join(output_dir, output_filename), "w", encoding="utf-8") as f:
    f.write(page_html)

print(f"Создан файл: {output_filename}")
