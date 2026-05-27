import os
import re

def fix_swiper_centering(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # 1. Update Swiper Config for better initialization and visibility
    swiper_init_replacement = '''var swiper = new Swiper(".mySwiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        watchSlidesProgress: true,
        loop: true,
        observer: true, 
        observeParents: true,'''
    
    pattern = r'var swiper = new Swiper\(".mySwiper", \{(.*?)\s+coverflowEffect:'
    content = re.sub(pattern, swiper_init_replacement + r'\n        coverflowEffect:', content, flags=re.DOTALL)

    # 2. Fix CSS: Ensure .swiper has overflow: visible so arrows are clickable even if slightly outside
    # And ensure it has a defined width
    swiper_css_pattern = r'\.swiper \{(.*?)\}'
    def update_swiper_css(match):
        css = match.group(1)
        if 'overflow: visible' not in css:
            css += '\n            overflow: visible !important;'
        return f'.swiper {{{css}}}'
    
    content = re.sub(swiper_css_pattern, update_swiper_css, content, flags=re.DOTALL)

    # 3. Ensure arrows have high z-index and are inside the clickable area
    arrow_css_pattern = r'\.swiper-button-next, \.swiper-button-prev \{(.*?)\}'
    def update_arrow_css(match):
        css = match.group(1)
        if 'z-index' not in css:
            css += '\n            z-index: 100 !important;'
        else:
            css = re.sub(r'z-index:.*?;', 'z-index: 100 !important;', css)
        return f'.swiper-button-next, .swiper-button-prev {{{css}}}'
    
    content = re.sub(arrow_css_pattern, update_arrow_css, content, flags=re.DOTALL)

    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Fixed centering and visibility in {filename}")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    fix_swiper_centering(f)
