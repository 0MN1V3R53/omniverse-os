/**
 * OmniDrop™ D2C Storefront - 20-Product Funnel & Attribution Engine
 * Authors: Julian Thorne (ecom_conversion_rate_optimizer) & Marcus Vance (ecom_media_buyer_lead)
 */

let catalog = [];
let activeHeroProduct = null;
let cart = [];
let currentCategory = 'ALL';

// Attribution State (Meta, TikTok, Google)
const attribution = {
    utm_source: getUrlParam('utm_source') || 'meta_advantage_plus',
    utm_medium: getUrlParam('utm_medium') || 'reels_ugc_01',
    utm_campaign: getUrlParam('utm_campaign') || '1k_to_100k_scale',
    fbclid: getUrlParam('fbclid') || 'fb.1.1788363000.ECOM_CONV_01',
    ttclid: getUrlParam('ttclid') || 'tt.1.1788363000.TIKTOK_SHOP_VIRAL'
};

window.addEventListener('DOMContentLoaded', async () => {
    trackPixelEvent('PageView', { attribution: attribution });
    await fetchFullCatalog();
    startUrgencyTimer();
    startViewerTicker();
    startSocialProofLoop();
});

function getUrlParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Marketing Pixel & Conversion API Dispatcher
function trackPixelEvent(eventName, eventData = {}) {
    console.log(`[ATTRIBUTION PIXEL] Event: ${eventName}`, eventData);
    // Simulated Meta Pixel fbq & TikTok Pixel ttq hooks
    if (window.fbq) window.fbq('track', eventName, eventData);
    if (window.ttq) window.ttq.track(eventName, eventData);
}

async function fetchFullCatalog() {
    try {
        const res = await fetch('/api/products');
        catalog = await res.json();
        if (catalog && catalog.length > 0) {
            setHeroProduct(catalog[0]);
            renderGrid(catalog);
            // Default 1 item in cart
            cart.push({ ...catalog[0], qty: 1 });
            updateCartUI();
        }
    } catch (e) {
        console.error('Catalog fetch error:', e);
    }
}

function setHeroProduct(prod) {
    activeHeroProduct = prod;
    document.getElementById('hero-title').innerText = prod.name;
    document.getElementById('hero-subhead').innerText = prod.tagline;
    document.getElementById('hero-price').innerText = `$${prod.price.toFixed(2)}`;
    document.getElementById('hero-compare').innerText = `$${prod.compare_price.toFixed(2)}`;
    document.getElementById('hero-img').src = prod.hero_image;
    document.getElementById('hero-badge').innerText = prod.badge;
    document.getElementById('hero-reviews-text').innerText = `${prod.rating}/5 | ${prod.reviews_count.toLocaleString()} Verified Customer Reviews`;
    document.getElementById('stock-left-count').innerText = `${prod.stock_left} items left in stock`;

    // Render Benefit Bullets
    const bList = document.getElementById('hero-benefit-list');
    bList.innerHTML = '';
    prod.benefits.forEach(b => {
        const li = document.createElement('li');
        li.style.cssText = 'font-size: 13px; color: #e2e8f0; margin-bottom: 8px; list-style: none; display: flex; align-items: center; gap: 10px;';
        li.innerHTML = `<span style="color: #00ff66; font-weight: bold;">✓</span> ${b}`;
        bList.appendChild(li);
    });

    trackPixelEvent('ViewContent', { content_name: prod.name, value: prod.price, currency: 'USD' });
}

function filterCategory(cat) {
    currentCategory = cat;
    document.querySelectorAll('.cat-pill').forEach(el => el.classList.remove('active'));
    event.target.classList.add('active');

    if (cat === 'ALL') {
        renderGrid(catalog);
    } else {
        const filtered = catalog.filter(p => p.category === cat);
        renderGrid(filtered);
    }
}

function renderGrid(products) {
    const grid = document.getElementById('grid-20-container');
    grid.innerHTML = '';

    products.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="card-image-wrap">
                <img src="${p.hero_image}" class="card-img" alt="${p.name}">
                <div class="card-badge">${p.badge}</div>
            </div>
            <div class="card-content">
                <div class="card-category">${p.category}</div>
                <div class="card-title">${p.name}</div>
                <div style="font-size: 11px; color: #ffb800;">★★★★★ <span>${p.rating} (${p.reviews_count})</span></div>
                <div class="card-bottom-row">
                    <div class="card-price-stack">
                        <span class="card-price-now">$${p.price.toFixed(2)}</span>
                        <span class="card-price-old">$${p.compare_price.toFixed(2)}</span>
                    </div>
                    <button class="quick-deal-btn" onclick="addToCart('${p.id}')">+ Add to Cart</button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Shopping Cart Drawer Controls
function toggleCartDrawer(show = true) {
    document.getElementById('cart-drawer-overlay').style.display = show ? 'block' : 'none';
}

function addToCart(prodId) {
    const item = catalog.find(p => p.id === prodId);
    if (!item) return;

    const existing = cart.find(c => c.id === prodId);
    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ ...item, qty: 1 });
    }
    updateCartUI();
    toggleCartDrawer(true);
    trackPixelEvent('AddToCart', { content_name: item.name, value: item.price, currency: 'USD' });
}

