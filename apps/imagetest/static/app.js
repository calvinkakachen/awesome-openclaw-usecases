/* imagetest — Frontend */

const $ = id => document.getElementById(id);

// ── State ──
let files = [];
let sessionId = null;
let manifest = null;
let apiKey = '';

// ── Error log ──
function logError(context, message, detail = '') {
  const section = $('log-section');
  section.classList.remove('hidden');

  const ts = new Date().toLocaleTimeString('zh-CN', { hour12: false });
  const fullText = `[${ts}] ${context}: ${message}${detail ? '\n' + detail : ''}`;

  const entry = document.createElement('div');
  entry.className = 'log-entry';
  entry.innerHTML = `
    <div class="log-meta">
      <span class="log-ts">${ts}</span>
      <span class="log-ctx">${context}</span>
      <button class="log-copy-btn" title="复制错误信息">复制</button>
    </div>
    <div class="log-msg">${escHtml(message)}</div>
    ${detail ? `<pre class="log-detail">${escHtml(detail)}</pre>` : ''}
  `;

  entry.querySelector('.log-copy-btn').addEventListener('click', () => {
    navigator.clipboard.writeText(fullText).then(() => {
      const btn = entry.querySelector('.log-copy-btn');
      btn.textContent = '已复制 ✓';
      setTimeout(() => { btn.textContent = '复制'; }, 1500);
    });
  });

  $('log-list').prepend(entry);
}

function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

$('log-clear-btn').addEventListener('click', () => {
  $('log-list').innerHTML = '';
  $('log-section').classList.add('hidden');
});

// ── API Key section ──
const apikeyInput   = $('apikey-input');
const apikeyToggle  = $('apikey-toggle');
const apikeySave    = $('apikey-save');
const apikeyStatus  = $('apikey-status');
const uploadSection = $('upload-section');

const saved = sessionStorage.getItem('google_api_key');
if (saved) {
  apikeyInput.value = saved;
  activateKey(saved);
}

apikeyToggle.addEventListener('click', () => {
  const show = apikeyInput.type === 'password';
  apikeyInput.type = show ? 'text' : 'password';
  apikeyToggle.textContent = show ? '隐藏' : '显示';
});

apikeySave.addEventListener('click', () => {
  const key = apikeyInput.value.trim();
  if (!key) { showKeyStatus('请输入 API Key', 'error'); return; }
  if (!key.startsWith('AIza')) {
    showKeyStatus('格式不对，Google API Key 通常以 AIza 开头', 'error'); return;
  }
  sessionStorage.setItem('google_api_key', key);
  activateKey(key);
});

apikeyInput.addEventListener('keydown', e => { if (e.key === 'Enter') apikeySave.click(); });

function activateKey(key) {
  apiKey = key;
  showKeyStatus('✓ API Key 已设置，可以上传图片了', 'ok');
  uploadSection.classList.remove('locked');
}

function showKeyStatus(msg, type) {
  apikeyStatus.textContent = msg;
  apikeyStatus.className = `apikey-status ${type}`;
  apikeyStatus.classList.remove('hidden');
}

// ── Upload section ──
// Drop zone: drag-and-drop only (file dialog is handled by the <label> element directly)
const dropZone    = $('drop-zone');
const fileInput   = $('file-input');
const previewGrid = $('preview-grid');
const analyzeBtn  = $('analyze-btn');

dropZone.addEventListener('dragover', e => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const dropped = [...e.dataTransfer.files].filter(f => f.type.startsWith('image/'));
  if (dropped.length === 0) {
    logError('文件上传', '所选文件不是图片格式', '仅支持 JPG / PNG / WEBP');
    return;
  }
  addFiles(dropped);
});

fileInput.addEventListener('change', e => {
  const selected = [...e.target.files];
  if (selected.length > 0) addFiles(selected);
  // Reset input so same file can be re-selected
  fileInput.value = '';
});

function addFiles(newFiles) {
  files = [...files, ...newFiles];
  renderPreviews();
}

function removeFile(index) {
  files.splice(index, 1);
  renderPreviews();
}

