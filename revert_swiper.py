import os
import re

def revert_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # 1. Remove swiper-zoom-container
    content = content.replace('<div class="swiper-zoom-container">', '')
    content = content.replace('</div>\n                </div>', '</div>') # Careful here
    
    # Better regex for cleanup
    content = re.sub(r'<div class="swiper-zoom-container">\s+(<img[^>]+>)\s+</div>', r'\1', content)
    
    # 2. Remove zoom: true
    content = content.replace('\n        zoom: true,', '')
    
    # 3. Simplify click handler back to basic lightbox
    new_click_handler = '''        on: {
          click: function(swiper, event) {
            if (event.target.tagName.toLowerCase() === "img") {
              openLightbox(event.target.src);
            }
          }
        }'''
    
    pattern = r'on: \{\s+click: function\(swiper, event\) \{.*?\}\s+\}'
    content = re.sub(pattern, new_click_handler, content, flags=re.DOTALL)
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Reverted {filename} to stable state")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    revert_file(f)
