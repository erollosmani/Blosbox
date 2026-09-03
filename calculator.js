/**
 * Blosbox Luxury Packaging - Mobile-First Configurator Application
 * Features:
 * 1. Popup Sliding Photo Gallery Modal (matching user drawing)
 * 2. Two Category Tabs: Textured & Pearl vs Luxe
 * 3. Touch swipe & arrow navigation for mobile phones
 * 4. Proportional SVG Line Drawings (without color)
 * 5. Proportional Die-Cut Foam Insert Drawings (3 Colors: Black, Dark Brown, Very Light Cream)
 * 6. Combination Pricing Formula: (Price 1 + Price 2) * 0.55
 */

document.addEventListener('DOMContentLoaded', () => {
  // Determine if running in a language subfolder (/de/, /fr/, etc.)
  const isInSubfolder = window.location.pathname.split('/').filter(Boolean).some(p => ['de', 'fr', 'it', 'sv', 'nl', 'sq', 'mk'].includes(p));
  const ASSET_PREFIX = isInSubfolder ? '../' : '';

  // Localization Helper
  function getActiveLang() {
    return (window.i18n && window.i18n.currentLang) ||
           (window.location.pathname.split('/').filter(Boolean).find(p => ['de', 'fr', 'it', 'sv', 'nl', 'sq', 'mk'].includes(p))) ||
           'en';
  }

  function t(key, fallback) {
    const lang = getActiveLang();
    const trans = (typeof window !== 'undefined' && window.translations) || (typeof translations !== 'undefined' ? translations : null);
    if (trans && trans[lang] && trans[lang][key]) {
      return trans[lang][key];
    }
    if (trans && trans['en'] && trans['en'][key]) {
      return trans['en'][key];
    }
    return fallback;
  }


  function resolveAsset(path) {
    if (!path) return '';
    if (path.startsWith('http') || path.startsWith('/') || path.startsWith('../')) return path;
    return ASSET_PREFIX + path;
  }


  // --- DATASETS ---
  const BOX_CATALOG = [
    // Jewellery Ring Boxes
    {
      id: 'r1',
      name: 'R1 Ring Box',
      category: 'Jewellery Ring Boxes',
      width: 41,
      length: 49,
      height: 29,
      size: '41 x 49 / 29 mm',
      priceStructured: 0.50,
      priceLuxe: 0.80,
      structure: 'Lid & Base Luxury Box',
      inserts: [
        { id: 'opt1', name: 'Option 1 (Single Ring Slot)', type: 'ring-standard', file: 'Inserts/Insert for Ring boxes.jpg' }
      ]
    },
    {
      id: 'r2',
      name: 'R2 Ring Box',
      category: 'Jewellery Ring Boxes',
      width: 47,
      length: 47,
      height: 34,
      size: '47 x 47 / 34 mm',
      priceStructured: 0.58,
      priceLuxe: 1.00,
      structure: 'Square Lid & Base Box',
      inserts: [
        { id: 'opt1', name: 'Option 1 (Single Ring Slot)', type: 'ring-standard', file: 'Inserts/Insert for Ring boxes.jpg' }
      ]
    },
    {
      id: 'r3',
      name: 'R3 Ring Box',
      category: 'Jewellery Ring Boxes',
      width: 58,
      length: 58,
      height: 45,
      size: '58 x 58 / 45 mm',
      priceStructured: 1.15,
      priceLuxe: 1.50,
      structure: 'R3 High-Lid Rigid Construction',
      inserts: [
        { id: 'opt1', name: 'Option 1 (Single Ring Slot)', type: 'ring-standard', file: 'Inserts/Insert for Ring boxes.jpg' },
        { id: 'opt2', name: 'Option 2 (H-Cut / Multi-Ring Slot)', type: 'ring-hcut', file: 'Inserts/Insert for Ring boxes option 2.jpg' }
      ]
    },
    {
      id: 'rlux',
      name: 'RLux Tall Ring Box',
      category: 'Jewellery Ring Boxes',
      width: 70,
      length: 70,
      height: 78,
      size: '70 x 70 / 78 mm',
      priceStructured: 5.00,
      priceLuxe: 7.30,
      structure: 'RLux Luxury Elevated Architecture',
      inserts: [
        { id: 'rlux-format', name: 'RLux Tall Insert Format', type: 'ring-standard', file: 'Inserts/Insert for RLux Tall.jpg' }
      ]
    },

    // Bracelet Box
    {
      id: 'bracelet-box',
      name: 'Bracelet Box',
      category: 'Bracelet Box',
      width: 220,
      length: 42,
      height: 26,
      size: '220 x 42 / 26 mm',
      priceStructured: 1.20,
      priceLuxe: 1.55,
      structure: 'Long Rigid Lid & Base',
      inserts: [
        { id: 'opt1', name: 'Die-Cut Bracelet Slits (Fabric-Laminated Foam)', type: 'bracelet', file: 'Inserts/Insert Barcelet Box 220x42 - 26mm.jpg' }
      ]
    },

    // Jewellery Set Boxes
    {
      id: 'super-small-set',
      name: 'Super Small Set',
      category: 'Jewellery Set Boxes',
      width: 65,
      length: 85,
      height: 27,
      size: '65 x 85 / 27 mm',
      priceStructured: 0.90,
      priceLuxe: 1.10,
      structure: 'Rigid Lid & Base',
      inserts: [
        { id: 'opt1', name: 'Jewellery Set Die-Cut Insert', type: 'set-type1', file: 'Inserts/Insert for Super Small Set.jpg' }
      ]
    },
    {
      id: 'small-set',
      name: 'Small Set (80x80)',
      category: 'Jewellery Set Boxes',
      width: 80,
      length: 80,
      height: 30,
      size: '80 x 80 / 30 mm',
      priceStructured: 1.10,
      priceLuxe: 1.40,
      structure: 'Square Set Box Type 1',
      inserts: [
        { id: 'opt1', name: 'Option 1 (Die-Cut Ring & Earring Slits)', type: 'small-set-opt1', file: 'Inserts/Insert Small Set 80x80 - 30mm and Small Set H 80x80 - 40mm.jpg' },
        { id: 'opt2', name: 'Option 2 (Die-Cut Pendant & Ring Slits)', type: 'small-set-opt2', file: 'Inserts/Insert Small Set 80x80 - 30mm and Small Set H 80x80 - 40mm option 2.jpg' }
      ]
    },
    {
      id: 'small-set-h',
      name: 'Small Set H (80x80 High)',
      category: 'Jewellery Set Boxes',
      width: 80,
      length: 80,
      height: 40,
      size: '80 x 80 / 40 mm',
      priceStructured: 1.30,
      priceLuxe: 1.80,
      structure: 'Square High-Rim Set Box',
      inserts: [
        { id: 'opt1', name: 'Option 1 (Die-Cut Ring & Earring Slits)', type: 'small-set-opt1', file: 'Inserts/Insert Small Set 80x80 - 30mm and Small Set H 80x80 - 40mm.jpg' },
        { id: 'opt2', name: 'Option 2 (Die-Cut Pendant & Ring Slits)', type: 'small-set-opt2', file: 'Inserts/Insert Small Set 80x80 - 30mm and Small Set H 80x80 - 40mm option 2.jpg' }
      ]
    },
    {
      id: 'middle-small-set',
      name: 'Middle Small Set',
      category: 'Jewellery Set Boxes',
      width: 110,
      length: 126,
      height: 30,
      size: '110 x 126 / 30 mm',
      priceStructured: 1.45,
      priceLuxe: 1.86,
      structure: 'Lid & Base Rigid Format',
      inserts: [
        { id: 'opt1', name: 'Jewellery Set Die-Cut Insert', type: 'set-type1', file: 'Inserts/Insert for Middle Small Set.jpg' }
      ]
    },
    {
      id: 'middle-set',
      name: 'Middle Set',
      category: 'Jewellery Set Boxes',
      width: 140,
      length: 180,
      height: 30,
      size: '140 x 180 / 30 mm',
      priceStructured: 2.45,
      priceLuxe: 3.20,
      structure: 'Rectangular Medium Set Architecture',
      inserts: [
        { id: 'opt1', name: 'Jewellery Set Die-Cut Insert', type: 'set-type1', file: 'Inserts/Insert for Middle set.jpg' }
      ]
    },
    {
      id: 'large-square-set',
      name: 'Large Square Set',
      category: 'Jewellery Set Boxes',
      width: 180,
      length: 180,
      height: 30,
      size: '180 x 180 / 30 mm',
      priceStructured: 2.76,
      priceLuxe: 3.60,
      structure: 'Large Square Presentation Box',
      inserts: [
        { id: 'opt1', name: 'Jewellery Set Die-Cut Insert', type: 'set-type1', file: 'Inserts/Insert for Large Squere set.jpg' }
      ]
    },
    {
      id: 'large-rectangle-set',
      name: 'Large Rectangle Set',
      category: 'Jewellery Set Boxes',
      width: 180,
      length: 215,
      height: 30,
      size: '180 x 215 / 30 mm',
      priceStructured: 3.00,
      priceLuxe: 4.00,
      structure: 'Wide Necklace & Tiara Box',
      inserts: [
        { id: 'opt1', name: 'Jewellery Set Die-Cut Insert', type: 'set-type1', file: 'Inserts/Insert for Large rectangle set.jpg' }
      ]
    },
    {
      id: 'large-xl-set',
      name: 'Large XL Set',
      category: 'Jewellery Set Boxes',
      width: 205,
      length: 240,
      height: 60,
      size: '205 x 240 / 60 mm',
      priceStructured: 6.00,
      priceLuxe: 8.50,
      structure: 'Deep XL Luxury Rigid Casket',
      inserts: [
        { id: 'opt1', name: 'Jewellery Set Die-Cut Insert', type: 'set-type1', file: 'Inserts/Insert for XL set.jpg' }
      ]
    },
    {
      id: 'large-xxs-set',
      name: 'Large XXS Set',
      category: 'Jewellery Set Boxes',
      width: 223,
      length: 303,
      height: 30,
      size: '223 x 303 / 30 mm',
      priceStructured: 5.00,
      priceLuxe: 7.50,
      structure: 'Master Suite Presentation Box',
      inserts: [
        { id: 'opt1', name: 'Jewellery Set Die-Cut Insert', type: 'set-type1', file: 'Inserts/Insert for XXL set.jpg' }
      ]
    },

    // Watch Box
    {
      id: 'watch-box',
      name: 'Watch Box',
      category: 'Watch Box',
      width: 100,
      length: 100,
      height: 110,
      size: '100 x 100 / 110 mm',
      priceStructured: 16.00,
      priceLuxe: 18.00,
      structure: 'Watch Box High-Tower Architecture',
      inserts: [
        { id: 'opt1', name: 'Curved Foam Watch Pillow / Holder', type: 'watch-pillow', file: 'Inserts/insert watch box.jpg' }
      ]
    }
  ];

  const MATERIALS_CATALOG = [
    // Textured & Pearl Collection (Price 1)
    { id: 'black-imitlin', name: 'Black Imitlin', category: 'Textured & Pearl', file: 'Size and Material Customization/Black Imitlin.webp' },
    { id: 'black-leatherlike', name: 'Black Leatherlike', category: 'Textured & Pearl', file: 'Size and Material Customization/Black Leatherlike.webp' },
    { id: 'blue-butterfly', name: 'Blue Butterfly', category: 'Textured & Pearl', file: 'Size and Material Customization/Blue Butterfly.webp' },
    { id: 'caramel-pearl', name: 'Caramel Pearl', category: 'Textured & Pearl', file: 'Size and Material Customization/Caramel Pearl.webp' },
    { id: 'castano-imitlin', name: 'Castano Imitlin', category: 'Textured & Pearl', file: 'Size and Material Customization/Castano Imitlin.webp' },
    { id: 'castano-leatherlike', name: 'Castano Leatherlike', category: 'Textured & Pearl', file: 'Size and Material Customization/Castano Leatherlike.webp' },
    { id: 'castano-pearl', name: 'Castano Pearl', category: 'Textured & Pearl', file: 'Size and Material Customization/Castano Pearl.webp' },
    { id: 'cream-imitlin', name: 'Cream Imitlin', category: 'Textured & Pearl', file: 'Size and Material Customization/Cream Imitlin.webp' },
    { id: 'cream-leatherlike', name: 'Cream Leatherlike', category: 'Textured & Pearl', file: 'Size and Material Customization/Cream Leatherlike.webp' },
    { id: 'green-leatherlike', name: 'Green Leatherlike', category: 'Textured & Pearl', file: 'Size and Material Customization/Green Leatherlike.webp' },
    { id: 'light-green-pearl', name: 'Light Green Pearl', category: 'Textured & Pearl', file: 'Size and Material Customization/Light Green Pearl.webp' },
    { id: 'light-purple-pearl', name: 'Light Purple Pearl', category: 'Textured & Pearl', file: 'Size and Material Customization/Light purple pearl.webp' },
    { id: 'orange-pearl', name: 'Orange Pearl', category: 'Textured & Pearl', file: 'Size and Material Customization/Orange Pearl.webp' },
    { id: 'red-butterfly', name: 'Red Butterfly', category: 'Textured & Pearl', file: 'Size and Material Customization/Red Butterfly.webp' },
    { id: 'red-leatherlike', name: 'Red Leatherlike', category: 'Textured & Pearl', file: 'Size and Material Customization/Red Leatherlike.webp' },
    { id: 'teal-pearl', name: 'Teal Pearl', category: 'Textured & Pearl', file: 'Size and Material Customization/Teal Pearl.webp' },
    { id: 'white-diamond', name: 'White Diamond', category: 'Textured & Pearl', file: 'Size and Material Customization/White Diamond.webp' },
    { id: 'white-imitlin', name: 'White Imitlin', category: 'Textured & Pearl', file: 'Size and Material Customization/White Imitlin.webp' },
    { id: 'white-leatherlike', name: 'White Leatherlike', category: 'Textured & Pearl', file: 'Size and Material Customization/White Leatherlike.webp' },

    // Luxe Collection (Price 2)
    { id: 'black-carbon', name: 'Black Carbon', category: 'Luxe', file: 'Size and Material Customization/Black Carbon.webp' },
    { id: 'black-velvet', name: 'Black Velvet', category: 'Luxe', file: 'Size and Material Customization/Black Velvet.webp' },
    { id: 'brown-velvet', name: 'Brown Velvet', category: 'Luxe', file: 'Size and Material Customization/Brown Velvet.webp' },
    { id: 'carbon-cream', name: 'Carbon Cream', category: 'Luxe', file: 'Size and Material Customization/Carbon Cream.webp' },
    { id: 'kraft-velvet', name: 'Kraft Velvet', category: 'Luxe', file: 'Size and Material Customization/Kraft Velvet.webp' },
    { id: 'red-velvet', name: 'Red Velvet', category: 'Luxe', file: 'Size and Material Customization/Red Velvet.webp' }
  ];

  // 3 Official Insert Colors (Black #141210, Dark Brown #3E2B22, Very Light Cream #FAF8F5)
  const INSERT_COLORS = [
    { name: 'Black', hex: '#141210', filterClass: 'insert-filter-black' },
    { name: 'Dark Brown', hex: '#3E2B22', filterClass: 'insert-filter-dark-brown' },
    { name: 'Very Light Cream', hex: '#FAF8F5', filterClass: 'insert-filter-cream' }
  ];

  // --- STATE ---
  let selectedBox = BOX_CATALOG[0]; // Default: R1
  let isSplitMaterialMode = false;  // false = Uniform, true = Lid & Base mix
  let selectedMaterialUniform = MATERIALS_CATALOG[0]; // Black Imitlin
  let selectedMaterialLid = MATERIALS_CATALOG[19];    // Black Carbon
  let selectedMaterialBase = MATERIALS_CATALOG[0];    // Black Imitlin
  let selectedInsert = selectedBox.inserts[0];
  let selectedInsertColor = INSERT_COLORS[0]; // Black

  // Sliding Gallery State
  let galleryTargetSlot = 'uniform'; // 'uniform', 'lid', or 'base'
  let galleryCategory = 'Textured & Pearl';
  let galleryIndex = 0;

  // --- DOM ELEMENTS ---
  const selectBoxSize = document.getElementById('select-box-size');
  
  // Material Mode & Buttons
  const btnModeUniform = document.getElementById('btn-mode-uniform');
  const btnModeSplit = document.getElementById('btn-mode-split');
  const wrapMaterialUniform = document.getElementById('wrap-material-uniform');
  const wrapMaterialSplit = document.getElementById('wrap-material-split');

  const btnOpenGalleryUniform = document.getElementById('btn-open-gallery-uniform');
  const thumbMaterialUniform = document.getElementById('thumb-material-uniform');
  const nameMaterialUniform = document.getElementById('name-material-uniform');
  const tierMaterialUniform = document.getElementById('tier-material-uniform');

  const btnOpenGalleryLid = document.getElementById('btn-open-gallery-lid');
  const thumbMaterialLid = document.getElementById('thumb-material-lid');
  const nameMaterialLid = document.getElementById('name-material-lid');
  const tierMaterialLid = document.getElementById('tier-material-lid');

  const btnOpenGalleryBase = document.getElementById('btn-open-gallery-base');
  const thumbMaterialBase = document.getElementById('thumb-material-base');
  const nameMaterialBase = document.getElementById('name-material-base');
  const tierMaterialBase = document.getElementById('tier-material-base');

  const selectInsertType = document.getElementById('select-insert-type');
  const selectInsertColor = document.getElementById('select-insert-color');
  const inputQty = document.getElementById('input-qty');

  const displayMaterialTier = document.getElementById('display-material-tier');
  const displayUnitPrice = document.getElementById('display-unit-price');
  const displayTotalPrice = document.getElementById('display-total-price');
  const displayActiveModelTag = document.getElementById('display-active-model-tag');

  // Visuals Panel Elements
  const displayBoxDrawingName = document.getElementById('display-box-drawing-name');
  const proportionalSvgContainer = document.getElementById('proportional-svg-container');
  const cardBoxDrawing = document.getElementById('card-box-drawing');

  const displayInsertDrawingName = document.getElementById('display-insert-drawing-name');
  const proportionalInsertContainer = document.getElementById('proportional-insert-container');
  const imgInsertDrawing = document.getElementById('img-insert-drawing');
  const cardInsertDrawing = document.getElementById('card-insert-drawing');
  const insertColorDot = document.getElementById('insert-color-dot');
  const insertColorText = document.getElementById('insert-color-text');

  const displayMaterialPreviewName = document.getElementById('display-material-preview-name');
  const materialPreviewContainer = document.getElementById('material-preview-container');
  const cardMaterialPreview = document.getElementById('card-material-preview');

  // Sliding Photo Gallery Modal Elements
  const modalGalleryOverlay = document.getElementById('modal-gallery-overlay');
  const btnCloseGallery = document.getElementById('btn-close-gallery');
  const tabCatTextured = document.getElementById('tab-cat-textured');
  const tabCatLuxe = document.getElementById('tab-cat-luxe');
  const gallerySlotTarget = document.getElementById('gallery-slot-target');
  
  const btnSlidePrev = document.getElementById('btn-slide-prev');
  const btnSlideNext = document.getElementById('btn-slide-next');
  const slideMainImage = document.getElementById('slide-main-image');
  const slideMaterialName = document.getElementById('slide-material-name');
  const slideMaterialTier = document.getElementById('slide-material-tier');
  const slideCounter = document.getElementById('slide-counter');
  const galleryThumbsStrip = document.getElementById('gallery-thumbs-strip');
  const btnApplySlideMaterial = document.getElementById('btn-apply-slide-material');
  const gallerySliderContainer = document.getElementById('gallery-slider-container');

  // Lightbox Modal Elements
  const modalLightbox = document.getElementById('modal-lightbox');
  const lightboxTitle = document.getElementById('lightbox-title');
  const lightboxSubtitle = document.getElementById('lightbox-subtitle');
  const btnCloseLightbox = document.getElementById('btn-close-lightbox');

  // Actions
  const btnCopySpecs = document.getElementById('btn-copy-specs');
  const btnPrintSpecs = document.getElementById('btn-print-specs');
  const toast = document.getElementById('toast');

  // --- ORDER TRACKING STATE & DOM ELEMENTS ---
  let orderItems = [];
  let editingItemId = null;

  const btnAddToOrder = document.getElementById('btn-add-to-order');
  const btnAddText = document.getElementById('btn-add-text');
  const navOrderTracker = document.getElementById('nav-order-tracker');
  const navOrderCount = document.getElementById('nav-order-count');
  const navOrderTotal = document.getElementById('nav-order-total');
  const orderSummarySection = document.getElementById('order-summary-section');
  const orderItemsBadge = document.getElementById('order-items-badge');
  const orderTableBody = document.getElementById('order-table-body');
  const orderFooterBar = document.getElementById('order-footer-bar');
  const orderGrandQty = document.getElementById('order-grand-qty');
  const orderGrandTotal = document.getElementById('order-grand-total');
  const btnCopyOrder = document.getElementById('btn-copy-order');
  const btnPrintOrder = document.getElementById('btn-print-order');
  const btnClearOrder = document.getElementById('btn-clear-order');

  // Wholesale Volume Discount DOM Elements
  const singleDiscountRow = document.getElementById('single-discount-row');
  const singleDiscountPct = document.getElementById('single-discount-pct');
  const singleDiscountAmount = document.getElementById('single-discount-amount');
  const singleSavingsTag = document.getElementById('single-savings-tag');

  const discountsLiveTag = document.getElementById('discounts-live-tag');
  const tierPill500 = document.getElementById('tier-pill-500');
  const tierPill1000 = document.getElementById('tier-pill-1000');
  const tierPill5000 = document.getElementById('tier-pill-5000');

  const orderGrandSubtotal = document.getElementById('order-grand-subtotal');
  const statDiscountWrap = document.getElementById('stat-discount-wrap');
  const orderDiscountPct = document.getElementById('order-discount-pct');
  const orderDiscountAmount = document.getElementById('order-discount-amount');
  const orderSavingsBadge = document.getElementById('order-savings-badge');

  // Custom Logo & Mold Fee Elements
  const chkCustomLogo = document.getElementById('chk-custom-logo');
  const chkNewLogo = document.getElementById('chk-new-logo');
  const singleMoldFeeRow = document.getElementById('single-mold-fee-row');
  const singleMoldFeeAmount = document.getElementById('single-mold-fee-amount');
  const statMoldWrap = document.getElementById('stat-mold-wrap');
  const orderGrandMold = document.getElementById('order-grand-mold');

  // Logo Upload Elements
  const logoUploadZone = document.getElementById('logo-upload-zone');
  const dropzoneBox = document.getElementById('dropzone-box');
  const inputLogoFile = document.getElementById('input-logo-file');
  const dropzoneUnselected = document.getElementById('dropzone-unselected');
  const dropzoneSelected = document.getElementById('dropzone-selected');
  const logoFileName = document.getElementById('logo-file-name');
  const logoFileSize = document.getElementById('logo-file-size');
  const btnClearLogoFile = document.getElementById('btn-clear-logo-file');
  const modalAttachmentRow = document.getElementById('modal-attachment-row');
  const modalAttachmentStatus = document.getElementById('modal-attachment-status');
  const inputModalLogoFile = document.getElementById('input-modal-logo-file');
  const modalUploadBtnText = document.getElementById('modal-upload-btn-text');
  const btnSendEmail = document.getElementById('btn-send-email');
  const btnResetChoices = document.getElementById('btn-reset-choices');
  const btnClearHeader = document.getElementById('btn-clear-header');

  const STORAGE_KEY = 'blosbox_packaging_order_state_v1';
  let savedLogoFileData = null;
  let currentLogoFile = null;
  let isInitializing = false;

  function dataURLtoFile(dataurl, filename) {
    try {
      const arr = dataurl.split(',');
      const mimeMatch = arr[0].match(/:(.*?);/);
      const mime = mimeMatch ? mimeMatch[1] : 'application/octet-stream';
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], filename, { type: mime });
    } catch (e) {
      return null;
    }
  }

  function formatBytes(bytes) {
    if (!bytes || bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  function saveStateToStorage() {
    if (isInitializing) return;
    try {
      const state = {
        selectedBoxId: selectedBox ? selectedBox.id : null,
        isSplitMaterialMode: isSplitMaterialMode,
        selectedMaterialUniform: selectedMaterialUniform,
        selectedMaterialLid: selectedMaterialLid,
        selectedMaterialBase: selectedMaterialBase,
        selectedInsertId: selectedInsert ? selectedInsert.id : null,
        selectedInsertColorName: selectedInsertColor ? selectedInsertColor.name : null,
        qty: inputQty ? (parseInt(inputQty.value, 10) || 100) : 100,
        hasCustomLogo: chkCustomLogo ? chkCustomLogo.checked : false,
        isNewLogoMold: chkNewLogo ? chkNewLogo.checked : false,
        logoFileData: savedLogoFileData,
        orderItems: orderItems,
        editingItemId: editingItemId,
        clientInfo: {
          name: submitClientName ? submitClientName.value : '',
          email: submitClientEmail ? submitClientEmail.value : '',
          phone: submitClientPhone ? submitClientPhone.value : '',
          country: submitClientCountry ? submitClientCountry.value : '',
          notes: submitClientNotes ? submitClientNotes.value : ''
        }
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (err) {
      console.warn('Failed to save state to localStorage:', err);
    }
  }

  function loadStateFromStorage() {
    function sanitizeLoadedMaterial(mat) {
      if (!mat || !mat.file) return mat;
      mat.file = mat.file.replace(/Finishing Materials\/(?:Structured & Pearl|Luxe)\//g, 'Size and Material Customization/');
      if (isInSubfolder && !mat.file.startsWith('../') && !mat.file.startsWith('http')) {
        mat.file = '../' + mat.file;
      }
      return mat;
    }

    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;
      const state = JSON.parse(raw);
      if (!state) return false;

      // 1. Box Selection
      if (state.selectedBoxId) {
        const foundBox = BOX_CATALOG.find(b => b.id === state.selectedBoxId);
        if (foundBox) {
          selectedBox = foundBox;
          if (selectBoxSize) selectBoxSize.value = selectedBox.id;
          populateInsertsDropdown();
        }
      }

      // 2. Material Mode & Selections
      if (state.isSplitMaterialMode) {
        isSplitMaterialMode = true;
        if (btnModeSplit) btnModeSplit.classList.add('active');
        if (btnModeUniform) btnModeUniform.classList.remove('active');
        if (wrapMaterialUniform) wrapMaterialUniform.style.display = 'none';
        if (wrapMaterialSplit) wrapMaterialSplit.style.display = 'flex';
        if (state.selectedMaterialLid) selectedMaterialLid = sanitizeLoadedMaterial(state.selectedMaterialLid);
        if (state.selectedMaterialBase) selectedMaterialBase = sanitizeLoadedMaterial(state.selectedMaterialBase);
      } else {
        isSplitMaterialMode = false;
        if (btnModeUniform) btnModeUniform.classList.add('active');
        if (btnModeSplit) btnModeSplit.classList.remove('active');
        if (wrapMaterialUniform) wrapMaterialUniform.style.display = 'block';
        if (wrapMaterialSplit) wrapMaterialSplit.style.display = 'none';
        if (state.selectedMaterialUniform) selectedMaterialUniform = sanitizeLoadedMaterial(state.selectedMaterialUniform);
      }

      // 3. Insert & Color Selection
      if (state.selectedInsertId && selectedBox && selectedBox.inserts) {
        const foundInsert = selectedBox.inserts.find(i => i.id === state.selectedInsertId);
        if (foundInsert) {
          selectedInsert = foundInsert;
          if (selectInsertType) selectInsertType.value = selectedInsert.id;
        }
      }
      if (state.selectedInsertColorName) {
        const foundColor = INSERT_COLORS.find(c => c.name === state.selectedInsertColorName);
        if (foundColor) {
          selectedInsertColor = foundColor;
          if (selectInsertColor) selectInsertColor.value = selectedInsertColor.name;
        }
      }

      // 4. Quantity
      if (state.qty && inputQty) {
        inputQty.value = state.qty;
      }

      // 5. Custom Logo & New Logo Checkboxes
      if (chkCustomLogo) chkCustomLogo.checked = !!state.hasCustomLogo;
      if (chkNewLogo) chkNewLogo.checked = !!state.isNewLogoMold;

      // 6. Uploaded Logo File
      if (state.logoFileData && state.logoFileData.name) {
        savedLogoFileData = state.logoFileData;
        if (savedLogoFileData.dataUrl) {
          currentLogoFile = dataURLtoFile(savedLogoFileData.dataUrl, savedLogoFileData.name);
        }
        if (logoFileName) logoFileName.textContent = savedLogoFileData.name;
        if (logoFileSize) logoFileSize.textContent = formatBytes(savedLogoFileData.size);
        if (dropzoneSelected && dropzoneUnselected) {
          dropzoneSelected.style.display = 'flex';
          dropzoneUnselected.style.display = 'none';
        }
        if (modalAttachmentStatus) {
          modalAttachmentStatus.textContent = `${savedLogoFileData.name} (${formatBytes(savedLogoFileData.size)}) — ready to send to order@blosbox.com`;
          modalAttachmentStatus.classList.remove('empty');
        }
        if (modalUploadBtnText) modalUploadBtnText.textContent = 'Change File';
      }

      // 7. Order Items
      if (Array.isArray(state.orderItems)) {
        orderItems = state.orderItems;
      }

      // 8. Edit item id
      if (state.editingItemId) {
        editingItemId = state.editingItemId;
        if (btnAddText) btnAddText.textContent = 'Update Box in Order';
        if (btnAddToOrder) btnAddToOrder.classList.add('btn-update-mode');
      }

      // 9. Client Info
      if (state.clientInfo) {
        if (submitClientName && state.clientInfo.name) submitClientName.value = state.clientInfo.name;
        if (submitClientEmail && state.clientInfo.email) submitClientEmail.value = state.clientInfo.email;
        if (submitClientPhone && state.clientInfo.phone) submitClientPhone.value = state.clientInfo.phone;
        if (submitClientCountry && state.clientInfo.country) submitClientCountry.value = state.clientInfo.country;
        if (submitClientNotes && state.clientInfo.notes) submitClientNotes.value = state.clientInfo.notes;
      }

      return true;
    } catch (err) {
      console.warn('Failed to load state from localStorage:', err);
      return false;
    }
  }

  function handleFileSelection(file) {
    if (!file) return;
    currentLogoFile = file;

    // Read as Data URL so the file survives page reloads
    try {
      const reader = new FileReader();
      reader.onload = (e) => {
        savedLogoFileData = {
          name: file.name,
          size: file.size,
          type: file.type || 'application/octet-stream',
          dataUrl: e.target.result
        };
        saveStateToStorage();
      };
      reader.readAsDataURL(file);
    } catch (err) {
      console.warn('Could not serialize logo file:', err);
    }

    if (dropzoneSelected && dropzoneUnselected) {
      dropzoneSelected.style.display = 'flex';
      dropzoneUnselected.style.display = 'none';
    }
    if (logoFileName) logoFileName.textContent = file.name;
    if (logoFileSize) logoFileSize.textContent = formatBytes(file.size);
    if (modalAttachmentStatus) {
      modalAttachmentStatus.textContent = `${file.name} (${formatBytes(file.size)}) — ready to send to order@blosbox.com`;
      modalAttachmentStatus.classList.remove('empty');
    }
    if (modalUploadBtnText) modalUploadBtnText.textContent = 'Change File';
    showToast(`Logo attached: ${file.name}`);
    saveStateToStorage();
  }

  function clearLogoFile() {
    currentLogoFile = null;
    savedLogoFileData = null;
    if (inputLogoFile) inputLogoFile.value = '';
    if (inputModalLogoFile) inputModalLogoFile.value = '';
    if (dropzoneSelected && dropzoneUnselected) {
      dropzoneSelected.style.display = 'none';
      dropzoneUnselected.style.display = 'flex';
    }
    if (modalAttachmentStatus) {
      const hasNewLogoInOrder = orderItems.some(item => item.isNewLogoMold) || (chkNewLogo && chkNewLogo.checked);
      if (hasNewLogoInOrder) {
        modalAttachmentStatus.textContent = 'New logo stamping mold requested (+€50) — upload logo to send with order';
      } else {
        modalAttachmentStatus.textContent = 'No logo file attached (Optional)';
      }
      modalAttachmentStatus.classList.add('empty');
    }
    if (modalUploadBtnText) modalUploadBtnText.textContent = 'Attach / Upload Logo';
    showToast('Attached logo file removed.');
    saveStateToStorage();
  }

  function toggleLogoUploadVisibility() {
    const isVisible = Boolean(chkNewLogo && chkNewLogo.checked);
    if (logoUploadZone) {
      logoUploadZone.style.display = isVisible ? 'block' : 'none';
    }
  }

  // Submit Order Modal Elements (order@blosbox.com)
  const btnSubmitOrder = document.getElementById('btn-submit-order');
  const modalSubmitOverlay = document.getElementById('modal-submit-overlay');
  const btnCloseSubmitModal = document.getElementById('btn-close-submit-modal');
  const submitOrderForm = document.getElementById('submit-order-form');
  const submitRecapBoxes = document.getElementById('submit-recap-boxes');
  const submitRecapQty = document.getElementById('submit-recap-qty');
  const submitRecapTotal = document.getElementById('submit-recap-total');
  const submitClientName = document.getElementById('submit-client-name');
  const submitClientEmail = document.getElementById('submit-client-email');
  const submitClientPhone = document.getElementById('submit-client-phone');
  const submitClientCountry = document.getElementById('submit-client-country');
  const submitClientNotes = document.getElementById('submit-client-notes');
  const btnSubmitCopyFallback = document.getElementById('btn-submit-copy-fallback');

  // --- WHOLESALE VOLUME DISCOUNT CALCULATION ---
  function getVolumeDiscount(amount) {
    if (amount >= 5000) {
      return { pct: 15, rate: 0.15, label: '15% off total orders over €5,000' };
    } else if (amount >= 1000) {
      return { pct: 10, rate: 0.10, label: '10% off total orders over €1,000' };
    } else if (amount >= 500) {
      return { pct: 5, rate: 0.05, label: '5% off total orders over €500' };
    } else {
      return { pct: 0, rate: 0, label: 'Standard Price' };
    }
  }

  // --- INITIALIZATION ---
  function init() {
    isInitializing = true;
    populateBoxSizesDropdown();
    populateInsertsDropdown();
    const restored = loadStateFromStorage();
    isInitializing = false;
    updateUI();
    renderOrderSummary();
    setupEventListeners();

    // Re-render when language changes
    window.addEventListener('languageChanged', () => {
      populateBoxSizesDropdown();
      populateInsertsDropdown();
      updateUI();
      renderOrderSummary();
    });
  }

  // --- POPULATE 1: SELECT BOX SIZE ---
  function populateBoxSizesDropdown() {
    selectBoxSize.innerHTML = '';
    const categories = ['Jewellery Ring Boxes', 'Bracelet Box', 'Jewellery Set Boxes', 'Watch Box'];

    const catLabels = {
      'Jewellery Ring Boxes': t('cat_ring_boxes', 'Jewellery Ring Boxes'),
      'Bracelet Box': t('cat_bracelet_box', 'Bracelet Box'),
      'Jewellery Set Boxes': t('cat_set_boxes', 'Jewellery Set Boxes'),
      'Watch Box': t('cat_watch_box', 'Watch Box')
    };
    categories.forEach(cat => {
      const group = document.createElement('optgroup');
      group.label = `── ${catLabels[cat] || cat} ──`;

      const boxesInCat = BOX_CATALOG.filter(b => b.category === cat);
      boxesInCat.forEach(box => {
        const opt = document.createElement('option');
        opt.value = box.id;
        opt.textContent = `${box.name}  —  [${box.size}]`;
        group.appendChild(opt);
      });

      selectBoxSize.appendChild(group);
    });

    selectBoxSize.value = selectedBox.id;
  }

  // --- POPULATE 3: SELECT INSERT TYPE ---
  function populateInsertsDropdown() {
    selectInsertType.innerHTML = '';

    if (selectedBox.id === 'watch-box') {
      const opt = document.createElement('option');
      opt.value = 'watch-pillow';
      opt.textContent = 'Custom Watch Pillow / Holder';
      selectInsertType.appendChild(opt);
      selectedInsert = {
        id: 'watch-pillow',
        name: 'Custom Watch Pillow / Holder',
        type: 'watch-pillow',
        file: 'Inserts/insert watch box.jpg'
      };
      selectInsertType.value = 'watch-pillow';
      return;
    }

    selectedBox.inserts.forEach(ins => {
      const opt = document.createElement('option');
      opt.value = ins.id;
      opt.textContent = ins.name;
      selectInsertType.appendChild(opt);
    });

    selectedInsert = selectedBox.inserts[0];
    selectInsertType.value = selectedInsert.id;
  }

  // --- RENDER PROPORTIONAL VECTOR LINE DRAWING (MATCHING EXACT USER SAMPLE) ---
  function renderProportionalLineDrawing(box) {
    if (box.id === 'watch-box') {
      proportionalSvgContainer.innerHTML = `
        <img src="Watch box tecnical drawing.jpg" alt="Watch Box Technical Drawing" style="width: 100%; height: 100%; object-fit: contain; background: #FFFFFF; display: block; border-radius: 2px;">
      `;
      return;
    }

    const W = box.width;
    const L = box.length;
    const H = box.height;

    const cos30 = 0.866025;
    const sin30 = 0.5;

    const projW = (W + L) * cos30;
    const projH = (W + L) * sin30 + H;

    // Scaling so the 3D wireframe box fits with ample clearance for outside dimensions
    const scale = Math.min(230 / projW, 130 / projH);

    const sW = W * scale;
    const sL = L * scale;
    const sH = H * scale;

    // Center reference anchor for front-top corner p2
    const p2x = 160.0;
    const p2y = 80.0;

    // Top lid face vertices (p2 is front-most corner)
    // Left edge (Width W): goes up-and-left from p2 to p3
    const p3x = p2x - sW * cos30;
    const p3y = p2y - sW * sin30;

    // Right edge (Length L): goes up-and-right from p2 to p1
    const p1x = p2x + sL * cos30;
    const p1y = p2y - sL * sin30;

    // Back corner p0
    const p0x = p3x + sL * cos30;
    const p0y = p3y - sL * sin30;

    // Base corners (straight down by sH)
    const b3x = p3x;
    const b3y = p3y + sH;

    const b2x = p2x;
    const b2y = p2y + sH;

    const b1x = p1x;
    const b1y = p1y + sH;

    // Calculate Lid Seam Line
    let lidRatio = 0.35;
    if (box.id === 'r3') lidRatio = 33.0 / 45.0;
    else if (box.id === 'rlux') lidRatio = 60.0 / 78.0;
    else if (box.id === 'watch-box') lidRatio = 85.0 / 110.0;

    const lidH = Math.max(sH * lidRatio, 6.0);
    const l3x = p3x, l3y = p3y + lidH;
    const l2x = p2x, l2y = p2y + lidH;
    const l1x = p1x, l1y = p1y + lidH;

    // 1. Left Dimension Line (Width W: e.g. 41mm)
    // Parallel to b3 -> b2, offset outward into clear area (down & left)
    const distLeft = 32.0;
    const nLx = -sin30;
    const nLy = cos30;

    const dimLx1 = b3x + nLx * distLeft;
    const dimLy1 = b3y + nLy * distLeft;
    const dimLx2 = b2x + nLx * distLeft;
    const dimLy2 = b2y + nLy * distLeft;

    const textLx = (dimLx1 + dimLx2) / 2.0 + nLx * 18.0;
    const textLy = (dimLy1 + dimLy2) / 2.0 + nLy * 18.0 + 5.0;

    // 2. Right Dimension Line (Length L: e.g. 49mm)
    // Parallel to b2 -> b1, offset outward into clear area (down & right)
    const distRight = 32.0;
    const nRx = sin30;
    const nRy = cos30;

    const dimRx1 = b2x + nRx * distRight;
    const dimRy1 = b2y + nRy * distRight;
    const dimRx2 = b1x + nRx * distRight;
    const dimRy2 = b1y + nRy * distRight;

    const textRx = (dimRx1 + dimRx2) / 2.0 + nRx * 18.0;
    const textRy = (dimRy1 + dimRy2) / 2.0 + nRy * 18.0 + 5.0;

    // 3. Height Dimension Line (Height H: e.g. 29mm)
    // Strictly vertical to the right of p1 / b1 in clear area
    const distH = 28.0;
    const dimHx = p1x + distH;
    const dimHy1 = p1y;
    const dimHy2 = b1y;

    const textHx = dimHx + 10.0;
    const textHy = (dimHy1 + dimHy2) / 2.0 + 5.0;

    // Calculate dynamic bounding box encompassing box + all dimensions + text
    const allX = [
      p0x, p1x, p2x, p3x, b1x, b2x, b3x,
      dimLx1, dimLx2, dimRx1, dimRx2, dimHx,
      textLx - 25.0, textLx + 25.0,
      textRx - 25.0, textRx + 25.0,
      textHx, textHx + 45.0
    ];

    const allY = [
      p0y, p1y, p2y, p3y, b1y, b2y, b3y,
      dimLy1, dimLy2, dimRy1, dimRy2, dimHy1, dimHy2,
      textLy - 14.0, textLy + 8.0,
      textRy - 14.0, textRy + 8.0,
      textHy - 14.0, textHy + 8.0
    ];

    const pad = 16.0;
    const minX = Math.floor(Math.min(...allX) - pad);
    const maxX = Math.ceil(Math.max(...allX) + pad);
    const minY = Math.floor(Math.min(...allY) - pad);
    const maxY = Math.ceil(Math.max(...allY) + pad);
    const vbW = maxX - minX;
    const vbH = maxY - minY;

    const svgHTML = `
      <svg viewBox="${minX} ${minY} ${vbW} ${vbH}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%;">
        <defs>
          <marker id="dim-arrow-start" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 8 1.5 L 2 5 L 8 8.5" fill="none" stroke="#222222" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
          </marker>
          <marker id="dim-arrow-end" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 2 1.5 L 8 5 L 2 8.5" fill="none" stroke="#222222" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
          </marker>
        </defs>

        <!-- Front-Left Base Face -->
        <polygon points="${p3x.toFixed(1)},${p3y.toFixed(1)} ${p2x.toFixed(1)},${p2y.toFixed(1)} ${b2x.toFixed(1)},${b2y.toFixed(1)} ${b3x.toFixed(1)},${b3y.toFixed(1)}" fill="#FFFFFF" stroke="#222222" stroke-width="1.4" stroke-linejoin="round"/>

        <!-- Front-Right Base Face -->
        <polygon points="${p1x.toFixed(1)},${p1y.toFixed(1)} ${p2x.toFixed(1)},${p2y.toFixed(1)} ${b2x.toFixed(1)},${b2y.toFixed(1)} ${b1x.toFixed(1)},${b1y.toFixed(1)}" fill="#FFFFFF" stroke="#222222" stroke-width="1.4" stroke-linejoin="round"/>

        <!-- Lid Seam Line (Clean technical dividing line) -->
        <polyline points="${l3x.toFixed(1)},${l3y.toFixed(1)} ${l2x.toFixed(1)},${l2y.toFixed(1)} ${l1x.toFixed(1)},${l1y.toFixed(1)}" fill="none" stroke="#222222" stroke-width="1.4" stroke-linejoin="round"/>

        <!-- Top Lid Face -->
        <polygon points="${p0x.toFixed(1)},${p0y.toFixed(1)} ${p1x.toFixed(1)},${p1y.toFixed(1)} ${p2x.toFixed(1)},${p2y.toFixed(1)} ${p3x.toFixed(1)},${p3y.toFixed(1)}" fill="#FFFFFF" stroke="#222222" stroke-width="1.4" stroke-linejoin="round"/>

        <!-- Width Dimension (Left in clear area) -->
        <line x1="${dimLx1.toFixed(1)}" y1="${dimLy1.toFixed(1)}" x2="${dimLx2.toFixed(1)}" y2="${dimLy2.toFixed(1)}" stroke="#222222" stroke-width="1.1" marker-start="url(#dim-arrow-start)" marker-end="url(#dim-arrow-end)"/>
        <text x="${textLx.toFixed(1)}" y="${textLy.toFixed(1)}" font-family="'Lato', -apple-system, BlinkMacSystemFont, sans-serif" font-size="14" font-weight="400" fill="#1A1A1A" text-anchor="middle">${W}mm</text>

        <!-- Length Dimension (Right in clear area) -->
        <line x1="${dimRx1.toFixed(1)}" y1="${dimRy1.toFixed(1)}" x2="${dimRx2.toFixed(1)}" y2="${dimRy2.toFixed(1)}" stroke="#222222" stroke-width="1.1" marker-start="url(#dim-arrow-start)" marker-end="url(#dim-arrow-end)"/>
        <text x="${textRx.toFixed(1)}" y="${textRy.toFixed(1)}" font-family="'Lato', -apple-system, BlinkMacSystemFont, sans-serif" font-size="14" font-weight="400" fill="#1A1A1A" text-anchor="middle">${L}mm</text>

        <!-- Height Dimension (Vertical Right in clear area) -->
        <line x1="${dimHx.toFixed(1)}" y1="${dimHy1.toFixed(1)}" x2="${dimHx.toFixed(1)}" y2="${dimHy2.toFixed(1)}" stroke="#222222" stroke-width="1.1" marker-start="url(#dim-arrow-start)" marker-end="url(#dim-arrow-end)"/>
        <text x="${textHx.toFixed(1)}" y="${textHy.toFixed(1)}" font-family="'Lato', -apple-system, BlinkMacSystemFont, sans-serif" font-size="14" font-weight="400" fill="#1A1A1A" text-anchor="start">${H}mm</text>
      </svg>
    `;

    proportionalSvgContainer.innerHTML = svgHTML;
  }

  // --- UPDATE EXACT INSERT BLUEPRINT FROM INSERTS FOLDER ---
  function updateInsertDrawing(insert, color) {
    if (!imgInsertDrawing) return;

    // Use the exact drawing file provided by the user in Inserts/
    imgInsertDrawing.src = resolveAsset(insert.file);
    imgInsertDrawing.alt = `${selectedBox.name} - ${insert.name}`;

    // Apply exact SVG filter class directly to the image (No frame/background around container)
    imgInsertDrawing.classList.remove('insert-filter-black', 'insert-filter-dark-brown', 'insert-filter-cream');

    if (selectedBox.id === 'watch-box') {
      // Unique watch insert: not a die-cut sponge, render pure clean technical drawing
      if (proportionalInsertContainer) {
        proportionalInsertContainer.classList.add('watch-insert-frame');
      }
    } else {
      if (proportionalInsertContainer) {
        proportionalInsertContainer.classList.remove('watch-insert-frame');
      }
      imgInsertDrawing.classList.add(color.filterClass);
    }
  }

  // --- POPUP SLIDING GALLERY LOGIC ---
  function getFilteredGalleryMaterials() {
    return MATERIALS_CATALOG.filter(m => m.category === galleryCategory);
  }

  function openSlidingGallery(targetSlot) {
    galleryTargetSlot = targetSlot; // 'uniform', 'lid', or 'base'
    
    // Set target badge text
    if (targetSlot === 'uniform') {
      gallerySlotTarget.textContent = t('calc_mode_uniform', 'Uniform Box');
      galleryCategory = selectedMaterialUniform.category;
    } else if (targetSlot === 'lid') {
      gallerySlotTarget.textContent = t('calc_lid_lbl', 'Lid Material');
      galleryCategory = selectedMaterialLid.category;
    } else if (targetSlot === 'base') {
      gallerySlotTarget.textContent = t('calc_base_lbl', 'Base Material');
      galleryCategory = selectedMaterialBase.category;
    }

    // Set active category tab
    updateCategoryTabsUI();

    // Find index of currently active material in that category
    const activeMat = (targetSlot === 'uniform') ? selectedMaterialUniform : (targetSlot === 'lid' ? selectedMaterialLid : selectedMaterialBase);
    const catList = getFilteredGalleryMaterials();
    const idx = catList.findIndex(m => m.id === activeMat.id);
    galleryIndex = idx >= 0 ? idx : 0;

    renderSlide();
    renderGalleryThumbnails();

    modalGalleryOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeSlidingGallery() {
    modalGalleryOverlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  function updateCategoryTabsUI() {
    if (galleryCategory === 'Textured & Pearl') {
      tabCatTextured.classList.add('active');
      tabCatLuxe.classList.remove('active');
    } else {
      tabCatLuxe.classList.add('active');
      tabCatTextured.classList.remove('active');
    }
  }

  function switchGalleryCategory(cat) {
    galleryCategory = cat;
    galleryIndex = 0;
    updateCategoryTabsUI();
    renderSlide();
    renderGalleryThumbnails();
  }

  function slidePrev() {
    const list = getFilteredGalleryMaterials();
    galleryIndex = (galleryIndex - 1 + list.length) % list.length;
    renderSlide();
  }

  function slideNext() {
    const list = getFilteredGalleryMaterials();
    galleryIndex = (galleryIndex + 1) % list.length;
    renderSlide();
  }

  function renderSlide() {
    const list = getFilteredGalleryMaterials();
    if (galleryIndex < 0 || galleryIndex >= list.length) galleryIndex = 0;
    const currentMat = list[galleryIndex];

    slideMainImage.src = resolveAsset(currentMat.file);
    slideMainImage.alt = currentMat.name;
    slideMaterialName.textContent = currentMat.name;
    slideMaterialTier.textContent = currentMat.category;
    slideCounter.textContent = `${galleryIndex + 1} / ${list.length}`;

    // Highlight thumbnail in strip
    const thumbs = galleryThumbsStrip.querySelectorAll('.gallery-thumb-item');
    thumbs.forEach((t, i) => {
      t.classList.toggle('active', i === galleryIndex);
      if (i === galleryIndex) {
        t.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      }
    });
  }

  function renderGalleryThumbnails() {
    galleryThumbsStrip.innerHTML = '';
    const list = getFilteredGalleryMaterials();

    list.forEach((mat, idx) => {
      const thumb = document.createElement('div');
      thumb.className = `gallery-thumb-item ${idx === galleryIndex ? 'active' : ''}`;
      thumb.innerHTML = `<img src="${resolveAsset(mat.file)}" alt="${mat.name}">`;
      thumb.addEventListener('click', () => {
        galleryIndex = idx;
        renderSlide();
      });
      galleryThumbsStrip.appendChild(thumb);
    });
  }

  function applyCurrentSlideMaterial() {
    const list = getFilteredGalleryMaterials();
    const chosenMat = list[galleryIndex];

    if (galleryTargetSlot === 'uniform') {
      selectedMaterialUniform = chosenMat;
      showToast(`Selected Material: ${chosenMat.name}`);
    } else if (galleryTargetSlot === 'lid') {
      selectedMaterialLid = chosenMat;
      showToast(`Selected Lid Material: ${chosenMat.name}`);
    } else if (galleryTargetSlot === 'base') {
      selectedMaterialBase = chosenMat;
      showToast(`Selected Base Material: ${chosenMat.name}`);
    }

    closeSlidingGallery();
    updateUI();
  }

  // --- CALCULATE UNIT PRICE WITH FORMULA ---
  function calculateUnitPrice(box) {
    if (!isSplitMaterialMode) {
      const isLuxe = selectedMaterialUniform.category === 'Luxe';
      return {
        unitPrice: isLuxe ? box.priceLuxe : box.priceStructured,
        tierLabel: selectedMaterialUniform.category,
        formulaApplied: false
      };
    } else {
      const isLidLuxe = selectedMaterialLid.category === 'Luxe';
      const isBaseLuxe = selectedMaterialBase.category === 'Luxe';

      if (!isLidLuxe && !isBaseLuxe) {
        return {
          unitPrice: box.priceStructured,
          tierLabel: 'Textured & Pearl (Both)',
          formulaApplied: false
        };
      } else if (isLidLuxe && isBaseLuxe) {
        return {
          unitPrice: box.priceLuxe,
          tierLabel: 'Luxe (Both Lid & Base)',
          formulaApplied: false
        };
      } else {
        const comboPrice = (box.priceStructured + box.priceLuxe) * 0.55;
        return {
          unitPrice: comboPrice,
          tierLabel: 'Mixed Tier: (P1 + P2) × 0.55',
          formulaApplied: true
        };
      }
    }
  }

  // --- UPDATE ALL UI ELEMENTS ---
  function updateUI() {
    // 1. Calculate Price based on formula
    const priceInfo = calculateUnitPrice(selectedBox);
    const qty = parseInt(inputQty ? inputQty.value : 100, 10) || 100;
    const boxSubtotal = priceInfo.unitPrice * qty;

    // Check one-time logo mold fee (€50 if new logo checked)
    const isNewLogoMold = chkNewLogo && chkNewLogo.checked;
    const moldFee = isNewLogoMold ? 50.00 : 0;
    if (singleMoldFeeRow) {
      singleMoldFeeRow.style.display = moldFee > 0 ? 'flex' : 'none';
      if (singleMoldFeeAmount) singleMoldFeeAmount.textContent = '+€50.00';
    }

    toggleLogoUploadVisibility();

    // Wholesale volume discount check for current box
    const discount = getVolumeDiscount(boxSubtotal);
    const discountAmount = boxSubtotal * discount.rate;
    const finalPrice = (boxSubtotal - discountAmount) + moldFee;
    const baseTotalWithMold = boxSubtotal + moldFee;

    if (displayMaterialTier) displayMaterialTier.textContent = priceInfo.tierLabel;
    if (displayUnitPrice) displayUnitPrice.textContent = `€${priceInfo.unitPrice.toFixed(2)}`;

    if (discount.pct > 0) {
      if (singleDiscountRow) singleDiscountRow.style.display = 'flex';
      if (singleDiscountPct) singleDiscountPct.textContent = `${discount.pct}%`;
      if (singleDiscountAmount) singleDiscountAmount.textContent = `-€${discountAmount.toFixed(2)}`;
      if (singleSavingsTag) {
        singleSavingsTag.style.display = 'inline-block';
        singleSavingsTag.textContent = `${t("calc_you_save", "You save")} €${discountAmount.toFixed(2)}`;
      }
      if (displayTotalPrice) displayTotalPrice.textContent = `€${finalPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    } else {
      if (singleDiscountRow) singleDiscountRow.style.display = 'none';
      if (singleSavingsTag) singleSavingsTag.style.display = 'none';
      if (displayTotalPrice) displayTotalPrice.textContent = `€${baseTotalWithMold.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    if (displayActiveModelTag) displayActiveModelTag.textContent = `${selectedBox.name} (${selectedBox.size})`;
    if (displayBoxDrawingName) displayBoxDrawingName.textContent = `${selectedBox.name} (${selectedBox.width} x ${selectedBox.length} x ${selectedBox.height} mm)`;

    // Update Insert Card & Controls for Watch Box vs standard boxes
    const isWatchBox = (selectedBox.id === 'watch-box');
    const insertCardTitle = document.getElementById('insert-card-title');
    const watchInsertNotice = document.getElementById('watch-insert-notice');
    const wrapSelectInsertType = document.getElementById('wrap-select-insert-type');
    const wrapSelectInsertColor = document.getElementById('wrap-select-insert-color');

    if (insertCardTitle) {
      insertCardTitle.textContent = isWatchBox ? t('calc_watch_insert_title', 'UNIQUE WATCH INSERT SPECIFICATION') : t('calc_insert_spec_title', 'PROPORTIONAL DIE-CUT FOAM INSERT');
    }

    if (isWatchBox) {
      if (selectInsertType) selectInsertType.disabled = true;
      if (selectInsertColor) {
        selectInsertColor.disabled = true;
        if (!selectInsertColor.querySelector('option[value="email-discussion"]')) {
          const emailOpt = document.createElement('option');
          emailOpt.value = 'email-discussion';
          emailOpt.textContent = t('calc_agreed_email', 'Agreed via Email');
          selectInsertColor.insertBefore(emailOpt, selectInsertColor.firstChild);
        }
        selectInsertColor.value = 'email-discussion';
      }
      if (wrapSelectInsertType) wrapSelectInsertType.classList.add('disabled-select-wrap');
      if (wrapSelectInsertColor) wrapSelectInsertColor.classList.add('disabled-select-wrap');
      if (watchInsertNotice) watchInsertNotice.style.display = 'flex';
    } else {
      if (selectInsertType) selectInsertType.disabled = false;
      if (selectInsertColor) {
        selectInsertColor.disabled = false;
        const emailOpt = selectInsertColor.querySelector('option[value="email-discussion"]');
        if (emailOpt) emailOpt.remove();
        selectInsertColor.value = selectedInsertColor.name;
      }
      if (wrapSelectInsertType) wrapSelectInsertType.classList.remove('disabled-select-wrap');
      if (wrapSelectInsertColor) wrapSelectInsertColor.classList.remove('disabled-select-wrap');
      if (watchInsertNotice) watchInsertNotice.style.display = 'none';
    }

    // 2. Render Exact Proportional Line Drawing (Vector / No Color)
    renderProportionalLineDrawing(selectedBox);

    // 3. Update Insert Blueprint from Inserts/ folder with chosen color
    updateInsertDrawing(selectedInsert, selectedInsertColor);

    if (insertColorDot) insertColorDot.style.background = selectedInsertColor.hex;
    if (insertColorText) insertColorText.textContent = selectedInsertColor.name;

    // 4. Update Form Material Pickers
    if (thumbMaterialUniform) thumbMaterialUniform.src = resolveAsset(selectedMaterialUniform.file);
    if (nameMaterialUniform) nameMaterialUniform.textContent = selectedMaterialUniform.name;
    if (tierMaterialUniform) tierMaterialUniform.textContent = selectedMaterialUniform.category;

    if (thumbMaterialLid) thumbMaterialLid.src = resolveAsset(selectedMaterialLid.file);
    if (nameMaterialLid) nameMaterialLid.textContent = selectedMaterialLid.name;
    if (tierMaterialLid) tierMaterialLid.textContent = selectedMaterialLid.category;

    if (thumbMaterialBase) thumbMaterialBase.src = resolveAsset(selectedMaterialBase.file);
    if (nameMaterialBase) nameMaterialBase.textContent = selectedMaterialBase.name;
    if (tierMaterialBase) tierMaterialBase.textContent = selectedMaterialBase.category;

    // 5. Update Finishing Material Preview Visual Card
    if (!isSplitMaterialMode) {
      displayMaterialPreviewName.textContent = `${selectedMaterialUniform.name} (${selectedMaterialUniform.category})`;
      materialPreviewContainer.innerHTML = `
        <img id="img-material-preview" src="${resolveAsset(selectedMaterialUniform.file)}" alt="${selectedMaterialUniform.name}">
        <div class="drawing-overlay">${t("calc_open_gallery", "🔍 Open Gallery")}</div>
      `;
    } else {
      displayMaterialPreviewName.textContent = `Lid: ${selectedMaterialLid.name} | Base: ${selectedMaterialBase.name}`;
      materialPreviewContainer.innerHTML = `
        <div class="split-material-display">
          <div class="split-mat-half">
            <span class="split-mat-label">Lid: ${selectedMaterialLid.name}</span>
            <img src="${resolveAsset(selectedMaterialLid.file)}" alt="Lid: ${selectedMaterialLid.name}">
          </div>
          <div class="split-mat-half" style="border-left: 2px solid #A48C77;">
            <span class="split-mat-label">Base: ${selectedMaterialBase.name}</span>
            <img src="${resolveAsset(selectedMaterialBase.file)}" alt="Base: ${selectedMaterialBase.name}">
          </div>
        </div>
        <div class="drawing-overlay">${t("calc_change_mix", "🔍 Change Mix")}</div>
      `;
    }

    saveStateToStorage();
  }

  // --- LIGHTBOX MODAL ---
  function openLightbox(title, subtitle, imgSrc, isVector = false, vectorContent = null, filterClass = null) {
    if (imgSrc) imgSrc = resolveAsset(imgSrc);
    if (lightboxTitle) lightboxTitle.textContent = title;
    if (lightboxSubtitle) lightboxSubtitle.textContent = subtitle;
    const body = document.querySelector('.lightbox-body');
    if (!body) return;

    body.className = 'lightbox-body';

    if (isVector && vectorContent) {
      body.innerHTML = `<div class="vector-lightbox-wrap">${vectorContent}</div>`;
    } else {
      const cls = filterClass ? `class="${filterClass}"` : '';
      body.innerHTML = `<img id="lightbox-img" ${cls} src="${imgSrc}" alt="${title}">`;
    }

    if (modalLightbox) {
      modalLightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeLightbox() {
    modalLightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  // --- ORDER TRACKING & SELECTIONS LOGIC ---

  function addCurrentBoxToOrder() {
    const priceInfo = calculateUnitPrice(selectedBox);
    const qty = parseInt(inputQty ? inputQty.value : 100, 10) || 100;
    const boxSubtotal = priceInfo.unitPrice * qty;

    const hasCustomLogo = chkCustomLogo ? chkCustomLogo.checked : false;
    const isNewLogoMold = chkNewLogo ? chkNewLogo.checked : false;
    const moldFee = isNewLogoMold ? 50.00 : 0;
    const lineSubtotal = boxSubtotal + moldFee;
    const attachedLogo = (hasCustomLogo && currentLogoFile) ? { name: currentLogoFile.name, size: currentLogoFile.size } : null;

    const materialConfig = isSplitMaterialMode ? {
      mode: 'split',
      label: 'Combination (Lid & Base)',
      lid: { ...selectedMaterialLid },
      base: { ...selectedMaterialBase },
      tierLabel: priceInfo.tierLabel
    } : {
      mode: 'uniform',
      label: 'Uniform',
      uniform: { ...selectedMaterialUniform },
      tierLabel: priceInfo.tierLabel
    };

    const isWatchBoxOrder = (selectedBox.id === 'watch-box');
    const insertObj = isWatchBoxOrder ? {
      id: 'watch-pillow',
      name: 'Custom Watch Pillow / Holder',
      type: 'watch-pillow',
      file: 'Inserts/insert watch box.jpg'
    } : { ...selectedInsert };

    const insertColorObj = isWatchBoxOrder ? {
      name: 'Agreed via Email',
      hex: '#8C7461',
      filterClass: ''
    } : { ...selectedInsertColor };

    if (editingItemId) {
      const itemIndex = orderItems.findIndex(i => i.id === editingItemId);
      if (itemIndex !== -1) {
        orderItems[itemIndex] = {
          ...orderItems[itemIndex],
          box: { ...selectedBox },
          materialConfig: materialConfig,
          insert: insertObj,
          insertColor: insertColorObj,
          unitPrice: priceInfo.unitPrice,
          qty: qty,
          boxSubtotal: boxSubtotal,
          hasCustomLogo: hasCustomLogo,
          isNewLogoMold: isNewLogoMold,
          moldFee: moldFee,
          logoFile: attachedLogo,
          subtotal: lineSubtotal
        };
        showToast(`Updated ${selectedBox.name} in your order.`);
      }
      editingItemId = null;
      if (btnAddText) btnAddText.textContent = 'Add Box to Order';
      if (btnAddToOrder) btnAddToOrder.classList.remove('btn-update-mode');
    } else {
      const newItem = {
        id: 'order_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
        box: { ...selectedBox },
        materialConfig: materialConfig,
        insert: insertObj,
        insertColor: insertColorObj,
        unitPrice: priceInfo.unitPrice,
        qty: qty,
        boxSubtotal: boxSubtotal,
        hasCustomLogo: hasCustomLogo,
        isNewLogoMold: isNewLogoMold,
        moldFee: moldFee,
        logoFile: attachedLogo,
        subtotal: lineSubtotal
      };
      orderItems.push(newItem);
      showToast(`Added ${selectedBox.name} (${qty} pcs) to order!`);
    }

    renderOrderSummary();

    if (orderItems.length === 1 && orderSummarySection) {
      orderSummarySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function renderOrderSummary() {
    const totalQty = orderItems.reduce((sum, item) => sum + item.qty, 0);
    const boxSubtotalTotal = orderItems.reduce((sum, item) => sum + (item.boxSubtotal !== undefined ? item.boxSubtotal : item.subtotal), 0);
    const totalMoldFee = orderItems.reduce((sum, item) => sum + (item.moldFee || 0), 0);

    // Calculate Wholesale Volume Discount based on Box Subtotal
    const discount = getVolumeDiscount(boxSubtotalTotal);
    const discountAmount = boxSubtotalTotal * discount.rate;
    const grandTotal = (boxSubtotalTotal - discountAmount) + totalMoldFee;

    // Update Wholesale Volume Discounts Card on the right
    if (tierPill500) tierPill500.classList.toggle('active-tier', discount.pct === 5);
    if (tierPill1000) tierPill1000.classList.toggle('active-tier', discount.pct === 10);
    if (tierPill5000) tierPill5000.classList.toggle('active-tier', discount.pct === 15);

    if (discountsLiveTag) {
      if (discount.pct > 0) {
        discountsLiveTag.textContent = `${discount.pct}% ${t('calc_discount_unlocked', 'DISCOUNT UNLOCKED!')}`;
        discountsLiveTag.classList.add('active-discount');
      } else {
        discountsLiveTag.classList.remove('active-discount');
        if (boxSubtotalTotal > 0 && boxSubtotalTotal < 500) {
          const needed = 500 - boxSubtotalTotal;
          discountsLiveTag.textContent = `${t('calc_add_prefix', 'Add')} €${needed.toFixed(2)} ${t('calc_to_save_5', 'to save 5%')}`;
        } else {
          discountsLiveTag.textContent = `${t('calc_tier_lbl', 'Tier:')} 0%`;
        }
      }
    }

    // Navbar Pill
    if (navOrderTracker) {
      if (orderItems.length > 0) {
        navOrderTracker.style.display = 'inline-flex';
        if (navOrderCount) navOrderCount.textContent = `${orderItems.length} Box Type${orderItems.length > 1 ? 's' : ''} (${totalQty.toLocaleString()} pcs)`;
        if (navOrderTotal) {
          navOrderTotal.textContent = `€${grandTotal.toFixed(2)}`;
          if (discount.pct > 0) {
            navOrderTotal.title = `Subtotal: €${boxSubtotalTotal.toFixed(2)} | Saved: €${discountAmount.toFixed(2)}`;
          }
        }
      } else {
        navOrderTracker.style.display = 'none';
      }
    }

    // Badge
    if (orderItemsBadge) {
      orderItemsBadge.textContent = `${orderItems.length} ${t("calc_boxes_count_unit", "Boxes")} Configured`;
    }

    // Grand Totals & Discounts in Footer
    if (orderGrandQty) {
      orderGrandQty.textContent = `${totalQty.toLocaleString()} pcs`;
    }
    if (orderGrandSubtotal) {
      orderGrandSubtotal.textContent = `€${boxSubtotalTotal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
    if (statMoldWrap) {
      if (totalMoldFee > 0) {
        statMoldWrap.style.display = 'flex';
        if (orderGrandMold) orderGrandMold.textContent = `+€${totalMoldFee.toFixed(2)}`;
      } else {
        statMoldWrap.style.display = 'none';
      }
    }
    if (statDiscountWrap) {
      if (discount.pct > 0) {
        statDiscountWrap.style.display = 'flex';
        if (orderDiscountPct) orderDiscountPct.textContent = `${discount.pct}%`;
        if (orderDiscountAmount) orderDiscountAmount.textContent = `-€${discountAmount.toFixed(2)}`;
        if (orderSavingsBadge) orderSavingsBadge.textContent = `${t("calc_you_save", "You save")} €${discountAmount.toFixed(2)}`;
      } else {
        statDiscountWrap.style.display = 'none';
      }
    }
    if (orderGrandTotal) {
      orderGrandTotal.textContent = `€${grandTotal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    if (!orderTableBody) return;

    if (orderItems.length === 0) {
      orderTableBody.innerHTML = `
        <tr class="order-empty-row" id="order-empty-row">
          <td colspan="7">
            <div class="order-empty-state">
              <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
              </svg>
              <p class="empty-title">${t("calc_empty_lead", "No boxes added to your order yet")}</p>
              <p class="empty-desc">${t("calc_empty_hint", "Choose a box type and materials above, then click + Add Box to Order to track your choices.")}</p>
            </div>
          </td>
        </tr>
      `;
      if (orderFooterBar) orderFooterBar.style.display = 'none';
      return;
    }

    if (orderFooterBar) orderFooterBar.style.display = 'flex';

    let html = '';
    orderItems.forEach((item) => {
      const isEditing = (editingItemId === item.id);
      
      let materialHTML = '';
      if (item.materialConfig.mode === 'split') {
        materialHTML = `
          <div class="order-material-cell">
            <div class="order-material-thumbs">
              <img src="${item.materialConfig.lid.file}" alt="Lid" class="order-thumb-mini" title="Lid: ${item.materialConfig.lid.name}">
              <img src="${item.materialConfig.base.file}" alt="Base" class="order-thumb-mini" title="Base: ${item.materialConfig.base.name}">
            </div>
            <div class="order-material-text">
              <span class="order-material-name">Lid: ${item.materialConfig.lid.name}</span>
              <span class="order-material-name">Base: ${item.materialConfig.base.name}</span>
              <span class="order-material-tier-tag">${item.materialConfig.tierLabel}</span>
            </div>
          </div>
        `;
      } else {
        materialHTML = `
          <div class="order-material-cell">
            <div class="order-material-thumbs">
              <img src="${item.materialConfig.uniform.file}" alt="${item.materialConfig.uniform.name}" class="order-thumb-mini">
            </div>
            <div class="order-material-text">
              <span class="order-material-name">${item.materialConfig.uniform.name}</span>
              <span class="order-material-tier-tag">${item.materialConfig.tierLabel}</span>
            </div>
          </div>
        `;
      }

      html += `
        <tr class="${isEditing ? 'editing-row' : ''}" data-id="${item.id}">
          <td class="td-box">
            <div class="order-item-box-title">${item.box.name}</div>
            <div class="order-item-box-dim">${item.box.width} x ${item.box.length} x ${item.box.height} mm (${item.box.size})</div>
            ${item.hasCustomLogo ? `<span class="order-logo-tag ${item.isNewLogoMold ? 'has-mold' : ''}">Hot Foil Logo (Included)${item.isNewLogoMold ? ' • New Mold (+€50)' : ''}${item.logoFile ? ' • 📎 ' + item.logoFile.name : ''}</span>` : ''}
          </td>
          <td class="td-material">
            ${materialHTML}
          </td>
          <td class="td-insert">
            <div class="order-insert-cell">
              <span class="order-insert-color-dot" style="background-color: ${item.insertColor.hex};"></span>
              <div class="order-insert-details">
                <span class="order-insert-name">${item.insert.name}</span>
                <span class="order-insert-color-name" style="${item.box.id === 'watch-box' ? 'color: #8C7461; font-style: italic; font-weight: 600;' : ''}">${item.insertColor.name}</span>
              </div>
            </div>
          </td>
          <td class="td-price">
            <span class="order-price-unit">€${item.unitPrice.toFixed(2)}</span>
          </td>
          <td class="td-qty">
            <div class="order-qty-control">
              <button type="button" class="order-qty-btn btn-qty-minus" data-id="${item.id}">−</button>
              <input type="number" class="order-qty-val input-item-qty" data-id="${item.id}" value="${item.qty}" min="10" step="10">
              <button type="button" class="order-qty-btn btn-qty-plus" data-id="${item.id}">+</button>
            </div>
          </td>
          <td class="td-subtotal">
            <span class="order-subtotal-val">€${item.subtotal.toFixed(2)}</span>
          </td>
          <td class="td-actions">
            <div class="order-actions-cell">
              <button type="button" class="btn-item-action btn-item-edit" data-id="${item.id}" title="Edit this box in configurator">
                <span>✏️ Edit</span>
              </button>
              <button type="button" class="btn-item-action btn-item-delete" data-id="${item.id}" title="Remove box from order">
                <span>🗑️</span>
              </button>
            </div>
          </td>
        </tr>
      `;
    });

    orderTableBody.innerHTML = html;

    // Attach listeners
    orderTableBody.querySelectorAll('.btn-qty-minus').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        const item = orderItems.find(i => i.id === id);
        if (item && item.qty > 10) {
          updateOrderItemQty(id, item.qty - 10);
        }
      });
    });

    orderTableBody.querySelectorAll('.btn-qty-plus').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        const item = orderItems.find(i => i.id === id);
        if (item) {
          updateOrderItemQty(id, item.qty + 10);
        }
      });
    });

    orderTableBody.querySelectorAll('.input-item-qty').forEach(inp => {
      inp.addEventListener('change', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        const val = parseInt(e.currentTarget.value, 10) || 10;
        updateOrderItemQty(id, val);
      });
    });

    orderTableBody.querySelectorAll('.btn-item-edit').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        editOrderItem(id);
      });
    });

    orderTableBody.querySelectorAll('.btn-item-delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        removeOrderItem(id);
      });
    });

    saveStateToStorage();
  }

  function updateOrderItemQty(id, newQty) {
    const item = orderItems.find(i => i.id === id);
    if (!item) return;
    item.qty = Math.max(1, newQty);
    const moldFee = item.isNewLogoMold ? 50.00 : 0;
    item.boxSubtotal = item.unitPrice * item.qty;
    item.subtotal = item.boxSubtotal + moldFee;
    renderOrderSummary();
  }

  function removeOrderItem(id) {
    const item = orderItems.find(i => i.id === id);
    const name = item ? item.box.name : 'Box';
    orderItems = orderItems.filter(i => i.id !== id);
    if (editingItemId === id) {
      editingItemId = null;
      if (btnAddText) btnAddText.textContent = 'Add Box to Order';
      if (btnAddToOrder) btnAddToOrder.classList.remove('btn-update-mode');
    }
    renderOrderSummary();
    showToast(`Removed ${name} from order.`);
  }

  function editOrderItem(id) {
    const item = orderItems.find(i => i.id === id);
    if (!item) return;

    editingItemId = id;
    if (btnAddText) btnAddText.textContent = 'Update Box in Order';
    if (btnAddToOrder) btnAddToOrder.classList.add('btn-update-mode');

    // 1. Box Size
    selectedBox = BOX_CATALOG.find(b => b.id === item.box.id) || selectedBox;
    selectBoxSize.value = selectedBox.id;

    // 2. Inserts
    populateInsertsDropdown();
    selectedInsert = selectedBox.inserts.find(i => i.id === item.insert.id) || selectedBox.inserts[0];
    selectInsertType.value = selectedInsert.id;

    selectedInsertColor = INSERT_COLORS.find(c => c.name === item.insertColor.name) || INSERT_COLORS[0];
    selectInsertColor.value = selectedInsertColor.name;

    // 3. Materials
    if (item.materialConfig.mode === 'split') {
      isSplitMaterialMode = true;
      btnModeSplit.classList.add('active');
      btnModeUniform.classList.remove('active');
      wrapMaterialUniform.style.display = 'none';
      wrapMaterialSplit.style.display = 'flex';
      selectedMaterialLid = item.materialConfig.lid;
      selectedMaterialBase = item.materialConfig.base;
    } else {
      isSplitMaterialMode = false;
      btnModeUniform.classList.add('active');
      btnModeSplit.classList.remove('active');
      wrapMaterialUniform.style.display = 'block';
      wrapMaterialSplit.style.display = 'none';
      selectedMaterialUniform = item.materialConfig.uniform;
    }

    // 4. Quantity
    if (inputQty) inputQty.value = item.qty;

    // 5. Custom Logo Options
    if (chkCustomLogo) chkCustomLogo.checked = !!item.hasCustomLogo;
    if (chkNewLogo) chkNewLogo.checked = !!item.isNewLogoMold;

    updateUI();
    renderOrderSummary();

    const controlsPanel = document.querySelector('.controls-panel');
    if (controlsPanel) controlsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    showToast(`Loaded ${selectedBox.name} into configurator for editing.`);
  }

  function clearAllChoicesAndOrder() {
    // 1. Reset configurator to defaults
    selectedBox = BOX_CATALOG[0];
    if (selectBoxSize) selectBoxSize.value = selectedBox.id;
    populateInsertsDropdown();
    selectedInsert = selectedBox.inserts[0];
    if (selectInsertType) selectInsertType.value = selectedInsert.id;
    selectedInsertColor = INSERT_COLORS[0];
    if (selectInsertColor) selectInsertColor.value = selectedInsertColor.name;

    isSplitMaterialMode = false;
    if (btnModeUniform && btnModeSplit) {
      btnModeUniform.classList.add('active');
      btnModeSplit.classList.remove('active');
    }
    if (wrapMaterialUniform && wrapMaterialSplit) {
      wrapMaterialUniform.style.display = 'block';
      wrapMaterialSplit.style.display = 'none';
    }
    selectedMaterialUniform = MATERIALS_CATALOG[0];
    selectedMaterialLid = MATERIALS_CATALOG[19] || MATERIALS_CATALOG[0];
    selectedMaterialBase = MATERIALS_CATALOG[0];

    if (inputQty) inputQty.value = 100;
    if (chkCustomLogo) chkCustomLogo.checked = false;
    if (chkNewLogo) chkNewLogo.checked = false;

    clearLogoFile();
    savedLogoFileData = null;

    // 2. Reset order items
    orderItems = [];
    editingItemId = null;
    if (btnAddText) btnAddText.textContent = 'Add Box to Order';
    if (btnAddToOrder) btnAddToOrder.classList.remove('btn-update-mode');

    // 3. Clear localStorage
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {}

    updateUI();
    renderOrderSummary();
    showToast('All choices and order items have been cleared.');
  }

  function clearAllOrderItems() {
    clearAllChoicesAndOrder(true);
  }

  // --- COPY SPECIFICATION SUMMARY (COMPLETE MULTI-BOX ORDER OR SINGLE BOX) ---
  function copySpecification() {
    let text = `====================================\n`;
    text += `PRICE CALCULATOR / PACKAGING ORDER FORM\n`;
    text += `BLOSBOX LUXURY PACKAGING MANIFEST\n`;
    text += `====================================\n\n`;

    if (orderItems.length > 0) {
      const totalQty = orderItems.reduce((sum, item) => sum + item.qty, 0);
      const boxSubtotal = orderItems.reduce((sum, item) => sum + (item.boxSubtotal !== undefined ? item.boxSubtotal : item.subtotal), 0);
      const totalMoldFee = orderItems.reduce((sum, item) => sum + (item.moldFee || 0), 0);
      const discount = getVolumeDiscount(boxSubtotal);
      const discountAmount = boxSubtotal * discount.rate;
      const grandTotal = (boxSubtotal - discountAmount) + totalMoldFee;

      text += `ORDER SUMMARY:\n`;
      text += `Total Box Configurations: ${orderItems.length}\n`;
      text += `Total Units: ${totalQty.toLocaleString()} pcs\n`;
      text += `Order Box Subtotal: €${boxSubtotal.toFixed(2)}\n`;
      if (totalMoldFee > 0) {
        text += `One-Time Stamping Mold Fee: +€${totalMoldFee.toFixed(2)}\n`;
      }
      if (discount.pct > 0) {
        text += `Wholesale Volume Discount (${discount.pct}%): -€${discountAmount.toFixed(2)} [You save €${discountAmount.toFixed(2)}]\n`;
      }
      text += `Grand Total: €${grandTotal.toFixed(2)}\n`;
      text += `------------------------------------\n\n`;

      orderItems.forEach((item, idx) => {
        text += `[${idx + 1}] ${item.box.name.toUpperCase()}\n`;
        text += `    Dimensions: ${item.box.width} x ${item.box.length} x ${item.box.height} mm (${item.box.size})\n`;
        text += `    Structure: ${item.box.structure}\n`;
        if (item.materialConfig.mode === 'split') {
          text += `    Material (Lid): ${item.materialConfig.lid.name} [${item.materialConfig.lid.category} Tier]\n`;
          text += `    Material (Base): ${item.materialConfig.base.name} [${item.materialConfig.base.category} Tier]\n`;
          text += `    Material Config: Combination Split (Formula: (P1 + P2) * 0.55)\n`;
        } else {
          text += `    Finishing Material: ${item.materialConfig.uniform.name} [${item.materialConfig.uniform.category} Tier]\n`;
        }
        if (item.box.id === 'watch-box') {
          text += `    Insert Specification: Unique Watch Pillow / Holder (To be confirmed with customer via email)\n`;
        } else {
          text += `    Insert Option: ${item.insert.name}\n`;
          text += `    Insert Fabric Color: ${item.insertColor.name}\n`;
        }
        if (item.hasCustomLogo) {
          text += `    Custom Logo: Hot Foil Stamping (Included in unit price)\n`;
          if (item.isNewLogoMold) {
            text += `    Logo Stamping Mold: New Logo Stamping Mold Fee (+€50.00 one-time fee)\n`;
          }
        }
        text += `    Unit Price: €${item.unitPrice.toFixed(2)} / unit\n`;
        text += `    Quantity: ${item.qty} pcs\n`;
        text += `    Line Subtotal: €${item.subtotal.toFixed(2)}\n\n`;
      });

      text += `====================================\n`;
      text += `SUBTOTAL: €${boxSubtotal.toFixed(2)}\n`;
      if (totalMoldFee > 0) {
        text += `ONE-TIME LOGO MOLD FEE: +€${totalMoldFee.toFixed(2)}\n`;
      }
      if (discount.pct > 0) {
        text += `WHOLESALE DISCOUNT (${discount.pct}%): -€${discountAmount.toFixed(2)} (You save €${discountAmount.toFixed(2)})\n`;
      }
      text += `GRAND TOTAL FOR ALL SELECTIONS: €${grandTotal.toFixed(2)}\n`;
      text += `====================================\n`;
    } else {
      const priceInfo = calculateUnitPrice(selectedBox);
      const qty = parseInt(inputQty.value, 10) || 100;
      const boxSubtotal = priceInfo.unitPrice * qty;
      const isNewMold = chkNewLogo && chkNewLogo.checked;
      const moldFee = isNewMold ? 50.00 : 0;
      const discount = getVolumeDiscount(boxSubtotal);
      const discountAmount = boxSubtotal * discount.rate;
      const totalPrice = (boxSubtotal - discountAmount) + moldFee;

      text += `Box Model: ${selectedBox.name}\n`;
      text += `Dimensions: ${selectedBox.width} x ${selectedBox.length} x ${selectedBox.height} mm (${selectedBox.size})\n`;
      text += `Box Structure: ${selectedBox.structure}\n`;
      if (!isSplitMaterialMode) {
        text += `Finishing Material: ${selectedMaterialUniform.name} [${selectedMaterialUniform.category} Tier]\n`;
      } else {
        text += `Lid Material: ${selectedMaterialLid.name} [${selectedMaterialLid.category} Tier]\n`;
        text += `Base Material: ${selectedMaterialBase.name} [${selectedMaterialBase.category} Tier]\n`;
        text += `Material Configuration: Combination Split (Formula: (P1 + P2) * 0.55)\n`;
      }
      if (selectedBox.id === 'watch-box') {
        text += `Insert Specification: Unique Watch Pillow / Holder (To be confirmed with customer via email)\n`;
      } else {
        text += `Insert: ${selectedInsert.name} (Fabric-Laminated Die-Cut Foam)\n`;
        text += `Insert Fabric Color: ${selectedInsertColor.name}\n`;
      }
      if (chkCustomLogo && chkCustomLogo.checked) {
        text += `Custom Logo: Hot Foil Stamping (Included in unit price)\n`;
        if (isNewMold) {
          text += `Logo Stamping Mold: New Logo Stamping Mold Fee (+€50.00 one-time fee)\n`;
        }
      }
      text += `Unit Price: €${priceInfo.unitPrice.toFixed(2)} / unit\n`;
      text += `Order Quantity: ${qty} pcs\n`;
      text += `Subtotal: €${boxSubtotal.toFixed(2)}\n`;
      if (moldFee > 0) {
        text += `One-Time Logo Mold Fee: +€50.00\n`;
      }
      if (discount.pct > 0) {
        text += `Wholesale Volume Discount (${discount.pct}%): -€${discountAmount.toFixed(2)} (You save €${discountAmount.toFixed(2)})\n`;
      }
      text += `Estimated Total: €${totalPrice.toFixed(2)}\n`;
      text += `====================================\n`;
    }

    navigator.clipboard.writeText(text).then(() => {
      showToast('Complete order manifest copied to clipboard!');
    }).catch(() => {
      showToast('Please copy specifications manually.');
    });
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  }

  // --- SUBMIT ORDER LOGIC (order@blosbox.com) ---

  function openSubmitOrderModal() {
    // If no items registered yet, auto-add current box to order
    if (orderItems.length === 0) {
      addCurrentBoxToOrder();
    }

    const totalBoxes = orderItems.length;
    const totalQty = orderItems.reduce((sum, item) => sum + item.qty, 0);
    const boxSubtotal = orderItems.reduce((sum, item) => sum + (item.boxSubtotal !== undefined ? item.boxSubtotal : item.subtotal), 0);
    const totalMoldFee = orderItems.reduce((sum, item) => sum + (item.moldFee || 0), 0);
    const discount = getVolumeDiscount(boxSubtotal);
    const grandTotal = (boxSubtotal - (boxSubtotal * discount.rate)) + totalMoldFee;

    if (submitRecapBoxes) submitRecapBoxes.textContent = `${totalBoxes} type${totalBoxes > 1 ? 's' : ''}`;
    if (submitRecapQty) submitRecapQty.textContent = `${totalQty.toLocaleString()} pcs`;
    if (submitRecapTotal) submitRecapTotal.textContent = `€${grandTotal.toFixed(2)}`;

    // Update modal attachment status
    if (modalAttachmentStatus) {
      const hasNewLogoInOrder = orderItems.some(item => item.isNewLogoMold) || (chkNewLogo && chkNewLogo.checked);
      if (currentLogoFile) {
        modalAttachmentStatus.textContent = `${currentLogoFile.name} (${formatBytes(currentLogoFile.size)}) — ready to send to order@blosbox.com`;
        modalAttachmentStatus.classList.remove('empty');
        if (modalUploadBtnText) modalUploadBtnText.textContent = 'Change File';
      } else if (hasNewLogoInOrder) {
        modalAttachmentStatus.textContent = 'New logo stamping mold requested (+€50) — upload logo to send with order';
        modalAttachmentStatus.classList.add('empty');
        if (modalUploadBtnText) modalUploadBtnText.textContent = 'Upload Logo';
      } else {
        modalAttachmentStatus.textContent = 'No logo file attached (Optional)';
        modalAttachmentStatus.classList.add('empty');
        if (modalUploadBtnText) modalUploadBtnText.textContent = 'Attach / Upload Logo';
      }
    }

    if (modalSubmitOverlay) {
      modalSubmitOverlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      if (submitClientName) setTimeout(() => submitClientName.focus(), 150);
    }
  }

  function closeSubmitOrderModal() {
    if (modalSubmitOverlay) {
      modalSubmitOverlay.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  function generateOrderManifestText(clientInfo = null) {
    let text = `====================================\n`;
    text += `PRICE CALCULATOR / PACKAGING ORDER FORM\n`;
    text += `BLOSBOX LUXURY PACKAGING MANIFEST\n`;
    text += `====================================\n\n`;

    if (clientInfo) {
      text += `CUSTOMER & DELIVERY DETAILS:\n`;
      text += `- Company / Contact Person: ${clientInfo.name}\n`;
      text += `- Contact Email: ${clientInfo.email}\n`;
      text += `- Phone / WhatsApp: ${clientInfo.phone || 'Not specified'}\n`;
      text += `- Delivery Destination: ${clientInfo.country}\n`;
      text += `- Production / Customization Notes: ${clientInfo.notes || 'None'}\n`;
      text += `====================================\n\n`;
    }

    if (currentLogoFile) {
      text += `ATTACHED LOGO FOR FOIL STAMPING:\n`;
      text += `- File Name: ${currentLogoFile.name} (${formatBytes(currentLogoFile.size)})\n`;
      text += `- Submission: Uploaded and attached to order@blosbox.com submission\n`;
      text += `====================================\n\n`;
    }

    const totalQty = orderItems.reduce((sum, item) => sum + item.qty, 0);
    const boxSubtotal = orderItems.reduce((sum, item) => sum + (item.boxSubtotal !== undefined ? item.boxSubtotal : item.subtotal), 0);
    const totalMoldFee = orderItems.reduce((sum, item) => sum + (item.moldFee || 0), 0);
    const discount = getVolumeDiscount(boxSubtotal);
    const discountAmount = boxSubtotal * discount.rate;
    const grandTotal = (boxSubtotal - discountAmount) + totalMoldFee;

    text += `ORDER SUMMARY:\n`;
    text += `Total Box Configurations: ${orderItems.length}\n`;
    text += `Total Units: ${totalQty.toLocaleString()} pcs\n`;
    text += `Order Box Subtotal: €${boxSubtotal.toFixed(2)}\n`;
    if (totalMoldFee > 0) {
      text += `One-Time Stamping Mold Fee: +€${totalMoldFee.toFixed(2)}\n`;
    }
    if (discount.pct > 0) {
      text += `Wholesale Volume Discount (${discount.pct}%): -€${discountAmount.toFixed(2)} [Customer Savings: €${discountAmount.toFixed(2)}]\n`;
    }
    text += `Grand Total: €${grandTotal.toFixed(2)}\n`;
    text += `------------------------------------\n\n`;

    orderItems.forEach((item, idx) => {
      text += `[${idx + 1}] ${item.box.name.toUpperCase()}\n`;
      text += `    Dimensions: ${item.box.width} x ${item.box.length} x ${item.box.height} mm (${item.box.size})\n`;
      text += `    Structure: ${item.box.structure}\n`;
      if (item.materialConfig.mode === 'split') {
        text += `    Material (Lid): ${item.materialConfig.lid.name} [${item.materialConfig.lid.category} Tier]\n`;
        text += `    Material (Base): ${item.materialConfig.base.name} [${item.materialConfig.base.category} Tier]\n`;
        text += `    Material Config: Combination Split (Formula: (P1 + P2) * 0.55)\n`;
      } else {
        text += `    Finishing Material: ${item.materialConfig.uniform.name} [${item.materialConfig.uniform.category} Tier]\n`;
      }
      if (item.box.id === 'watch-box') {
        text += `    Insert Specification: Unique Watch Pillow / Holder (To be confirmed with customer via email)\n`;
      } else {
        text += `    Insert Option: ${item.insert.name}\n`;
        text += `    Insert Fabric Color: ${item.insertColor.name}\n`;
      }
      if (item.hasCustomLogo) {
        text += `    Custom Logo: Hot Foil Stamping (Included in unit price)\n`;
        if (item.isNewLogoMold) {
          text += `    Logo Stamping Mold: New Logo Stamping Mold Fee (+€50.00 one-time fee)\n`;
        }
      }
      text += `    Unit Price: €${item.unitPrice.toFixed(2)} / unit\n`;
      text += `    Quantity: ${item.qty} pcs\n`;
      text += `    Line Subtotal: €${item.subtotal.toFixed(2)}\n\n`;
    });

    text += `====================================\n`;
    text += `SUBTOTAL: €${boxSubtotal.toFixed(2)}\n`;
    if (totalMoldFee > 0) {
      text += `ONE-TIME LOGO MOLD FEE: +€${totalMoldFee.toFixed(2)}\n`;
    }
    if (discount.pct > 0) {
      text += `WHOLESALE DISCOUNT (${discount.pct}%): -€${discountAmount.toFixed(2)} (You save €${discountAmount.toFixed(2)})\n`;
    }
    text += `GRAND TOTAL FOR ALL SELECTIONS: €${grandTotal.toFixed(2)}\n`;
    text += `====================================\n\n`;
    text += `Please confirm freight shipping timeline and production schedule.\n`;

    return text;
  }

  async function handleOrderSubmit(e) {
    e.preventDefault();

    const clientInfo = {
      name: submitClientName ? submitClientName.value.trim() : 'Customer',
      email: submitClientEmail ? submitClientEmail.value.trim() : '',
      phone: submitClientPhone ? submitClientPhone.value.trim() : '',
      country: submitClientCountry ? submitClientCountry.value.trim() : '',
      notes: submitClientNotes ? submitClientNotes.value.trim() : ''
    };

    const fullManifest = generateOrderManifestText(clientInfo);

    // Copy to clipboard for guaranteed preservation
    navigator.clipboard.writeText(fullManifest).catch(() => {});

    const totalQty = orderItems.reduce((sum, item) => sum + item.qty, 0);
    const boxSubtotal = orderItems.reduce((sum, item) => sum + (item.boxSubtotal !== undefined ? item.boxSubtotal : item.subtotal), 0);
    const totalMoldFee = orderItems.reduce((sum, item) => sum + (item.moldFee || 0), 0);
    const discount = getVolumeDiscount(boxSubtotal);
    const grandTotal = (boxSubtotal - (boxSubtotal * discount.rate)) + totalMoldFee;

    const originalBtnHTML = btnSendEmail ? btnSendEmail.innerHTML : '';
    if (btnSendEmail) {
      btnSendEmail.disabled = true;
      btnSendEmail.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" class="spin">
          <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="12"></circle>
        </svg>
        <span>Sending Order & Logo Attachment...</span>
      `;
    }

    let uploadedFileUrl = '';
    let isServerSubmitted = false;

    // Send multipart/form-data with logo attachment to backend API
    try {
      const formData = new FormData();
      formData.append('clientName', clientInfo.name);
      formData.append('clientEmail', clientInfo.email);
      formData.append('clientPhone', clientInfo.phone);
      formData.append('clientCountry', clientInfo.country);
      formData.append('clientNotes', clientInfo.notes);
      formData.append('orderManifest', fullManifest);
      if (currentLogoFile) {
        formData.append('logoFile', currentLogoFile, currentLogoFile.name);
      }

      const response = await fetch('/api/send-order', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        isServerSubmitted = true;
        if (result.fileUrl) uploadedFileUrl = result.fileUrl;
      }
    } catch (err) {
      console.warn('Direct server submit error, falling back to mailto:', err);
    }

    // Reset button
    if (btnSendEmail) {
      btnSendEmail.disabled = false;
      btnSendEmail.innerHTML = originalBtnHTML;
    }

    // Prepare email client fallback / confirmation
    let finalBody = fullManifest;
    if (uploadedFileUrl) {
      finalBody = `[ATTACHMENT: ${currentLogoFile ? currentLogoFile.name : 'Logo'} uploaded to server and attached for order@blosbox.com]\n\n` + fullManifest;
    }

    const recipient = 'order@blosbox.com';
    const hasLogoTag = currentLogoFile ? ' + Logo Attached' : '';
    const subject = encodeURIComponent(`Packaging Order - ${clientInfo.name} (${totalQty.toLocaleString()} pcs, €${grandTotal.toFixed(2)})${hasLogoTag}`);
    const body = encodeURIComponent(finalBody);
    const mailtoUrl = `mailto:${recipient}?subject=${subject}&body=${body}`;

    if (isServerSubmitted) {
      const attachMsg = currentLogoFile ? ` with logo file "${currentLogoFile.name}" attached` : '';
      showToast(`Order${attachMsg} successfully submitted to order@blosbox.com!`);
    } else {
      showToast('Order manifest & specifications prepared for order@blosbox.com.');
    }

    // Open user's default email client
    window.location.href = mailtoUrl;

    setTimeout(() => {
      closeSubmitOrderModal();
    }, 1500);
  }

  function handleOrderCopyFallback() {
    const clientInfo = {
      name: submitClientName ? (submitClientName.value.trim() || 'Client') : 'Client',
      email: submitClientEmail ? submitClientEmail.value.trim() : '',
      phone: submitClientPhone ? submitClientPhone.value.trim() : '',
      country: submitClientCountry ? submitClientCountry.value.trim() : '',
      notes: submitClientNotes ? submitClientNotes.value.trim() : ''
    };

    const fullManifest = generateOrderManifestText(clientInfo);

    // If logo file attached, queue upload to server in background
    if (currentLogoFile) {
      try {
        const formData = new FormData();
        formData.append('clientName', clientInfo.name);
        formData.append('clientEmail', clientInfo.email);
        formData.append('clientPhone', clientInfo.phone);
        formData.append('clientCountry', clientInfo.country);
        formData.append('clientNotes', clientInfo.notes);
        formData.append('orderManifest', fullManifest);
        formData.append('logoFile', currentLogoFile, currentLogoFile.name);
        fetch('/api/send-order', { method: 'POST', body: formData }).catch(() => {});
      } catch (err) {}
    }

    navigator.clipboard.writeText(fullManifest).then(() => {
      showToast('Full order manifest & contact details copied to clipboard!');
      const totalQty = orderItems.reduce((sum, item) => sum + item.qty, 0);
      const subtotal = orderItems.reduce((sum, item) => sum + item.subtotal, 0);
      const discount = getVolumeDiscount(subtotal);
      const grandTotal = subtotal - (subtotal * discount.rate);

      const subject = encodeURIComponent(`Packaging Order - ${clientInfo.name} (${totalQty.toLocaleString()} pcs, €${grandTotal.toFixed(2)})`);
      const body = encodeURIComponent(fullManifest);
      window.open(`https://mail.google.com/mail/?view=cm&fs=1&to=order@blosbox.com&su=${subject}&body=${body}`, '_blank');
    }).catch(() => {
      showToast('Please copy specifications manually.');
    });
  }

  // --- EVENT LISTENERS ---
  function setupEventListeners() {
    
    // 1. Box Size Dropdown Change
    selectBoxSize.addEventListener('change', (e) => {
      const box = BOX_CATALOG.find(b => b.id === e.target.value);
      if (box) {
        selectedBox = box;
        populateInsertsDropdown();
        updateUI();
      }
    });

    // Material Mode Toggles (Uniform vs Split)
    btnModeUniform.addEventListener('click', () => {
      isSplitMaterialMode = false;
      btnModeUniform.classList.add('active');
      btnModeSplit.classList.remove('active');
      wrapMaterialUniform.style.display = 'block';
      wrapMaterialSplit.style.display = 'none';
      updateUI();
    });

    btnModeSplit.addEventListener('click', () => {
      isSplitMaterialMode = true;
      btnModeSplit.classList.add('active');
      btnModeUniform.classList.remove('active');
      wrapMaterialUniform.style.display = 'none';
      wrapMaterialSplit.style.display = 'flex';
      updateUI();
    });

    // Material Picker Card Buttons -> Open Sliding Gallery
    btnOpenGalleryUniform.addEventListener('click', () => openSlidingGallery('uniform'));
    btnOpenGalleryLid.addEventListener('click', () => openSlidingGallery('lid'));
    btnOpenGalleryBase.addEventListener('click', () => openSlidingGallery('base'));
    cardMaterialPreview.addEventListener('click', () => openSlidingGallery(isSplitMaterialMode ? 'lid' : 'uniform'));

    // Sliding Gallery Category Tabs
    tabCatTextured.addEventListener('click', () => switchGalleryCategory('Textured & Pearl'));
    tabCatLuxe.addEventListener('click', () => switchGalleryCategory('Luxe'));

    // Slide Arrows
    btnSlidePrev.addEventListener('click', slidePrev);
    btnSlideNext.addEventListener('click', slideNext);

    // Apply Button
    btnApplySlideMaterial.addEventListener('click', applyCurrentSlideMaterial);

    // Close Sliding Gallery
    btnCloseGallery.addEventListener('click', closeSlidingGallery);
    modalGalleryOverlay.addEventListener('click', (e) => {
      if (e.target === modalGalleryOverlay) closeSlidingGallery();
    });

    // Touch Swipe Gesture on Gallery Slider (Mobile phone gesture)
    let touchStartX = 0;
    let touchEndX = 0;

    gallerySliderContainer.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    gallerySliderContainer.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });

    function handleSwipe() {
      const threshold = 40;
      if (touchEndX < touchStartX - threshold) {
        // Swiped Left -> Next
        slideNext();
      } else if (touchEndX > touchStartX + threshold) {
        // Swiped Right -> Prev
        slidePrev();
      }
    }

    // Mouse Wheel (Roller) Horizontal Scrolling for Gallery Thumbnails Strip
    const galleryBottomBar = document.querySelector('.gallery-bottom-bar');
    const handleThumbsWheel = (e) => {
      const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (delta !== 0 && galleryThumbsStrip) {
        e.preventDefault();
        galleryThumbsStrip.scrollLeft += delta;
      }
    };

    if (galleryThumbsStrip) {
      galleryThumbsStrip.addEventListener('wheel', handleThumbsWheel, { passive: false });
    }
    if (galleryBottomBar && galleryBottomBar !== galleryThumbsStrip) {
      galleryBottomBar.addEventListener('wheel', handleThumbsWheel, { passive: false });
    }

    // Mouse Wheel on Main Slide Viewport to cycle materials
    let wheelSlideLock = false;
    if (gallerySliderContainer) {
      gallerySliderContainer.addEventListener('wheel', (e) => {
        const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
        if (Math.abs(delta) > 15) {
          e.preventDefault();
          if (wheelSlideLock) return;
          wheelSlideLock = true;
          if (delta > 0) {
            slideNext();
          } else {
            slidePrev();
          }
          setTimeout(() => { wheelSlideLock = false; }, 200);
        }
      }, { passive: false });
    }

    // Keyboard Arrow Keys for Gallery Navigation
    document.addEventListener('keydown', (e) => {
      if (modalGalleryOverlay.classList.contains('open')) {
        if (e.key === 'ArrowLeft') slidePrev();
        if (e.key === 'ArrowRight') slideNext();
        if (e.key === 'Escape') closeSlidingGallery();
        if (e.key === 'Enter') applyCurrentSlideMaterial();
      }
    });

    // 3. Insert Type Dropdown Change
    selectInsertType.addEventListener('change', (e) => {
      const ins = selectedBox.inserts.find(i => i.id === e.target.value);
      if (ins) {
        selectedInsert = ins;
        updateUI();
      }
    });

    // 4. Insert Color Dropdown Change (Black, Dark Brown, Very Light Cream)
    selectInsertColor.addEventListener('change', (e) => {
      const colorObj = INSERT_COLORS.find(c => c.name === e.target.value);
      if (colorObj) {
        selectedInsertColor = colorObj;
      }
      updateUI();
    });

    // Quantity Input Change
    inputQty.addEventListener('input', updateUI);

    // Lightbox Triggers on Drawing Frames (Only triggering on drawing area, not dropdown controls)
    proportionalSvgContainer.addEventListener('click', () => {
      if (selectedBox.id === 'watch-box') {
        openLightbox(
          `${selectedBox.name} — Technical Drawing`,
          `Authentic Technical Blueprint: 100 x 100 mm / Base: 25 mm / Lid: 84 mm`,
          'Watch box tecnical drawing.jpg',
          false,
          null
        );
      } else {
        const svgCode = proportionalSvgContainer.innerHTML;
        openLightbox(
          `${selectedBox.name} - Proportional Vector Blueprint`,
          `Exact dimension wireframe: ${selectedBox.width} x ${selectedBox.length} x ${selectedBox.height} mm`,
          null,
          true,
          svgCode
        );
      }
    });

    proportionalInsertContainer.addEventListener('click', () => {
      if (selectedBox.id === 'watch-box') {
        openLightbox(
          `Watch Box — Unique Watch Pillow Insert`,
          `Custom Watch Insert Structure (Specifications to be confirmed with customer via email)`,
          'Inserts/insert watch box.jpg',
          false,
          null,
          null
        );
      } else {
        openLightbox(
          `${selectedBox.name} — ${selectedInsert.name}`,
          `Exact CAD Insert Blueprint (Color: ${selectedInsertColor.name})`,
          selectedInsert.file,
          false,
          null,
          selectedInsertColor.filterClass
        );
      }
    });

    // Close Lightbox
    btnCloseLightbox.addEventListener('click', closeLightbox);
    modalLightbox.addEventListener('click', (e) => {
      if (e.target === modalLightbox) closeLightbox();
    });

    // Actions
    btnCopySpecs.addEventListener('click', copySpecification);
    btnPrintSpecs.addEventListener('click', () => window.print());

    // Order Tracking Actions
    if (btnAddToOrder) btnAddToOrder.addEventListener('click', addCurrentBoxToOrder);
    if (navOrderTracker) {
      navOrderTracker.addEventListener('click', () => {
        if (orderSummarySection) {
          orderSummarySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }
    if (btnCopyOrder) btnCopyOrder.addEventListener('click', copySpecification);
    if (btnPrintOrder) btnPrintOrder.addEventListener('click', () => window.print());
    if (btnClearOrder) btnClearOrder.addEventListener('click', () => clearAllChoicesAndOrder(false));
    if (btnClearHeader) btnClearHeader.addEventListener('click', () => clearAllChoicesAndOrder(false));
    if (btnResetChoices) btnResetChoices.addEventListener('click', () => clearAllChoicesAndOrder(false));

    // Custom Logo & Stamping Mold Checkboxes
    if (chkCustomLogo) {
      chkCustomLogo.addEventListener('change', () => {
        if (!chkCustomLogo.checked && chkNewLogo) {
          chkNewLogo.checked = false;
        }
        toggleLogoUploadVisibility();
        updateUI();
      });
    }

    if (chkNewLogo) {
      chkNewLogo.addEventListener('change', () => {
        if (chkNewLogo.checked && chkCustomLogo) {
          chkCustomLogo.checked = true;
        }
        toggleLogoUploadVisibility();
        updateUI();
      });
    }

    // Logo File Upload Listeners
    if (dropzoneBox) {
      ['dragenter', 'dragover'].forEach(evt => {
        dropzoneBox.addEventListener(evt, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneBox.classList.add('dragover');
        });
      });

      ['dragleave', 'drop'].forEach(evt => {
        dropzoneBox.addEventListener(evt, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneBox.classList.remove('dragover');
        });
      });

      dropzoneBox.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        if (dt && dt.files && dt.files.length > 0) {
          handleFileSelection(dt.files[0]);
        }
      });
    }

    if (inputLogoFile) {
      inputLogoFile.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
          handleFileSelection(e.target.files[0]);
        }
      });
    }

    if (inputModalLogoFile) {
      inputModalLogoFile.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
          handleFileSelection(e.target.files[0]);
        }
      });
    }

    if (btnClearLogoFile) {
      btnClearLogoFile.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        clearLogoFile();
      });
    }

    // Submit Order to order@blosbox.com Actions
    if (btnSubmitOrder) btnSubmitOrder.addEventListener('click', openSubmitOrderModal);
    if (btnCloseSubmitModal) btnCloseSubmitModal.addEventListener('click', closeSubmitOrderModal);
    if (modalSubmitOverlay) {
      modalSubmitOverlay.addEventListener('click', (e) => {
        if (e.target === modalSubmitOverlay) closeSubmitOrderModal();
      });
    }
    if (submitOrderForm) submitOrderForm.addEventListener('submit', handleOrderSubmit);
    if (btnSubmitCopyFallback) btnSubmitCopyFallback.addEventListener('click', handleOrderCopyFallback);

    [submitClientName, submitClientEmail, submitClientPhone, submitClientCountry, submitClientNotes].forEach(inp => {
      if (inp) inp.addEventListener('input', saveStateToStorage);
    });
  }

  // Start application
  init();
});
