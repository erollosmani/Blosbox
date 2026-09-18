import os
import re

def parse_translations_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    languages = ['en', 'fr', 'de', 'it', 'sv', 'nl', 'sq', 'mk']
    translations_dict = {lang: {} for lang in languages}
    
    lang_starts = list(re.finditer(r'^\s*([a-z]{2})\s*:\s*\{', content, re.MULTILINE))
    for i, m in enumerate(lang_starts):
        lang = m.group(1)
        if lang not in languages:
            continue
        start_pos = m.end()
        end_pos = lang_starts[i+1].start() if i + 1 < len(lang_starts) else content.rfind('};')
        block = content[start_pos:end_pos]
        
        kv_pattern = r'([a-zA-Z0-9_]+)\s*:\s*(?:"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\')'
        for kv in re.finditer(kv_pattern, block):
            key = kv.group(1)
            val = kv.group(2) if kv.group(2) is not None else kv.group(3)
            val = val.replace('\\"', '"').replace("\\'", "'")
            translations_dict[lang][key] = val
                
    return translations_dict

def get_page_key(filename):
    raw_key = filename.replace('.html', '').lower().replace('-', '_')
    return 'home' if raw_key == 'index' else raw_key

def add_asset_prefix(html_content):
    # Fix paths for assets when page is located inside subfolder like `/de/`
    html_content = re.sub(r'href="styles\.css(\?v=\d+)?"', r'href="../styles.css\1"', html_content)
    html_content = re.sub(r'href="calculator\.css(\?v=\d+)?"', r'href="../calculator.css\1"', html_content)
    html_content = re.sub(r'src="translations\.js(\?v=\d+)?"', r'src="../translations.js\1"', html_content)
    html_content = re.sub(r'src="i18n\.js(\?v=\d+)?"', r'src="../i18n.js\1"', html_content)
    html_content = re.sub(r'src="script\.js(\?v=\d+)?"', r'src="../script.js\1"', html_content)
    html_content = re.sub(r'src="calculator\.js(\?v=\d+)?"', r'src="../calculator.js\1"', html_content)
    
    html_content = re.sub(r'href="Logo%20FAV%20Icon\.(png|webp)"', r'href="../Logo%20FAV%20Icon.webp"', html_content)
    html_content = re.sub(r'href="Logo FAV Icon\.(png|webp)"', r'href="../Logo%20FAV%20Icon.webp"', html_content)
    html_content = re.sub(r'src="Logo\.(png|webp)"', r'src="../Logo.webp"', html_content)
    html_content = re.sub(r'src="Logo%20FAV%20Icon\.(png|webp)"', r'src="../Logo%20FAV%20Icon.webp"', html_content)
    html_content = re.sub(r'src="Logo FAV Icon\.(png|webp)"', r'src="../Logo%20FAV%20Icon.webp"', html_content)
    html_content = re.sub(r'src="Son%20and%20Father\.(png|webp)"', r'src="../Son%20and%20Father.webp"', html_content)
    html_content = re.sub(r'src="Son and Father\.(png|webp)"', r'src="../Son and Father.webp"', html_content)
    html_content = re.sub(r'src="Blosbox%20main\.(jpeg|jpg|webp)"', r'src="../Blosbox%20main.webp"', html_content)
    html_content = re.sub(r'src="Blosbox main\.(jpeg|jpg|webp)"', r'src="../Blosbox main.webp"', html_content)
    html_content = re.sub(r'src="BlosBox%20Handcrafting\.(jpeg|jpg|webp)"', r'src="../BlosBox%20Handcrafting.webp"', html_content)
    html_content = re.sub(r'src="BlosBox Handcrafting\.(jpeg|jpg|webp)"', r'src="../BlosBox Handcrafting.webp"', html_content)
    
    root_assets = [
        'combine_these_boxes_202604262144.webp',
        'combine_these_boxes_202604262144.jpeg',
        'Blosbox-Jewellery-Pricelist.pdf',
        'Proposal ring box technical drawing.jpg',
        'Proposal ring box tecnical drawing.jpg',
        'R3 Ring Box technical drawing.jpg',
        'Texhnical drawing Lid and Base Type.jpg',
        'Texhnical drawing R3, RLux and Watch box type.jpg',
        'Watch box tecnical drawing.jpg'
    ]
    for asset in root_assets:
        encoded = asset.replace(' ', '%20')
        for a in {asset, encoded}:
            html_content = re.sub(r'src="' + re.escape(a) + r'"', f'src="../{a}"', html_content)
            html_content = re.sub(r'href="' + re.escape(a) + r'"', f'href="../{a}"', html_content)
            html_content = re.sub(r'"' + re.escape(a) + r'"', f'"../{a}"', html_content)

    dirs = [
        'Jewellery', 'Chocolates', 'Watches', 'Leather%20Goods', 'Leather Goods',
        'Cosmetics', 'Corporate%20Gifts', 'Corporate Gifts', 'Catalogue',
        'Textured', 'Pearl', 'Luxe', 'Planning',
        'Printing Foil Embossing', 'Printing%20Foil%20Embossing',
        'Bespoke design & prototyping', 'Bespoke%20design%20%26%20prototyping',
        'Size and Material Customization', 'Size%20and%20Material%20Customization',
        'Other', 'Inserts', 'About Us', 'About%20Us', 'Insights'
    ]
    for d in dirs:
        html_content = re.sub(r'src="' + d + r'/', r'src="../' + d + r'/', html_content)
        html_content = re.sub(r'href="' + d + r'/', r'href="../' + d + r'/', html_content)
        html_content = re.sub(r'"' + d + r'/', r'"../' + d + r'/', html_content)
        
    return html_content

