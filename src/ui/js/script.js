// ===== КОНФИГУРАЦИЯ =====
const API_BASE = '/api/v1';
const POLL_INTERVAL = 1000; // мс — частота опроса API

const POLL_INTERVAL_GRAPH = 3000; // мс — частота опроса API/Graph

// Состояние приложения
const state = {
    inputHotTemp: 85,
    inputColdTemp: 15,
    outputTemp: 25,
    waterLevel: 0,
    valveHot: 50,
    valveCold: 50,
    valveOut: 100,
    targetOutputTemp: 25,
};

let warningActive = false;
const WARNING_THRESHOLD_ON = 98;   // показать при >=98%
const WARNING_THRESHOLD_OFF = 95;  // скрыть при <=95%

// Текущий контекст модального окна
let modalContext = null;

// ===== DOM-ЭЛЕМЕНТЫ =====
const $ = (id) => document.getElementById(id);
const statusEl = $('connectionStatus');
const modalOverlay = $('modalOverlay');
const modalTitle = $('modalTitle');
const modalSlider = $('modalSlider');
const sliderValue = $('sliderValue');
const sliderUnit = $('sliderUnit');
const sliderMin = $('sliderMin');
const sliderMax = $('sliderMax');

const graph_im = $('graph_img');
const targetTemp = $('tempTextTarget');

// ===== API =====
async function fetchData() {
    try {
        const res = await fetch(`${API_BASE}/data`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        Object.assign(state, data);
        render();
        setStatus('connected', '● Подключено');
    } catch (err) {
        console.error('Ошибка чтения данных:', err);
        setStatus('error', '● Ошибка соединения');
    }
}

async function fetchGraph() {
    try {
        const res = await fetch(`${API_BASE}/graph`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const imageBlob = await res.blob();
        const imageURL = URL.createObjectURL(imageBlob);

        graph_im.src = imageURL;

        render();
        setStatus('connected', '● Подключено');
    } catch (err) {
        console.error('Ошибка чтения данных:', err);
        setStatus('error', '● Ошибка соединения');
    }
}

async function sendValue(name, value) {
    try {
        const res = await fetch(`${API_BASE}/data`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, value: parseFloat(value) }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return true;
    } catch (err) {
        console.error('Ошибка записи:', err);
        alert(`Не удалось изменить ${name}: ${err.message}`);
        return false;
    }
}

function setStatus(cls, text) {
    statusEl.className = 'status ' + cls;
    statusEl.textContent = text;
}

// ===== РЕНДЕРИНГ =====
function render() {
    // Значения в карточках клапанов
    $('valveHot-value').textContent = state.valveHot.toFixed(0) + '%';
    $('valveCold-value').textContent = state.valveCold.toFixed(0) + '%';
    $('valveOut-value').textContent = state.valveOut.toFixed(0) + '%';
    $('valveHot-percent').textContent = state.valveHot.toFixed(0) + '%';
    $('valveCold-percent').textContent = state.valveCold.toFixed(0) + '%';
    $('valveOut-percent').textContent = state.valveOut.toFixed(0) + '%';

    $('inputHotTemp-value').textContent = state.inputHotTemp.toFixed(1) + ' °C';
    $('inputColdTemp-value').textContent = state.inputColdTemp.toFixed(1) + ' °C';
    $('outputTemp-value').textContent = state.outputTemp.toFixed(1) + ' °C';

    // Поворот ручки клапана пропорционально открытию
    document.querySelectorAll('.valve-card').forEach(card => {
        const valveName = card.dataset.valve;
        if (valveName && state[valveName] !== undefined) {
            const handles = card.querySelectorAll('.valve-handle');
            const angle = (state[valveName] / 100) * 90; // 0° (закрыт) → 90° (открыт)
            handles.forEach(h => h.style.transform = `rotate(${angle}deg)`);
        }
    });

    // Бойлер: уровень воды
    const tankHeight = 290;
    const tankBottom = 395;
    const waterHeight = (state.waterLevel / 100) * tankHeight;
    const waterY = tankBottom - waterHeight;
    const water = $('waterLevel');
    water.setAttribute('height', waterHeight);
    water.setAttribute('y', waterY);

    // Цвет воды зависит от температуры (градиент синий→фиолетовый→красный)
    water.setAttribute('fill', tempToColor(state.outputTemp));

    // Термометр (диапазон 0–100 °C)
    const thermoHeight = 130;
    const thermoBottom = 313;
    const tempClamped = Math.max(0, Math.min(100, state.outputTemp));
    const fillH = (tempClamped / 100) * thermoHeight;
    $('thermoFill').setAttribute('height', fillH);
    $('thermoFill').setAttribute('y', thermoBottom - fillH);
    $('tempText').textContent = state.outputTemp.toFixed(1) + ' °C';

    targetTemp.textContent = state.targetOutputTemp.toFixed(1) + ' °C';

    // Индикатор уровня сбоку
    const levelBarHeight = 260;
    const levelBarBottom = 380;
    const lvlH = (state.waterLevel / 100) * levelBarHeight;
    $('levelBar').setAttribute('height', lvlH);
    $('levelBar').setAttribute('y', levelBarBottom - lvlH);
    $('levelText').textContent = state.waterLevel.toFixed(0) + '%';

    // Скорость анимации потоков зависит от открытия клапанов
    setFlowSpeed('.hot-flow', state.valveHot);
    setFlowSpeed('.cold-flow', state.valveCold);
    setFlowSpeed('.out-flow', state.valveOut);

    // ===== ПРЕДУПРЕЖДЕНИЕ О КРИТИЧЕСКОМ УРОВНЕ =====
    const banner = $('warningBanner');
    if (banner) {
        if (!warningActive && state.waterLevel >= WARNING_THRESHOLD_ON) {
            warningActive = true;
            banner.classList.add('active');
        } else if (warningActive && state.waterLevel <= WARNING_THRESHOLD_OFF) {
            warningActive = false;
            banner.classList.remove('active');
        }
    }
}



// // Для выходной трубы: учитываем и клапан, и уровень воды
// const outFlowEl = document.querySelector('.out-flow');
// if (outFlowEl) {
//     // Если бак пуст ИЛИ клапан закрыт — останавливаем поток
//     if (state.waterLevel < 0.1 || state.valveOut < 0.1) {
//         outFlowEl.style.animationPlayState = 'paused';
//         outFlowEl.style.opacity = '0.2';
//     } else {
//         outFlowEl.style.animationPlayState = 'running';
//         outFlowEl.style.opacity = '0.9';
//         const duration = 2 - (state.valveOut / 100) * 1.5;
//         outFlowEl.style.animationDuration = duration + 's';
//     }
// }

function setFlowSpeed(selector, valvePercent) {
    const el = document.querySelector(selector);
    if (!el) return;
    if (valvePercent < 1) {
        el.style.animationPlayState = 'paused';
        el.style.opacity = '0.2';
    } else {
        el.style.animationPlayState = 'running';
        el.style.opacity = '0.9';
        // Чем больше открыт клапан — тем быстрее поток
        const duration = 2 - (valvePercent / 100) * 1.5; // от 2s до 0.5s
        el.style.animationDuration = duration + 's';
    }
}

function tempToColor(temp) {
    // 0°C → синий, 50°C → фиолетовый, 100°C → красный
    const t = Math.max(0, Math.min(100, temp));
    if (t < 50) {
        // синий → фиолетовый
        const k = t / 50;
        return mixColors('#3498db', '#9b59b6', k);
    } else {
        // фиолетовый → красный
        const k = (t - 50) / 50;
        return mixColors('#9b59b6', '#e74c3c', k);
    }
}

function mixColors(c1, c2, k) {
    const r1 = parseInt(c1.slice(1, 3), 16), g1 = parseInt(c1.slice(3, 5), 16), b1 = parseInt(c1.slice(5, 7), 16);
    const r2 = parseInt(c2.slice(1, 3), 16), g2 = parseInt(c2.slice(3, 5), 16), b2 = parseInt(c2.slice(5, 7), 16);
    const r = Math.round(r1 + (r2 - r1) * k);
    const g = Math.round(g1 + (g2 - g1) * k);
    const b = Math.round(b1 + (b2 - b1) * k);
    return `rgb(${r},${g},${b})`;
}

// ===== МОДАЛЬНОЕ ОКНО =====
document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.target; // valveHot / inputHotTemp / ...
        const type = btn.dataset.type;     // percent / temp

        let title, min, max, unit, current;
        if (type === 'percent') {
            title = `Открытие: ${getDisplayName(target)}`;
            min = 0; max = 100; unit = '%';
            current = state[target];
        } else {
            title = `Температура: ${getDisplayName(target)}`;
            min = state.inputColdTemp; max = state.inputHotTemp; unit = '°C';
            current = state[target];
        }

        modalContext = { target, type };
        modalTitle.textContent = title;
        modalSlider.min = min;
        modalSlider.max = max;
        modalSlider.value = current;
        sliderUnit.textContent = unit;
        sliderMin.textContent = min + unit;
        sliderMax.textContent = max + unit;
        sliderValue.textContent = formatValue(current, type);

        modalOverlay.classList.add('active');
    });
});

