/* Amazon Image Auto — Frontend */

const $ = id => document.getElementById(id);

// ── State ──
let files = [];
let sessionId = null;
let manifest = null;
let apiKey = '';

// ── API Key section ──
const apikeyInput  = $('apikey-input');
const apikeyToggle = $('apikey-toggle');
const apikeySave   = $('apikey-save');
const apikeyStatus = $('apikey-status');
const uploadSection = $('upload-section');

// Restore from sessionStorage (stays for current tab only)
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
  if (!key) {
    showKeyStatus('请输入 API Key', 'error');
    return;
  }
  if (!key.startsWith('AIza')) {
    showKeyStatus('格式不对，Google API Key 通常以 AIza 开头', 'error');
    return;
  }
  sessionStorage.setItem('google_api_key', key);
  activateKey(key);
});

apikeyInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') apikeySave.click();
});

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
const dropZone    = $('drop-zone');
const fileInput   = $('file-input');
const previewGrid = $('preview-grid');
const analyzeBtn  = $('analyze-btn');

dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', e => addFiles([...e.target.files]));

dropZone.addEventListener('dragover', e => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  addFiles([...e.dataTransfer.files].filter(f => f.type.startsWith('image/')));
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
  if (!apiKey) { alert('请先输入 Google API Key'); return; }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = '识别中…';

  const formData = new FormData();
  files.forEach(f => formData.append('files', f));
  formData.append('api_key', apiKey);

  try {
    const res = await fetch('/api/analyze', { method: 'POST', body: formData });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || '识别失败');
    }
    const profile = await res.json();
    sessionId = profile.session_id;
    showDetection(profile);
  } catch (e) {
    alert('识别出错：' + e.message);
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
      <strong>${profile.product_name || '产品'}</strong> ·
      类别：${profile.category || '–'} ·
      材质：${profile.material || '–'} ·
      识别置信度：${confidenceLabel}
    </div>
    <div class="detection-meta" style="font-style:italic;color:#888;">
      ${profile.detection_reason || ''}
    </div>
    <div class="profile-pills">
      ${profile.surface ? `<span class="pill"><strong>表面</strong> ${profile.surface}</span>` : ''}
      ${profile.opacity_percent != null ? `<span class="pill"><strong>透光率</strong> ${profile.opacity_percent}%</span>` : ''}
      ${profile.dimensions_note ? `<span class="pill"><strong>尺寸</strong> ${profile.dimensions_note}</span>` : ''}
      ${colors.length ? `<span class="pill"><strong>色系</strong> ${colorSwatches}</span>` : ''}
      ${(profile.key_features || []).map(f => `<span class="pill">${f}</span>`).join('')}
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
    const event = JSON.parse(e.data);

    if (event.type === 'progress') {
      total = event.total;
      current = event.current;
      const pct = Math.round((current / total) * 100);
      $('progress-bar').style.width = pct + '%';
      $('progress-label').textContent = `${event.step}（${current}/${total}）`;

      const card = document.createElement('div');
      card.className = 'result-card generating';
      card.id = `card-${current}`;
      card.innerHTML = `<img src="" alt="" /><div class="card-label">${event.step}</div>`;
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
      $('progress-label').textContent = '⚠ 错误：' + event.message;
    }
  };

  evtSource.onerror = () => {
    evtSource.close();
    $('progress-label').textContent = '连接中断，请刷新重试';
  };
}

function createCard(event) {
  const card = document.createElement('div');
  card.className = 'result-card';
  card.innerHTML = `<img src="" alt="" /><div class="card-label">${event.label}</div>`;
  $('live-grid').appendChild(card);
  return card;
}

// ── Results ──
function showResults() {
  $('progress-section').classList.add('hidden');
  $('results-section').classList.remove('hidden');

  const files = (manifest && manifest.files) || [];
  $('results-count').textContent = `共 ${files.length} 张图片`;

  const folders = [...new Set(files.map(f => f.folder))];
  const tabBar = $('tab-bar');
  tabBar.innerHTML = '';
  tabBar.appendChild(createTab('全部', 'all', true));
  folders.forEach(folder => tabBar.appendChild(createTab(folderLabel(folder), folder, false)));

  renderResultGrid('all', files);

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

function renderResultGrid(folder, files) {
  const grid = $('result-grid');
  grid.innerHTML = '';
  const filtered = folder === 'all' ? files : files.filter(f => f.folder === folder);
  filtered.forEach(file => {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.style.cursor = 'pointer';
    card.innerHTML = `
      <img src="${file.url}?t=${Date.now()}" alt="${file.label}" loading="lazy" />
      <div class="card-label">${file.label}</div>
      <div class="card-folder">${folderLabel(file.folder)} · ${file.dimensions || ''}</div>
    `;
    card.querySelector('img').addEventListener('click', () => window.open(file.url, '_blank'));
    grid.appendChild(card);
  });
}

function folderLabel(folder) {
  return { 'renders': '白底渲染图', 'lifestyle': '生活场景图', 'amazon-aplus': 'Amazon A+' }[folder] || folder;
}
