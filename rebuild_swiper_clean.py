import os
import re

def clean_rebuild_swiper(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # Define the clean, correct script block
    clean_scripts = '''    <script src="script.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js"></script>
    <script>
      var swiper = new Swiper(".mySwiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        watchSlidesProgress: true,
        loop: true,
        observer: true, 
        observeParents: true,
        coverflowEffect: {
          rotate: 0,
          stretch: -180,
          depth: 250,
          modifier: 1,
          scale: 0.70,
          slideShadows: true,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        on: {
          click: function(swiper, event) {
            if (event.target.tagName.toLowerCase() === "img") {
              openLightbox(event.target.src);
            }
          }
        }
      });
    </script>'''
    
    # Replace the entire script section
    pattern = r'    <script src="script.js">.*?</script>\s*</script>'
    # Actually, better to just replace everything between the first script and the end of the last one
    content = re.sub(r'    <!-- Scripts -->.*?<script src="script.js">.*?</script>\s*(?:\s*</script>)*', '    <!-- Scripts -->\n' + clean_scripts, content, flags=re.DOTALL)
    
    # Also fix the CSS mess in the head
    content = re.sub(r'overflow: visible !important;\}', '}', content)

    with open(filename, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Cleanly rebuilt Swiper scripts and CSS in {filename}")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    clean_rebuild_swiper(f)
