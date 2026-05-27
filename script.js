// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
    console.log("Blosbox Script v12 Loaded");
    
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileBtn.innerHTML = navLinks.classList.contains('active') ? '✕' : '☰';
        });
    }

    // Mobile Dropdown Toggle
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
        if (link) {
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 850) {
                    if (!dropdown.classList.contains('active')) {
                        e.preventDefault();
                        e.stopPropagation();
                        dropdowns.forEach(other => {
                            if (other !== dropdown && !other.contains(dropdown) && !dropdown.contains(other)) {
                                other.classList.remove('active');
                            }
                        });
                        dropdown.classList.add('active');
                    } else {
                        if (link.getAttribute('href') === '#') {
                            e.preventDefault();
                            dropdown.classList.remove('active');
                        }
                    }
                }
            });
        }
    });

    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (this.classList.contains('floating-cta') || targetId === '#quote') {
                e.preventDefault();
                showContactModal();
                return;
            }
            e.preventDefault();
            if (targetId === '#') return;
            try {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            } catch (err) {}
        });
    });

    function createContactModal() {
        if (document.getElementById('contactModal')) return;
        const modalHtml = `
            <div class="modal-overlay" id="contactModal">
                <div class="modal-container">
                    <div class="modal-close" id="closeModal">✕</div>
                    <div class="modal-content">
                        <h2>Request a Quote</h2>
                        <div class="modal-info">
                            <p>Hoshimin 216-b, Skopje 1000<br>North Macedonia</p>
                            <p>Email: <a href="mailto:contact@blosbox.com">contact@blosbox.com</a></p>
                            <p>Phone: <a href="tel:+38975222228">+389 75 222228</a></p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
    createContactModal();
});

function showContactModal() {
    const modal = document.getElementById('contactModal');
    if (modal) modal.classList.add('active');
}

/**
 * Lightbox / Zoom Logic - v12 (Viewport Anchored)
 */
let lb_isDragging = false;
let lb_startX, lb_startY, lb_currentX = 0, lb_currentY = 0, lb_initialX = 0, lb_initialY = 0;
let lb_totalMoved = 0;

function openLightbox(src) {
    let overlay = document.getElementById('lightboxOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'lightboxOverlay';
        overlay.className = 'lightbox-overlay';
        overlay.style.cssText = "position:fixed; top:0; left:0; width:100%; height:100%; background:#000; display:none; justify-content:center; align-items:center; z-index:2147483647; opacity:0; transition:opacity 0.3s ease; overscroll-behavior:none; touch-action:none;";
        overlay.innerHTML = `
            <div class="lightbox-close" id="lightboxClose" style="position:fixed; top:20px; right:20px; width:45px; height:45px; background:rgba(255,255,255,0.2); color:#fff; display:flex; justify-content:center; align-items:center; border-radius:50%; font-size:20px; cursor:pointer; z-index:2147483648; backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,0.3);"><i class="fas fa-times"></i></div>
            <div id="lbContainer" style="width:100%; height:100%; display:flex; justify-content:center; align-items:center; overflow:hidden; touch-action:none; background:#000; position:relative;">
                <img id="lbImg" src="" draggable="false" style="width:auto; height:auto; max-width:90%; max-height:90%; transition: transform 0.3s cubic-bezier(0.2, 0, 0.2, 1); cursor:zoom-in; user-select:none; touch-action:none; transform: translate3d(0,0,0) scale(1); display:block; margin:auto;">
            </div>
        `;
        document.body.appendChild(overlay);

        const img = document.getElementById('lbImg');
        const closeBtn = document.getElementById('lightboxClose');

        closeBtn.onclick = (e) => { e.stopPropagation(); closeLB(); };
        overlay.onclick = (e) => { if (e.target === overlay || e.target.id === 'lbContainer') closeLB(); };

        img.addEventListener('pointerdown', (e) => {
            lb_isDragging = true;
            lb_totalMoved = 0;
            lb_startX = e.clientX;
            lb_startY = e.clientY;
            lb_initialX = lb_currentX;
            lb_initialY = lb_currentY;
            img.style.transition = 'none';
            if (e.target.setPointerCapture) e.target.setPointerCapture(e.pointerId);
        });

        img.addEventListener('pointermove', (e) => {
            if (!lb_isDragging) return;
            const dx = e.clientX - lb_startX;
            const dy = e.clientY - lb_startY;
            lb_totalMoved = Math.max(lb_totalMoved, Math.abs(dx) + Math.abs(dy));

            if (img.getAttribute('data-zoomed') === 'true') {
                const scale = window.innerWidth <= 850 ? 3.5 : 3;
                
                // Use a safer, more robust boundary calculation
                const vw = window.innerWidth;
                const vh = window.innerHeight;
                const iw = img.offsetWidth * scale;
                const ih = img.offsetHeight * scale;

                // We want to ensure that the edges of the image never cross the viewport center minus half-viewport
                // Max X translation should be (ImageWidth - ViewportWidth) / 2
                const maxX = iw > vw ? (iw - vw) / 2 : 0;
                const maxY = ih > vh ? (ih - vh) / 2 : 0;

                lb_currentX = Math.max(-maxX, Math.min(maxX, lb_initialX + dx));
                lb_currentY = Math.max(-maxY, Math.min(maxY, lb_initialY + dy));

                img.style.transform = `translate3d(${lb_currentX}px, ${lb_currentY}px, 0) scale(${scale})`;
            }
        });

        img.addEventListener('pointerup', (e) => {
            if (!lb_isDragging) return;
            lb_isDragging = false;
            if (e.target.releasePointerCapture) e.target.releasePointerCapture(e.pointerId);
            
            img.style.transition = 'transform 0.3s cubic-bezier(0.2, 0, 0.2, 1)';
            
            if (lb_totalMoved < 15) {
                const scale = window.innerWidth <= 850 ? 3.5 : 3;
                if (img.getAttribute('data-zoomed') === 'true') {
                    img.setAttribute('data-zoomed', 'false');
                    img.style.cursor = 'zoom-in';
                    lb_currentX = 0; lb_currentY = 0;
                    img.style.transform = 'translate3d(0, 0, 0) scale(1)';
                } else {
                    img.setAttribute('data-zoomed', 'true');
                    img.style.cursor = 'grab';
                    img.style.transform = `translate3d(0, 0, 0) scale(${scale})`;
                }
            }
        });

        img.addEventListener('pointercancel', () => { lb_isDragging = false; });
    }

    const img = document.getElementById('lbImg');
    img.src = src;
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden'; // Double lock
    setTimeout(() => { overlay.style.opacity = '1'; }, 10);
}

function closeLB() {
    const overlay = document.getElementById('lightboxOverlay');
    const img = document.getElementById('lbImg');
    if (!overlay) return;
    overlay.style.display = 'none';
    overlay.style.opacity = '0';
    img.setAttribute('data-zoomed', 'false');
    img.style.transform = 'translate3d(0, 0, 0) scale(1)';
    lb_currentX = 0; lb_currentY = 0;
    document.body.style.overflow = '';
    document.documentElement.style.overflow = '';
}
