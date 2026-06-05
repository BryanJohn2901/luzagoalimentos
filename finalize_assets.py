#!/usr/bin/env python3
"""Renomeia assets órfãos, completa cereais e garante alt em todas as imagens."""
import hashlib
import re
import shutil
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent

CEREAIS_NEW = [
    (17, 'Feijão Branco Argentino', '500g | Saca'),
    (18, 'Feijão Carioca Tipo 01 Fardo', '1Kg | 30Kg'),
    (19, 'Feijão Cavalo', '1Kg'),
    (20, 'Feijão Fradinho', '500g | 1Kg'),
    (21, 'Feijão Preto Tipo 01 Fardo', '1Kg | 30Kg'),
    (22, 'Gergelim Branco sem Casca', 'Saca'),
    (23, 'Gergelim Preto', 'Saca'),
    (24, 'Gergelim Torrado', 'Saca'),
    (25, 'Girassol Pepita sem Casca', '100g | 1Kg'),
    (26, 'Goma de Tapioca Hidratada (Massa Pronta)', '1Kg'),
    (27, 'Grão de Bico 12mm', '1Kg | Saca'),
    (28, 'Grão de Bico 9mm', '500g | 1Kg | 25Kg'),
    (29, 'Lentilha Canadense', '500g | 1Kg | 25Kg'),
    (30, 'Linhaça Dourada', '100g | 1Kg | Saca'),
    (31, 'Linhaça Marrom', 'Saca | 1Kg'),
    (32, 'Pipoca Americana', '1Kg'),
    (33, 'Proteína de Soja Caramelo (PTS)', '1Kg | Saca'),
    (34, 'Proteína de Soja Natural (PTS)', '1Kg'),
    (35, 'Quinoa em Grão', '100g | 1Kg | Saca'),
    (36, 'Quinoa Mista', '1Kg'),
    (37, 'Quinoa Preta em Grão', '1Kg'),
    (38, 'Quinoa Vermelha em Grão', '1Kg'),
    (39, 'Semente de Abóbora', '100g | 1Kg'),
    (40, 'Soja em Grão', '500g | 1Kg | Saca'),
    (41, 'Trigo em Grão', '1Kg | Saca'),
]

ICON_RENAMES = {
    'assets/icones/asset 0.svg': 'assets/icones/icone-usuario.svg',
    'assets/icones/asset 15.svg': 'assets/icones/icone-estrela.svg',
    'assets/icones/asset 16.svg': 'assets/icones/icone-estrela-meia.svg',
    'assets/icones/asset 18.svg': 'assets/icones/icone-google-colorido.svg',
    'assets/icones/asset 21.png': 'assets/icones/favicon-luzago.png',
    'assets/icones/asset 22.png': 'assets/icones/notificacao-copia-sucesso.png',
    'assets/icones/asset 23.png': 'assets/icones/notificacao-generica.png',
    'assets/icones/asset 24.svg': 'assets/icones/icone-whatsapp.svg',
    'assets/icones/asset 25.svg': 'assets/icones/icone-facebook.svg',
    'assets/icones/asset 26.svg': 'assets/icones/icone-linkedin.svg',
    'assets/icones/asset 27.svg': 'assets/icones/icone-instagram.svg',
    'assets/icones/asset 28.svg': 'assets/icones/icone-seta-dropdown.svg',
    'assets/icones/asset 29.svg': 'assets/icones/icone-menu-abrir.svg',
    'assets/icones/asset 30.svg': 'assets/icones/icone-menu-fechar.svg',
    'assets/icones/asset 31.svg': 'assets/icones/categoria-temperos-alt.svg',
    'assets/icones/asset 32.svg': 'assets/icones/categoria-cereais-alt.svg',
    'assets/icones/asset 33.svg': 'assets/icones/icone-telefone.svg',
    'assets/icones/asset 34.svg': 'assets/icones/icone-email.svg',
    'assets/icones/asset 35.svg': 'assets/icones/icone-localizacao.svg',
    'assets/icones/asset 36.svg': 'assets/icones/categoria-conservas-alt.svg',
    'assets/icones/asset 37.svg': 'assets/icones/icone-setas.svg',
    'assets/icones/asset 38.svg': 'assets/icones/categoria-food-service-alt.svg',
    'assets/icones/asset 43.png': 'assets/icones/overlay-preto.png',
    'assets/icones/asset 44.png': 'assets/icones/overlay-preto-2.png',
}

