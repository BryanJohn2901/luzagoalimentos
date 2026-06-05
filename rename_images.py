#!/usr/bin/env python3
"""Renomeia imagens de produtos e institucionais conforme alt/uso e atualiza referências."""
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent

CATEGORIES = {
    'temperos-e-condimentos/index.html': 'assets/temperos',
    'cereais/index.html': 'assets/cereais',
    'farinaceos/index.html': 'assets/Farináceos',
    'frutas-secas-e-castanhas/index.html': 'assets/Frutas Secas e Castanhas',
    'conservas/index.html': 'assets/Conservas',
    'food-service/index.html': 'assets/Food Service',
    'refrescos-e-sobremesas/index.html': 'assets/Refrescos e Sobremesas',
}

STATIC_RENAMES = {
    'assets/icones/asset 3.png': 'assets/icones/logo-luzago.png',
    'assets/icones/asset 4.png': 'assets/icones/icone-folha-luzago.png',
    'assets/icones/asset 5.svg': 'assets/icones/categoria-temperos.svg',
    'assets/icones/asset 6.svg': 'assets/icones/categoria-cereais.svg',
    'assets/icones/asset 7.svg': 'assets/icones/categoria-farinaceos.svg',
    'assets/icones/asset 8.svg': 'assets/icones/categoria-frutas-secas.svg',
    'assets/icones/asset 9.svg': 'assets/icones/categoria-conservas.svg',
    'assets/icones/asset 10.svg': 'assets/icones/categoria-refrescos-sobremesas.svg',
    'assets/icones/asset 11.svg': 'assets/icones/categoria-food-service.svg',
    'assets/icones/asset 17.svg': 'assets/icones/icone-google.svg',
    'assets/icones/asset 19.png': 'assets/icones/avatar-arthur-alexandre.png',
    'assets/icones/asset 20.png': 'assets/icones/avatar-luanny-scalada.png',
    'assets/icones/asset 41.svg': 'assets/icones/icone-verificado.svg',
    'assets/imagens/asset 39.png': 'assets/imagens/hero-vegetais.png',
    'assets/imagens/asset 40.jpeg': 'assets/imagens/hero-alimentos-variedade.jpeg',
    'assets/imagens/asset 12.png': 'assets/imagens/maquina-empacotamento.png',
    'assets/imagens/asset 13.png': 'assets/imagens/interior-armazem.png',
    'assets/imagens/asset 14.png': 'assets/imagens/estoque-sacarias.png',
    'assets/imagens/hero_bg.png': 'assets/imagens/hero-banner.png',
    'assets/imagens/company_img1.png': 'assets/imagens/empresa-instalacao-1.png',
    'assets/imagens/company_img2.png': 'assets/imagens/empresa-instalacao-2.png',
    'assets/imagens/company_img3.png': 'assets/imagens/empresa-instalacao-3.png',
}


def slugify(name: str) -> str:
    name = name.lower()
    name = unicodedata.normalize('NFKD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name or 'produto'


def update_product_html():
    """Atualiza src das imagens de produto nas páginas de categoria."""
    pair_renames = []  # (old_rel, new_rel) na ordem de aparição
    html_updates = 0

    for fname, folder in CATEGORIES.items():
        path = BASE / fname
        html = path.read_text(encoding='utf-8')
        grid_m = re.search(r'(<!-- Products Grid -->)(.*?)(<!-- Footer -->)', html, re.S)
        if not grid_m:
            print(f'AVISO: grid não encontrado em {fname}')
            continue

        prefix, grid, suffix = grid_m.group(1), grid_m.group(2), grid_m.group(3)
        used_slugs: dict[str, int] = {}

        def repl_img(m: re.Match) -> str:
            nonlocal html_updates
            src = m.group(1)
            alt = m.group(2)
            rest = m.group(3)
            ext = Path(src).suffix.lower()
            slug = slugify(alt)
            if slug in used_slugs:
                used_slugs[slug] += 1
                slug = f'{slug}-{used_slugs[slug]}'
            else:
                used_slugs[slug] = 1
            new_rel = f'{folder}/{slug}{ext}'
            pair_renames.append((src, new_rel))
            html_updates += 1
            return f'<img src="{new_rel}" alt="{alt}"{rest}>'

        new_grid = re.sub(r'<img src="([^"]+)" alt="([^"]+)"([^>]*)>', repl_img, grid)
        if new_grid != grid:
            path.write_text(html[:grid_m.start(2)] + new_grid + html[grid_m.end(2):], encoding='utf-8')

    print(f'HTML produtos: {html_updates} imagens atualizadas')
    return pair_renames


def apply_file_renames(pair_renames: list[tuple[str, str]]):
    """Renomeia/copia arquivos de produto no disco."""
    by_old: dict[str, list[str]] = defaultdict(list)
    for old, new in pair_renames:
        if new not in by_old[old]:
            by_old[old].append(new)

    renamed = copied = missing = 0
    for old_rel, new_rels in by_old.items():
        old_abs = BASE / old_rel
        if not old_abs.exists():
            print(f'FALTANDO: {old_rel}')
            missing += 1
            continue

        first_abs = BASE / new_rels[0]
        first_abs.parent.mkdir(parents=True, exist_ok=True)

        if old_abs.resolve() != first_abs.resolve():
            if not first_abs.exists():
                shutil.move(str(old_abs), str(first_abs))
                renamed += 1

        for nr in new_rels[1:]:
            dest = BASE / nr
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copy2(str(first_abs), str(dest))
                copied += 1

    print(f'Arquivos: {renamed} renomeados, {copied} copiados, {missing} ausentes')


def apply_static_renames():
    for old_rel, new_rel in STATIC_RENAMES.items():
        old_abs = BASE / old_rel
        new_abs = BASE / new_rel
        if old_abs.exists() and not new_abs.exists():
            new_abs.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_abs), str(new_abs))
            print(f'estático: {old_rel} -> {new_rel}')


def replace_in_text_files(replacements: dict[str, str]):
    text_exts = {'.html', '.js', '.css', '.py', '.json'}
    for fpath in BASE.rglob('*'):
        if fpath.suffix not in text_exts or fpath.name == 'rename_images.py':
            continue
        content = fpath.read_text(encoding='utf-8', errors='ignore')
        orig = content
        for old, new in sorted(replacements.items(), key=lambda x: -len(x[0])):
            content = content.replace(old, new)
        if content != orig:
            fpath.write_text(content, encoding='utf-8')
            print(f'refs: {fpath.relative_to(BASE)}')


def main():
    pair_renames = update_product_html()
    apply_file_renames(pair_renames)
    apply_static_renames()

    # Substituições globais apenas para assets estáticos (produtos já atualizados no HTML)
    replace_in_text_files(STATIC_RENAMES)

    remaining = list(BASE.rglob('asset *'))
    remaining = [p for p in remaining if p.is_file()]
    if remaining:
        print(f'\nAinda com nome genérico ({len(remaining)} arquivos):')
        for p in sorted(remaining)[:20]:
            print(f'  {p.relative_to(BASE)}')
        if len(remaining) > 20:
            print(f'  ... e mais {len(remaining) - 20}')


if __name__ == '__main__':
    main()
