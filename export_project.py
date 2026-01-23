import os
import re

# --- SOZLAMALAR ---
OUTPUT_FILE = "project_context_ultra.md"

# Mutlaqo o'qilmaydigan papkalar
IGNORE_DIRS = {
    'venv', '.venv', 'env', '.git', '.idea', '.vscode', '__pycache__',
    'migrations', 'media', 'static_root', 'staticfiles', 'node_modules', 'locale'
}

# O'qilmaydigan fayllar (standart yoki keraksiz)
IGNORE_FILES = {
    'db.sqlite3', 'package-lock.json', 'yarn.lock', '.DS_Store',
    'poetry.lock', 'Pipfile.lock', 'manage.py', 'LICENSE', 'README.md'
}

# Kerakli kengaytmalar
ALLOWED_EXTENSIONS = {'.py', '.html', '.css', '.js'}


def remove_comments_and_docs(source):
    """Python kodidan izohlar va docstringlarni tozalaydi"""
    # Docstringlarni ("""...""" yoki '''...''') o'chirish
    pattern = r"(\"\"\"[\s\S]*?\"\"\")|(\'\'\'[\s\S]*?\'\'\')"
    source = re.sub(pattern, "", source)

    # # bilan boshlanadigan izohlarni o'chirish
    source = re.sub(r"#.*", "", source)

    # Bo'sh qatorlarni olib tashlash va kodni siqish
    lines = [line.rstrip() for line in source.splitlines() if line.strip()]
    return "\n".join(lines)


def minify_html(content):
    """HTML/CSS/JS dan ortiqcha bo'shliqlarni olib tashlaydi"""
    # HTML commentlarni o'chirish <!-- ... -->
    content = re.sub(r"<!--[\s\S]*?-->", "", content)
    # Bo'sh qatorlarni tozalash
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return "\n".join(lines)


def is_boilerplate(filename, content):
    """Agar fayl standart va muhim bo'lmasa, uni o'tkazib yuboramiz"""
    # Bo'sh fayllar
    if not content.strip():
        return True

    # __init__.py faqat bo'sh bo'lsa tashlanadi (yuqorida tekshirildi), 
    # lekin importlar bo'lsa qoladi.

    # apps.py ko'pincha o'zgartirilmaydi
    if filename == "apps.py" and "AppConfig" in content and len(content) < 150:
        return True

    # tests.py agar ichida hech narsa yozilmagan bo'lsa
    if filename == "tests.py" and len(content) < 100:
        return True

    return False


def generate_tree(root_dir):
    tree_str = "# TREE\n"
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = root.replace(root_dir, '').count(os.sep)
        indent = '  ' * level  # 2 probel yetadi
        folder = os.path.basename(root)
        if level == 0: folder = "."

        # Faqat ichida allowed fayl bor papkalarni ko'rsatish mantig'i murakkab,
        # shuning uchun oddiy daraxt chizamiz, lekin ixcham.
        tree_str += f"{indent}{folder}/\n"

        for f in files:
            if f.endswith(tuple(ALLOWED_EXTENSIONS)) and f not in IGNORE_FILES:
                tree_str += f"{indent}  {f}\n"
    tree_str += "\n"
    return tree_str


def main():
    root_dir = os.getcwd()
    print("🚀 Ultra-Optimallashtirish boshlandi...")

    total_files = 0
    ignored_count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # 1. Tizim uchun qisqa prompt
        outfile.write("CONTEXT: Django Project. Comments removed for brevity. Interpret code logic.\n\n")

        # 2. Daraxt (Juda ixcham)
        outfile.write(generate_tree(root_dir))

        outfile.write("# CODE\n")

        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext in ALLOWED_EXTENSIONS and file not in IGNORE_FILES and file != "export_ultra.py":

                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, root_dir)

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            raw_content = f.read()

                        # Fayl turiga qarab tozalash
                        if ext == '.py':
                            clean_content = remove_comments_and_docs(raw_content)
                        else:
                            clean_content = minify_html(raw_content)

                        # Agar tozalagandan keyin fayl keraksiz deb topilsa
                        if is_boilerplate(file, clean_content):
                            ignored_count += 1
                            continue

                        # Natijani yozish (Markdown header ishlatmaymiz, joy oladi)
                        outfile.write(f"--- {rel_path} ---\n")
                        outfile.write(clean_content)
                        outfile.write("\n\n")

                        total_files += 1
                        print(f"📦 {rel_path}")

                    except Exception as e:
                        print(f"❌ Xato: {rel_path}")

    print(f"\n✅ TAYYOR! {total_files} ta fayl yozildi. {ignored_count} ta keraksiz fayl tashlab ketildi.")
    print(f"📁 Natija: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()