IMAGEM_RENAMES = {
    'assets/imagens/asset 1.jpeg': 'assets/imagens/avatar-padrao-1.jpeg',
    'assets/imagens/asset 2.jpeg': 'assets/imagens/avatar-padrao-2.jpeg',
    'assets/imagens/asset 42.jpeg': 'assets/imagens/moldura-vegetais-frescos.jpeg',
    'assets/Refrescos e Sobremesas/asset 22.jpeg': 'assets/Refrescos e Sobremesas/reserva-refresco.jpeg',
    'assets/cereais/asset 42.jpeg': 'assets/cereais/trigo-em-grao-variacao.jpeg',
}


def slugify(name: str) -> str:
    name = name.lower()
    name = unicodedata.normalize('NFKD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r'[^a-z0-9]+', '-', name)
    return re.sub(r'-+', '-', name).strip('-') or 'produto'


def md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def rename_on_disk(mapping: dict[str, str]) -> None:
    for old_rel, new_rel in mapping.items():
        old = BASE / old_rel
        new = BASE / new_rel
        if not old.exists():
            continue
        if new.exists() and md5(old) == md5(new):
            old.unlink()
            print(f'removido duplicata: {old_rel}')
            continue
        new.parent.mkdir(parents=True, exist_ok=True)
        if not new.exists():
            shutil.move(str(old), str(new))
            print(f'renomeado: {old_rel} -> {new_rel}')


def rename_cereais() -> dict[str, str]:
    folder = BASE / 'assets/cereais'
    replacements = {}
    grao_bico_12 = None

    for num, name, _sizes in CEREAIS_NEW:
        old = folder / f'asset {num}.jpeg'
        slug = slugify(name)
        new_rel = f'assets/cereais/{slug}.jpeg'
        new = BASE / new_rel
        if not old.exists():
            print(f'AVISO cereais ausente: asset {num}.jpeg')
            continue
        if num == 27:
            grao_bico_12 = new
        if num == 28 and grao_bico_12 and grao_bico_12.exists():
            if not new.exists():
                shutil.copy2(grao_bico_12, new)
            old.unlink()
            print(f'copiado grao-de-bico-9mm a partir de 12mm')
        else:
            if not new.exists():
                shutil.move(str(old), str(new))
            else:
                old.unlink()
        replacements[f'assets/cereais/asset {num}.jpeg'] = new_rel

    return replacements


def product_card(src: str, name: str, sizes: str) -> str:
    return f'''
                <div class="bg-white rounded-xl shadow-md p-6 flex flex-col items-center text-center border border-gray-100 hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
                    <div class="w-24 h-24 md:w-32 md:h-32 rounded-full overflow-hidden mb-6 border-4 border-gray-100 bg-gray-50 flex items-center justify-center shadow-inner">
                        <img src="{src}" alt="{name}" class="w-full h-full object-cover">
                    </div>
                    <h3 class="text-lg font-bold text-luzago-green-dark mb-4">{name}</h3>
                    <div class="mt-auto w-full">
                        <p class='text-xs text-gray-500 font-bold mb-1 uppercase tracking-wider'>DISPONÍVEL EM:</p><p class='text-sm text-gray-700 font-semibold'>{sizes}</p>
                    </div>
                </div>
'''


def append_cereais_products() -> None:
    path = BASE / 'cereais' / 'index.html'
    html = path.read_text(encoding='utf-8')
    cards = []
    for _num, name, sizes in CEREAIS_NEW:
        src = f'assets/cereais/{slugify(name)}.jpeg'
        cards.append(product_card(src, name, sizes))

    marker = '\n            </div>\n            \n            <div class="mt-12 text-center border-t border-gray-200 pt-8">'
    if 'feijao-branco-argentino.jpeg' in html:
        print('cereais/index.html já contém produtos extras')
        return
    if marker not in html:
        raise RuntimeError('Marcador não encontrado em cereais/index.html')
    html = html.replace(marker, ''.join(cards) + marker, 1)
    path.write_text(html, encoding='utf-8')
    print(f'Adicionados {len(cards)} produtos em cereais/index.html')


def remove_duplicate_orphans() -> None:
    named_hashes: dict[str, Path] = {}
    for p in BASE.rglob('*'):
        if p.is_file() and 'asset ' not in p.name and p.suffix.lower() in {
            '.jpeg', '.jpg', '.png', '.svg', '.webp'
        }:
            named_hashes[md5(p)] = p

    for p in list(BASE.rglob('asset *')):
        if not p.is_file():
            continue
        h = md5(p)
        if h in named_hashes:
            p.unlink()
            print(f'removido duplicata: {p.relative_to(BASE)}')


def cleanup_frutas_orphans() -> None:
    folder = BASE / 'assets/Frutas Secas e Castanhas'
    icon_hashes = {md5(p) for p in (BASE / 'assets/icones').glob('*') if p.is_file()}
    imagem_hashes = {md5(p) for p in (BASE / 'assets/imagens').glob('*') if p.is_file()}

    for p in folder.glob('asset *'):
        if not p.is_file():
            continue
        h = md5(p)
        if h in icon_hashes or h in imagem_hashes:
            p.unlink()
            print(f'removido cópia de ícone/imagem: {p.name}')
        elif p.suffix.lower() in {'.svg', '.png'}:
            p.unlink()
            print(f'removido svg/png órfão: {p.name}')
        elif p.suffix.lower() in {'.jpeg', '.jpg'}:
            p.rename(folder / 'avatar-placeholder-frutas.jpeg')
            print('renomeado avatar placeholder em frutas secas')


def fix_alt_attributes() -> None:
    alt_fixes = {
        'assets/icones/icone-verificado.svg" class="w-3 h-3"':
            'assets/icones/icone-verificado.svg" alt="Conta verificada no Google" class="w-3 h-3"',
        'alt="Luzago no Instagram" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">\n                    <div class="absolute inset-0 bg-black/20':
            '',  # handled individually below
    }

    index = BASE / 'index.html'
    html = index.read_text(encoding='utf-8')

    html = html.replace(
        '<img src="assets/icones/icone-verificado.svg" class="w-3 h-3">',
        '<img src="assets/icones/icone-verificado.svg" alt="Conta verificada no Google" class="w-3 h-3">',
    )

    instagram_alts = [
        ('hero-vegetais.png" alt="Luzago no Instagram"', 'hero-vegetais.png" alt="Produtos e fachada Luzago Alimentos no Instagram"'),
        ('interior-armazem.png" alt="Luzago no Instagram"', 'interior-armazem.png" alt="Interior do armazém Luzago no Instagram"'),
        ('estoque-sacarias.png" alt="Luzago no Instagram"', 'estoque-sacarias.png" alt="Estoque de sacarias Luzago no Instagram"'),
        ('maquina-empacotamento.png" alt="Luzago no Instagram"', 'maquina-empacotamento.png" alt="Linha de empacotamento Luzago no Instagram"'),
        ('hero-alimentos-variedade.jpeg" alt="Luzago no Instagram"', 'hero-alimentos-variedade.jpeg" alt="Variedade de alimentos Luzago no Instagram"'),
    ]
    for old, new in instagram_alts:
        html = html.replace(old, new)

    index.write_text(html, encoding='utf-8')

    for html_path in BASE.glob('*.html'):
        content = html_path.read_text(encoding='utf-8')
        orig = content

        def add_alt(match: re.Match) -> str:
            tag = match.group(0)
            if re.search(r'\balt\s*=', tag, re.I):
                return tag
            src_m = re.search(r'src="([^"]+)"', tag)
            if not src_m:
                return tag
            src = src_m.group(1)
            filename = Path(src).stem.replace('-', ' ').replace('_', ' ')
            alt = filename.title()
            if 'logo-luzago' in src:
                alt = 'Luzago Alimentos'
            elif 'icone-folha' in src:
                alt = 'Ícone folha Luzago'
            elif 'icone-google' in src:
                alt = 'Google'
            elif 'icone-verificado' in src:
                alt = 'Conta verificada no Google'
            elif 'categoria-' in src:
                alt = filename.replace('categoria ', '').replace(' alt', '').title()
            return tag.replace('<img ', f'<img alt="{alt}" ', 1)

        content = re.sub(r'<img\b[^>]*>', add_alt, content)
        if content != orig:
            html_path.write_text(content, encoding='utf-8')
            print(f'alt revisado: {html_path.name}')


def main():
    rename_cereais()
    rename_on_disk({**ICON_RENAMES, **IMAGEM_RENAMES})
    remove_duplicate_orphans()
    cleanup_frutas_orphans()
    append_cereais_products()
    fix_alt_attributes()

    remaining = list(BASE.rglob('asset *'))
    remaining = [p for p in remaining if p.is_file()]
    print(f'\nArquivos genéricos restantes: {len(remaining)}')
    for p in sorted(remaining)[:15]:
        print(f'  {p.relative_to(BASE)}')


if __name__ == '__main__':
    main()
