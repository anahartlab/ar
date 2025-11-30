import os
import csv
import re

# 1. Определяем текущую папку, где находится скрипт
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Ищем файл paintings.csv в этой папке
csv_path = os.path.join(current_dir, 'paintings.csv')
if not os.path.isfile(csv_path):
    raise FileNotFoundError(f"'paintings.csv' not found in {current_dir}")

# 3. Для каждой строки CSV с колонкой Name генерируем SEO URL и формируем блок <div class="section-card">
cards_html = ''
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row.get('Name', '').strip()
        if not name:
            continue
        # Генерируем SEO URL: lowercase, replace spaces and non-alphanumeric with hyphens
        seo_url = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        cards_html += f'<div class="section-card"><a href="{seo_url}.html">{name}</a></div>\n'

# 4. Открываем index.html в той же папке, находим закрывающий тег </header> и вставляем секцию AR примерки
index_path = os.path.join(current_dir, 'index.html')
if not os.path.isfile(index_path):
    raise FileNotFoundError(f"'index.html' not found in {current_dir}")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем любой существующий блок <section class="u-clearfix u-section-hero" ... </section> после </header>
pattern = re.compile(r'(<section *?</section>)', re.DOTALL)
header_end_index = content.find('</header>')
if header_end_index != -1:
    after_header = content[header_end_index + len('</header>'):]
    after_header = pattern.sub('', after_header)
    content = content[:header_end_index + len('</header>')] + after_header

# Секция AR примерки по шаблону, включая стили и сформированные карточки
ar_section = f"""\
  <section class="u-clearfix u-section-hero" style="padding: 50px 0; text-align: center;">
    <h4 style="font-family: inherit; font-weight: bold; margin-bottom: 40px;">Полотна в AR для примерки.</h4>

    <div class="sections-grid">

{cards_html}
  <style>
    .sections-grid {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 15px;
      /* vertical spacing between cards */
    }}

    .section-card {{
      width: 480px;
      /* horizontal brick width */
      height: 60px;
      /* brick height updated */
      border: 1px solid #ccc;
      border-radius: 10px;
      padding: 10px 20px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: center;
    }}

    .section-card a {{
      text-decoration: none;
      color: inherit;
      display: block;
      height: 100%;
    }}

    .section-card h3 {{
      margin: 0;
      font-size: 16px;
    }}
  </style>

</div>
</section>
"""

# Вставляем ar_section сразу после закрывающего тега </header>
new_content = content.replace('</header>', f'</header>\n{ar_section}')

# 5. Сохраняем обновленный index.html
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
