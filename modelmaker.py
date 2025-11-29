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


# Читаем шаблон из файла index.html
with open("index.html", "r", encoding="utf-8") as f:
    template = f.read()

csv_path = "paintings.csv"
output_dir = "./"  # можно указать папку для выхода

with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Name"].strip()
        size = row.get("Size", "").strip()

        # Генерируем SEO-friendly URL из названия
        seo_name = slugify(name)
        output_filename = f"{seo_name}.html"

        # Имя файлов моделей (предполагается, что они совпадают с Name)
        model_glb = f"{name}.glb"
        model_usdz = f"{name}.usdz"

        # Заполняем шаблон данными
        html_content = (
            template.replace("{name}", name)
            .replace("{size}", size)
            .replace("{model_glb}", model_glb)
            .replace("{model_usdz}", model_usdz)
        )

        # Записываем в файл
        with open(
            os.path.join(output_dir, output_filename), "w", encoding="utf-8"
        ) as f:
            f.write(html_content)
        print(f"Создан файл: {output_filename}")
