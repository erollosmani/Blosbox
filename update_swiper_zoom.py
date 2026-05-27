import os
import re

def update_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # 1. Wrap images in swiper-zoom-container
    # Looking for <div class="swiper-slide">\s+<img ...>
    pattern = r'(<div class="swiper-slide">)\s+(<img[^>]+>)'
    replacement = r'\1\n                    <div class="swiper-zoom-container">\n                        \2\n                    </div>'
    
    content = re.sub(pattern, replacement, content)
    
    # 2. Add zoom: true to Swiper config
    if 'zoom: true' not in content:
        # Insert it after loop: true or before navigation
        content = content.replace('loop: true,', 'loop: true,\n        zoom: true,')
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Updated {filename} with Zoom structure and config")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    update_file(f)