def update_hreflang_and_canonical(html_content, lang, filename):
    base_url = "https://www.blosbox.com"
    
    html_content = re.sub(r'^[ \t]*<link rel="canonical"[^>]*>\r?\n?', '', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^[ \t]*<link rel="alternate" hreflang="[^"]*"[^>]*>\r?\n?', '', html_content, flags=re.MULTILINE)
    
    if filename == 'index.html':
        canonical_url = f"{base_url}/" if lang == 'en' else f"{base_url}/{lang}/"
        en_url = f"{base_url}/"
        de_url = f"{base_url}/de/"
        fr_url = f"{base_url}/fr/"
        it_url = f"{base_url}/it/"
        sv_url = f"{base_url}/sv/"
        nl_url = f"{base_url}/nl/"
        sq_url = f"{base_url}/sq/"
        mk_url = f"{base_url}/mk/"
        x_default = f"{base_url}/"
    else:
        canonical_url = f"{base_url}/{filename}" if lang == 'en' else f"{base_url}/{lang}/{filename}"
        en_url = f"{base_url}/{filename}"
        de_url = f"{base_url}/de/{filename}"
        fr_url = f"{base_url}/fr/{filename}"
        it_url = f"{base_url}/it/{filename}"
        sv_url = f"{base_url}/sv/{filename}"
        nl_url = f"{base_url}/nl/{filename}"
        sq_url = f"{base_url}/sq/{filename}"
        mk_url = f"{base_url}/mk/{filename}"
        x_default = f"{base_url}/{filename}"
    
    hreflangs = [
        f'<link rel="canonical" href="{canonical_url}">',
        f'<link rel="alternate" hreflang="en" href="{en_url}">',
        f'<link rel="alternate" hreflang="de" href="{de_url}">',
        f'<link rel="alternate" hreflang="fr" href="{fr_url}">',
        f'<link rel="alternate" hreflang="it" href="{it_url}">',
        f'<link rel="alternate" hreflang="sv" href="{sv_url}">',
        f'<link rel="alternate" hreflang="nl" href="{nl_url}">',
        f'<link rel="alternate" hreflang="sq" href="{sq_url}">',
        f'<link rel="alternate" hreflang="mk" href="{mk_url}">',
        f'<link rel="alternate" hreflang="x-default" href="{x_default}">'
    ]
    
    hreflang_str = "\n    " + "\n    ".join(hreflangs) + "\n"

    # Insert prominently near top of head right after meta description (best practice for Googlebot)
    desc_match = re.search(r'(<meta\s+name=["\']description["\'][^>]*>)', html_content, re.IGNORECASE)
    if desc_match:
        html_content = html_content[:desc_match.end()] + hreflang_str + html_content[desc_match.end():]
    else:
        html_content = html_content.replace('</head>', f'{hreflang_str}</head>')

    # Clean up any accumulated multiple blank lines inside <head>
    head_match = re.search(r'(<head[^>]*>)(.*?)(</head>)', html_content, flags=re.DOTALL)
    if head_match:
        head_inner = head_match.group(2)
        cleaned_head_inner = re.sub(r'\n[ \t]*\n([ \t]*\n)+', '\n\n', head_inner)
        html_content = html_content[:head_match.start(2)] + cleaned_head_inner + html_content[head_match.end(2):]

    return html_content

