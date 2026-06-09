#!/usr/bin/env python3
"""CTAs: formulário no lugar de WhatsApp disperso; mapa GMB; footer com único WhatsApp."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent

WA_FOOTER = (
    'https://wa.me/554136687866?text='
    'Ol%C3%A1%21%20Vim%20pelo%20site%20da%20Luzago%20Alimentos%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es.'
)
MAP_EMBED = (
    'https://maps.google.com/maps?q=Luzago+Alimentos'
    '&cid=8370212234163883768&hl=pt-BR&z=10&output=embed'
)
MAP_GMB = 'https://www.google.com/maps/place/?cid=8370212234163883768'

FOOTER_CONTACT_OLD = re.compile(
    r'<div class="w-full md:text-center text-sm">\s*'
    r'<p class="mb-1 flex items-center md:justify-center gap-2"><i class="fa-solid fa-phone"></i> \(41\) 3668-7866</p>\s*'
    r'<p class="(?:flex|mb-4 flex) items-center md:justify-center gap-2"><i class="fa-solid fa-envelope"></i> sac@luzagoalimentos\.com\.br</p>\s*'
    r'(?:<a href="https://wa\.me/[^"]*"[^>]*>.*?</a>\s*)?'
    r'</div>',
    re.S,
)

FOOTER_CONTACT_NEW = f'''                <div class="w-full md:text-center text-sm">
                    <p class="mb-1 flex items-center md:justify-center gap-2"><i class="fa-solid fa-phone"></i> (41) 3668-7866</p>
                    <p class="mb-4 flex items-center md:justify-center gap-2"><i class="fa-solid fa-envelope"></i> sac@luzagoalimentos.com.br</p>
                    <a href="{WA_FOOTER}" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 bg-[#25D366] hover:bg-[#20bd5a] text-white font-bold py-2.5 px-5 rounded transition text-sm">
                        <i class="fa-brands fa-whatsapp text-lg" aria-hidden="true"></i> Fale no WhatsApp
                    </a>
                </div>'''

FLOATING_WA = re.compile(
    r'\s*(?:<!-- WhatsApp \(estilo Joinchat\) -->\s*)?'
    r'<a[^>]*class="luzago-wa-widget"[^>]*>[\s\S]*?</a>\s*',
)

EMPRESA_WA_BTN = re.compile(
    r'<a href="/contato/" target="_blank" rel="noopener" '
    r'class="bg-luzago-green-dark text-white font-bold py-3 px-8 rounded shadow-md '
    r'hover:bg-luzago-green transition flex items-center gap-2 uppercase text-sm">\s*'
    r'<i class="fa-brands fa-whatsapp text-lg"></i> ENTRAR EM CONTATO\s*</a>',
    re.S,
)

EMPRESA_WA_BTN_NEW = '<a href="/contato/" class="btn btn--primary">Solicite orçamento</a>'

TOPBAR_WA_ICON = re.compile(
    r'\s*<a href="https://wa\.me/[^"]*" target="_blank" rel="noopener" '
    r'aria-label="WhatsApp Luzago" class="hover:opacity-80 transition">'
    r'<i class="fa-brands fa-whatsapp text-2xl text-green-400"></i></a>',
)

TOPBAR_SOCIAL_WA = re.compile(
    r'\s*<a href="https://wa\.me/[^"]*" target="_blank" rel="noopener" '
    r'aria-label="WhatsApp Luzago" class="w-8 h-8 rounded-full bg-white text-luzago-green-dark '
    r'flex items-center justify-center hover:bg-gray-200 transition">'
    r'<i class="fa-brands fa-whatsapp text-sm"></i></a>',
)

FOOTER_SOCIAL_WA = re.compile(
    r'\s*<a href="https://wa\.me/[^"]*" target="_blank" rel="noopener" '
    r'aria-label="WhatsApp Luzago" class="w-8 h-8 rounded-full bg-luzago-green text-white '
    r'flex items-center justify-center hover:bg-luzago-green-dark transition">'
    r'<i class="fa-brands fa-whatsapp text-sm"></i></a>',
)

URGENCY_WA = re.compile(
    r'\s*<a href="https://wa\.me/[^"]*" target="_blank" rel="noopener" '
    r'class="text-gray-500 text-xs hover:text-luzago-green transition">Urgência\? WhatsApp comercial</a>',
)

PREFERE_WA = re.compile(
    r'\s*<a href="https://wa\.me/[^"]*" target="_blank" rel="noopener" '
    r'class="text-white/80 text-sm hover:text-white transition underline underline-offset-4">\s*'
    r'Prefere WhatsApp\? Clique aqui\s*</a>',
    re.S,
)

CONSULTOR_WA = re.compile(
    r'href="https://wa\.me/554136687866\?text=[^"]*"([^>]*class="btn btn--secondary">Falar com Consultor</a>)',
)

MAP_IFRAME_SRC = re.compile(
    r'src="https://maps\.google\.com/maps\?[^"]*"',
)

MAP_CAPTION_OLD = re.compile(
    r'(<div class="bg-luzago-green-dark text-white text-center py-3 text-sm">)\s*'
    r'<a href="https://www\.google\.com/maps/place/\?cid=8370212234163883768"[^>]*>.*?</a>\s*'
    r'</div>',
    re.S,
)

MAP_CAPTION_NEW = f'''<div class="bg-luzago-green-dark text-white text-center py-4 text-sm px-4">
            <p class="font-semibold text-base mb-1">Atendemos Curitiba e Região Metropolitana</p>
            <a href="{MAP_GMB}" target="_blank" rel="noopener" class="hover:underline inline-flex items-center justify-center gap-2">
                <i class="fa-solid fa-location-dot"></i> Ver no Google Meu Negócio — Rua Alto Paraná, 1645, Pinhais - PR
            </a>
        </div>'''


def patch_content(content: str, path: Path) -> str:
    content = content.replace('    <link rel="stylesheet" href="/css/whatsapp-widget.css">\n', '')
    content = FLOATING_WA.sub('\n', content)
    content = TOPBAR_WA_ICON.sub('', content)
    content = TOPBAR_SOCIAL_WA.sub('', content)
    content = FOOTER_SOCIAL_WA.sub('', content)
    content = FOOTER_CONTACT_OLD.sub(FOOTER_CONTACT_NEW, content)
    content = URGENCY_WA.sub('', content)
    content = PREFERE_WA.sub('', content)
    content = CONSULTOR_WA.sub(r'href="/contato/"\1', content)
    content = EMPRESA_WA_BTN.sub(EMPRESA_WA_BTN_NEW, content)
    content = MAP_IFRAME_SRC.sub(f'src="{MAP_EMBED}"', content)
    content = MAP_CAPTION_OLD.sub(MAP_CAPTION_NEW, content)

    # Mapa home: altura e título
    content = content.replace('class="h-[400px] w-full bg-gray-200 relative"', 'class="h-[450px] w-full bg-gray-200 relative"')
    content = content.replace(
        'title="Luzago Alimentos no Google Maps"',
        'title="Luzago Alimentos — Curitiba e Região Metropolitana"',
    )
    content = content.replace(
        'title="Localização Luzago Alimentos"',
        'title="Luzago Alimentos — Curitiba e Região Metropolitana"',
    )

    # Home: hero e seção empresa → formulário na própria página
    if path.name == 'index.html' and path.parent == BASE:
        content = content.replace(
            '<a href="/contato/" class="btn btn--primary">\n                    Solicite seu orçamento\n                </a>',
            '<a href="#orcamento" class="btn btn--primary">\n                    Solicite seu orçamento\n                </a>',
        )
        content = content.replace(
            '<a href="/contato/" class="btn btn--primary">Solicite orçamento</a>',
            '<a href="#orcamento" class="btn btn--primary">Solicite orçamento</a>',
        )
        content = content.replace(
            '<a href="/contato/" class="btn btn--primary btn--sm">Solicite orçamento</a>',
            '<a href="#orcamento" class="btn btn--primary btn--sm">Solicite orçamento</a>',
        )

    # Demais wa.me → formulário de contato
    content = re.sub(
        r'href="https://wa\.me/[^"]*"',
        'href="/contato/"',
        content,
    )

    # Restaurar único WhatsApp no footer
    content = content.replace(
        'href="/contato/" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 bg-[#25D366]',
        f'href="{WA_FOOTER}" target="_blank" rel="noopener" class="inline-flex items-center justify-center gap-2 bg-[#25D366]',
    )

    return content


def main() -> None:
    count = 0
    for html in sorted(BASE.rglob('index.html')):
        if '.vercel' in html.parts:
            continue
        original = html.read_text(encoding='utf-8')
        updated = patch_content(original, html)
        if updated != original:
            html.write_text(updated, encoding='utf-8')
            print(f'Atualizado: {html.relative_to(BASE)}')
            count += 1
    print(f'Concluído: {count} arquivo(s).')


if __name__ == '__main__':
    main()
