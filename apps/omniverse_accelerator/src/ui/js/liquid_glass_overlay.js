/**
 * Omniverse OS - Liquid Glass Modern macOS Desktop UI Interactions
 * Author: Charlotte Duval (macos_modern_ui_themer)
 */

function launchApp(appName) {
    console.log(`Launching ${appName} via Omniverse Shell...`);
    alert(`Omniverse OS: Fast-launching ${appName} with Metal 2 priority QoS.`);
}

function switchVectorMode(mode) {
    const btn8 = document.getElementById('btn-8bit');
    const btn1024 = document.getElementById('btn-1024bit');
    if (mode === '1024') {
        btn1024.style.background = '#00f0ff';
        btn1024.style.color = '#05080f';
        btn8.style.background = 'transparent';
        btn8.style.color = '#8a99ad';
        fetch('/api/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ setting: 'vector_mode', value: '1024-BIT' })
        });
    } else {
        btn8.style.background = '#00f0ff';
        btn8.style.color = '#05080f';
        btn1024.style.background = 'transparent';
        btn1024.style.color = '#8a99ad';
        fetch('/api/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ setting: 'vector_mode', value: '8-BIT' })
        });
    }
}