def pre_render_html(base_html, lang, lang_dict, filename):
    content = base_html
    page_key = get_page_key(filename)
    
    content = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', content)

    locales = {
        'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'it': 'it_IT',
        'sv': 'sv_SE', 'nl': 'nl_NL', 'sq': 'sq_AL', 'mk': 'mk_MK'
    }
    target_locale = locales.get(lang, 'en_US')
    content = re.sub(r'<meta property="og:locale" content="[^"]*"', f'<meta property="og:locale" content="{target_locale}"', content)
    
    base_url = "https://www.blosbox.com"
    if filename == 'index.html':
        page_url = f"{base_url}/" if lang == 'en' else f"{base_url}/{lang}/"
    else:
        page_url = f"{base_url}/{filename}" if lang == 'en' else f"{base_url}/{lang}/{filename}"
    content = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{page_url}"', content)
    
    title_key = f'meta_title_{page_key}'
    if title_key in lang_dict:
        content = re.sub(r'<title>.*?</title>', f'<title>{lang_dict[title_key]}</title>', content, flags=re.DOTALL)
        content = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{lang_dict[title_key]}"', content)
        content = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{lang_dict[title_key]}"', content)
        
    desc_key = f'meta_desc_{page_key}'
    if desc_key in lang_dict:
        meta_desc_val = lang_dict[desc_key]
        content = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{meta_desc_val}"', content)
        content = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{meta_desc_val}"', content)
        content = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{meta_desc_val}"', content)

    def replace_i18n_node(match):
        full_tag = match.group(0)
        tag_name = match.group(1)
        attrs = match.group(2)
        inner_text = match.group(3)
        
        key_match = re.search(r'data-i18n="([^"]+)"', attrs)
        if not key_match:
            return full_tag
        key = key_match.group(1)
        
        if key in lang_dict:
            new_text = lang_dict[key]
            if '<span class="caret">' in inner_text:
                new_text = f'{new_text} <span class="caret">▾</span>'
            return f'<{tag_name}{attrs}>{new_text}</{tag_name}>'
        return full_tag

    pattern = r'<([a-zA-Z0-9]+)([^>]*?\bdata-i18n="[^"]+"[^>]*)>(.*?)</\1>'
    content = re.sub(pattern, replace_i18n_node, content, flags=re.DOTALL)
    
    def replace_i18n_input(match):
        full_tag = match.group(0)
        key_match = re.search(r'data-i18n="([^"]+)"', full_tag)
        if key_match and key_match.group(1) in lang_dict:
            key = key_match.group(1)
            new_placeholder = lang_dict[key]
            return re.sub(r'placeholder="[^"]*"', f'placeholder="{new_placeholder}"', full_tag)
        return full_tag
        
    content = re.sub(r'<(?:input|textarea)[^>]*\bdata-i18n="[^"]+"[^>]*>', replace_i18n_input, content)

    return content

def update_language_dropdown(html_content, current_lang, filename):
    # Update active language label in dropdown
    html_content = re.sub(r'<span id="activeLangLabel">.*?</span>', f'<span id="activeLangLabel">{current_lang.upper()}</span>', html_content)
    html_content = re.sub(r'<span id="mobileActiveLangLabel">.*?</span>', f'<span id="mobileActiveLangLabel">{current_lang.upper()}</span>', html_content)
    
    lang_names = [
        ('en', '🇬🇧 English'),
        ('fr', '🇫🇷 Français'),
        ('de', '🇩🇪 Deutsch'),
        ('it', '🇮🇹 Italiano'),
        ('sv', '🇸🇪 Svenska'),
        ('nl', '🇳🇱 Nederlands'),
        ('sq', '🇦🇱 Shqip'),
        ('mk', '🇲🇰 Македонски')
    ]
    
    items = []
    for code, label in lang_names:
        if current_lang == 'en':
            href = filename if code == 'en' else f"{code}/{filename}"
        else:
            if code == 'en':
                href = f"../{filename}"
            elif code == current_lang:
                href = filename
            else:
                href = f"../{code}/{filename}"
        active_cls = " active" if code == current_lang else ""
        items.append(f'<li><a href="{href}" class="lang-item{active_cls}" data-lang="{code}">{label}</a></li>')
    
    new_menu_inner = "\n                        " + "\n                        ".join(items) + "\n                    "
    
    pattern = r'(<ul class="dropdown-menu lang-dropdown-menu">)(.*?)(</ul>)'
    html_content = re.sub(pattern, rf'\1{new_menu_inner}\3', html_content, flags=re.DOTALL)
    return html_content

