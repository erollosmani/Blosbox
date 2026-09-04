"""
generate_catalog.py
Builds pricelist-catalog.html and compiles Blosbox-Jewellery-Pricelist.pdf using Headless Chrome/Edge.
Strictly 4 A4 pages (divisible by 4), ordered from smallest to largest box.

Specifications:
- Catalog Name: "Jewellery & Watch Box Pricelist"
- Header on EVERY page corresponds to website header style (#302C27 dark band, gold accents, white text, Blosbox logo)
- Displays "Jewellery & Watch Box Pricelist" in the header of every page
- Category 1 (Textured & Pearl): Dark Brown (#2D2825) 2-row swatch showcase
- Category 2 (Luxe Finishes): Kraft (#9E826B) 1-row swatch showcase
- Product cards pricing boxes match category background colors with negative white text
"""

import os
import io
import base64
import math
import subprocess
from PIL import Image

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_b64(rel_path, max_dim=600, quality=90):
    abs_path = os.path.join(WORKSPACE_DIR, rel_path)
    if not os.path.exists(abs_path):
        print(f"Warning: File not found: {abs_path}")
        return ""
    try:
        img = Image.open(abs_path)
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img.save(buf, format='PNG', optimize=True)
            mime = 'image/png'
        else:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(buf, format='JPEG', quality=quality, optimize=True)
            mime = 'image/jpeg'
        return f'data:{mime};base64,' + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        print(f"Error encoding {abs_path}: {e}")
        return ""

def generate_box_svg(width, length, height, box_id):
    W = float(width)
    L = float(length)
    H = float(height)

    cos30 = 0.86602540378
    sin30 = 0.5

    projW = (W + L) * cos30
    projH = (W + L) * sin30 + H

    # Scaling so the 3D wireframe box fits with ample clearance for outside dimensions
    scale = min(220.0 / projW, 120.0 / projH)

    sW = W * scale
    sL = L * scale
    sH = H * scale

    p2x = 160.0
    p2y = 75.0

    p3x = p2x - sW * cos30
    p3y = p2y - sW * sin30

    p1x = p2x + sL * cos30
    p1y = p2y - sL * sin30

    p0x = p3x + sL * cos30
    p0y = p3y - sL * sin30

    b3x = p3x
    b3y = p3y + sH

    b2x = p2x
    b2y = p2y + sH

    b1x = p1x
    b1y = p1y + sH

    lidRatio = 0.35
    if box_id == 'r3':
        lidRatio = 33.0 / 45.0
    elif box_id == 'rlux':
        lidRatio = 60.0 / 78.0
    elif box_id == 'watch-box':
        lidRatio = 85.0 / 110.0

    lidH = max(sH * lidRatio, 5.0)
    l3x, l3y = p3x, p3y + lidH
    l2x, l2y = p2x, p2y + lidH
    l1x, l1y = p1x, p1y + lidH

    # Dimensions lines
    distLeft = 26.0
    nLx = -sin30
    nLy = cos30
    dimLx1 = b3x + nLx * distLeft
    dimLy1 = b3y + nLy * distLeft
    dimLx2 = b2x + nLx * distLeft
    dimLy2 = b2y + nLy * distLeft
    textLx = (dimLx1 + dimLx2) / 2.0 + nLx * 15.0
    textLy = (dimLy1 + dimLy2) / 2.0 + nLy * 15.0 + 4.0

    distRight = 26.0
    nRx = sin30
    nRy = cos30
    dimRx1 = b2x + nRx * distRight
    dimRy1 = b2y + nRy * distRight
    dimRx2 = b1x + nRx * distRight
    dimRy2 = b1y + nRy * distRight
    textRx = (dimRx1 + dimRx2) / 2.0 + nRx * 15.0
    textRy = (dimRy1 + dimRy2) / 2.0 + nRx * 15.0 + 4.0

    distH = 24.0
    dimHx = p1x + distH
    dimHy1 = p1y
    dimHy2 = b1y
    textHx = dimHx + 8.0
    textHy = (dimHy1 + dimHy2) / 2.0 + 4.0

    allX = [
        p0x, p1x, p2x, p3x, b1x, b2x, b3x,
        dimLx1, dimLx2, dimRx1, dimRx2, dimHx,
        textLx - 22.0, textLx + 22.0,
        textRx - 22.0, textRx + 22.0,
        textHx, textHx + 38.0
    ]
    allY = [
        p0y, p1y, p2y, p3y, b1y, b2y, b3y,
        dimLy1, dimLy2, dimRy1, dimRy2, dimHy1, dimHy2,
        textLy - 11.0, textLy + 5.0,
        textRy - 11.0, textRy + 5.0,
        textHy - 11.0, textHy + 5.0
    ]

    pad = 10.0
    minX = math.floor(min(allX) - pad)
    maxX = math.ceil(max(allX) + pad)
    minY = math.floor(min(allY) - pad)
    maxY = math.ceil(max(allY) + pad)
    vbW = maxX - minX
    vbH = maxY - minY

    marker_id_start = f"dim-arr-s-{box_id}"
    marker_id_end = f"dim-arr-e-{box_id}"

    svg = f'''<svg viewBox="{minX} {minY} {vbW} {vbH}" xmlns="http://www.w3.org/2000/svg" class="box-svg">
      <defs>
        <marker id="{marker_id_start}" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
          <path d="M 8 1.5 L 2 5 L 8 8.5" fill="none" stroke="#222222" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
        <marker id="{marker_id_end}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
          <path d="M 2 1.5 L 8 5 L 2 8.5" fill="none" stroke="#222222" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
      </defs>
      <polygon points="{p3x:.1f},{p3y:.1f} {p2x:.1f},{p2y:.1f} {b2x:.1f},{b2y:.1f} {b3x:.1f},{b3y:.1f}" fill="#FFFFFF" stroke="#222222" stroke-width="1.2" stroke-linejoin="round"/>
      <polygon points="{p1x:.1f},{p1y:.1f} {p2x:.1f},{p2y:.1f} {b2x:.1f},{b2y:.1f} {b1x:.1f},{b1y:.1f}" fill="#F6F6F6" stroke="#222222" stroke-width="1.2" stroke-linejoin="round"/>
      <polyline points="{l3x:.1f},{l3y:.1f} {l2x:.1f},{l2y:.1f} {l1x:.1f},{l1y:.1f}" fill="none" stroke="#222222" stroke-width="1.2" stroke-linejoin="round"/>
      <polygon points="{p0x:.1f},{p0y:.1f} {p1x:.1f},{p1y:.1f} {p2x:.1f},{p2y:.1f} {p3x:.1f},{p3y:.1f}" fill="#FFFFFF" stroke="#222222" stroke-width="1.2" stroke-linejoin="round"/>
      <line x1="{dimLx1:.1f}" y1="{dimLy1:.1f}" x2="{dimLx2:.1f}" y2="{dimLy2:.1f}" stroke="#333333" stroke-width="0.9" marker-start="url(#{marker_id_start})" marker-end="url(#{marker_id_end})"/>
      <text x="{textLx:.1f}" y="{textLy:.1f}" font-family="'Outfit', sans-serif" font-size="11" font-weight="600" fill="#111111" text-anchor="middle">{int(W)}mm</text>
      <line x1="{dimRx1:.1f}" y1="{dimRy1:.1f}" x2="{dimRx2:.1f}" y2="{dimRy2:.1f}" stroke="#333333" stroke-width="0.9" marker-start="url(#{marker_id_start})" marker-end="url(#{marker_id_end})"/>
      <text x="{textRx:.1f}" y="{textRy:.1f}" font-family="'Outfit', sans-serif" font-size="11" font-weight="600" fill="#111111" text-anchor="middle">{int(L)}mm</text>
      <line x1="{dimHx:.1f}" y1="{dimHy1:.1f}" x2="{dimHx:.1f}" y2="{dimHy2:.1f}" stroke="#333333" stroke-width="0.9" marker-start="url(#{marker_id_start})" marker-end="url(#{marker_id_end})"/>
      <text x="{textHx:.1f}" y="{textHy:.1f}" font-family="'Outfit', sans-serif" font-size="11" font-weight="600" fill="#111111" text-anchor="start">{int(H)}mm</text>
    </svg>'''
    return svg

