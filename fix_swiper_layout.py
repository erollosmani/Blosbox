import os
import re

def fix_swiper_layout(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # 1. Remove flexbox from .hero to avoid Swiper width calculation issues
    content = content.replace('display: flex;', 'display: block;')
    content = content.replace('align-items: center;', '')
    content = content.replace('justify-content: center;', '')
    
    # 2. Add z-index and pointer-events fix to intro-wipe
    if 'pointer-events: none' not in content:
        content = content.replace('animation-delay: 1.2s; /* wait before wiping */', 'animation-delay: 1.2s; /* wait before wiping */\n            pointer-events: none;')
    
    # 3. Ensure Swiper arrows are clickable
    arrow_style = '.swiper-button-next, .swiper-button-prev {'
    if arrow_style in content:
        content = content.replace(arrow_style, arrow_style + '\n            z-index: 100;')

    # 4. Refine Swiper Initialization for perfect centering
    # We want to ensure centeredSlides and slidesPerView are correct
    swiper_init_start = 'var swiper = new Swiper(".mySwiper", {'
    swiper_init_replacement = '''var swiper = new Swiper(".mySwiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        watchSlidesProgress: true,
        loop: true,'''
    
    # Search for the start of Swiper init and replace the first few lines
    pattern = r'var swiper = new Swiper\(".mySwiper", \{(.*?)\s+coverflowEffect:'
    content = re.sub(pattern, swiper_init_replacement + r'\n        coverflowEffect:', content, flags=re.DOTALL)

    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Refined Swiper layout and interaction in {filename}")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    fix_swiper_layout(f)
