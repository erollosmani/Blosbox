import os

def clean_file_end(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    
    # We want everything up to the end of the footer, then our clean scripts and closing tags
    footer_end_marker = '</footer>'
    idx = content.find(footer_end_marker)
    if idx == -1:
        print(f"Footer end marker not found in {filename}")
        return
    
    base_content = content[:idx + len(footer_end_marker)]
    
    clean_footer_and_scripts = '''
    
    <script src="script.js"></script>
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
    </script>
</body>
</html>'''

    new_content = base_content + clean_footer_and_scripts
    
    with open(filename, 'wb') as f:
        f.write(new_content.encode('utf-8'))
    print(f"Hard-reset and cleaned {filename}")

files = [
    'c:/Blosbox antigravity/textured.html',
    'c:/Blosbox antigravity/pearl.html',
    'c:/Blosbox antigravity/luxe.html'
]

for f in files:
    clean_file_end(f)