function removeFromCart(prodId) {
    cart = cart.filter(c => c.id !== prodId);
    updateCartUI();
}

function updateCartUI() {
    const container = document.getElementById('drawer-items-list');
    container.innerHTML = '';

    let total = 0;
    let totalQty = 0;

    cart.forEach(item => {
        total += item.price * item.qty;
        totalQty += item.qty;

        const row = document.createElement('div');
        row.className = 'cart-item-row';
        row.innerHTML = `
            <img src="${item.hero_image}" class="cart-item-thumb">
            <div class="cart-item-meta">
                <div style="font-weight: 700;">${item.name}</div>
                <div class="cart-item-price">$${item.price.toFixed(2)} x ${item.qty}</div>
            </div>
            <button onclick="removeFromCart('${item.id}')" style="background: none; border: none; color: #ff0055; cursor: pointer; font-weight: bold;">✕</button>
        `;
        container.appendChild(row);
    });

    document.getElementById('cart-total-badge').innerText = totalQty;
    document.getElementById('cart-subtotal-val').innerText = `$${total.toFixed(2)}`;
}

// 1-Click Checkout Modal
function openDirectCheckout() {
    if (!activeHeroProduct) return;
    document.getElementById('checkout-modal-prod-name').innerText = activeHeroProduct.name;
    document.getElementById('checkout-modal-price').innerText = `Total: $${activeHeroProduct.price.toFixed(2)} (Free Express Shipping)`;
    document.getElementById('checkout-modal').style.display = 'flex';
}

function closeDirectCheckout() {
    document.getElementById('checkout-modal').style.display = 'none';
}

async function submitOrder(e) {
    e.preventDefault();
    const btn = document.getElementById('stripe-pay-btn');
    btn.innerText = 'AUTHORIZING APPLE PAY / STRIPE EXPRESS...';

    const email = document.getElementById('checkout-email').value || 'buyer@omniversestore.com';

    try {
        const res = await fetch('/api/order/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_id: activeHeroProduct.id,
                product_name: activeHeroProduct.name,
                price: activeHeroProduct.price,
                email: email,
                attribution: attribution
            })
        });
        const data = await res.json();
        trackPixelEvent('Purchase', { value: activeHeroProduct.price, currency: 'USD', order_id: data.order.order_id });

        btn.innerText = '✓ 1-CLICK PAYMENT VERIFIED!';
        setTimeout(() => {
            closeDirectCheckout();
            toggleCartDrawer(false);
            alert(`🎉 ORDER CONFIRMED! Order ID: ${data.order.order_id}\n\nTracking code generated for ${activeHeroProduct.name}.\nAttributed to: ${attribution.utm_source} (${attribution.utm_campaign})`);
            btn.innerText = 'PAY WITH 1-CLICK STRIPE / APPLE PAY';
        }, 1200);
    } catch (err) {
        btn.innerText = 'PAYMENT FAILED';
    }
}

// Urgency Countdown Timer (3 min 45 sec reset loop)
function startUrgencyTimer() {
    let secsLeft = 225;
    setInterval(() => {
        secsLeft--;
        if (secsLeft <= 0) secsLeft = 240;
        const mins = String(Math.floor(secsLeft / 60)).padStart(2, '0');
        const secs = String(secsLeft % 60).padStart(2, '0');
        const el = document.getElementById('flash-countdown');
        if (el) el.innerText = `${mins}:${secs}`;
    }, 1000);
}

// Viewer Counter
function startViewerTicker() {
    setInterval(() => {
        const count = Math.floor(Math.random() * 16) + 32;
        const el = document.getElementById('live-viewers-tag');
        if (el) el.innerText = `${count} customers are viewing this product right now`;
    }, 4500);
}

// Real-Time Social Proof Toasts
const sampleCustomers = [
    'Sarah L. from Miami, FL',
    'Marcus B. from Los Angeles, CA',
    'Emma W. from London, UK',
    'Liam P. from Toronto, CA',
    'Olivia S. from Sydney, AU'
];

function startSocialProofLoop() {
    setInterval(() => {
        if (!catalog || catalog.length === 0) return;
        const randomCustomer = sampleCustomers[Math.floor(Math.random() * sampleCustomers.length)];
        const randomItem = catalog[Math.floor(Math.random() * catalog.length)];
        const toast = document.getElementById('live-toast');
        if (toast) {
            toast.innerHTML = `<span style="font-size: 18px;">🛍️</span> <div><strong>${randomCustomer}</strong> just bought <em>${randomItem.name}</em> (2m ago)</div>`;
            toast.style.display = 'flex';
            setTimeout(() => { toast.style.display = 'none'; }, 4500);
        }
    }, 11000);
}