def generate_redirect_stubs(root_dir):
    redirect_map = [
        ('luxe.html', 'customization.html', 'Size & Material Customization'),
        ('pearl.html', 'customization.html', 'Size & Material Customization'),
        ('textured.html', 'customization.html', 'Size & Material Customization'),
        ('fashion.html', 'products.html', 'Products & Collections'),
        ('electronics.html', 'products.html', 'Products & Collections'),
        ('under-construction.html', '', 'Blosbox Luxury Packaging')
    ]
    
    languages = ['en', 'de', 'fr', 'it', 'sv', 'nl', 'sq', 'mk']
    base_url = "https://www.blosbox.com"
    
    for filename, target_rel, title in redirect_map:
        for lang in languages:
            if lang == 'en':
                dest_dir = root_dir
                target_url = f"{base_url}/{target_rel}" if target_rel else f"{base_url}/"
            else:
                dest_dir = os.path.join(root_dir, lang)
                os.makedirs(dest_dir, exist_ok=True)
                target_url = f"{base_url}/{lang}/{target_rel}" if target_rel else f"{base_url}/{lang}/"
            
            stub_content = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, follow">
    <meta http-equiv="refresh" content="0; url={target_url}">
    <link rel="canonical" href="{target_url}">
    <title>Redirecting - Blosbox Luxury Packaging</title>
    <script>
        window.location.replace("{target_url}" + window.location.search + window.location.hash);
    </script>
    <style>
        body {{
            font-family: 'Playfair Display', serif, system-ui;
            background-color: #f7f4ee;
            color: #2b2725;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }}
        a {{
            color: #8c6d46;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div>
        <p>Redirecting to <a href="{target_url}">{title}</a>...</p>
    </div>
</body>
</html>
"""
            out_path = os.path.join(dest_dir, filename)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(stub_content)
    print(f"Generated clean SEO redirect stubs across all 8 languages for legacy URLs ({len(redirect_map)} stubs x {len(languages)} langs = {len(redirect_map)*len(languages)} files)")

def main():
    root_dir = 'c:/Blosbox antigravity'
    translations_file = os.path.join(root_dir, 'translations.js')
    
    translations = parse_translations_js(translations_file)
    print("Parsed translations for languages:", list(translations.keys()))
    
    exclude_files = [
        '404.html', 'pricelist-catalog.html', 'under-construction.html',
        'luxe.html', 'pearl.html', 'textured.html', 'electronics.html', 'fashion.html'
    ]
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and not f.startswith('.') and f not in exclude_files]
    
    # 1. First, update root HTML files with clean canonical & hreflang tags
    for filename in html_files:
        src_path = os.path.join(root_dir, filename)
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = update_hreflang_and_canonical(content, 'en', filename)
        updated_content = update_language_dropdown(updated_content, 'en', filename)
        with open(src_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    print(f"Updated root HTML files ({len(html_files)} pages) with clean hreflang tags and language dropdowns")

    # 2. Generate localized static subfolders
    languages = ['de', 'fr', 'it', 'sv', 'nl', 'sq', 'mk']
    
    for lang in languages:
        lang_dir = os.path.join(root_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        for filename in html_files:
            src_path = os.path.join(root_dir, filename)
            with open(src_path, 'r', encoding='utf-8') as f:
                base_html = f.read()
                
            rendered_html = pre_render_html(base_html, lang, translations[lang], filename)
            rendered_html = add_asset_prefix(rendered_html)
            rendered_html = update_hreflang_and_canonical(rendered_html, lang, filename)
            rendered_html = update_language_dropdown(rendered_html, lang, filename)
            
            dest_path = os.path.join(lang_dir, filename)
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
                
        print(f"Generated static subfolder: /{lang}/ ({len(html_files)} pages)")

    # 3. Generate clean, SEO-compliant redirect stubs for legacy deleted URLs
    generate_redirect_stubs(root_dir)

if __name__ == '__main__':
    main()
