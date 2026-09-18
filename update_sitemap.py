import os

def generate_sitemap():
    base_url = "https://www.blosbox.com"
    pages = [
        ("index.html", "1.0"),
        ("about.html", "0.8"),
        ("products.html", "0.8"),
        ("custom.html", "0.8"),
        ("bespoke.html", "0.8"),
        ("printing.html", "0.8"),
        ("customization.html", "0.8"),
        ("jewellery.html", "0.9"),
        ("jewellery-calculator.html", "0.95"),
        ("watches.html", "0.9"),
        ("leather.html", "0.9"),
        ("chocolates.html", "0.9"),
        ("gifts.html", "0.9"),
        ("cosmetics.html", "0.9"),
        ("insights.html", "0.85"),
        ("custom-proposal-diamond-ring-box.html", "0.90"),
        ("other.html", "0.7")
    ]
    
    languages = ["en", "de", "fr", "it", "sv", "nl", "sq", "mk"]
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    for filename, priority in pages:
        for lang in languages:
            if filename == "index.html":
                url_loc = f"{base_url}/" if lang == "en" else f"{base_url}/{lang}/"
                en_loc = f"{base_url}/"
                default_loc = f"{base_url}/"
            else:
                url_loc = f"{base_url}/{filename}" if lang == "en" else f"{base_url}/{lang}/{filename}"
                en_loc = f"{base_url}/{filename}"
                default_loc = f"{base_url}/{filename}"
            
            xml.append('  <url>')
            xml.append(f'    <loc>{url_loc}</loc>')
            xml.append('    <changefreq>weekly</changefreq>')
            xml.append(f'    <priority>{priority}</priority>')
            
            # Hreflang links
            xml.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en_loc}"/>')
            for l in ["de", "fr", "it", "sv", "nl", "sq", "mk"]:
                lang_href = f"{base_url}/{l}/" if filename == "index.html" else f"{base_url}/{l}/{filename}"
                xml.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{lang_href}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{default_loc}"/>')
            xml.append('  </url>')
            
    xml.append('</urlset>')
    
    sitemap_path = 'c:/Blosbox antigravity/sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml) + '\n')
        
    print(f"Generated comprehensive sitemap.xml with {len(pages) * len(languages)} URL entries")

if __name__ == '__main__':
    generate_sitemap()
