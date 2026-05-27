import os
import re

def fix_html_structure(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # Remove any stray empty lines or weird whitespace inside slides
    # And specifically fix the broken </div> structure
    # We want: <div class="swiper-slide">\s*<img[^>]+>\s*</div>
    
    # First, let's normalize the mess. 
    # Match any swiper-slide block and rebuild it cleanly.
    pattern = r'<div class="swiper-slide">.*?<img\s+src="([^"]+)"\s+alt="([^"]+)">.*?</div>\s*</div>'
    replacement = r'<div class="swiper-slide">\n                    <img src="\1" alt="\2">\n                </div>'
    
    # If the above doesn't match because of the extra div, let's try a broader one
    # We'll search for the img and its surrounding slide tags
    
    # Re-writing the entire swiper-wrapper content is often safer
    
    def clean_slide(match):
        img_src = match.group(1)
        img_alt = match.group(2)
        return f'<div class="swiper-slide">\n                    <img src="{img_src}" alt="{img_alt}">\n                </div>'

    # This pattern looks for the img and captures its src/alt, then replaces the whole messy slide
    content = re.sub(r'<div class="swiper-slide">.*?<img\s+src="([^"]+)"\s+alt="([^"]+)".*?</div>\s*</div>', clean_slide, content, flags=re.DOTALL)

    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Fixed HTML structure in {filename}")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    fix_html_structure(f)