def main():
    print("Pre-encoding logo and blueprints...")
    logo_b64 = get_b64("Logo.png", 500)
    proposal_box_drawing_b64 = get_b64("Proposal ring box tecnical drawing.jpg", 600)
    watch_box_drawing_b64 = get_b64("Watch box tecnical drawing.jpg", 600)

    # 15 Products ordered from Smallest to Largest Box
    products = [
        # Page 1: 1 - 4
        {
            "id": "r1",
            "name": "R1 Ring Box",
            "category": "Jewellery Ring Box",
            "width": 41, "length": 49, "height": 29,
            "size": "41 × 49 / 29 mm",
            "price_structured": "€0.50",
            "price_luxe": "€0.80",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Rigid Lid & Base Luxury Box",
            "insert_img": "Inserts/Insert for Ring boxes.jpg",
            "insert_name": "Single Ring Slot Die-Cut Foam"
        },
        {
            "id": "r2",
            "name": "R2 Ring Box",
            "category": "Jewellery Ring Box",
            "width": 47, "length": 47, "height": 34,
            "size": "47 × 47 / 34 mm",
            "price_structured": "€0.58",
            "price_luxe": "€1.00",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Square Lid & Base Architecture",
            "insert_img": "Inserts/Insert for Ring boxes.jpg",
            "insert_name": "Single Ring Slot Die-Cut Foam"
        },
        {
            "id": "r3",
            "name": "R3 Ring Box",
            "category": "Jewellery Ring Box",
            "width": 58, "length": 58, "height": 45,
            "size": "58 × 58 / 45 mm",
            "price_structured": "€1.15",
            "price_luxe": "€1.50",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "High-Lid Rigid Presentation Casket",
            "insert_img": "Inserts/Insert for Ring boxes.jpg",
            "insert_name": "Single Ring or H-Cut Multi-Slot"
        },
        {
            "id": "rlux",
            "name": "Proposal Ring Box (70 x 70 / 78)",
            "category": "Jewellery Ring Box",
            "width": 70, "length": 70, "height": 78,
            "size": "70 × 70 / 78 mm",
            "price_structured": "€5.00",
            "price_luxe": "€7.30",
            "thickness": "2.5mm",
            "is_heavy": True,
            "structure": "Proposal Ring Luxury Elevated Architecture",
            "insert_img": "Inserts/Insert for RLux Tall.jpg",
            "insert_name": "Proposal Elevated Ring Holder"
        },

        # Page 2: 5 - 8
        {
            "id": "bracelet-box",
            "name": "Bracelet Box",
            "category": "Bracelet Box",
            "width": 220, "length": 42, "height": 26,
            "size": "220 × 42 / 26 mm",
            "price_structured": "€1.20",
            "price_luxe": "€1.55",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Long Rigid Lid & Base Box",
            "insert_img": "Inserts/Insert Barcelet Box 220x42 - 26mm.jpg",
            "insert_name": "Die-Cut Dual Bracelet Elastic Slits"
        },
        {
            "id": "super-small-set",
            "name": "Super Small Set",
            "category": "Jewellery Set Box",
            "width": 65, "length": 85, "height": 27,
            "size": "65 × 85 / 27 mm",
            "price_structured": "€0.90",
            "price_luxe": "€1.10",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Compact Suite Lid & Base Box",
            "insert_img": "Inserts/Insert for Super Small Set.jpg",
            "insert_name": "Pendant & Earring Die-Cut Insert"
        },
        {
            "id": "small-set",
            "name": "Small Set (80x80)",
            "category": "Jewellery Set Box",
            "width": 80, "length": 80, "height": 30,
            "size": "80 × 80 / 30 mm",
            "price_structured": "€1.10",
            "price_luxe": "€1.40",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Square Rigid Presentation Box",
            "insert_img": "Inserts/Insert Small Set 80x80 - 30mm and Small Set H 80x80 - 40mm.jpg",
            "insert_name": "Multi-Slit Ring, Earring & Pendant"
        },
        {
            "id": "small-set-h",
            "name": "Small Set H (80x80 High)",
            "category": "Jewellery Set Box",
            "width": 80, "length": 80, "height": 40,
            "size": "80 × 80 / 40 mm",
            "price_structured": "€1.30",
            "price_luxe": "€1.80",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Square High-Profile Rim Presentation Box",
            "insert_img": "Inserts/Insert Small Set 80x80 - 30mm and Small Set H 80x80 - 40mm.jpg",
            "insert_name": "Multi-Slit Ring, Earring & Pendant"
        },

        # Page 3: 9 - 12
        {
            "id": "middle-small-set",
            "name": "Middle Small Set",
            "category": "Jewellery Set Box",
            "width": 110, "length": 126, "height": 30,
            "size": "110 × 126 / 30 mm",
            "price_structured": "€1.45",
            "price_luxe": "€1.86",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Medium Set Presentation Architecture",
            "insert_img": "Inserts/Insert for Middle Small Set.jpg",
            "insert_name": "Necklace & Earring Suite Insert"
        },
        {
            "id": "middle-set",
            "name": "Middle Set",
            "category": "Jewellery Set Box",
            "width": 140, "length": 180, "height": 30,
            "size": "140 × 180 / 30 mm",
            "price_structured": "€2.45",
            "price_luxe": "€3.20",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Rectangular Luxury Presentation Box",
            "insert_img": "Inserts/Insert for Middle set.jpg",
            "insert_name": "Full Parure Statement Insert"
        },
        {
            "id": "large-square-set",
            "name": "Large Square Set",
            "category": "Jewellery Set Box",
            "width": 180, "length": 180, "height": 30,
            "size": "180 × 180 / 30 mm",
            "price_structured": "€2.76",
            "price_luxe": "€3.60",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Large Square Statement Suite Box",
            "insert_img": "Inserts/Insert for Large Squere set.jpg",
            "insert_name": "Broad Collar & Tiara Foam Insert"
        },
        {
            "id": "large-rectangle-set",
            "name": "Large Rectangle Set",
            "category": "Jewellery Set Box",
            "width": 180, "length": 215, "height": 30,
            "size": "180 × 215 / 30 mm",
            "price_structured": "€3.00",
            "price_luxe": "€4.00",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Wide Grand Necklace Presentation Box",
            "insert_img": "Inserts/Insert for Large rectangle set.jpg",
            "insert_name": "Grand Necklace & Tiara Insert"
        },

        # Page 4: 13 - 15
        {
            "id": "large-xl-set",
            "name": "Large XL Set",
            "category": "Jewellery Set Box",
            "width": 205, "length": 240, "height": 60,
            "size": "205 × 240 / 60 mm",
            "price_structured": "€6.00",
            "price_luxe": "€8.50",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Deep XL Luxury Rigid Presentation Casket",
            "insert_img": "Inserts/Insert for XL set.jpg",
            "insert_name": "High-Volume Statement Foam Insert"
        },
        {
            "id": "large-xxs-set",
            "name": "Large XXS (XXL) Set",
            "category": "Jewellery Set Box",
            "width": 223, "length": 303, "height": 30,
            "size": "223 × 303 / 30 mm",
            "price_structured": "€5.00",
            "price_luxe": "€7.50",
            "thickness": "1.2mm",
            "is_heavy": False,
            "structure": "Master Suite Archival Presentation Box",
            "insert_img": "Inserts/Insert for XXL set.jpg",
            "insert_name": "Master Suite Comprehensive Foam Insert"
        },
        {
            "id": "watch-box",
            "name": "Watch Box",
            "category": "Horology Presentation Box",
            "width": 100, "length": 100, "height": 110,
            "size": "100 × 100 / 110 mm",
            "price_structured": "€16.00",
            "price_luxe": "€18.00",
            "thickness": "2.5mm",
            "is_heavy": True,
            "structure": "Watch Box High-Tower Architecture",
            "insert_img": "Inserts/insert watch box.jpg",
            "insert_name": "Curved Foam Watch Pillow / Holder"
        }
    ]

    print("Pre-encoding insert images...")
    for p in products:
        p["insert_b64"] = get_b64(p["insert_img"], 450)

    # 19 Textured & Pearl Swatches
    swatches_tp_all = [
        {"name": "Black Imitlin", "short": "Black Imitlin", "file": "Size and Material Customization/Black Imitlin.webp"},
        {"name": "Black Leatherlike", "short": "Black Leather", "file": "Size and Material Customization/Black Leatherlike.webp"},
        {"name": "Blue Butterfly", "short": "Blue Butterfly", "file": "Size and Material Customization/Blue Butterfly.webp"},
        {"name": "Caramel Pearl", "short": "Caramel Pearl", "file": "Size and Material Customization/Caramel Pearl.webp"},
        {"name": "Castano Imitlin", "short": "Castano Imitlin", "file": "Size and Material Customization/Castano Imitlin.webp"},
        {"name": "Castano Leatherlike", "short": "Castano Leather", "file": "Size and Material Customization/Castano Leatherlike.webp"},
        {"name": "Castano Pearl", "short": "Castano Pearl", "file": "Size and Material Customization/Castano Pearl.webp"},
        {"name": "Cream Imitlin", "short": "Cream Imitlin", "file": "Size and Material Customization/Cream Imitlin.webp"},
        {"name": "Cream Leatherlike", "short": "Cream Leather", "file": "Size and Material Customization/Cream Leatherlike.webp"},
        {"name": "Green Leatherlike", "short": "Green Leather", "file": "Size and Material Customization/Green Leatherlike.webp"},
        {"name": "Light Green Pearl", "short": "Light Green", "file": "Size and Material Customization/Light Green Pearl.webp"},
        {"name": "Light Purple Pearl", "short": "Light Purple", "file": "Size and Material Customization/Light purple pearl.webp"},
        {"name": "Orange Pearl", "short": "Orange Pearl", "file": "Size and Material Customization/Orange Pearl.webp"},
        {"name": "Red Butterfly", "short": "Red Butterfly", "file": "Size and Material Customization/Red Butterfly.webp"},
        {"name": "Red Leatherlike", "short": "Red Leather", "file": "Size and Material Customization/Red Leatherlike.webp"},
        {"name": "Teal Pearl", "short": "Teal Pearl", "file": "Size and Material Customization/Teal Pearl.webp"},
        {"name": "White Diamond", "short": "White Diamond", "file": "Size and Material Customization/White Diamond.webp"},
        {"name": "White Imitlin", "short": "White Imitlin", "file": "Size and Material Customization/White Imitlin.webp"},
        {"name": "White Leatherlike", "short": "White Leather", "file": "Size and Material Customization/White Leatherlike.webp"},
    ]

    # 6 Luxe Swatches
    swatches_luxe_all = [
        {"name": "Black Carbon", "desc": "Carbon Fiber Weave", "file": "Size and Material Customization/Black Carbon.webp"},
        {"name": "Black Velvet", "desc": "Plush Matte Velvet", "file": "Size and Material Customization/Black Velvet.webp"},
        {"name": "Brown Velvet", "desc": "Chocolate Suede Velvet", "file": "Size and Material Customization/Brown Velvet.webp"},
        {"name": "Carbon Cream", "desc": "Ivory Carbon Weave", "file": "Size and Material Customization/Carbon Cream.webp"},
        {"name": "Kraft Velvet", "desc": "Natural Kraft Velvet", "file": "Size and Material Customization/Kraft Velvet.webp"},
        {"name": "Red Velvet", "desc": "Crimson Royal Velvet", "file": "Size and Material Customization/Red Velvet.webp"},
    ]

    print("Pre-encoding paper swatches at high resolution (300px) for crisp printing...")
    for s in swatches_tp_all:
        s["b64"] = get_b64(s["file"], 280, 92)

    for s in swatches_luxe_all:
        s["b64"] = get_b64(s["file"], 360, 92)

    # Helper to render the user-requested bottom showcase:
    # - Category 1: Dark Brown (#2D2825) with 2 rows (Row 1: Label + 9 swatches, Row 2: 10 swatches)
    # - Category 2: Kraft (#9E826B) with 1 row (Label + 6 large swatches)
    def render_bottom_swatch_strip():
        cat1_label_html = '''
        <div class="cat-label-card tp-label-card">
          <div class="cat-label-badge">CATEGORY ONE</div>
          <div class="cat-label-title">TEXTURED &amp; PEARL</div>
          <div class="cat-label-tier">PRICE 1</div>
        </div>
        '''

        tp_row1_html = "".join([
            f'''<div class="swatch-cell" title="{s['name']}">
                <div class="swatch-img-frame"><img src="{s['b64']}" alt="{s['name']}" class="swatch-img"></div>
                <div class="swatch-name-neg">{s['short']}</div>
            </div>''' for s in swatches_tp_all[0:9]
        ])

        tp_row2_html = "".join([
            f'''<div class="swatch-cell" title="{s['name']}">
                <div class="swatch-img-frame"><img src="{s['b64']}" alt="{s['name']}" class="swatch-img"></div>
                <div class="swatch-name-neg">{s['short']}</div>
            </div>''' for s in swatches_tp_all[9:19]
        ])

        cat2_label_html = '''
        <div class="cat-label-card luxe-label-card">
          <div class="cat-label-badge">CATEGORY TWO</div>
          <div class="cat-label-title">LUXE FINISHES</div>
          <div class="cat-label-tier">PRICE 2</div>
        </div>
        '''

        luxe_swatches_html = "".join([
            f'''<div class="luxe-swatch-cell" title="{s['name']}">
                <div class="luxe-img-frame"><img src="{s['b64']}" alt="{s['name']}" class="luxe-img"></div>
                <div class="luxe-name-neg">{s['name']}</div>
            </div>''' for s in swatches_luxe_all
        ])

        return f'''
        <div class="bottom-paper-showcase">
          <!-- CATEGORY 1: DARK BROWN CONTAINER (#2D2825) - 2 ROWS -->
          <div class="cat-band tp-band">
            <div class="tp-row tp-row-top">
              {cat1_label_html}
              {tp_row1_html}
            </div>
            <div class="tp-row tp-row-bottom">
              {tp_row2_html}
            </div>
          </div>

          <!-- CATEGORY 2: KRAFT CONTAINER (#9E826B) - 1 ROW -->
          <div class="cat-band luxe-band">
            <div class="luxe-single-row">
              {cat2_label_html}
              {luxe_swatches_html}
            </div>
          </div>
        </div>
        '''

    def render_product_card(p):
        if p["id"] == "rlux":
            drawing_html = f'''<div class="drawing-img-box"><img src="{proposal_box_drawing_b64}" alt="Proposal Box Technical Drawing" class="blueprint-img"></div>'''
        elif p["id"] == "watch-box":
            drawing_html = f'''<div class="drawing-img-box"><img src="{watch_box_drawing_b64}" alt="Watch Box Technical Drawing" class="blueprint-img"></div>'''
        else:
            drawing_html = f'''<div class="drawing-svg-box">{generate_box_svg(p["width"], p["length"], p["height"], p["id"])}</div>'''

        thickness_badge_class = "thickness-badge heavy-duty" if p["is_heavy"] else "thickness-badge"
        thickness_text = f"Cardboard thickness: {p['thickness']}"
        if p["is_heavy"]:
            thickness_text += " (Reinforced)"

        return f'''
        <div class="product-card">
          <!-- Col 1: Box Technical Drawing with Dimensions -->
          <div class="col-drawing">
            <div class="col-label">TECHNICAL DRAWING</div>
            {drawing_html}
            <div class="size-callout">{p["size"]}</div>
          </div>

          <!-- Col 2: Precision Die-Cut Insert Drawing -->
          <div class="col-insert">
            <div class="col-label">PRECISION INSERT</div>
            <div class="insert-img-wrap">
              <img src="{p['insert_b64']}" alt="{p['insert_name']}" class="insert-img">
            </div>
            <div class="insert-caption">{p["insert_name"]}</div>
          </div>

          <!-- Col 3: Specifications & Cardboard Thickness -->
          <div class="col-specs">
            <div class="product-name">{p["name"]}</div>
            <div class="product-structure">{p["structure"]}</div>
            <div class="product-dims-text">Dimensions: <strong>{p["size"]}</strong> (W × L / H)</div>
            <div class="{thickness_badge_class}">{thickness_text}</div>
            <div class="insert-specs-note">Includes 15mm Die-Cut Velvet-Top Foam (Black, Dark Brown, Cream)</div>
          </div>

          <!-- Col 4: Dual Pricing Matching Category Background Colors Exactly -->
          <div class="col-pricing">
            <div class="price-box tp-price">
              <div class="price-header">TEXTURED &amp; PEARL</div>
              <div class="price-amount">{p["price_structured"]}<span class="price-unit"> / pc</span></div>
              <div class="price-sub">PRICE TIER 1</div>
            </div>
            <div class="price-box luxe-price">
              <div class="price-header">LUXE FINISHES</div>
              <div class="price-amount">{p["price_luxe"]}<span class="price-unit"> / pc</span></div>
              <div class="price-sub">PRICE TIER 2</div>
            </div>
            <div class="vol-hint">From 100 pcs • Up to -15% on volume</div>
          </div>
        </div>
        '''

    # Build the 4 Pages
    p1_cards = "".join([render_product_card(p) for p in products[0:4]])
    p2_cards = "".join([render_product_card(p) for p in products[4:8]])
    p3_cards = "".join([render_product_card(p) for p in products[8:12]])
    p4_cards = "".join([render_product_card(p) for p in products[12:15]])

    bottom_swatches = render_bottom_swatch_strip()

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Jewellery &amp; Watch Box Pricelist | Blosbox Luxury Packaging</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2•family=Playfair+Display:ital,wght@0€500;0,600;0,700;1,400&family=Cinzel:wght@600;700;800&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* Global Page Geometry for A4 Print */
    @page {{
      size: A4 portrait;
      margin: 0;
    }}
    *, *:before, *:after {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}
    body {{
      margin: 0;
      padding: 0;
      background: #E8E6E1;
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #1A1A1A;
      -webkit-font-smoothing: antialiased;
    }}

    .page {{
      width: 210mm;
      height: 297mm;
      margin: 0 auto 20px auto;
      background: #FFFFFF;
      padding: 5.5mm 10mm 4.5mm 10mm;
      page-break-after: always;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 16px rgba(0€0€0€0.12);
    }}

    @media print {{
      body {{
        background: #FFFFFF;
      }}
      .page {{
        margin: 0;
        box-shadow: none;
        page-break-after: always;
        height: 297mm;
        max-height: 297mm;
      }}
    }}

    /* =========================================================
       WEBSITE-CORRESPONDING HEADER DESIGN (#302C27 Top Band)
       Exact dark top band matching the Blosbox website navbar
       ========================================================= */
    .website-style-header {{
      background: #302C27;
      color: #F9F7F3;
      border-radius: 4px;
      padding: 3.5mm 7mm;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #C5A059;
      margin-bottom: 3.5mm;
      box-shadow: 0 2px 8px rgba(0,0,0,0.22);
    }}

    .header-brand-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .header-logo {{
      height: 30px;
      width: auto;
      object-fit: contain;
    }}
    .header-brand-divider {{
      width: 1.5px;
      height: 24px;
      background: rgba(197, 160, 89, 0.45);
    }}
    .header-text-group {{
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .header-main-title {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 14.5pt;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: #FFFFFF;
      line-height: 1.1;
    }}
    .header-sub-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 6.5pt;
      font-weight: 600;
      letter-spacing: 1.5px;
      color: #C5A059;
      text-transform: uppercase;
      margin-top: 1.5px;
    }}

    .header-meta-group {{
      text-align: right;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 2px;
    }}
    .header-badge {{
      display: inline-block;
      background: #443F38;
      border: 1px solid #C5A059;
      color: #F4EBD9;
      font-size: 6.5pt;
      font-weight: 700;
      letter-spacing: 0.8px;
      padding: 2.5px 8px;
      border-radius: 3px;
      text-transform: uppercase;
      white-space: nowrap;
    }}
    .header-url {{
      font-size: 6.5pt;
      color: #C5A059;
      font-weight: 600;
      letter-spacing: 0.6px;
      text-transform: uppercase;
    }}

    .header-brand-group {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .header-logo {{
      height: 28px;
      width: auto;
      object-fit: contain;
    }}
    .header-text-group {{
      display: flex;
      flex-direction: column;
    }}
    .header-main-title {{
      font-family: 'Playfair Display', serif;
      font-size: 13.5pt;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: #FFFFFF;
      line-height: 1.1;
    }}
    .header-sub-title {{
      font-size: 6.5pt;
      font-weight: 600;
      letter-spacing: 1.6px;
      color: #C5A059;
      text-transform: uppercase;
      margin-top: 1.5px;
    }}

    .header-meta-group {{
      text-align: right;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }}
    .header-badge {{
      display: inline-block;
      background: #443F38;
      border: 1px solid #C5A059;
      color: #F4EBD9;
      font-size: 6.5pt;
      font-weight: 700;
      letter-spacing: 0.8px;
      padding: 2px 8px;
      border-radius: 3px;
      text-transform: uppercase;
    }}
    .header-url {{
      font-size: 6pt;
      color: #C5A059;
      margin-top: 2px;
      font-weight: 500;
      letter-spacing: 0.4px;
    }}

    /* SECTION BANNER */
    .section-banner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #F9F7F2;
      border: 1px solid #EAE2D2;
      border-left: 3px solid #C5A059;
      padding: 2px 7px;
      margin-bottom: 3.5px;
      border-radius: 2px;
    }}
    .banner-text {{
      font-size: 6.8pt;
      font-weight: 700;
      color: #333333;
      letter-spacing: 0.4px;
      text-transform: uppercase;
    }}
    .banner-badge {{
      font-size: 5.8pt;
      background: #EAE2D2;
      color: #555555;
      padding: 1px 5px;
      border-radius: 2px;
      font-weight: 600;
    }}

    /* PRODUCT CARDS CONTAINER */
    .products-container {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    /* PRODUCT CARD GRID */
    .product-card {{
      display: grid;
      grid-template-columns: 46mm 39mm 63mm 42mm;
      background: #FCFCFA;
      border: 1px solid #E5E1D8;
      border-radius: 3.5px;
      padding: 3.5px 5.5px;
      align-items: center;
      gap: 5.5px;
      height: 38mm;
      max-height: 38.5mm;
      box-shadow: 0 1px 2px rgba(0€0€0€0.02);
    }}

    .col-label {{
      font-size: 4.8pt;
      font-weight: 700;
      color: #888888;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 1px;
    }}

    /* Col 1: Drawing */
    .col-drawing {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      background: #FFFFFF;
      border: 1px solid #ECEAE4;
      border-radius: 2.5px;
      padding: 1px;
    }}
    .drawing-svg-box {{
      width: 100%;
      height: 25.5mm;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .box-svg {{
      width: 100%;
      height: 100%;
      max-height: 25.5mm;
    }}
    .drawing-img-box {{
      width: 100%;
      height: 25.5mm;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #FFFFFF;
    }}
    .blueprint-img {{
      max-width: 100%;
      max-height: 25.5mm;
      object-fit: contain;
    }}
    .size-callout {{
      font-size: 5.8pt;
      font-weight: 700;
      color: #222222;
      margin-top: 0px;
      letter-spacing: 0.2px;
    }}

    /* Col 2: Insert */
    .col-insert {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      background: #FFFFFF;
      border: 1px solid #ECEAE4;
      border-radius: 2.5px;
      padding: 1px;
    }}
    .insert-img-wrap {{
      width: 100%;
      height: 25mm;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #FAF8F5;
      border-radius: 2px;
      overflow: hidden;
    }}
    .insert-img {{
      max-width: 95%;
      max-height: 25mm;
      object-fit: contain;
    }}
    .insert-caption {{
      font-size: 4.8pt;
      color: #555555;
      text-align: center;
      margin-top: 1px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      width: 37mm;
      font-weight: 500;
    }}

    /* Col 3: Specs */
    .col-specs {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-left: 2px;
    }}
    .product-name {{
      font-family: 'Playfair Display', serif;
      font-size: 8.8pt;
      font-weight: 700;
      color: #111111;
      line-height: 1.15;
    }}
    .product-structure {{
      font-size: 5.8pt;
      color: #777777;
      margin-top: 1.5px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      font-weight: 500;
    }}
    .product-dims-text {{
      font-size: 6.4pt;
      color: #333333;
      margin-top: 2px;
    }}
    .product-dims-text strong {{
      color: #111111;
    }}
    .thickness-badge {{
      display: inline-block;
      margin-top: 2.5px;
      font-size: 5.8pt;
      font-weight: 700;
      color: #2D3748;
      background: #EDF2F7;
      border: 1px solid #CBD5E0;
      padding: 1.5px 5px;
      border-radius: 2.5px;
      width: fit-content;
      letter-spacing: 0.2px;
    }}
    .thickness-badge.heavy-duty {{
      background: #FEF3C7;
      color: #92400E;
      border-color: #FCD34D;
      font-weight: 800;
    }}
    .insert-specs-note {{
      font-size: 4.8pt;
      color: #666666;
      margin-top: 2px;
      line-height: 1.2;
    }}

    /* =========================================================
       Col 4: Pricing Matching Category Background Colors Exactly
       - Category 1 Price: Dark Brown (#2D2825) with Negative White Text
       - Category 2 Price: Kraft (#9E826B) with Negative White Text
       ========================================================= */
    .col-pricing {{
      display: flex;
      flex-direction: column;
      gap: 2.5px;
      justify-content: center;
    }}
    .price-box {{
      border-radius: 2.5px;
      padding: 2px 4px;
      text-align: center;
    }}
    .price-box.tp-price {{
      background: #2D2825;
      border: 1px solid #1A1614;
      color: #FFFFFF;
    }}
    .price-box.luxe-price {{
      background: #9E826B;
      border: 1px solid #856B54;
      color: #FFFFFF;
    }}
    .price-header {{
      font-size: 4.8pt;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .tp-price .price-header {{
      color: #E2D9C8;
    }}
    .luxe-price .price-header {{
      color: #FFF2E3;
    }}
    .price-amount {{
      font-size: 10.2pt;
      font-weight: 800;
      line-height: 1;
      margin-top: 0.5px;
      color: #FFFFFF;
    }}
    .price-unit {{
      font-size: 5.5pt;
      font-weight: 500;
      color: rgba(255,255,255€0.85);
    }}
    .price-sub {{
      font-size: 4.3pt;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}
    .tp-price .price-sub {{
      color: #C2B8A8;
    }}
    .luxe-price .price-sub {{
      color: #F3E4D3;
    }}
    .vol-hint {{
      font-size: 4.6pt;
      color: #777777;
      text-align: center;
      margin-top: 0.5px;
      font-weight: 500;
    }}

    /* PAGE 4 B2B TERMS BLOCK */
    .b2b-terms-block {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 6px;
      background: #FBF9F5;
      border: 1px solid #E8DFD0;
      border-left: 3px solid #C5A059;
      border-radius: 3px;
      padding: 3.5px 7px;
      margin-bottom: 3px;
    }}
    .b2b-col-title {{
      font-size: 5.8pt;
      font-weight: 800;
      color: #111111;
      letter-spacing: 0.4px;
      text-transform: uppercase;
      margin-bottom: 2px;
      border-bottom: 1px solid #E2D9C8;
      padding-bottom: 1.5px;
    }}
    .b2b-item {{
      font-size: 5.2pt;
      color: #333333;
      margin-bottom: 1.5px;
      line-height: 1.2;
    }}
    .b2b-item strong {{
      color: #111111;
    }}
    .b2b-discount-highlight {{
      color: #9A752B;
      font-weight: 800;
    }}

    /* =========================================================
       BOTTOM PAPER SHOWCASE: EXACT USER DIAGRAM IMPLEMENTATION
       - Category 1 Band: Dark Brown (#2D2825) with 2 rows of swatches
       - Category 2 Band: Kraft (#9E826B) with 1 row of swatches
       ========================================================= */
    .bottom-paper-showcase {{
      margin-top: 3.5px;
      display: flex;
      flex-direction: column;
      gap: 2.5px;
    }}

    .cat-band {{
      border-radius: 3.5px;
      padding: 3.5px 4.5px;
    }}
    .tp-band {{
      background: #2D2825;
      border: 1px solid #1A1614;
    }}
    .luxe-band {{
      background: #9E826B;
      border: 1px solid #856B54;
    }}

    /* Category 1: 10 Columns Grid for Both Rows */
    .tp-row {{
      display: grid;
      grid-template-columns: repeat(10, 1fr);
      gap: 3px;
      align-items: center;
    }}
    .tp-row-top {{
      margin-bottom: 2.5px;
    }}

    /* White Category Label Box (matching user drawing) */
    .cat-label-card {{
      background: #FFFFFF;
      border-radius: 2.5px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 2px 1px;
      box-shadow: 0 1px 3px rgba(0€0€0€0.18);
    }}
    .tp-label-card {{
      height: 18.5mm;
      border: 1.5px solid #FFFFFF;
    }}
    .luxe-label-card {{
      width: 24mm;
      height: 20mm;
      flex-shrink: 0;
      border: 1.5px solid #FFFFFF;
    }}

    .cat-label-badge {{
      font-size: 4.8pt;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: #111111;
      line-height: 1.1;
    }}
    .cat-label-title {{
      font-size: 4.5pt;
      font-weight: 700;
      letter-spacing: 0.3px;
      text-transform: uppercase;
      margin-top: 1.5px;
      line-height: 1.15;
    }}
    .tp-label-card .cat-label-title {{
      color: #2D2825;
    }}
    .luxe-label-card .cat-label-title {{
      color: #7D634E;
    }}
    .cat-label-tier {{
      font-size: 4.2pt;
      font-weight: 800;
      color: #C5A059;
      margin-top: 1.5px;
      letter-spacing: 0.4px;
      text-transform: uppercase;
    }}

    /* Swatch Cell in Category 1 */
    .swatch-cell {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }}
    .swatch-img-frame {{
      width: 100%;
      height: 13mm;
      background: #FFFFFF;
      border: 1.5px solid #FFFFFF;
      border-radius: 2px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0€0€0€0.2);
    }}
    .swatch-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .swatch-name-neg {{
      font-size: 4.1pt;
      font-weight: 600;
      color: #FFFFFF;
      margin-top: 1px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      letter-spacing: -0.1px;
    }}

    /* Category 2 Luxe Single Row Layout */
    .luxe-single-row {{
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .luxe-swatch-cell {{
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
      text-align: center;
    }}
    .luxe-img-frame {{
      width: 100%;
      height: 14mm;
      background: #FFFFFF;
      border: 1.5px solid #FFFFFF;
      border-radius: 2px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0€0€0€0.2);
    }}
    .luxe-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .luxe-name-neg {{
      font-size: 4.8pt;
      font-weight: 700;
      color: #FFFFFF;
      margin-top: 1.5px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      letter-spacing: 0.1px;
    }}

    /* FOOTER */
    .master-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 2.5px;
      border-top: 1px solid #E5E1D8;
      margin-top: 2.5px;
      font-size: 5.2pt;
      color: #777777;
    }}
    .footer-left {{
      font-weight: 600;
      color: #444444;
    }}
    .footer-center {{
      color: #666666;
    }}
    .footer-right {{
      font-weight: 700;
      color: #111111;
    }}
  </style>
