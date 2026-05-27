import os
import re

def place_floating_in_hero(filename):
    if not os.path.exists(filename) or not filename.endswith('.html'):
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # 1. Remove existing floating objects
    content = re.sub(r'<!-- Floating Catalog Download -->.*?</a>\s*<!-- Floating CTA -->.*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a [^>]*class="floating-catalog"[^>]*>.*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a [^>]*class="floating-cta"[^>]*>.*?</a>', '', content, flags=re.DOTALL)
    
    # 2. Re-insert them at the end of the HERO section
    # Search for the closing </section> of the first <section class="hero">
    floating_html = '''
        <!-- Floating Catalog Download -->
        <a href="Catalogue/BlosBox Catalog.pdf" class="floating-catalog" target="_blank" aria-label="Download Catalog">
            <i class="fas fa-file-pdf"></i> Catalog
        </a>

        <a href="#quote" class="floating-cta" aria-label="Request a Quote">
            <i class="fas fa-quote-right"></i>
        </a>
    '''
    
    # Use regex to find the first hero section and append before its closing tag
    pattern = r'(<section class="hero[^>]*>.*?)(\s*</section>)'
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, r'\1' + floating_html + r'\2', content, count=1, flags=re.DOTALL)
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Placed floating objects in Hero of {filename}")

files = [f for f in os.listdir('c:/Blosbox antigravity') if f.endswith('.html')]

for f in files:
    place_floating_in_hero(os.path.join('c:/Blosbox antigravity', f))
