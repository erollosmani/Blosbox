import os
import re

def fix_button_centering(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # Target the industries-grid div that has display: block
    # and change it to display: flex with justify-content: center
    pattern = r'<div class="industries-grid" style="display:\s*block;[^>]+>'
    replacement = '<div class="industries-grid" style="display: flex; justify-content: center; flex-wrap: wrap; gap: 1rem; width: 100%;">'
    
    content = re.sub(pattern, replacement, content)
    
    # Also ensure the buttons inside don't have conflicting flex or max-width if they prevent centering
    # Actually, flex: 1 on children in a center-justified flex container will make them fill space.
    # If we want them centered but not necessarily filling the whole width, we should remove flex: 1.
    
    # Let's make them more elegant:
    content = content.replace('flex: 1;', 'flex: 0 1 auto;')
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Fixed button centering in {filename}")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    fix_button_centering(f)
