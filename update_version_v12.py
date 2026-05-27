import os
import re

def update_version_v12(filename):
    if not os.path.exists(filename) or not filename.endswith('.html'):
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # Update script.js?v=X to script.js?v=12
    content = re.sub(r'script\.js(\?v=\d+)?', 'script.js?v=12', content)
    # Update styles.css?v=X to styles.css?v=12
    content = re.sub(r'styles\.css(\?v=\d+)?', 'styles.css?v=12', content)
    
    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Updated version to v12 in {filename}")

files = [f for f in os.listdir('c:/Blosbox antigravity') if f.endswith('.html')]

for f in files:
    update_version_v12(os.path.join('c:/Blosbox antigravity', f))
