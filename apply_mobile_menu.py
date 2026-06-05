#!/usr/bin/env python3
"""Aplica menu mobile e CSS responsivo em todas as páginas."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

MOBILE_CSS = '    <link rel="stylesheet" href="/css/mobile-menu.css">\n'
RESPONSIVE_CSS = '    <link rel="stylesheet" href="/css/responsive.css">\n'

MOBILE_JS = '    <script src="/js/mobile-menu.js"></script>\n'

TOGGLE_OLD = re.compile(
    r'<button[^>]*class="[^"]*md:hidden[^"]*"[^>]*>\s*'
    r'<i class="fa-solid fa-bars"></i>\s*'
    r'</button>',
    re.S,
)

TOGGLE_NEW = '''            <button type="button" class="mobile-menu-toggle md:hidden" aria-label="Abrir menu" aria-expanded="false" aria-controls="mobile-menu-panel">
                <i class="fa-solid fa-bars" aria-hidden="true"></i>
            </button>'''


def patch_head(content: str) -> str:
    if '/css/mobile-menu.css' not in content:
        anchor = '    <link rel="stylesheet" href="/css/effects.css">'
        if anchor in content:
            content = content.replace(anchor, anchor + '\n' + MOBILE_CSS.rstrip() + '\n' + RESPONSIVE_CSS.rstrip())
        else:
            anchor2 = '    <link rel="stylesheet" href="/css/buttons.css">'
            content = content.replace(anchor2, anchor2 + '\n' + MOBILE_CSS.rstrip() + '\n' + RESPONSIVE_CSS.rstrip())
    return content


def patch_scripts(content: str) -> str:
    if 'mobile-menu.js' in content:
        return content
    if '<script src="/js/site-effects.js"></script>' in content:
        content = content.replace(
            '    <script src="/js/site-effects.js"></script>',
            MOBILE_JS.rstrip() + '\n    <script src="/js/site-effects.js"></script>',
        )
    elif '</body>' in content:
        content = content.replace('</body>', MOBILE_JS + '</body>')
    return content


def patch_toggle(content: str) -> str:
    return TOGGLE_OLD.sub(TOGGLE_NEW, content)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    updated = original
    updated = patch_head(updated)
    updated = patch_scripts(updated)
    updated = patch_toggle(updated)
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
    print(f'Concluído: {changed} arquivo(s).')


if __name__ == '__main__':
    main()
