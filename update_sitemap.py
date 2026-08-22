import os

def generate_sitemap():
    base_url = "https://blosbox.com"
    pages = [
        ("index.html", "1.0"),
        ("about.html", "0.8"),
        ("products.html", "0.8"),
        ("bespoke.html", "0.8"),
        ("printing.html", "0.8"),
        ("customization.html", "0.8"),
        ("jewellery.html", "0.9"),
        ("watches.html", "0.9"),
        ("leather.html", "0.9"),
        ("chocolates.html", "0.9"),
        ("gifts.html", "0.9"),
        ("cosmetics.html", "0.9"),
        ("other.html", "0.7"),
        ("textured.html", "0.7"),
        ("pearl.html", "0.7"),
        ("luxe.html", "0.7")
    ]
    
    languages = ["en", "de", "fr", "it", "sv", "nl", "sq", "mk"]
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    xml.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    for filename, priority in pages:
        # Default English URL
        for lang in languages:
            url_loc = f"{base_url}/{filename}" if lang == "en" else f"{base_url}/{lang}/{filename}"
            xml.append('  <url>')
            xml.append(f'    <loc>{url_loc}</loc>')
            xml.append('    <changefreq>weekly</changefreq>')
            xml.append(f'    <priority>{priority}</priority>')
            
            # Hreflang links
            xml.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{base_url}/{filename}"/>')
            for l in ["de", "fr", "it", "sv", "nl", "sq", "mk"]:
                xml.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{base_url}/{l}/{filename}"/>')
            xml.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{base_url}/{filename}"/>')
            xml.append('  </url>')
            
    xml.append('</urlset>')
    
    sitemap_path = 'c:/Blosbox antigravity/sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml) + '\n')
        
    print(f"Generated comprehensive sitemap.xml with {len(pages) * len(languages)} URL entries")

if __name__ == '__main__':
    generate_sitemap()
