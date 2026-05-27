import os

def update_file(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    search_str = '      });'
    replacement = '''        on: {
          click: function(swiper, event) {
            if (event.target.tagName.toLowerCase() === "img") {
              openLightbox(event.target.src);
            }
          }
        }
      });'''
    
    if search_str in content:
        new_content = content.replace(search_str, replacement)
        with open(filename, 'wb') as f:
            f.write(new_content.encode('utf-8'))
        print(f"Updated {filename}")
    else:
        print(f"Search string not found in {filename}")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    update_file(f)
