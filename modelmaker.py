import csv
import re
import os


def slugify(text):
    """
    Преобразует строку в SEO-friendly URL:
    - переводит в нижний регистр,
    - заменяет пробелы и недопустимые символы на '-'.
    """
    text = text.lower()
    # заменить пробелы на дефисы и удалить все кроме букв и цифр
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9\-]", "", text)
    # убрать повторяющиеся дефисы
    text = re.sub(r"-+", "-", text).strip("-")
    return text


# Читаем шаблон из файла index.html полностью
with open("index.html", "r", encoding="utf-8") as f:
    full_html = f.read()

# Находим закрывающий тег </header>
header_end = full_html.find("</header>")
if header_end == -1:
    raise ValueError("Не найден закрывающий тег </header> в index.html")

# Разделяем html на до </header> и после
before_header_close = full_html[: header_end + len("</header>")]
after_header_close = full_html[header_end + len("</header>") :]

csv_path = "paintings.csv"
output_dir = "./"  # можно указать папку для выхода

with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Name"].strip()
        size = row.get("Size", "").strip()
        seo_name = slugify(name)
        output_filename = f"{seo_name}.html"

        # Формируем AR секцию с model-viewer
        ar_section = f"""

  <section class="u-clearfix u-section-1" id="block-1" style="padding: 20px;">
    <div class="u-sheet u-valign-middle u-sheet-1" style="max-width: 700px; margin: 0 auto;">
      <h4 style="text-align: center; margin-bottom: 30px;">AR-примерка полотна {name} {size} </h4>
      <model-viewer src="images/{name}.glb" ios-src="images/{name}.usdz" alt="{seo_name}"
        ar ar-modes="scene-viewer quick-look webxr" camera-controls
        style="width: 100%; height: 600px; background: #000;">
      </model-viewer>
      <p style="text-align:center; font-size:14px; color:#ccc; margin-top:10px;">
        Для корректного отображения используйте Google Chrome для Android либо Safari для iPhone.
      </p>
    </div>
  </section>
"""

        # Вставляем AR секцию после </header>
        page_html = before_header_close + ar_section + after_header_close

        # Записываем в файл
        with open(
            os.path.join(output_dir, output_filename), "w", encoding="utf-8"
        ) as f:
            f.write(page_html)
        print(f"Создан файл: {output_filename}")
