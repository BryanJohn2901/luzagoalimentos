#!/usr/bin/env python3
"""Aplica lazy load, AOS e effects.css em todas as páginas HTML."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

AOS_CSS = '    <link rel="stylesheet" href="https://unpkg.com/aos@2.3.4/dist/aos.css">\n'
EFFECTS_CSS = '    <link rel="stylesheet" href="/css/effects.css">\n'

AOS_SCRIPTS = '''    <script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
    <script src="/js/site-effects.js"></script>
'''

EAGER_SRC = ('logo-luzago.png', 'icone-folha-luzago.png', 'favicon-luzago.png')

PRODUCT_ITEM_OLD = (
    'class="bg-white rounded-xl shadow-md p-6 flex flex-col items-center '
    'text-center border border-gray-100 hover:shadow-lg transition duration-300 '
    'transform hover:-translate-y-1"'
)
PRODUCT_ITEM_NEW = (
    'class="product-item bg-white rounded-xl shadow-md p-6 flex flex-col '
    'items-center text-center border border-gray-100"'
)


def patch_head(content: str) -> str:
    if 'aos@2.3.4' not in content:
        anchor = '    <link rel="stylesheet" href="/css/buttons.css">'
        blog_anchor = '    <link rel="stylesheet" href="/css/blog.css">'
        if blog_anchor in content:
            content = content.replace(blog_anchor, blog_anchor + '\n' + AOS_CSS + EFFECTS_CSS.rstrip())
        elif anchor in content:
            content = content.replace(anchor, anchor + '\n' + AOS_CSS + EFFECTS_CSS.rstrip())
    elif '/css/effects.css' not in content:
        content = content.replace(AOS_CSS.strip(), AOS_CSS.strip() + '\n' + EFFECTS_CSS.rstrip())
    return content


def patch_scripts(content: str) -> str:
    if 'site-effects.js' in content:
        return content
    if '</body>' in content:
        content = content.replace('</body>', AOS_SCRIPTS + '\n</body>')
    return content


def patch_lazy_images(content: str) -> str:
    def repl(match: re.Match) -> str:
        tag = match.group(0)
        if 'loading=' in tag:
            if 'decoding=' not in tag:
                tag = tag.replace('<img ', '<img decoding="async" ', 1)
            return tag

        src_match = re.search(r'src="([^"]+)"', tag)
        src = src_match.group(1) if src_match else ''
        eager = any(p in src for p in EAGER_SRC)

        attrs = 'loading="eager" decoding="async" ' if eager else 'loading="lazy" decoding="async" '
        tag = tag.replace('<img ', '<img ' + attrs, 1)

        if not eager and '/assets/' in src and '.svg' not in src:
            if 'class="' in tag:
                tag = tag.replace('class="', 'class="img-lazy ', 1)
            else:
                tag = tag.replace('<img ', '<img class="img-lazy" ', 1)
        return tag

    return re.sub(r'<img\s[^>]*>', repl, content)


def patch_product_items(content: str) -> str:
    return content.replace(PRODUCT_ITEM_OLD, PRODUCT_ITEM_NEW)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    updated = original
    updated = patch_head(updated)
    updated = patch_scripts(updated)
    updated = patch_lazy_images(updated)
    updated = patch_product_items(updated)
    if updated != original:
        path.write_text(updated, encoding='utf-8')
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(BASE.rglob('*.html')):
        if '.vercel' in path.parts or '.git' in path.parts:
            continue
        if process_file(path):
            print(f'Atualizado: {path.relative_to(BASE)}')
            changed += 1
    print(f'Concluído: {changed} arquivo(s) modificados.')


if __name__ == '__main__':
    main()
