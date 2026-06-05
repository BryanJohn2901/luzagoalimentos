#!/usr/bin/env python3
"""Move páginas para pastas (clean URLs) e atualiza links/caminhos."""
import os
import re
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))

PAGE_SLUGS = [
    'temperos-e-condimentos',
    'frutas-secas-e-castanhas',
    'refrescos-e-sobremesas',
    'trabalhe-conosco',
    'food-service',
    'farinaceos',
    'catalogo',
    'conservas',
    'cereais',
    'contato',
    'empresa',
]


def transform_html(content: str) -> str:
    for slug in PAGE_SLUGS:
        content = content.replace(f'href="{slug}.html#', f'href="/{slug}/#')
        content = content.replace(f"href='{slug}.html#", f"href='/{slug}/#")
        content = content.replace(f'href="{slug}.html"', f'href="/{slug}/"')
        content = content.replace(f"href='{slug}.html'", f"href='/{slug}/'")

    content = content.replace('href="index.html"', 'href="/"')
    content = content.replace("href='index.html'", "href='/'")

    content = re.sub(r'href="css/', 'href="/css/', content)
    content = re.sub(r'src="js/', 'src="/js/', content)
    content = re.sub(r'src="assets/', 'src="/assets/', content)
    content = re.sub(r"url\('assets/", "url('/assets/", content)
    content = re.sub(r'url\("assets/', 'url("/assets/', content)

    return content


def migrate_pages():
    for slug in PAGE_SLUGS:
        src = os.path.join(BASE, f'{slug}.html')
        if not os.path.isfile(src):
            print(f'Pulando (não existe): {slug}.html')
            continue

        dest_dir = os.path.join(BASE, slug)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, 'index.html')

        with open(src, encoding='utf-8') as f:
            content = transform_html(f.read())

        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)

        os.remove(src)
        print(f'{slug}.html → {slug}/index.html')

    index_path = os.path.join(BASE, 'index.html')
    with open(index_path, encoding='utf-8') as f:
        content = transform_html(f.read())
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('index.html atualizado (raiz)')


def update_catalog_data():
    path = os.path.join(BASE, 'js', 'catalog-data.js')
    with open(path, encoding='utf-8') as f:
        content = f.read()

    for slug in PAGE_SLUGS:
        content = content.replace(f'"{slug}.html"', f'"/{slug}/"')

    content = re.sub(r'"image": "assets/', '"image": "/assets/', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('js/catalog-data.js atualizado')


if __name__ == '__main__':
    migrate_pages()
    update_catalog_data()
