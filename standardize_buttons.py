import os
import re

def standardize_buttons(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # Define the exact HTML block from jewellery.html
    exact_block = '''        <div class="industries-grid" style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center; width: 100%;">
            <a href="textured.html" class="btn-primary" style="padding: 0.5rem 1rem; font-size: 0.8rem; flex: 1; white-space: nowrap; max-width: 200px;">Textured</a>
            <a href="pearl.html" class="btn-primary" style="padding: 0.5rem 1rem; font-size: 0.8rem; flex: 1; white-space: nowrap; max-width: 200px;">Pearl</a>
            <a href="luxe.html" class="btn-primary" style="padding: 0.5rem 1rem; font-size: 0.8rem; flex: 1; white-space: nowrap; max-width: 200px;">Luxe</a>
        </div>'''
    
    # Replace the existing industries-grid section
    # Regex to find the highlights section content
    pattern = r'<div class="industries-grid".*?</div>'
    content = re.sub(pattern, exact_block, content, flags=re.DOTALL)
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Standardized buttons in {filename} to match jewellery.html")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    standardize_buttons(f)
