import os
import re

def update_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # Replace the existing click handler with a more sophisticated one that handles Zoom
    new_click_handler = '''        on: {
          click: function(swiper, event) {
            // Check if we clicked an image
            if (event.target.tagName.toLowerCase() === "img") {
              // If it's the active slide, toggle native zoom (smooth for mobile)
              if (swiper.clickedIndex === swiper.activeIndex) {
                if (swiper.zoom.scale > 1) {
                  swiper.zoom.out();
                } else {
                  swiper.zoom.in();
                }
              } else {
                // Otherwise, open the desktop-friendly lightbox
                openLightbox(event.target.src);
              }
            }
          }
        }'''
    
    # Find the existing 'on: { click: ... }' block and replace it
    pattern = r'on: \{\s+click: function\(swiper, event\) \{.*?\}\s+\}'
    content = re.sub(pattern, new_click_handler, content, flags=re.DOTALL)
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Updated {filename} with smart click-to-zoom handler")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    update_file(f)
