#!/usr/bin/env python3
"""Extrai produtos das páginas de categoria e gera js/catalog-data.js"""
import re
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

CATEGORIES = {
    'temperos-e-condimentos/index.html': {'id': 'temperos', 'name': 'Temperos e Condimentos', 'page': '/temperos-e-condimentos/'},
    'cereais/index.html': {'id': 'cereais', 'name': 'Cereais', 'page': '/cereais/'},
    'farinaceos/index.html': {'id': 'farinaceos', 'name': 'Farináceos', 'page': '/farinaceos/'},
    'frutas-secas-e-castanhas/index.html': {'id': 'frutas-secas', 'name': 'Frutas Secas e Castanhas', 'page': '/frutas-secas-e-castanhas/'},
    'conservas/index.html': {'id': 'conservas', 'name': 'Conservas', 'page': '/conservas/'},
    'food-service/index.html': {'id': 'food-service', 'name': 'Food Service', 'page': '/food-service/'},
    'refrescos-e-sobremesas/index.html': {'id': 'refrescos', 'name': 'Refrescos e Sobremesas', 'page': '/refrescos-e-sobremesas/'},
}


def extract_grid(html: str) -> str:
    match = re.search(r'<!-- Products Grid -->(.*?)<!-- Footer -->', html, re.S)
    if not match:
        match = re.search(r'<!-- Products Grid -->(.*?)<footer', html, re.S | re.I)
    return match.group(1) if match else ''


def main():
    products = []
    for fname, cat in CATEGORIES.items():
        path = os.path.join(BASE, fname)
        with open(path, encoding='utf-8') as f:
            grid = extract_grid(f.read())
        blocks = re.findall(
            r'<div class="w-24 h-24[^"]*"[^>]*>\s*<img src="([^"]+)" alt="([^"]+)"[^>]*>\s*</div>\s*<h3[^>]*>([^<]+)</h3>.*?DISPONÍVEL EM:</p><p[^>]*>([^<]+)</p>',
            grid,
            re.S,
        )
        for img, _alt, name, sizes in blocks:
            products.append({
                'name': name.strip(),
                'image': img.strip(),
                'sizes': sizes.strip(),
                'category': cat['id'],
                'categoryName': cat['name'],
                'categoryPage': cat['page'],
            })

    payload = {
        'categories': [{'id': v['id'], 'name': v['name'], 'page': v['page']} for v in CATEGORIES.values()],
        'products': products,
    }

    out = os.path.join(BASE, 'js', 'catalog-data.js')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('window.LUZAGO_CATALOG = ' + json.dumps(payload, ensure_ascii=False, indent=2) + ';\n')

    print(f'Gerado {out} com {len(products)} produtos.')


if __name__ == '__main__':
    main()
