import os
import re

def unify_floating_objects(filename):
    if not os.path.exists(filename) or not filename.endswith('.html'):
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # 1. Remove any existing floating objects from anywhere in the file
    # This prevents duplicates if they were in the hero and at the bottom
    content = re.sub(r'<!-- Floating Catalog Download -->.*?</a>\s*<!-- Floating CTA -->.*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a [^>]*class="floating-catalog"[^>]*>.*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a [^>]*class="floating-cta"[^>]*>.*?</a>', '', content, flags=re.DOTALL)
    
    # 2. Add them cleanly right before the closing </body> tag
    floating_html = '''
    <!-- Floating Catalog Download -->
    <a href="Catalogue/BlosBox Catalog.pdf" class="floating-catalog" target="_blank" aria-label="Download Catalog">
        <i class="fas fa-file-pdf"></i> Catalog
    </a>

    <!-- Floating CTA -->
    <a href="#quote" class="floating-cta" aria-label="Request a Quote">
        <i class="fas fa-quote-right"></i>
    </a>
'''
    
    if '</body>' in content:
        content = content.replace('</body>', floating_html + '</body>')
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Unified floating objects in {filename}")

files = [f for f in os.listdir('c:/Blosbox antigravity') if f.endswith('.html')]

for f in files:
    unify_floating_objects(os.path.join('c:/Blosbox antigravity', f))
