import re
import os
import glob

# 1. Parse raw text
products = []
with open('raw_text.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

current_product = None
for i, line in enumerate(lines):
    if line == "DISPONÍVEL EM:":
        continue
    elif i > 0 and lines[i-1] == "DISPONÍVEL EM:":
        # This line is sizes
        if current_product:
            current_product["sizes"] = line
    else:
        # This is a new product
        current_product = {"name": line, "sizes": ""}
        products.append(current_product)

# 2. Get and sort images
image_files = glob.glob('assets/temperos/asset *.*')
# Sort by the integer number in "asset XX.ext"
def get_num(filename):
    match = re.search(r'asset (\d+)\.', filename)
    return int(match.group(1)) if match else 0

image_files.sort(key=get_num)

# Map images
for i, p in enumerate(products):
    img_idx = min(i, len(image_files) - 1)
    p["image"] = image_files[img_idx]

# 3. Read base template
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

header_match = re.search(r'(?s)(<!DOCTYPE html>.*?</header>)', content)
header = header_match.group(1) if header_match else ""

# Modify header style to include the hero-bg
style_insertion = """
        .temperos-hero-bg {
            background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)), url('assets/asset 40.jpeg');
            background-size: cover;
            background-position: center;
        }
"""
header = header.replace('</style>', style_insertion + '    </style>')

footer_match = re.search(r'(?s)(<!-- Footer -->.*)', content)
footer = footer_match.group(1) if footer_match else ""

# 4. Generate specific content
hero_section = """
    <!-- Hero -->
    <section class="temperos-hero-bg h-[300px] md:h-[400px] flex items-center justify-center text-center px-4 relative mt-[72px] md:mt-0">
        <div class="flex flex-col items-center">
            <img src="assets/asset 5.svg" alt="Temperos e Condimentos" class="w-12 h-12 md:w-16 md:h-16 mb-4 object-contain invert">
            <h1 class="text-4xl md:text-5xl font-bold text-white tracking-wide">Temperos e Condimentos</h1>
        </div>
    </section>
"""

grid_items_html = ""
for p in products:
    img_src = p['image']
    sizes_html = f"<p class='text-xs text-gray-500 font-bold mb-1 uppercase tracking-wider'>DISPONÍVEL EM:</p><p class='text-sm text-gray-700 font-semibold'>{p['sizes']}</p>" if p['sizes'] else "<p class='text-sm text-gray-500 italic mt-4'>Sob consulta</p>"
    
    # We create the card design
    card = f"""
                <div class="bg-white rounded-xl shadow-md p-6 flex flex-col items-center text-center border border-gray-100 hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
                    <div class="w-24 h-24 md:w-32 md:h-32 rounded-full overflow-hidden mb-6 border-4 border-gray-100 bg-gray-50 flex items-center justify-center shadow-inner">
                        <img src="{img_src}" alt="{p['name']}" class="w-full h-full object-cover">
                    </div>
                    <h3 class="text-lg font-bold text-luzago-green-dark mb-4">{p['name']}</h3>
                    <div class="mt-auto w-full">
                        {sizes_html}
                    </div>
                </div>
    """
    grid_items_html += card

main_content = f"""
    <!-- Products Grid -->
    <section class="py-16 bg-gray-50">
        <div class="container mx-auto px-4 max-w-6xl">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {grid_items_html}
            </div>
        </div>
    </section>
"""

page_content = header + hero_section + main_content + footer

with open('temperos-e-condimentos.html', 'w', encoding='utf-8') as out:
    out.write(page_content)

print("Generated temperos-e-condimentos.html successfully with {} products.".format(len(products)))
