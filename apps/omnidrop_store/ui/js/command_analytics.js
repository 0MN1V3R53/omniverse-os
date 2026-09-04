/**
 * OmniDrop Executive Command Center - Real-Time Ledger Analytics
 * Author: Marcus Vance & Maya Lin
 */

window.addEventListener('DOMContentLoaded', async () => {
    await fetchAnalytics();
    await fetchCatalogTable();
    setInterval(fetchAnalytics, 2500);
});

async function fetchAnalytics() {
    try {
        const res = await fetch('/api/analytics');
        const data = await res.json();
        
        document.getElementById('kpi-rev').innerText = `$${data.total_revenue.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpi-roas').innerText = data.blended_roas;
        document.getElementById('kpi-profit').innerText = `$${data.net_profit.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpi-margin').innerText = `${data.net_profit_margin} Net Margin`;
        document.getElementById('kpi-orders').innerText = data.total_orders;
        document.getElementById('goal-progress').innerText = `${data.goal_progress_pct}% ($1k -> $100k Target)`;
        document.getElementById('progress-bar-fill').style.width = `${Math.min(data.goal_progress_pct, 100)}%`;

        // Render Recent Ledger Transactions
        renderRecentTransactions(data.recent_orders || []);
    } catch (e) {
        console.error('Analytics fetch error:', e);
    }
}

function renderRecentTransactions(orders) {
    const list = document.getElementById('recent-orders-list');
    if (!list) return;

    if (orders.length === 0) {
        list.innerHTML = `<div style="color: var(--text-muted); font-size: 12px; text-align: center; padding: 20px 0;">No transactions yet. Ledger initialized at $0.00. Place an order on the storefront to test live recording.</div>`;
        return;
    }

    list.innerHTML = '';
    orders.slice().reverse().forEach(o => {
        const row = document.createElement('div');
        row.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(0,240,255,0.15); border-radius: 6px; font-size: 11px; margin-bottom: 6px;';
        row.innerHTML = `
            <div>
                <strong>${o.order_id}</strong> — <span style="color: #00f0ff;">${o.product_name}</span><br>
                <span style="color: var(--text-muted);">${o.timestamp} • ${o.customer_email}</span>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: bold; color: #fff;">$${o.gross_amount.toFixed(2)}</div>
                <div style="color: #00ff66; font-size: 10px;">Net Profit: +$${o.net_profit.toFixed(2)}</div>
            </div>
        `;
        list.appendChild(row);
    });
}

async function fetchCatalogTable() {
    try {
        const res = await fetch('/api/products');
        const prods = await res.json();
        const tbody = document.getElementById('catalog-table-body');
        tbody.innerHTML = '';

        prods.forEach((p, idx) => {
            const tr = document.createElement('tr');
            const pillClass = p.status === 'HERO_WINNER' ? 'pill-hero' : 'pill-scaling';
            tr.innerHTML = `
                <td><strong>#${idx + 1}</strong></td>
                <td><strong>${p.name}</strong><br><span style="font-size: 10px; color: #8292a6;">${p.category}</span></td>
                <td>$${p.cogs.toFixed(2)}</td>
                <td>$${p.price.toFixed(2)}</td>
                <td style="color: #00ff66; font-weight: bold;">$${p.gross_margin.toFixed(2)} (${p.margin_pct})</td>
                <td>${p.weekly_volume.toLocaleString()} /wk</td>
                <td><span class="status-pill ${pillClass}">${p.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error('Catalog table error:', e);
    }
}

async function triggerEvaluator() {
    const btn = document.getElementById('eval-btn');
    btn.innerText = 'EVALUATING REAL LEDGER CONVERSIONS...';
    try {
        const res = await fetch('/api/rotator/evaluate', { method: 'POST' });
        const data = await res.json();
        btn.innerText = '✓ REAL PORTFOLIO SYNCHRONIZED';
        setTimeout(() => {
            btn.innerText = '⚡ EXECUTE 48H EVALUATION & AUTO-PRUNE';
        }, 2000);
        await fetchCatalogTable();
        await fetchAnalytics();
    } catch (e) {
        btn.innerText = 'EVALUATION FAILED';
        setTimeout(() => { btn.innerText = '⚡ EXECUTE 48H EVALUATION & AUTO-PRUNE'; }, 2000);
    }
}

async function testSimulatedTransaction() {
    const btn = document.getElementById('test-order-btn');
    btn.innerText = 'PROCESSING STRIPE TRANSACTION...';
    try {
        const res = await fetch('/api/order/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_id: 'luminaglow-pro',
                product_name: 'LuminaGlow™ Pro 4-in-1 Red Light Facial Sculptor',
                price: 49.95,
                email: 'direct_buyer@omniversestore.com',
                shipping_address: '120 Broadway, New York, NY 10271',
                attribution: { utm_source: 'tiktok_shop_viral', utm_campaign: '1k_to_100k_scale' }
            })
        });
        const data = await res.json();
        btn.innerText = '✓ ORDER RECORDED IN LEDGER!';
        setTimeout(() => {
            btn.innerText = '⚡ SIMULATE REAL ORDER (+$49.95)';
        }, 1500);
        await fetchAnalytics();
    } catch (e) {
        btn.innerText = 'ERROR';
    }
}
