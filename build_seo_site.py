import os
import re

def parse_translations_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    languages = ['en', 'fr', 'de', 'it', 'sv', 'nl', 'sq', 'mk']
    translations_dict = {lang: {} for lang in languages}
    
    for lang in languages:
        pattern = r'\b' + lang + r'\s*:\s*\{([^}]+)\}'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            block = match.group(1)
            kv_pattern = r'([a-zA-Z0-9_]+)\s*:\s*(?:"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\')'
            for kv in re.finditer(kv_pattern, block):
                key = kv.group(1)
                val = kv.group(2) if kv.group(2) is not None else kv.group(3)
                val = val.replace('\\"', '"').replace("\\'", "'")
                translations_dict[lang][key] = val
                
    return translations_dict

def get_page_key(filename):
    raw_key = filename.replace('.html', '').lower()
    return 'home' if raw_key == 'index' else raw_key

def add_asset_prefix(html_content):
    # Fix paths for assets when page is located inside subfolder like `/de/`
    html_content = re.sub(r'href="styles\.css(\?v=\d+)?"', r'href="../styles.css\1"', html_content)
    html_content = re.sub(r'src="translations\.js(\?v=\d+)?"', r'src="../translations.js\1"', html_content)
    html_content = re.sub(r'src="i18n\.js(\?v=\d+)?"', r'src="../i18n.js\1"', html_content)
    html_content = re.sub(r'src="script\.js(\?v=\d+)?"', r'src="../script.js\1"', html_content)
    
    html_content = re.sub(r'href="Logo%20FAV%20Icon\.(png|webp)"', r'href="../Logo%20FAV%20Icon.webp"', html_content)
    html_content = re.sub(r'src="Logo\.(png|webp)"', r'src="../Logo.webp"', html_content)
    html_content = re.sub(r'src="Logo%20FAV%20Icon\.(png|webp)"', r'src="../Logo%20FAV%20Icon.webp"', html_content)
    html_content = re.sub(r'src="Son%20and%20Father\.(png|webp)"', r'src="../Son%20and%20Father.webp"', html_content)
    html_content = re.sub(r'src="Son and Father\.(png|webp)"', r'src="../Son and Father.webp"', html_content)
    html_content = re.sub(r'src="Blosbox%20main\.(jpeg|jpg|webp)"', r'src="../Blosbox%20main.webp"', html_content)
    html_content = re.sub(r'src="BlosBox%20Handcrafting\.(jpeg|jpg|webp)"', r'src="../BlosBox%20Handcrafting.webp"', html_content)
    
    dirs = ['Jewellery', 'Chocolates', 'Watches', 'Leather%20Goods', 'Leather Goods', 'Cosmetics', 'Corporate%20Gifts', 'Corporate Gifts', 'Catalogue', 'Textured', 'Pearl', 'Luxe', 'Planning', 'Printing Foil Embossing', 'Printing%20Foil%20Embossing', 'Bespoke design & prototyping', 'Bespoke%20design%20%26%20prototyping', 'Size and Material Customization', 'Size%20and%20Material%20Customization', 'Other']
    for d in dirs:
        html_content = re.sub(r'src="' + d + r'/', r'src="../' + d + r'/', html_content)
        html_content = re.sub(r'href="' + d + r'/', r'href="../' + d + r'/', html_content)
        html_content = re.sub(r'"' + d + r'/', r'"../' + d + r'/', html_content)
        
    return html_content

def update_hreflang_and_canonical(html_content, lang, filename):
    base_url = "https://blosbox.com"
    
    html_content = re.sub(r'<link rel="canonical"[^>]*>', '', html_content)
    html_content = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>', '', html_content)
    
    canonical_url = f"{base_url}/{filename}" if lang == 'en' else f"{base_url}/{lang}/{filename}"
    
    hreflangs = [
        f'<link rel="canonical" href="{canonical_url}">',
        f'<link rel="alternate" hreflang="en" href="{base_url}/{filename}">',
        f'<link rel="alternate" hreflang="de" href="{base_url}/de/{filename}">',
        f'<link rel="alternate" hreflang="fr" href="{base_url}/fr/{filename}">',
        f'<link rel="alternate" hreflang="it" href="{base_url}/it/{filename}">',
        f'<link rel="alternate" hreflang="sv" href="{base_url}/sv/{filename}">',
        f'<link rel="alternate" hreflang="nl" href="{base_url}/nl/{filename}">',
        f'<link rel="alternate" hreflang="sq" href="{base_url}/sq/{filename}">',
        f'<link rel="alternate" hreflang="mk" href="{base_url}/mk/{filename}">',
        f'<link rel="alternate" hreflang="x-default" href="{base_url}/{filename}">'
    ]
    
    hreflang_str = "\n    " + "\n    ".join(hreflangs) + "\n"
    html_content = html_content.replace('</head>', f'{hreflang_str}</head>')
    return html_content

def pre_render_html(base_html, lang, lang_dict, filename):
    content = base_html
    page_key = get_page_key(filename)
    
    content = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', content)
    
    title_key = f'meta_title_{page_key}'
    if title_key in lang_dict:
        content = re.sub(r'<title>.*?</title>', f'<title>{lang_dict[title_key]}</title>', content, flags=re.DOTALL)
        
    desc_key = f'meta_desc_{page_key}'
    if desc_key in lang_dict:
        meta_desc_val = lang_dict[desc_key]
        content = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{meta_desc_val}"', content)
        content = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{meta_desc_val}"', content)
        
    if title_key in lang_dict:
        content = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{lang_dict[title_key]}"', content)

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

def main():
    root_dir = 'c:/Blosbox antigravity'
    translations_file = os.path.join(root_dir, 'translations.js')
    
    translations = parse_translations_js(translations_file)
    print("Parsed translations for languages:", list(translations.keys()))
    
    html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and not f.startswith('.')]
    
    # 1. First, update root HTML files with clean canonical & hreflang tags
    for filename in html_files:
        src_path = os.path.join(root_dir, filename)
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = update_hreflang_and_canonical(content, 'en', filename)
        with open(src_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    print(f"Updated root HTML files ({len(html_files)} pages) with clean hreflang tags")

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
            
            dest_path = os.path.join(lang_dir, filename)
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
                
        print(f"Generated static subfolder: /{lang}/ ({len(html_files)} pages)")

if __name__ == '__main__':
    main()