</head>
<body>

  <!-- ==================== PAGE 1 OF 4 ==================== -->
  <div class="page" id="page-1">
    <!-- Header: Website dark band #302C27 with "Jewellery & Watch Box Pricelist" -->
    <header class="website-style-header">
      <div class="header-brand-group">
        <img src="{logo_b64}" alt="Blosbox Logo" class="header-logo">
        <div class="header-brand-divider"></div>
        <div class="header-text-group">
          <div class="header-main-title">Jewellery &amp; Watch Box Pricelist</div>
          <div class="header-sub-title">Blosbox Luxury Packaging • B2B Wholesale Catalogue</div>
        </div>
      </div>
      <div class="header-meta-group">
        <div class="header-badge">Edition 2026 • Page 1 of 4</div>
        <div class="header-url">www.blosbox.com</div>
      </div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 1: Jewellery Ring &amp; Proposal Boxes (Smallest to Largest)</span>
      <span class="banner-badge">Page 1 of 4 • Rigid Box Architecture</span>
    </div>

    <!-- Product Cards -->
    <div class="products-container">
      {p1_cards}
    </div>

    <!-- Bottom Swatches Showcase: Category 1 (Dark Brown 2 Rows) & Category 2 (Kraft 1 Row) -->
    {bottom_swatches}

    <!-- Footer -->
    <footer class="master-footer">
      <div class="footer-left">Blosbox Luxury Packaging • Premium Jewellery &amp; Watch Box Manufacturer</div>
      <div class="footer-center">Direct Inquiries: info@blosbox.com • Orders: orders@blosbox.com</div>
      <div class="footer-right">Page 1 of 4</div>
    </footer>
  </div>

  <!-- ==================== PAGE 2 OF 4 ==================== -->
  <div class="page" id="page-2">
    <!-- Header: Website dark band #302C27 with "Jewellery & Watch Box Pricelist" -->
    <header class="website-style-header">
      <div class="header-brand-group">
        <img src="{logo_b64}" alt="Blosbox Logo" class="header-logo">
        <div class="header-brand-divider"></div>
        <div class="header-text-group">
          <div class="header-main-title">Jewellery &amp; Watch Box Pricelist</div>
          <div class="header-sub-title">Blosbox Luxury Packaging • B2B Wholesale Catalogue</div>
        </div>
      </div>
      <div class="header-meta-group">
        <div class="header-badge">Edition 2026 • Page 2 of 4</div>
        <div class="header-url">www.blosbox.com</div>
      </div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 2: Long Bracelet &amp; Small Set Presentations</span>
      <span class="banner-badge">Page 2 of 4 • Precision Rigid Architecture</span>
    </div>

    <!-- Product Cards -->
    <div class="products-container">
      {p2_cards}
    </div>

    <!-- Bottom Swatches Showcase -->
    {bottom_swatches}

    <!-- Footer -->
    <footer class="master-footer">
      <div class="footer-left">Blosbox Luxury Packaging • Premium Jewellery &amp; Watch Box Manufacturer</div>
      <div class="footer-center">Direct Inquiries: info@blosbox.com • Orders: orders@blosbox.com</div>
      <div class="footer-right">Page 2 of 4</div>
    </footer>
  </div>

  <!-- ==================== PAGE 3 OF 4 ==================== -->
  <div class="page" id="page-3">
    <!-- Header: Website dark band #302C27 with "Jewellery & Watch Box Pricelist" -->
    <header class="website-style-header">
      <div class="header-brand-group">
        <img src="{logo_b64}" alt="Blosbox Logo" class="header-logo">
        <div class="header-brand-divider"></div>
        <div class="header-text-group">
          <div class="header-main-title">Jewellery &amp; Watch Box Pricelist</div>
          <div class="header-sub-title">Blosbox Luxury Packaging • B2B Wholesale Catalogue</div>
        </div>
      </div>
      <div class="header-meta-group">
        <div class="header-badge">Edition 2026 • Page 3 of 4</div>
        <div class="header-url">www.blosbox.com</div>
      </div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 3: Middle &amp; Large Set Presentation Suites</span>
      <span class="banner-badge">Page 3 of 4 • Master Craftsmanship</span>
    </div>

    <!-- Product Cards -->
    <div class="products-container">
      {p3_cards}
    </div>

    <!-- Bottom Swatches Showcase -->
    {bottom_swatches}

    <!-- Footer -->
    <footer class="master-footer">
      <div class="footer-left">Blosbox Luxury Packaging • Premium Jewellery &amp; Watch Box Manufacturer</div>
      <div class="footer-center">Direct Inquiries: info@blosbox.com • Orders: orders@blosbox.com</div>
      <div class="footer-right">Page 3 of 4</div>
    </footer>
  </div>

  <!-- ==================== PAGE 4 OF 4 ==================== -->
  <div class="page" id="page-4">
    <!-- Header: Website dark band #302C27 with "Jewellery & Watch Box Pricelist" -->
    <header class="website-style-header">
      <div class="header-brand-group">
        <img src="{logo_b64}" alt="Blosbox Logo" class="header-logo">
        <div class="header-brand-divider"></div>
        <div class="header-text-group">
          <div class="header-main-title">Jewellery &amp; Watch Box Pricelist</div>
          <div class="header-sub-title">Blosbox Luxury Packaging • B2B Wholesale Catalogue</div>
        </div>
      </div>
      <div class="header-meta-group">
        <div class="header-badge">Edition 2026 • Page 4 of 4</div>
        <div class="header-url">www.blosbox.com</div>
      </div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 4: Grand Statement Sets &amp; Horology Architecture</span>
      <span class="banner-badge">Page 4 of 4 • Complete Technical Overview</span>
    </div>

    <!-- Product Cards (3 cards) -->
    <div class="products-container">
      {p4_cards}
    </div>

    <!-- B2B Wholesale Terms & Guide -->
    <div class="b2b-terms-block">
      <div class="b2b-col">
        <div class="b2b-col-title">Wholesale Volume Discounts</div>
        <div class="b2b-item">• <strong>100 – 499 pcs:</strong> Base Catalog Rate</div>
        <div class="b2b-item">• <strong>500 – 999 pcs:</strong> <span class="b2b-discount-highlight">5% Volume Discount</span></div>
        <div class="b2b-item">• <strong>1€000 – 4,999 pcs:</strong> <span class="b2b-discount-highlight">10% Volume Discount</span></div>
        <div class="b2b-item">• <strong>5€000+ pcs:</strong> <span class="b2b-discount-highlight">15% Volume Discount</span></div>
      </div>
      <div class="b2b-col">
        <div class="b2b-col-title">Custom Logo &amp; Hot Stamping</div>
        <div class="b2b-item">• <strong>Stamping Mold Fee:</strong> €50 (One-time tooling fee)</div>
        <div class="b2b-item">• <strong>Subsequent Reorders:</strong> Free mold reuse (€0)</div>
        <div class="b2b-item">• <strong>Finishes:</strong> Gold Foil, Silver, Rose Gold, Gloss/Matte Black, Deboss</div>
        <div class="b2b-item">• <strong>Logo Position:</strong> Centered on outer lid or inside lid satin</div>
      </div>
      <div class="b2b-col">
        <div class="b2b-col-title">Material &amp; Packaging Logic</div>
        <div class="b2b-item">• <strong>Inserts Included:</strong> 15mm High-Density Die-Cut Foam</div>
        <div class="b2b-item">• <strong>Insert Colors:</strong> Black, Dark Brown, or Light Cream</div>
        <div class="b2b-item">• <strong>Mixed Material Formula:</strong> (Price 1 + Price 2) × 0.55</div>
        <div class="b2b-item">• <strong>Cardboard:</strong> 1.2mm Rigid (2.5mm for Proposal &amp; Watch)</div>
      </div>
    </div>

    <!-- Bottom Swatches Showcase -->
    {bottom_swatches}

    <!-- Footer -->
    <footer class="master-footer">
      <div class="footer-left">Blosbox Luxury Packaging • B2B Master Wholesale Document</div>
      <div class="footer-center">Web: www.blosbox.com • Contact: info@blosbox.com</div>
      <div class="footer-right">Page 4 of 4</div>
    </footer>
  </div>

</body>
</html>
'''

    output_html_path = os.path.join(WORKSPACE_DIR, "pricelist-catalog.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {output_html_path} successfully ({len(html_content)} bytes).")

    # Compile to PDF using Headless Chrome or Edge
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser_path = chrome_path if os.path.exists(chrome_path) else edge_path

    output_pdf_path = os.path.join(WORKSPACE_DIR, "Blosbox-Jewellery-Pricelist.pdf")
    cmd = [
        browser_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f'--print-to-pdf={output_pdf_path}',
        output_html_path
    ]

    print(f"Compiling PDF with {browser_path}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and os.path.exists(output_pdf_path):
        size_kb = os.path.getsize(output_pdf_path) / 1024
        print(f"PDF generated successfully: {output_pdf_path} ({size_kb:.1f} KB)")
        
        # Verify page count
        import pypdf
        reader = pypdf.PdfReader(output_pdf_path)
        page_count = len(reader.pages)
        print(f"TOTAL PAGES IN PDF: {page_count} (Divisible by 4: {page_count % 4 == 0})")
    else:
        print(f"Error compiling PDF: {result.stderr}")

if __name__ == "__main__":
    main()