function getDisplayName(key) {
    const names = {
        valveHot: 'Горячий вход',
        valveCold: 'Холодный вход',
        valveOut: 'Выход (слив)',
        inputHotTemp: 'Горячий вход',
        inputColdTemp: 'Холодный вход',
        outputTemp: 'Выход (слив)', 
    };
    return names[key] || key;
}

function formatValue(v, type) {
    return type === 'temp' ? v.toFixed(1) : v.toFixed(0);
}

// Ползунок в реальном времени
modalSlider.addEventListener('input', () => {
    sliderValue.textContent = formatValue(parseFloat(modalSlider.value), modalContext.type);
});

// Закрытие
$('modalClose').addEventListener('click', closeModal);
$('btnCancel').addEventListener('click', closeModal);
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
});
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('active')) closeModal();
});

function closeModal() {
    modalOverlay.classList.remove('active');
    modalContext = null;
}

// Применение
$('btnApply').addEventListener('click', async () => {
    if (!modalContext) return;
    const { target, type } = modalContext;
    const value = parseFloat(modalSlider.value);
    const ok = await sendValue(target, value);
    if (ok) {
        // Сразу обновляем локально для отзывчивости
        // state[target] = value;
        // render();
        closeModal();
    }
});

// ===== ЗАПУСК =====
fetchData();
setInterval(fetchData, POLL_INTERVAL);

fetchGraph();
setInterval(fetchGraph, POLL_INTERVAL_GRAPH);
