"""
generate_catalog.py
Builds pricelist-catalog.html and compiles Blosbox-Jewellery-Pricelist.pdf using Headless Chrome/Edge.
Strictly 4 A4 pages (divisible by 4), ordered from smallest to largest box.
"""

import os
import io
import base64
import math
import subprocess
from PIL import Image

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_b64(rel_path, max_dim=600, quality=85):
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
    scale = min(230.0 / projW, 130.0 / projH)

    sW = W * scale
    sL = L * scale
    sH = H * scale

    p2x = 160.0
    p2y = 80.0

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

    lidH = max(sH * lidRatio, 6.0)
    l3x, l3y = p3x, p3y + lidH
    l2x, l2y = p2x, p2y + lidH
    l1x, l1y = p1x, p1y + lidH

    # Dimensions lines
    distLeft = 28.0
    nLx = -sin30
    nLy = cos30
    dimLx1 = b3x + nLx * distLeft
    dimLy1 = b3y + nLy * distLeft
    dimLx2 = b2x + nLx * distLeft
    dimLy2 = b2y + nLy * distLeft
    textLx = (dimLx1 + dimLx2) / 2.0 + nLx * 16.0
    textLy = (dimLy1 + dimLy2) / 2.0 + nLy * 16.0 + 4.0

    distRight = 28.0
    nRx = sin30
    nRy = cos30
    dimRx1 = b2x + nRx * distRight
    dimRy1 = b2y + nRy * distRight
    dimRx2 = b1x + nRx * distRight
    dimRy2 = b1y + nRy * distRight
    textRx = (dimRx1 + dimRx2) / 2.0 + nRx * 16.0
    textRy = (dimRy1 + dimRy2) / 2.0 + nRx * 16.0 + 4.0

    distH = 26.0
    dimHx = p1x + distH
    dimHy1 = p1y
    dimHy2 = b1y
    textHx = dimHx + 8.0
    textHy = (dimHy1 + dimHy2) / 2.0 + 4.0

    allX = [
        p0x, p1x, p2x, p3x, b1x, b2x, b3x,
        dimLx1, dimLx2, dimRx1, dimRx2, dimHx,
        textLx - 24.0, textLx + 24.0,
        textRx - 24.0, textRx + 24.0,
        textHx, textHx + 40.0
    ]
    allY = [
        p0y, p1y, p2y, p3y, b1y, b2y, b3y,
        dimLy1, dimLy2, dimRy1, dimRy2, dimHy1, dimHy2,
        textLy - 12.0, textLy + 6.0,
        textRy - 12.0, textRy + 6.0,
        textHy - 12.0, textHy + 6.0
    ]

    pad = 12.0
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
    logo_b64 = get_b64("Logo.png", 350)
    proposal_box_drawing_b64 = get_b64("Proposal ring box tecnical drawing.jpg", 700)
    watch_box_drawing_b64 = get_b64("Watch box tecnical drawing.jpg", 700)

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
            "insert_name": "High-Volume Haute Parure Foam Insert"
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
        p["insert_b64"] = get_b64(p["insert_img"], 500)

    # 19 Textured & Pearl Swatches
    swatches_textured_pearl = [
        {"name": "Black Imitlin", "file": "Size and Material Customization/Black Imitlin.webp"},
        {"name": "Black Leatherlike", "file": "Size and Material Customization/Black Leatherlike.webp"},
        {"name": "Blue Butterfly", "file": "Size and Material Customization/Blue Butterfly.webp"},
        {"name": "Caramel Pearl", "file": "Size and Material Customization/Caramel Pearl.webp"},
        {"name": "Castano Imitlin", "file": "Size and Material Customization/Castano Imitlin.webp"},
        {"name": "Castano Leatherlike", "file": "Size and Material Customization/Castano Leatherlike.webp"},
        {"name": "Castano Pearl", "file": "Size and Material Customization/Castano Pearl.webp"},
        {"name": "Cream Imitlin", "file": "Size and Material Customization/Cream Imitlin.webp"},
        {"name": "Cream Leatherlike", "file": "Size and Material Customization/Cream Leatherlike.webp"},
        {"name": "Green Leatherlike", "file": "Size and Material Customization/Green Leatherlike.webp"},
        {"name": "Light Green Pearl", "file": "Size and Material Customization/Light Green Pearl.webp"},
        {"name": "Light Purple Pearl", "file": "Size and Material Customization/Light purple pearl.webp"},
        {"name": "Orange Pearl", "file": "Size and Material Customization/Orange Pearl.webp"},
        {"name": "Red Butterfly", "file": "Size and Material Customization/Red Butterfly.webp"},
        {"name": "Red Leatherlike", "file": "Size and Material Customization/Red Leatherlike.webp"},
        {"name": "Teal Pearl", "file": "Size and Material Customization/Teal Pearl.webp"},
        {"name": "White Diamond", "file": "Size and Material Customization/White Diamond.webp"},
        {"name": "White Imitlin", "file": "Size and Material Customization/White Imitlin.webp"},
        {"name": "White Leatherlike", "file": "Size and Material Customization/White Leatherlike.webp"},
    ]

    # 6 Luxe Swatches
    swatches_luxe = [
        {"name": "Black Carbon", "file": "Size and Material Customization/Black Carbon.webp"},
        {"name": "Black Velvet", "file": "Size and Material Customization/Black Velvet.webp"},
        {"name": "Brown Velvet", "file": "Size and Material Customization/Brown Velvet.webp"},
        {"name": "Carbon Cream", "file": "Size and Material Customization/Carbon Cream.webp"},
        {"name": "Kraft Velvet", "file": "Size and Material Customization/Kraft Velvet.webp"},
        {"name": "Red Velvet", "file": "Size and Material Customization/Red Velvet.webp"},
    ]

    print("Pre-encoding paper swatches...")
    for s in swatches_textured_pearl:
        s["b64"] = get_b64(s["file"], 120, 80)

    for s in swatches_luxe:
        s["b64"] = get_b64(s["file"], 120, 80)

    # Helper to render the 2-row bottom paper strip
    def render_bottom_swatch_strip():
        # Row 1: 19 Textured & Pearl
        tp_chips_html = "".join([
            f'''<div class="swatch-item" title="{s['name']}">
                <img src="{s['b64']}" alt="{s['name']}" class="swatch-img">
                <span class="swatch-label">{s['name']}</span>
            </div>''' for s in swatches_textured_pearl
        ])

        # Row 2: 6 Luxe
        luxe_chips_html = "".join([
            f'''<div class="swatch-item luxe-item" title="{s['name']}">
                <img src="{s['b64']}" alt="{s['name']}" class="swatch-img">
                <span class="swatch-label">{s['name']}</span>
            </div>''' for s in swatches_luxe
        ])

        return f'''
        <div class="bottom-paper-strip">
          <div class="swatch-row tp-row">
            <div class="swatch-row-tag tp-tag">
              <span class="tag-title">TEXTURED & PEARL</span>
              <span class="tag-price">PRICE 1</span>
            </div>
            <div class="swatch-chips-container">
              {tp_chips_html}
            </div>
          </div>
          <div class="swatch-row luxe-row">
            <div class="swatch-row-tag luxe-tag">
              <span class="tag-title">LUXE FINISHES</span>
              <span class="tag-price">PRICE 2</span>
            </div>
            <div class="swatch-chips-container">
              {luxe_chips_html}
            </div>
          </div>
        </div>
        '''

    def render_product_card(p):
        is_blueprint_box = (p["id"] in ("rlux", "watch-box"))
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

          <!-- Col 4: Dual Pricing (Price 1 vs Price 2) -->
          <div class="col-pricing">
            <div class="price-box tp-price">
              <div class="price-header">TEXTURED & PEARL</div>
              <div class="price-amount">{p["price_structured"]}<span class="price-unit"> / pc</span></div>
              <div class="price-sub">Price Tier 1</div>
            </div>
            <div class="price-box luxe-price">
              <div class="price-header">LUXE FINISHES</div>
              <div class="price-amount">{p["price_luxe"]}<span class="price-unit"> / pc</span></div>
              <div class="price-sub">Price Tier 2</div>
            </div>
            <div class="vol-hint">From 100 pcs • Up to -15% on volume</div>
          </div>
        </div>
        '''

    # Build the 4 Pages
    # Page 1: Boxes 0 to 3 (R1, R2, R3, Proposal Ring Box)
    p1_cards = "".join([render_product_card(p) for p in products[0:4]])
    p2_cards = "".join([render_product_card(p) for p in products[4:8]])
    p3_cards = "".join([render_product_card(p) for p in products[8:12]])
    p4_cards = "".join([render_product_card(p) for p in products[12:15]])

    bottom_swatches = render_bottom_swatch_strip()

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Blosbox Luxury Jewellery Boxes - B2B Wholesale Pricelist & Technical Catalogue</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
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
      background: #EAEAE6;
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #1A1A1A;
      -webkit-font-smoothing: antialiased;
    }}

    .page {{
      width: 210mm;
      height: 297mm;
      margin: 0 auto 20px auto;
      background: #FFFFFF;
      padding: 10mm 12mm 8mm 12mm;
      page-break-after: always;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 16px rgba(0,0,0,0.12);
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

    /* HEADER STYLES */
    .master-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 7px;
      border-bottom: 2px solid #C5A059;
      margin-bottom: 7px;
    }}
    .brand-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-logo {{
      height: 38px;
      width: auto;
      object-fit: contain;
    }}
    .brand-title-group {{
      display: flex;
      flex-direction: column;
    }}
    .brand-main-title {{
      font-family: 'Cinzel', serif;
      font-size: 15pt;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: #111111;
      line-height: 1.1;
    }}
    .brand-sub-title {{
      font-size: 7.5pt;
      font-weight: 500;
      letter-spacing: 2px;
      color: #A67C37;
      text-transform: uppercase;
      margin-top: 2px;
    }}
    .brand-right {{
      text-align: right;
    }}
    .catalog-pill {{
      display: inline-block;
      background: #111111;
      color: #F4EBD9;
      font-size: 7.5pt;
      font-weight: 700;
      letter-spacing: 1px;
      padding: 3px 9px;
      border-radius: 3px;
      text-transform: uppercase;
    }}
    .catalog-date {{
      font-size: 7pt;
      color: #777777;
      margin-top: 3px;
      font-weight: 500;
    }}

    /* Sub-header on pages 2, 3, 4 */
    .running-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 5px;
      border-bottom: 1.5px solid #C5A059;
      margin-bottom: 6px;
    }}
    .running-left {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .running-logo {{
      height: 22px;
      width: auto;
    }}
    .running-title {{
      font-family: 'Cinzel', serif;
      font-size: 9pt;
      font-weight: 700;
      letter-spacing: 1px;
      color: #111111;
    }}
    .running-cat {{
      font-size: 7.5pt;
      color: #A67C37;
      font-weight: 600;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}

    /* SECTION BANNER */
    .section-banner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #F9F7F2;
      border: 1px solid #EAE2D2;
      border-left: 3px solid #C5A059;
      padding: 3px 8px;
      margin-bottom: 7px;
      border-radius: 2px;
    }}
    .banner-text {{
      font-size: 7.5pt;
      font-weight: 700;
      color: #333333;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .banner-badge {{
      font-size: 6.5pt;
      background: #EAE2D2;
      color: #555555;
      padding: 1px 6px;
      border-radius: 2px;
      font-weight: 600;
    }}

    /* PRODUCT CARDS CONTAINER */
    .products-container {{
      display: flex;
      flex-direction: column;
      gap: 5px;
      flex: 1;
    }}

    /* PRODUCT CARD GRID */
    .product-card {{
      display: grid;
      grid-template-columns: 46mm 40mm 58mm 42mm;
      background: #FCFCFA;
      border: 1px solid #E5E1D8;
      border-radius: 4px;
      padding: 5px 7px;
      align-items: center;
      gap: 8px;
      min-height: 48mm;
      max-height: 50mm;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }}

    .col-label {{
      font-size: 5.5pt;
      font-weight: 700;
      color: #888888;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 2px;
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
      border-radius: 3px;
      padding: 2px;
    }}
    .drawing-svg-box {{
      width: 100%;
      height: 34mm;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .box-svg {{
      width: 100%;
      height: 100%;
      max-height: 34mm;
    }}
    .drawing-img-box {{
      width: 100%;
      height: 34mm;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #FFFFFF;
    }}
    .blueprint-img {{
      max-width: 100%;
      max-height: 34mm;
      object-fit: contain;
    }}
    .size-callout {{
      font-size: 6.5pt;
      font-weight: 700;
      color: #222222;
      margin-top: 1px;
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
      border-radius: 3px;
      padding: 2px;
    }}
    .insert-img-wrap {{
      width: 100%;
      height: 33mm;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #FAF8F5;
      border-radius: 2px;
      overflow: hidden;
    }}
    .insert-img {{
      max-width: 95%;
      max-height: 33mm;
      object-fit: contain;
    }}
    .insert-caption {{
      font-size: 5.5pt;
      color: #555555;
      text-align: center;
      margin-top: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      width: 38mm;
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
      font-family: 'Cinzel', serif;
      font-size: 9.5pt;
      font-weight: 700;
      color: #111111;
      line-height: 1.15;
    }}
    .product-structure {{
      font-size: 6.5pt;
      color: #777777;
      margin-top: 2px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 500;
    }}
    .product-dims-text {{
      font-size: 7pt;
      color: #333333;
      margin-top: 3px;
    }}
    .product-dims-text strong {{
      color: #111111;
    }}
    .thickness-badge {{
      display: inline-block;
      margin-top: 4px;
      font-size: 6.5pt;
      font-weight: 700;
      color: #2D3748;
      background: #EDF2F7;
      border: 1px solid #CBD5E0;
      padding: 2px 6px;
      border-radius: 3px;
      width: fit-content;
      letter-spacing: 0.3px;
    }}
    .thickness-badge.heavy-duty {{
      background: #FEF3C7;
      color: #92400E;
      border-color: #FCD34D;
      font-weight: 800;
    }}
    .insert-specs-note {{
      font-size: 5.5pt;
      color: #666666;
      margin-top: 4px;
      line-height: 1.2;
    }}

    /* Col 4: Pricing */
    .col-pricing {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      justify-content: center;
    }}
    .price-box {{
      border-radius: 3px;
      padding: 3px 5px;
      text-align: center;
      border: 1px solid transparent;
    }}
    .price-box.tp-price {{
      background: #F4F4F2;
      border-color: #DCD9D0;
    }}
    .price-box.luxe-price {{
      background: #FFFDF7;
      border-color: #E2D1A6;
    }}
    .price-header {{
      font-size: 5.5pt;
      font-weight: 700;
      letter-spacing: 0.6px;
      text-transform: uppercase;
    }}
    .tp-price .price-header {{
      color: #444444;
    }}
    .luxe-price .price-header {{
      color: #9A752B;
    }}
    .price-amount {{
      font-size: 11pt;
      font-weight: 800;
      line-height: 1;
      margin-top: 1px;
    }}
    .tp-price .price-amount {{
      color: #1A1A1A;
    }}
    .luxe-price .price-amount {{
      color: #9A752B;
    }}
    .price-unit {{
      font-size: 6.5pt;
      font-weight: 500;
      color: #666666;
    }}
    .price-sub {{
      font-size: 5pt;
      color: #888888;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}
    .vol-hint {{
      font-size: 5.2pt;
      color: #777777;
      text-align: center;
      margin-top: 1px;
      font-weight: 500;
    }}

    /* PAGE 4 B2B TERMS BLOCK */
    .b2b-terms-block {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 7px;
      background: #FBF9F5;
      border: 1px solid #E8DFD0;
      border-left: 3px solid #C5A059;
      border-radius: 3px;
      padding: 6px 9px;
      margin-bottom: 6px;
    }}
    .b2b-col-title {{
      font-size: 6.5pt;
      font-weight: 800;
      color: #111111;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 4px;
      border-bottom: 1px solid #E2D9C8;
      padding-bottom: 2px;
    }}
    .b2b-item {{
      font-size: 6pt;
      color: #333333;
      margin-bottom: 2px;
      line-height: 1.25;
    }}
    .b2b-item strong {{
      color: #111111;
    }}
    .b2b-discount-highlight {{
      color: #9A752B;
      font-weight: 800;
    }}

    /* BOTTOM PAPER STRIP (EXACT USER REQUIREMENT) */
    .bottom-paper-strip {{
      margin-top: 6px;
      border: 1px solid #E5E1D8;
      border-radius: 4px;
      background: #FFFFFF;
      padding: 4px 6px;
    }}
    .swatch-row {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .swatch-row.tp-row {{
      padding-bottom: 3px;
      border-bottom: 1px dashed #E2DCCF;
      margin-bottom: 3px;
    }}
    .swatch-row-tag {{
      display: flex;
      flex-direction: column;
      width: 32mm;
      flex-shrink: 0;
      border-radius: 2px;
      padding: 2px 4px;
      text-align: center;
    }}
    .tp-tag {{
      background: #F2F0EB;
      border: 1px solid #DCD7CB;
    }}
    .luxe-tag {{
      background: #FAF3E6;
      border: 1px solid #E6D5B3;
    }}
    .swatch-row-tag .tag-title {{
      font-size: 5.5pt;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .tp-tag .tag-title {{
      color: #222222;
    }}
    .luxe-tag .tag-title {{
      color: #9A752B;
    }}
    .swatch-row-tag .tag-price {{
      font-size: 5pt;
      font-weight: 600;
      color: #666666;
      text-transform: uppercase;
    }}
    .swatch-chips-container {{
      display: flex;
      flex: 1;
      justify-content: space-between;
      align-items: center;
      gap: 2px;
    }}
    .swatch-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 7.6mm;
      text-align: center;
    }}
    .luxe-item {{
      width: 23mm;
    }}
    .swatch-img {{
      width: 7.2mm;
      height: 7.2mm;
      border-radius: 2px;
      object-fit: cover;
      border: 1px solid #DCD7CB;
    }}
    .luxe-item .swatch-img {{
      width: 22mm;
      height: 6.8mm;
    }}
    .swatch-label {{
      font-size: 4pt;
      color: #555555;
      margin-top: 1px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      font-weight: 500;
    }}

    /* FOOTER */
    .master-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 4px;
      border-top: 1px solid #E5E1D8;
      margin-top: 4px;
      font-size: 6pt;
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
    <!-- Header -->
    <header class="master-header">
      <div class="brand-left">
        <img src="{logo_b64}" alt="Blosbox Logo" class="brand-logo">
        <div class="brand-title-group">
          <div class="brand-main-title">BLOSBOX LUXURY PACKAGING</div>
          <div class="brand-sub-title">B2B Wholesale Pricelist & Technical Catalogue</div>
        </div>
      </div>
      <div class="brand-right">
        <div class="catalog-pill">Official 2026 Price Index</div>
        <div class="catalog-date">Order Online: www.blosbox.com</div>
      </div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 1: Jewellery Ring & Proposal Boxes (Smallest to Largest)</span>
      <span class="banner-badge">Page 1 of 4 • Rigid Box Architecture</span>
    </div>

    <!-- Product Cards -->
    <div class="products-container">
      {p1_cards}
    </div>

    <!-- Bottom Swatches Strip (Row 1: Textured & Pearl, Row 2: Luxe) -->
    {bottom_swatches}

    <!-- Footer -->
    <footer class="master-footer">
      <div class="footer-left">Blosbox Luxury Packaging • Premium Jewellery Box Manufacturer</div>
      <div class="footer-center">Direct Inquiries: info@blosbox.com • Orders: orders@blosbox.com</div>
      <div class="footer-right">Page 1 of 4</div>
    </footer>
  </div>

  <!-- ==================== PAGE 2 OF 4 ==================== -->
  <div class="page" id="page-2">
    <!-- Running Header -->
    <header class="running-header">
      <div class="running-left">
        <img src="{logo_b64}" alt="Blosbox" class="running-logo">
        <span class="running-title">BLOSBOX LUXURY PACKAGING</span>
      </div>
      <div class="running-cat">Part 2: Bracelet & Small Presentation Sets</div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 2: Long Bracelet & Small Set Presentations</span>
      <span class="banner-badge">Page 2 of 4 • Precision Rigid Architecture</span>
    </div>

    <!-- Product Cards -->
    <div class="products-container">
      {p2_cards}
    </div>

    <!-- Bottom Swatches Strip -->
    {bottom_swatches}

    <!-- Footer -->
    <footer class="master-footer">
      <div class="footer-left">Blosbox Luxury Packaging • Premium Jewellery Box Manufacturer</div>
      <div class="footer-center">Direct Inquiries: info@blosbox.com • Orders: orders@blosbox.com</div>
      <div class="footer-right">Page 2 of 4</div>
    </footer>
  </div>

  <!-- ==================== PAGE 3 OF 4 ==================== -->
  <div class="page" id="page-3">
    <!-- Running Header -->
    <header class="running-header">
      <div class="running-left">
        <img src="{logo_b64}" alt="Blosbox" class="running-logo">
        <span class="running-title">BLOSBOX LUXURY PACKAGING</span>
      </div>
      <div class="running-cat">Part 3: Medium & Large Presentation Suites</div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 3: Middle & Large Set Presentation Suites</span>
      <span class="banner-badge">Page 3 of 4 • Master Craftsmanship</span>
    </div>

    <!-- Product Cards -->
    <div class="products-container">
      {p3_cards}
    </div>

    <!-- Bottom Swatches Strip -->
    {bottom_swatches}

    <!-- Footer -->
    <footer class="master-footer">
      <div class="footer-left">Blosbox Luxury Packaging • Premium Jewellery Box Manufacturer</div>
      <div class="footer-center">Direct Inquiries: info@blosbox.com • Orders: orders@blosbox.com</div>
      <div class="footer-right">Page 3 of 4</div>
    </footer>
  </div>

  <!-- ==================== PAGE 4 OF 4 ==================== -->
  <div class="page" id="page-4">
    <!-- Running Header -->
    <header class="running-header">
      <div class="running-left">
        <img src="{logo_b64}" alt="Blosbox" class="running-logo">
        <span class="running-title">BLOSBOX LUXURY PACKAGING</span>
      </div>
      <div class="running-cat">Part 4: Master Suites, Watch Box & B2B Wholesale Terms</div>
    </header>

    <!-- Sub-banner -->
    <div class="section-banner">
      <span class="banner-text">Part 4: Grand Statement Sets & Horology Architecture</span>
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
        <div class="b2b-item">• <strong>1,000 – 4,999 pcs:</strong> <span class="b2b-discount-highlight">10% Volume Discount</span></div>
        <div class="b2b-item">• <strong>5,000+ pcs:</strong> <span class="b2b-discount-highlight">15% Volume Discount</span></div>
      </div>
      <div class="b2b-col">
        <div class="b2b-col-title">Custom Logo & Hot Stamping</div>
        <div class="b2b-item">• <strong>Stamping Mold Fee:</strong> €50 (One-time tooling fee)</div>
        <div class="b2b-item">• <strong>Subsequent Reorders:</strong> Free mold reuse (€0)</div>
        <div class="b2b-item">• <strong>Finishes:</strong> Gold Foil, Silver, Rose Gold, Gloss/Matte Black, Deboss</div>
        <div class="b2b-item">• <strong>Logo Position:</strong> Centered on outer lid or inside lid satin</div>
      </div>
      <div class="b2b-col">
        <div class="b2b-col-title">Material & Packaging Logic</div>
        <div class="b2b-item">• <strong>Inserts Included:</strong> 15mm High-Density Die-Cut Foam</div>
        <div class="b2b-item">• <strong>Insert Colors:</strong> Black, Dark Brown, or Light Cream</div>
        <div class="b2b-item">• <strong>Mixed Material Formula:</strong> (Price 1 + Price 2) × 0.55</div>
        <div class="b2b-item">• <strong>Cardboard:</strong> 1.2mm Rigid (2.5mm for Proposal & Watch)</div>
      </div>
    </div>

    <!-- Bottom Swatches Strip -->
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
