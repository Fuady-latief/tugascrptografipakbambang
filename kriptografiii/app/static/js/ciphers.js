// ===================================================================
// Ciphers Controller (Bagian A - 7 Kriptosistem)
// ===================================================================

const Ciphers = {
  currentCipher: 'shift',

  init() {
    this.bindPills();
    this.renderKeyInput();
    this.bindActions();
  },

  bindPills() {
    const pills = document.querySelectorAll('.cipher-pill');
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.currentCipher = pill.dataset.cipher;
        this.renderKeyInput();
        this.clearResult();
      });
    });
  },

  renderKeyInput() {
    const container = document.getElementById('key-input-container');
    if (!container) return;

    let html = '';
    switch (this.currentCipher) {
      case 'shift':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Key Pergeseran (k &isin; [0..25])</span>
              <span class="badge badge-cyan" id="shift-badge">k = 3</span>
            </div>
            <div style="display: flex; gap: 16px; align-items: center;">
              <input type="range" id="shift-range" min="0" max="25" value="3" style="flex: 1;" class="input-ctrl">
              <input type="number" id="shift-number" min="0" max="25" value="3" class="input-ctrl" style="width: 80px; text-align: center;">
            </div>
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;">
              Formula: C = (P + k) mod 26 | P = (C - k) mod 26
            </p>
          </div>
        `;
        break;

      case 'substitution':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Key Substitusi Alfabet (26 Huruf Unik)</span>
              <button type="button" class="btn btn-outline btn-sm" id="btn-random-sub-key">🎲 Acak Key</button>
            </div>
            <input type="text" id="sub-key-input" maxlength="26" class="input-ctrl" style="font-family: var(--font-mono); letter-spacing: 2px; font-weight: 700; text-transform: uppercase;" value="QWERTYUIOPASDFGHJKLZXCVBNM">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
              <span style="font-size: 0.8rem; color: var(--text-muted);" id="sub-key-status">Status: 26/26 Karakter Unik (Valid)</span>
              <button type="button" class="btn btn-outline btn-sm" id="btn-reset-sub-key">Reset A-Z</button>
            </div>
          </div>
        `;
        break;

      case 'affine':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Key Affine: C = (a &times; P + b) mod 26</span>
              <span class="badge badge-amber" id="affine-coprime-badge">gcd(a, 26) = 1</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div>
                <label class="form-label">Koefisien Multiplikatif (a):</label>
                <select id="affine-a" class="input-ctrl">
                  <option value="1">1 (Identitas)</option>
                  <option value="3">3</option>
                  <option value="5">5</option>
                  <option value="7" selected>7</option>
                  <option value="9">9</option>
                  <option value="11">11</option>
                  <option value="15">15</option>
                  <option value="17">17</option>
                  <option value="19">19</option>
                  <option value="21">21</option>
                  <option value="23">23</option>
                  <option value="25">25</option>
                </select>
              </div>
              <div>
                <label class="form-label">Pergeseran (b):</label>
                <input type="number" id="affine-b" min="0" max="25" value="10" class="input-ctrl">
              </div>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;" id="affine-inv-note">
              Invers a modulo 26: a<sup>-1</sup> = 15 | Formula Dekripsi: P = a<sup>-1</sup>(C - b) mod 26
            </p>
          </div>
        `;
        break;

      case 'vigenere':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Kata Kunci (Keyword) Vigenere</span>
              <span class="badge badge-purple">Polialfabetik</span>
            </div>
            <input type="text" id="vigenere-key" class="input-ctrl" placeholder="Contoh: LEMON / KRIPTOGRAFI" value="LEMON" style="text-transform: uppercase; font-family: var(--font-mono); font-weight: 700;">
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
              ℹ️ Sesuai ketentuan tugas: Angka, spasi, dan tanda baca diabaikan dan tidak dimasukkan ke dalam ciphertext.
            </p>
          </div>
        `;
        break;

      case 'hill':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Matriks Kunci Hill Cipher (Mod 26)</span>
              <div style="display: flex; gap: 8px;">
                <button type="button" class="btn btn-outline btn-sm active" id="btn-hill-dim-2">2 &times; 2</button>
                <button type="button" class="btn btn-outline btn-sm" id="btn-hill-dim-3">3 &times; 3</button>
              </div>
            </div>
            <div id="hill-matrix-inputs">
              <!-- Rendered dynamically -->
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
              <span id="hill-status-badge" class="badge badge-cyan">det(K) = 9 mod 26 (Invertible)</span>
              <button type="button" class="btn btn-outline btn-sm" id="btn-hill-preset">Muat Contoh Matriks Valid</button>
            </div>
          </div>
        `;
        break;

      case 'permutation':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Key Permutasi Blok (Urutan Transposisi)</span>
              <span class="badge badge-cyan">Transposisi Blok</span>
            </div>
            <input type="text" id="perm-key-input" class="input-ctrl" placeholder="Contoh: 3, 1, 4, 2 atau keyword ZEBRA" value="3, 1, 4, 2" style="font-family: var(--font-mono); font-weight: 700;">
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
              ℹ️ Masukkan permutasi angka (misal: <code>3, 1, 4, 2</code> untuk blok ukuran 4) atau kata kunci alfabet. Teks akan dipad dengan 'X' jika panjang bukan kelipatan blok.
            </p>
          </div>
        `;
        break;

      case 'otp':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 File Key One-Time Pad (.txt)</span>
              <button type="button" class="btn btn-primary btn-sm" id="btn-generate-otp-file">📥 Generate & Download File Key</button>
            </div>
            <div class="dropzone" id="otp-dropzone">
              <div class="dropzone-icon">📄</div>
              <div class="dropzone-text">Klik atau seret file teks key (.txt) acak ke sini</div>
              <div class="dropzone-filename" id="otp-filename">Belum ada file dipilih</div>
              <input type="file" id="otp-file-input" accept=".txt" style="display: none;">
            </div>
            <div style="margin-top: 12px;">
              <label class="form-label">
                <span>Konten Key OTP (Dapat diedit langsung):</span>
                <span id="otp-char-count" class="char-counter">0 Karakter</span>
              </label>
              <textarea id="otp-key-text" class="textarea-ctrl" style="min-height: 80px;" placeholder="Huruf acak A-Z..."></textarea>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
              ℹ️ Sesuai ketentuan: Jumlah karakter key yang digunakan mengikuti panjang pesan. Sisa karakter key yang tidak digunakan dibiarkan.
            </p>
          </div>
        `;
        break;
    }

    container.innerHTML = html;
    this.bindKeyListeners();
  },

  bindKeyListeners() {
    if (this.currentCipher === 'shift') {
      const range = document.getElementById('shift-range');
      const num = document.getElementById('shift-number');
      const badge = document.getElementById('shift-badge');
      if (range && num) {
        range.addEventListener('input', () => {
          num.value = range.value;
          badge.textContent = `k = ${range.value}`;
        });
        num.addEventListener('input', () => {
          range.value = num.value;
          badge.textContent = `k = ${num.value}`;
        });
      }
    } else if (this.currentCipher === 'substitution') {
      const subInput = document.getElementById('sub-key-input');
      const subStatus = document.getElementById('sub-key-status');
      const btnRand = document.getElementById('btn-random-sub-key');
      const btnReset = document.getElementById('btn-reset-sub-key');

      const validateSub = () => {
        const val = (subInput.value || '').toUpperCase().replace(/[^A-Z]/g, '');
        subInput.value = val;
        const unique = new Set(val).size;
        if (val.length === 26 && unique === 26) {
          subStatus.innerHTML = `<span style="color: var(--accent-green);">✓ 26/26 Karakter Unik (Valid)</span>`;
        } else {
          subStatus.innerHTML = `<span style="color: var(--accent-red);">✗ Panjang: ${val.length}/26, Karakter Unik: ${unique}/26</span>`;
        }
      };

      if (subInput) subInput.addEventListener('input', validateSub);
      if (btnRand) {
        btnRand.addEventListener('click', () => {
          const alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split('');
          for (let i = alpha.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [alpha[i], alpha[j]] = [alpha[j], alpha[i]];
          }
          subInput.value = alpha.join('');
          validateSub();
          App.toast("Kunci substitusi acak telah dibuat!", "success");
        });
      }
      if (btnReset) {
        btnReset.addEventListener('click', () => {
          subInput.value = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
          validateSub();
        });
      }
    } else if (this.currentCipher === 'affine') {
      const aSelect = document.getElementById('affine-a');
      const note = document.getElementById('affine-inv-note');
      if (aSelect && note) {
        const updateAffineNote = () => {
          const a = parseInt(aSelect.value, 10);
          // Mod inverse of a mod 26
          const invMap = { 1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25 };
          const inv = invMap[a] || '?';
          note.innerHTML = `Invers a modulo 26: <strong>a<sup>-1</sup> = ${inv}</strong> | Formula Dekripsi: P = a<sup>-1</sup>(C - b) mod 26`;
        };
        aSelect.addEventListener('change', updateAffineNote);
        updateAffineNote();
      }
    } else if (this.currentCipher === 'hill') {
      this.hillDim = 2;
      this.renderHillGrid();
      const btn2 = document.getElementById('btn-hill-dim-2');
      const btn3 = document.getElementById('btn-hill-dim-3');
      const btnPreset = document.getElementById('btn-hill-preset');

      if (btn2 && btn3) {
        btn2.addEventListener('click', () => {
          this.hillDim = 2;
          btn2.classList.add('active');
          btn3.classList.remove('active');
          this.renderHillGrid();
        });
        btn3.addEventListener('click', () => {
          this.hillDim = 3;
          btn3.classList.add('active');
          btn2.classList.remove('active');
          this.renderHillGrid();
        });
      }
      if (btnPreset) {
        btnPreset.addEventListener('click', () => {
          if (this.hillDim === 2) {
            this.setHillValues([[3, 3], [2, 5]]);
          } else {
            this.setHillValues([[6, 24, 1], [13, 16, 10], [20, 17, 15]]);
          }
          this.checkHillValidity();
          App.toast("Preset matriks Hill berhasil dimuat!", "success");
        });
      }
    } else if (this.currentCipher === 'otp') {
      const dropzone = document.getElementById('otp-dropzone');
      const fileInput = document.getElementById('otp-file-input');
      const filenameLabel = document.getElementById('otp-filename');
      const keyTextArea = document.getElementById('otp-key-text');
      const charCount = document.getElementById('otp-char-count');
      const btnGen = document.getElementById('btn-generate-otp-file');

      const updateKeyCount = () => {
        const clean = (keyTextArea.value || '').toUpperCase().replace(/[^A-Z]/g, '');
        charCount.textContent = `${clean.length} Huruf A-Z`;
      };

      if (keyTextArea) {
        keyTextArea.addEventListener('input', updateKeyCount);
      }

      if (dropzone && fileInput) {
        dropzone.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => {
          const file = e.target.files[0];
          if (file) {
            filenameLabel.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
            const reader = new FileReader();
            reader.onload = (evt) => {
              keyTextArea.value = evt.target.result;
              updateKeyCount();
              App.toast(`File key ${file.name} berhasil dibaca!`, "success");
            };
            reader.readAsText(file);
          }
        });
      }

      if (btnGen) {
        btnGen.addEventListener('click', async () => {
          try {
            const resp = await fetch('/api/cipher/otp/generate-key?length=2000');
            const data = await resp.json();
            if (data.success) {
              keyTextArea.value = data.key;
              updateKeyCount();
              filenameLabel.textContent = `random_otp_key_${data.length}_chars.txt (Generated)`;
              App.downloadFile(data.key, "otp_secret_key.txt");
              App.toast("File key OTP 2000 karakter acak berhasil dibuat dan diunduh!", "success");
            }
          } catch (err) {
            App.toast("Gagal menghasilkan key OTP: " + err.message, "error");
          }
        });
      }
    }
  },

  renderHillGrid() {
    const container = document.getElementById('hill-matrix-inputs');
    if (!container) return;

    if (this.hillDim === 2) {
      container.innerHTML = `
        <div class="matrix-grid-2x2">
          <input type="number" class="matrix-cell" id="h-0-0" value="3">
          <input type="number" class="matrix-cell" id="h-0-1" value="3">
          <input type="number" class="matrix-cell" id="h-1-0" value="2">
          <input type="number" class="matrix-cell" id="h-1-1" value="5">
        </div>
      `;
    } else {
      container.innerHTML = `
        <div class="matrix-grid-3x3">
          <input type="number" class="matrix-cell" id="h-0-0" value="6">
          <input type="number" class="matrix-cell" id="h-0-1" value="24">
          <input type="number" class="matrix-cell" id="h-0-2" value="1">
          <input type="number" class="matrix-cell" id="h-1-0" value="13">
          <input type="number" class="matrix-cell" id="h-1-1" value="16">
          <input type="number" class="matrix-cell" id="h-1-2" value="10">
          <input type="number" class="matrix-cell" id="h-2-0" value="20">
          <input type="number" class="matrix-cell" id="h-2-1" value="17">
          <input type="number" class="matrix-cell" id="h-2-2" value="15">
        </div>
      `;
    }

    const cells = container.querySelectorAll('.matrix-cell');
    cells.forEach(cell => {
      cell.addEventListener('input', () => this.checkHillValidity());
    });
    this.checkHillValidity();
  },

  getHillMatrix() {
    const dim = this.hillDim;
    const mat = [];
    for (let r = 0; r < dim; r++) {
      const row = [];
      for (let c = 0; c < dim; c++) {
        const val = parseInt(document.getElementById(`h-${r}-${c}`)?.value || '0', 10);
        row.push(val);
      }
      mat.push(row);
    }
    return mat;
  },

  setHillValues(mat) {
    const dim = mat.length;
    for (let r = 0; r < dim; r++) {
      for (let c = 0; c < dim; c++) {
        const cell = document.getElementById(`h-${r}-${c}`);
        if (cell) cell.value = mat[r][c];
      }
    }
  },

  async checkHillValidity() {
    const mat = this.getHillMatrix();
    const badge = document.getElementById('hill-status-badge');
    if (!badge) return;

    try {
      const resp = await fetch('/api/cipher/hill/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ matrix: mat })
      });
      const data = await resp.json();
      if (data.success) {
        badge.className = 'badge badge-green';
        badge.textContent = `det(K) = ${data.data.det_mod} (Invers det = ${data.data.det_inv}) - Valid!`;
      } else {
        badge.className = 'badge badge-amber';
        badge.textContent = `Tidak Invertible: ${data.error || 'Determinannya tidak koprima dengan 26'}`;
      }
    } catch {
      badge.className = 'badge badge-amber';
      badge.textContent = `Validasi matriks...`;
    }
  },

  bindActions() {
    const btnEncrypt = document.getElementById('btn-cipher-encrypt');
    const btnDecrypt = document.getElementById('btn-cipher-decrypt');
    const btnClear = document.getElementById('btn-cipher-clear');

    if (btnEncrypt) {
      btnEncrypt.addEventListener('click', () => this.processCipher('encrypt'));
    }
    if (btnDecrypt) {
      btnDecrypt.addEventListener('click', () => this.processCipher('decrypt'));
    }
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        document.getElementById('cipher-input-text').value = '';
        this.clearResult();
      });
    }
  },

  async processCipher(action) {
    const inputText = document.getElementById('cipher-input-text')?.value || '';
    if (!inputText.trim()) {
      App.toast("Mohon masukkan pesan teks terlebih dahulu!", "error");
      return;
    }

    let url = `/api/cipher/${this.currentCipher}/${action}`;
    let payload = { text: inputText };

    try {
      switch (this.currentCipher) {
        case 'shift':
          payload.key = parseInt(document.getElementById('shift-number').value, 10);
          break;
        case 'substitution':
          payload.key = document.getElementById('sub-key-input').value;
          break;
        case 'affine':
          payload.a = parseInt(document.getElementById('affine-a').value, 10);
          payload.b = parseInt(document.getElementById('affine-b').value, 10);
          break;
        case 'vigenere':
          payload.key = document.getElementById('vigenere-key').value;
          break;
        case 'hill':
          payload.matrix = this.getHillMatrix();
          break;
        case 'permutation':
          payload.key = document.getElementById('perm-key-input').value;
          break;
        case 'otp':
          payload.key_text = document.getElementById('otp-key-text').value;
          if (!payload.key_text.trim()) {
            App.toast("Mohon upload atau generate file key One-Time Pad terlebih dahulu!", "error");
            return;
          }
          break;
      }

      const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const res = await resp.json();
      if (!res.success) {
        App.toast(res.error || "Operasi gagal dijalankan.", "error");
        return;
      }

      this.displayResult(res.data, action);
      App.toast(`${action === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} ${this.currentCipher.toUpperCase()} berhasil!`, "success");
    } catch (err) {
      App.toast("Terjadi kesalahan koneksi server: " + err.message, "error");
    }
  },

  displayResult(data, action) {
    const resultBox = document.getElementById('cipher-output-display');
    const resultLen = document.getElementById('cipher-output-length');
    const accordion = document.getElementById('cipher-math-accordion');
    const mathContent = document.getElementById('cipher-math-content');

    const resultText = action === 'encrypt' ? data.ciphertext : data.plaintext;
    if (resultBox) resultBox.textContent = resultText;
    if (resultLen) resultLen.textContent = `${resultText.length} Karakter`;

    // Render step-by-step breakdown
    if (mathContent) {
      let breakdownHtml = `<div><strong>Algoritma:</strong> ${this.currentCipher.toUpperCase()} (${action.toUpperCase()})</div>`;
      if (data.ignored_characters_note) {
        breakdownHtml += `<div style="color: var(--accent-amber); margin: 6px 0;">ℹ️ ${data.ignored_characters_note}</div>`;
      }

      if (data.analysis) {
        const a = data.analysis;
        breakdownHtml += `
          <div style="margin: 8px 0; padding: 8px; background: rgba(255,255,255,0.03); border-radius: 4px;">
            <strong>Analisis Matriks Hill:</strong> Ukuran: ${a.size}&times;${a.size} | det(K) = ${a.det_mod} | Invers det = ${a.det_inv} (mod 26)
            <div>Invers Matriks Modulo 26: <code>${JSON.stringify(a.inverse_matrix)}</code></div>
          </div>
        `;
      }

      if (data.steps && data.steps.length > 0) {
        breakdownHtml += `<table class="table-crypto" style="margin-top: 10px;">
          <thead>
            <tr>
              <th>Posisi</th>
              <th>Karakter Input</th>
              <th>Perhitungan / Mapping</th>
              <th>Karakter Output</th>
            </tr>
          </thead>
          <tbody>
            ${data.steps.map(s => `
              <tr>
                <td>#${s.index + 1}</td>
                <td><strong>${s.plain_char || s.cipher_char}</strong></td>
                <td><code>${s.calculation || s.mapping || '-'}</code></td>
                <td style="color: var(--accent-cyan); font-weight: bold;">${s.cipher_char || s.plain_char}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
        ${data.input_length > 20 ? `<div style="color: var(--text-subtle); margin-top: 6px;">(Menampilkan 20 karakter pertama untuk visualisasi langkah)</div>` : ''}
        `;
      } else if (data.block_steps && data.block_steps.length > 0) {
        breakdownHtml += `<div style="margin-top: 10px;"><strong>Langkah Blok:</strong></div>
          <table class="table-crypto">
            <thead>
              <tr>
                <th>Blok</th>
                <th>Blok Input</th>
                <th>Vektor / Transformasi</th>
                <th>Blok Output</th>
              </tr>
            </thead>
            <tbody>
              ${data.block_steps.map(b => `
                <tr>
                  <td>Blok #${b.block_index + 1}</td>
                  <td><code>${b.in_block}</code></td>
                  <td><code>${b.out_vector ? JSON.stringify(b.out_vector) : JSON.stringify(b.mapping)}</code></td>
                  <td style="color: var(--accent-cyan); font-weight: bold;">${b.out_block}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
      }

      mathContent.innerHTML = breakdownHtml;
      if (accordion) accordion.classList.add('open');
    }
  },

  clearResult() {
    const resultBox = document.getElementById('cipher-output-display');
    const resultLen = document.getElementById('cipher-output-length');
    const mathContent = document.getElementById('cipher-math-content');
    const accordion = document.getElementById('cipher-math-accordion');

    if (resultBox) resultBox.textContent = 'Hasil enkripsi/dekripsi akan tampil di sini...';
    if (resultLen) resultLen.textContent = '0 Karakter';
    if (mathContent) mathContent.innerHTML = 'Jalankan enkripsi/dekripsi untuk melihat langkah kalkulasi.';
    if (accordion) accordion.classList.remove('open');
  }
};

