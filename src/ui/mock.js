// ===== MOCK API — имитация бэкенда =====
// Перехватываем fetch и возвращаем синтетические данные

// Внутреннее "состояние сервера"
const mockState = {
    inputHotTemp: 85,
    inputColdTemp: 15,
    outputTemp: 25,
    waterLevel: 0,
    valveHot: 50,
    valveCold: 50,
    valveOut: 100,
};

// История для графика (последние 60 точек)
const history = {
    tempGraph: [],
    waterLevelGraph: [],
};

// ===== ИМИТАЦИЯ ФИЗИКИ =====
// Запускаем "симуляцию" — каждые 500мс пересчитываем состояние
setInterval(() => {
    // Притоки (л/условных единиц в секунду)
    const hotFlow = mockState.valveHot / 100;   // 0..1
    const coldFlow = mockState.valveCold / 100;
    const outFlow = mockState.valveOut / 100;

    const totalIn = hotFlow + coldFlow;
    const delta = totalIn - outFlow; // положительный → уровень растёт

    // Уровень воды (0..100)
    mockState.waterLevel = Math.max(0, Math.min(100, mockState.waterLevel + delta * 0.5));

    // Температура смешения: взвешенное среднее по потокам
    if (totalIn > 0.01) {
        const mixedTemp = (hotFlow * mockState.inputHotTemp + coldFlow * mockState.inputColdTemp) / totalIn;
        // Плавно стремимся к смешанной температуре
        mockState.outputTemp += (mixedTemp - mockState.outputTemp) * 0.1;
    } else {
        // Если нет притока — остывает до комнатной
        mockState.outputTemp += (20 - mockState.outputTemp) * 0.02;
    }

    // Небольшой "шум" для живости
    mockState.outputTemp += (Math.random() - 0.5) * 0.2;
    mockState.waterLevel += (Math.random() - 0.5) * 0.1;
    mockState.waterLevel = Math.max(0, Math.min(100, mockState.waterLevel));

    // Копим историю
    history.tempGraph.push({ t: Date.now(), v: mockState.outputTemp });
    history.waterLevelGraph.push({ t: Date.now(), v: mockState.waterLevel });
    if (history.tempGraph.length > 60) history.tempGraph.shift();
    if (history.waterLevelGraph.length > 60) history.waterLevelGraph.shift();
}, 500);

// ===== ПЕРЕХВАТЧИК FETCH =====
const originalFetch = window.fetch;
window.fetch = async function(url, options = {}) {
    const urlStr = String(url);

    // GET /api/v1/data
    if (urlStr.endsWith('/api/v1/data') && (!options.method || options.method === 'GET')) {
        await sleep(50); // имитация сетевой задержки
        return mockResponse({ ...mockState });
    }

    // POST /api/v1/data
    if (urlStr.endsWith('/api/v1/data') && options.method === 'POST') {
        await sleep(50);
        try {
            const body = JSON.parse(options.body);
            const { name, value } = body;
            if (name in mockState) {
                mockState[name] = parseFloat(value);
                return mockResponse(null, 200);
            } else {
                return mockResponse({ error: 'unknown name' }, 400);
            }
        } catch (e) {
            return mockResponse({ error: e.message }, 400);
        }
    }

    // GET /api/v1/graph
    if (urlStr.endsWith('/api/v1/graph')) {
        await sleep(50);
        return mockResponse({
            tempGraph: JSON.stringify(history.tempGraph),
            waterLevelGraph: JSON.stringify(history.waterLevelGraph),
        });
    }

    // Всё остальное — пропускаем к реальному fetch
    return originalFetch(url, options);
};

function mockResponse(body, status = 200) {
    return new Response(JSON.stringify(body), {
        status,
        headers: { 'Content-Type': 'application/json' },
    });
}

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

console.log('🎭 Mock API активирован — бэкенд не нужен');