function renderPreviews() {
  previewGrid.innerHTML = '';
  if (files.length === 0) {
    previewGrid.classList.add('hidden');
    analyzeBtn.disabled = true;
    return;
  }
  previewGrid.classList.remove('hidden');
  analyzeBtn.disabled = false;

  files.forEach((file, i) => {
    const item = document.createElement('div');
    item.className = 'preview-item';
    const url = URL.createObjectURL(file);
    item.innerHTML = `
      <img src="${url}" alt="${file.name}" />
      <button class="remove-btn" onclick="removeFile(${i})">✕</button>
    `;
    previewGrid.appendChild(item);
  });
}

// ── Analyze ──
analyzeBtn.addEventListener('click', async () => {
  if (files.length === 0) return;
  if (!apiKey) {
    logError('识别', '未设置 API Key', '请先在顶部输入 Google API Key');
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = '识别中…';

  const formData = new FormData();
  files.forEach(f => formData.append('files', f));
  formData.append('api_key', apiKey);

  try {
    const res = await fetch('/api/analyze', { method: 'POST', body: formData });
    const text = await res.text();
    let body;
    try { body = JSON.parse(text); } catch (_) {
      throw new Error(`服务器返回非 JSON 响应 (HTTP ${res.status}): ${text.slice(0, 300)}`);
    }
    if (!res.ok) {
      throw new Error(body.detail || `HTTP ${res.status}`);
    }
    sessionId = body.session_id;
    showDetection(body);
  } catch (e) {
    logError('识别失败', e.message, e.stack || '');
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = '开始识别';
  }
});

function showDetection(profile) {
  $('upload-section').classList.add('hidden');
  $('detection-section').classList.remove('hidden');

  const type = (profile.product_type || 'unknown').toUpperCase();
  const confidence = profile.confidence || 'medium';
  const confidenceLabel = { high: '高', medium: '中', low: '低' }[confidence] || confidence;
  const typeLabels = {
    COMPOSITE: '贴图合成（薄膜/贴纸）',
    HARDWARE:  '五金配件 3D 建模',
    FABRIC:    '织物悬垂模拟',
    SOLID:     '实体产品 3D 渲染',
  };

  const colors = profile.color_palette || [];
  const colorSwatches = colors.map(c =>
    `<span style="display:inline-block;width:16px;height:16px;background:${c};border-radius:50%;border:1px solid #ccc;vertical-align:middle;"></span>`
  ).join(' ');

  $('detection-result').innerHTML = `
    <div>
      <span class="detection-badge badge-${type}">${typeLabels[type] || type}</span>
    </div>
    <div class="detection-meta">
      <strong>${escHtml(profile.product_name || '产品')}</strong> ·
      类别：${escHtml(profile.category || '–')} ·
      材质：${escHtml(profile.material || '–')} ·
      识别置信度：${confidenceLabel}
    </div>
    <div class="detection-meta" style="font-style:italic;color:#888;">
      ${escHtml(profile.detection_reason || '')}
    </div>
    <div class="profile-pills">
      ${profile.surface ? `<span class="pill"><strong>表面</strong> ${escHtml(profile.surface)}</span>` : ''}
      ${profile.opacity_percent != null ? `<span class="pill"><strong>透光率</strong> ${profile.opacity_percent}%</span>` : ''}
      ${profile.dimensions_note ? `<span class="pill"><strong>尺寸</strong> ${escHtml(profile.dimensions_note)}</span>` : ''}
      ${colors.length ? `<span class="pill"><strong>色系</strong> ${colorSwatches}</span>` : ''}
      ${(profile.key_features || []).map(f => `<span class="pill">${escHtml(f)}</span>`).join('')}
    </div>
  `;
}

// ── Generate ──
$('generate-btn').addEventListener('click', startGeneration);
$('reupload-btn').addEventListener('click', () => {
  files = [];
  sessionId = null;
  renderPreviews();
  $('detection-section').classList.add('hidden');
  $('upload-section').classList.remove('hidden');
  analyzeBtn.textContent = '开始识别';
  analyzeBtn.disabled = true;
});

function startGeneration() {
  if (!sessionId) return;
  $('detection-section').classList.add('hidden');
  $('progress-section').classList.remove('hidden');
  $('live-grid').innerHTML = '';

  const url = `/api/generate/${sessionId}?api_key=${encodeURIComponent(apiKey)}`;
  const evtSource = new EventSource(url);
  let total = 0;
  let current = 0;

  evtSource.onmessage = e => {
    let event;
    try {
      event = JSON.parse(e.data);
    } catch (err) {
      logError('SSE解析', '无法解析服务器消息', e.data);
      return;
    }

    if (event.type === 'progress') {
      total = event.total;
      current = event.current;
      const pct = Math.round((current / total) * 100);
      $('progress-bar').style.width = pct + '%';
      $('progress-label').textContent = `${event.step}（${current}/${total}）`;

      const card = document.createElement('div');
      card.className = 'result-card generating';
      card.id = `card-${current}`;
      card.innerHTML = `<img src="" alt="" /><div class="card-label">${escHtml(event.step)}</div>`;
      $('live-grid').appendChild(card);
    }

    if (event.type === 'image') {
      const card = $('card-' + current) || createCard(event);
      card.classList.remove('generating');
      card.querySelector('img').src = event.url + '?t=' + Date.now();
      card.querySelector('.card-label').textContent = event.label;
      if (!card.querySelector('.card-folder')) {
        card.innerHTML += `<div class="card-folder">${folderLabel(event.folder)}</div>`;
      }
    }

    if (event.type === 'image_error') {
      const card = $('card-' + current);
      if (card) {
        card.classList.remove('generating');
        card.style.background = '#fff0f0';
        card.querySelector('.card-label').textContent = '⚠ 生成失败';
      }
      logError(`图片生成 — ${event.filename || ''}`, event.message || '生成失败');
    }

    if (event.type === 'done') {
      evtSource.close();
      manifest = event.manifest;
      $('progress-bar').style.width = '100%';
      $('progress-label').textContent = '全部完成！';
      setTimeout(showResults, 800);
    }

    if (event.type === 'error') {
      evtSource.close();
      $('progress-label').textContent = '⚠ 生成出错，详见下方日志';
      logError('图集生成', event.message || '未知错误');
    }
  };

  evtSource.onerror = (e) => {
    evtSource.close();
    $('progress-label').textContent = '连接中断，详见下方日志';
    logError('SSE连接', '服务器连接中断', '请检查服务是否正常运行，或刷新页面重试');
  };
}

function createCard(event) {
  const card = document.createElement('div');
  card.className = 'result-card';
  card.innerHTML = `<img src="" alt="" /><div class="card-label">${escHtml(event.label)}</div>`;
  $('live-grid').appendChild(card);
  return card;
}

// ── Results ──
function showResults() {
  $('progress-section').classList.add('hidden');
  $('results-section').classList.remove('hidden');

  const fileList = (manifest && manifest.files) || [];
  $('results-count').textContent = `共 ${fileList.length} 张图片`;

  const folders = [...new Set(fileList.map(f => f.folder))];
  const tabBar = $('tab-bar');
  tabBar.innerHTML = '';
  tabBar.appendChild(createTab('全部', 'all', true));
  folders.forEach(folder => tabBar.appendChild(createTab(folderLabel(folder), folder, false)));

  renderResultGrid('all', fileList);

  $('download-btn').onclick = () => {
    window.location.href = `/api/download/${sessionId}`;
  };
}

function createTab(label, value, active) {
  const btn = document.createElement('button');
  btn.className = 'tab-btn' + (active ? ' active' : '');
  btn.textContent = label;
  btn.onclick = () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderResultGrid(value, (manifest && manifest.files) || []);
  };
  return btn;
}

function renderResultGrid(folder, fileList) {
  const grid = $('result-grid');
  grid.innerHTML = '';
  const filtered = folder === 'all' ? fileList : fileList.filter(f => f.folder === folder);
  filtered.forEach(file => {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.style.cursor = 'pointer';
    card.innerHTML = `
      <img src="${file.url}?t=${Date.now()}" alt="${escHtml(file.label)}" loading="lazy" />
      <div class="card-label">${escHtml(file.label)}</div>
      <div class="card-folder">${folderLabel(file.folder)} · ${file.dimensions || ''}</div>
    `;
    card.querySelector('img').addEventListener('click', () => window.open(file.url, '_blank'));
    grid.appendChild(card);
  });
}

function folderLabel(folder) {
  return { 'renders': '白底渲染图', 'lifestyle': '生活场景图', 'amazon-aplus': 'Amazon A+' }[folder] || folder;
}