// ===================================================================
// File Ciphers Controller (Arbitrary & Binary File Processing)
// ===================================================================

const FileCiphers = {
  currentCipher: 'shift',
  selectedFile: null,
  fileMeta: null,
  processedBlob: null,
  processedFilename: '',
  otpKeyFile: null,

  init() {
    this.bindPills();
    this.bindFileInput();
    this.renderKeyInput();
    this.bindActions();
  },

  bindPills() {
    const pills = document.querySelectorAll('[data-bin-cipher]');
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.currentCipher = pill.dataset.binCipher;
        this.renderKeyInput();
      });
    });
  },

  bindFileInput() {
    const dropzone = document.getElementById('bin-file-dropzone');
    const fileInput = document.getElementById('bin-file-input');

    if (dropzone && fileInput) {
      dropzone.addEventListener('click', () => fileInput.click());

      fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
          this.handleFileSelect(e.target.files[0]);
        }
      });

      ['dragenter', 'dragover'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
          e.preventDefault();
          dropzone.classList.add('dragover');
        });
      });

      ['dragleave', 'drop'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
          e.preventDefault();
          dropzone.classList.remove('dragover');
        });
      });

      dropzone.addEventListener('drop', (e) => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
          this.handleFileSelect(e.dataTransfer.files[0]);
        }
      });
    }
  },

  async handleFileSelect(file) {
    this.selectedFile = file;
    const dropzoneName = document.getElementById('bin-file-dropzone-name');
    if (dropzoneName) {
      dropzoneName.textContent = `${file.name} (${this.formatSize(file.size)})`;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const resp = await fetch('/api/file-cipher/inspect', {
        method: 'POST',
        body: formData
      });
      const res = await resp.json();
      if (res.success) {
        this.fileMeta = res;
        const metaCard = document.getElementById('bin-file-meta-card');
        if (metaCard) {
          metaCard.style.display = 'block';
          document.getElementById('bin-meta-filename').textContent = res.filename;
          document.getElementById('bin-meta-size').textContent = `${this.formatSize(res.size)} (${res.size.toLocaleString()} bytes)`;
          document.getElementById('bin-meta-sha256').textContent = res.sha256;
        }
        App.toast(`Berkas ${file.name} siap diproses!`, 'success');
      }
    } catch (err) {
      console.error(err);
    }
  },

  formatSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  },

  renderKeyInput() {
    const container = document.getElementById('bin-key-container');
    if (!container) return;

    let html = '';
    switch (this.currentCipher) {
      case 'shift':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Key Pergeseran Byte (k &isin; [0..255])</span>
              <span class="badge badge-cyan" id="bin-shift-badge">k = 42</span>
            </div>
            <div style="display: flex; gap: 16px; align-items: center;">
              <input type="range" id="bin-shift-range" min="0" max="255" value="42" style="flex: 1;" class="input-ctrl">
              <input type="number" id="bin-shift-number" min="0" max="255" value="42" class="input-ctrl" style="width: 80px; text-align: center;">
            </div>
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;">
              Formula: C<sub>i</sub> = (B<sub>i</sub> + k) mod 256 | B<sub>i</sub> = (C<sub>i</sub> - k) mod 256
            </p>
          </div>
        `;
        break;

      case 'substitution':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 S-Box Seed / Password Substitusi Biner</span>
              <span class="badge badge-purple">Permutasi 256 Byte</span>
            </div>
            <input type="text" id="bin-sub-key" class="input-ctrl" value="CRYPTODEX_SECRET_SBOX_KEY" placeholder="Masukkan password/kunci untuk membangkitkan S-Box 256-byte...">
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;">
              Kunci string/password digunakan untuk menghasilkan permutasi 256 byte unik (S-Box) yang 100% reversible.
            </p>
          </div>
        `;
        break;

      case 'affine':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Key Affine Biner: C = (a &times; B + b) mod 256</span>
              <span class="badge badge-amber" id="bin-affine-coprime-badge">gcd(a, 256) = 1 (Ganjil)</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div>
                <label class="form-label">Koefisien Multiplikatif (a - Ganjil):</label>
                <input type="number" id="bin-affine-a" value="15" step="2" min="1" max="255" class="input-ctrl">
              </div>
              <div>
                <label class="form-label">Pergeseran (b):</label>
                <input type="number" id="bin-affine-b" value="73" min="0" max="255" class="input-ctrl">
              </div>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;">
              Syarat invers modulo 256: nilai <strong>a</strong> harus berupa bilangan GANJIL.
            </p>
          </div>
        `;
        break;

      case 'vigenere':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Kata Kunci (Keyword / Bytes) Vigenere Biner</span>
              <span class="badge badge-purple">Polyalphabetic</span>
            </div>
            <input type="text" id="bin-vigenere-key" class="input-ctrl" value="KUNCI_VIGENERE_BINER_2026" placeholder="Ketik kata kunci...">
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;">
              Formula: C<sub>i</sub> = (B<sub>i</sub> + K<sub>i mod |K|</sub>) mod 256
            </p>
          </div>
        `;
        break;

      case 'hill':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Matriks Kunci Hill Biner (Mod 256)</span>
              <span class="badge badge-cyan">Invertible mod 256</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(2, 70px); gap: 8px; justify-content: center; margin: 10px 0;">
              <input type="number" class="matrix-cell" id="bin-h-0-0" value="3">
              <input type="number" class="matrix-cell" id="bin-h-0-1" value="2">
              <input type="number" class="matrix-cell" id="bin-h-1-0" value="5">
              <input type="number" class="matrix-cell" id="bin-h-1-1" value="7">
            </div>
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;">
              det(K) = (3&times;7 - 2&times;5) = 11 mod 256 (Ganjil &rarr; Invertible!). Dilengkapi PKCS#7 padding otomatis.
            </p>
          </div>
        `;
        break;

      case 'permutation':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 Permutasi Blok Bytes</span>
              <span class="badge badge-cyan">Transposisi Blok</span>
            </div>
            <input type="text" id="bin-perm-key" class="input-ctrl" value="3, 1, 4, 2" placeholder="Contoh: 3, 1, 4, 2">
            <p style="font-size: 0.8rem; color: var(--text-subtle); margin-top: 8px;">
              Menukar posisi byte dalam blok ukuran 4 secara reversible menggunakan padding PKCS#7.
            </p>
          </div>
        `;
        break;

      case 'otp':
        html = `
          <div class="key-box">
            <div class="key-header">
              <span class="key-title">🔑 File Key One-Time Pad Biner</span>
              <button type="button" class="btn btn-primary btn-sm" id="btn-bin-gen-otp">📥 Generate Key Biner (64 KB)</button>
            </div>
            <div class="dropzone" id="bin-otp-file-dropzone" style="margin-top: 8px;">
              <div class="dropzone-icon">🗝️</div>
              <div class="dropzone-text">Unggah file key biner OTP (.bin / berkas apapun) di sini</div>
              <div class="dropzone-filename" id="bin-otp-filename">Belum ada file key</div>
              <input type="file" id="bin-otp-file-input" accept="*" style="display: none;">
            </div>
            <div style="display: flex; gap: 16px; align-items: center; margin-top: 10px;">
              <label style="font-size: 0.85rem; color: var(--text-muted);">Mode Operasi:</label>
              <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                <input type="radio" name="bin-otp-mode" value="xor" checked> Byte XOR (&oplus;)
              </label>
              <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                <input type="radio" name="bin-otp-mode" value="add"> Penjumlahan Mod 256
              </label>
            </div>
          </div>
        `;
        break;
    }

    container.innerHTML = html;
    this.bindKeyEvents();
  },

  bindKeyEvents() {
    if (this.currentCipher === 'shift') {
      const range = document.getElementById('bin-shift-range');
      const num = document.getElementById('bin-shift-number');
      const badge = document.getElementById('bin-shift-badge');
      if (range && num) {
        range.addEventListener('input', () => {
          num.value = range.value;
          badge.textContent = `k = ${range.value}`;
        });
        num.addEventListener('input', () => {
          range.value = num.value;
          badge.textContent = `k = ${num.value}`;
        });
      }
    } else if (this.currentCipher === 'otp') {
      const otpDrop = document.getElementById('bin-otp-file-dropzone');
      const otpInp = document.getElementById('bin-otp-file-input');
      const otpName = document.getElementById('bin-otp-filename');
      const btnGen = document.getElementById('btn-bin-gen-otp');

      if (otpDrop && otpInp) {
        otpDrop.addEventListener('click', () => otpInp.click());
        otpInp.addEventListener('change', (e) => {
          if (e.target.files && e.target.files[0]) {
            this.otpKeyFile = e.target.files[0];
            otpName.textContent = `${this.otpKeyFile.name} (${this.formatSize(this.otpKeyFile.size)})`;
            App.toast(`File key OTP ${this.otpKeyFile.name} dimuat!`, 'success');
          }
        });
      }

      if (btnGen) {
        btnGen.addEventListener('click', async () => {
          try {
            const resp = await fetch('/api/file-cipher/otp-generate-key?size=65536');
            const blob = await resp.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "otp_key_65536_bytes.bin";
            a.click();
            URL.revokeObjectURL(url);
            App.toast("File key OTP acak 64 KB berhasil diunduh!", "success");
          } catch (err) {
            App.toast("Gagal mengunduh key OTP: " + err.message, "error");
          }
        });
      }
    }
  },

  bindActions() {
    const btnEnc = document.getElementById('btn-bin-encrypt');
    const btnDec = document.getElementById('btn-bin-decrypt');
    const btnClear = document.getElementById('btn-bin-clear');
    const btnDownload = document.getElementById('btn-bin-download');

    if (btnEnc) btnEnc.addEventListener('click', () => this.processFile('encrypt'));
    if (btnDec) btnDec.addEventListener('click', () => this.processFile('decrypt'));
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        this.selectedFile = null;
        this.fileMeta = null;
        this.processedBlob = null;
        const metaCard = document.getElementById('bin-file-meta-card');
        if (metaCard) metaCard.style.display = 'none';
        const nameLabel = document.getElementById('bin-file-dropzone-name');
        if (nameLabel) nameLabel.textContent = 'Belum ada file dipilih';
        const emptyEl = document.getElementById('bin-result-empty');
        if (emptyEl) emptyEl.style.display = 'block';
        const detailsEl = document.getElementById('bin-result-details');
        if (detailsEl) detailsEl.style.display = 'none';
      });
    }

    if (btnDownload) {
      btnDownload.addEventListener('click', () => {
        if (this.processedBlob && this.processedFilename) {
          const url = URL.createObjectURL(this.processedBlob);
          const a = document.createElement('a');
          a.href = url;
          a.download = this.processedFilename;
          a.click();
          URL.revokeObjectURL(url);
          App.toast(`File ${this.processedFilename} berhasil diunduh!`, 'success');
        }
      });
    }
  },

  async processFile(action) {
    if (!this.selectedFile) {
      App.toast("Silakan unggah berkas terlebih dahulu!", "error");
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('cipher', this.currentCipher);
    formData.append('action', action);

    switch (this.currentCipher) {
      case 'shift':
        formData.append('key', document.getElementById('bin-shift-number')?.value || '42');
        break;
      case 'substitution':
        formData.append('key', document.getElementById('bin-sub-key')?.value || 'CRYPTODEX_DEFAULT');
        break;
      case 'affine':
        formData.append('key_a', document.getElementById('bin-affine-a')?.value || '15');
        formData.append('key_b', document.getElementById('bin-affine-b')?.value || '73');
        break;
      case 'vigenere':
        formData.append('key', document.getElementById('bin-vigenere-key')?.value || 'LEMON');
        break;
      case 'hill':
        formData.append('key', JSON.stringify([[3, 2], [5, 7]]));
        break;
      case 'permutation':
        formData.append('key', document.getElementById('bin-perm-key')?.value || '3, 1, 4, 2');
        break;
      case 'otp':
        if (!this.otpKeyFile) {
          App.toast("Mohon unggah file key One-Time Pad terlebih dahulu!", "error");
          return;
        }
        formData.append('otp_file', this.otpKeyFile);
        const mode = document.querySelector('input[name="bin-otp-mode"]:checked')?.value || 'xor';
        formData.append('otp_mode', mode);
        break;
    }

    App.toast(`Memproses ${action === 'encrypt' ? 'enkripsi' : 'dekripsi'} berkas...`, 'info');

    try {
      const resp = await fetch('/api/file-cipher/process', {
        method: 'POST',
        body: formData
      });

      if (!resp.ok) {
        const errJson = await resp.json().catch(() => null);
        App.toast(errJson?.error || "Gagal memproses berkas.", "error");
        return;
      }

      const outFilename = resp.headers.get('X-Output-Filename') || `${this.selectedFile.name}.${action === 'encrypt' ? 'enc' : 'out'}`;
      const origSha = resp.headers.get('X-Original-SHA256') || '-';
      const procSha = resp.headers.get('X-Processed-SHA256') || '-';
      const outSize = parseInt(resp.headers.get('X-Processed-Size') || '0', 10);

      this.processedBlob = await resp.blob();
      this.processedFilename = outFilename;

      document.getElementById('bin-result-empty').style.display = 'none';
      document.getElementById('bin-result-details').style.display = 'block';
      const badge = document.getElementById('bin-result-status-badge');
      badge.textContent = action === 'encrypt' ? '✓ Terenkripsi' : '✓ Terdekripsi';
      badge.className = 'badge badge-green';

      document.getElementById('bin-out-filename').textContent = outFilename;
      document.getElementById('bin-btn-download-name').textContent = outFilename;
      document.getElementById('bin-out-size').textContent = `${this.formatSize(outSize)} (${outSize.toLocaleString()} bytes)`;
      document.getElementById('bin-out-sha256').textContent = procSha;

      const revBox = document.getElementById('bin-reversibility-box');
      if (action === 'decrypt') {
        revBox.style.display = 'block';
        document.getElementById('bin-rev-orig').textContent = origSha;
        document.getElementById('bin-rev-out').textContent = procSha;
      } else {
        revBox.style.display = 'none';
      }

      App.toast(`Berkas berhasil ${action === 'encrypt' ? 'dienkripsi' : 'didekripsi'}!`, 'success');
    } catch (err) {
      App.toast("Kesalahan: " + err.message, "error");
    }
  }
};

window.Ciphers = Ciphers;
window.FileCiphers = FileCiphers;

