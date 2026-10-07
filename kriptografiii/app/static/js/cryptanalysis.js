// ===================================================================
// Cryptanalysis Controller (Bagian B - Analisis Abjad-Tunggal)
// ===================================================================

const Cryptanalysis = {
  currentLang: 'id',
  ciphertext: '',
  analysisData: null,
  mapping: {}, // Cipher letter -> Plain letter

  // Presets for demo
  samples: {
    id: "KDFDFLD QHJDFD VDQJDW SHQWLQJ XQWXN GLMDJD GHQJDQ VHJHQDS MLZD GDQ WDJD PHUHN DPHQ MDJD NXWXK DQEDQ JVDGD QQHJD UDGHQ JDQVH PDQJD WMXDQ JSHQ XKKDN LNDWN HELDV DDQGD QNHPH UGHND DQKD UXVGL SHUWDK DQN DQ", // Shift 3
    id_sub: "IEOEOSD TMBEDO LEFEMX ZMTXTMG VTXVY ZMWOEB ZMTXTM LHBMTEZ WMWO ZMT OLEB DLEBM TLEBO VXVY OTEBT LEBDO ZMTXM TLHTM ZMTXM XLEBO OLEBM TLEBO OLEBM TEZLE BMZMT", // Mixed substitution
    en: "WKLVLV DVHFU HWPHV VDJHW KDWFD QEHGH FRGHG XVLQJ IUHTX HQFBD QDOBV LVWRR OWKHG HIHQV HRIWK HQDWL RQGHU LYHVW UHQJW KRIWK HSHRS OH", // English shift 3
    en_sub: "GHEEL TLELD VTEES WIEES EGTEK GHRTE KGEEW DTEEH GREWD SEWER TEKGT EWDSW EERGR EDSSW ETHRE EWDS"
  },

  init() {
    this.bindEvents();
    this.initMapping();
    this.renderMappingGrid();
  },

  initMapping() {
    this.mapping = {};
    for (let c = 65; c <= 90; c++) {
      const ch = String.fromCharCode(c);
      this.mapping[ch] = '';
    }
  },

  bindEvents() {
    const btnAnalyze = document.getElementById('btn-ca-analyze');
    const btnAutoCrack = document.getElementById('btn-ca-autocrack');
    const langSelect = document.getElementById('ca-lang-select');
    const btnLoadSampleId = document.getElementById('btn-ca-sample-id');
    const btnLoadSampleEn = document.getElementById('btn-ca-sample-en');
    const btnResetMapping = document.getElementById('btn-ca-reset-map');
    const btnApplyAutoKey = document.getElementById('btn-ca-apply-auto-key');
    const caInput = document.getElementById('ca-ciphertext-input');

    if (langSelect) {
      langSelect.addEventListener('change', () => {
        this.currentLang = langSelect.value;
        if (this.ciphertext) this.runFrequencyAnalysis();
      });
    }

    if (btnAnalyze) {
      btnAnalyze.addEventListener('click', () => {
        this.ciphertext = (caInput?.value || '').trim();
        if (!this.ciphertext) {
          App.toast("Masukkan ciphertext terlebih dahulu!", "error");
          return;
        }
        this.runFrequencyAnalysis();
      });
    }

    if (btnAutoCrack) {
      btnAutoCrack.addEventListener('click', () => this.runAutoCrack());
    }

    if (btnLoadSampleId) {
      btnLoadSampleId.addEventListener('click', () => {
        if (caInput) {
          caInput.value = this.samples.id;
          this.ciphertext = this.samples.id;
          if (langSelect) langSelect.value = 'id';
          this.currentLang = 'id';
          this.runFrequencyAnalysis();
          App.toast("Contoh ciphertext Bahasa Indonesia dimuat!", "success");
        }
      });
    }

    if (btnLoadSampleEn) {
      btnLoadSampleEn.addEventListener('click', () => {
        if (caInput) {
          caInput.value = this.samples.en;
          this.ciphertext = this.samples.en;
          if (langSelect) langSelect.value = 'en';
          this.currentLang = 'en';
          this.runFrequencyAnalysis();
          App.toast("Contoh ciphertext English dimuat!", "success");
        }
      });
    }

    if (btnResetMapping) {
      btnResetMapping.addEventListener('click', () => {
        this.initMapping();
        this.renderMappingGrid();
        this.updateLivePreview();
        App.toast("Mapping huruf di-reset.", "success");
      });
    }

    if (btnApplyAutoKey) {
      btnApplyAutoKey.addEventListener('click', () => {
        if (this.lastDiscoveredMapping) {
          this.mapping = { ...this.lastDiscoveredMapping };
          this.renderMappingGrid();
          this.updateLivePreview();
          App.toast("Kunci hasil Auto-Crack berhasil dipasang ke Workbench!", "success");
        }
      });
    }

    if (caInput) {
      caInput.addEventListener('input', () => {
        this.ciphertext = caInput.value.trim();
        this.updateLivePreview();
      });
    }
  },

  async runFrequencyAnalysis() {
    if (!this.ciphertext) return;

    try {
      const resp = await fetch('/api/cryptanalysis/frequency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ciphertext: this.ciphertext, language: this.currentLang })
      });

      const res = await resp.json();
      if (!res.success) {
        App.toast(res.error || "Gagal melakukan analisis frekuensi.", "error");
        return;
      }

      this.analysisData = res.data;
      this.renderAnalysisResults(res.data);
      this.updateLivePreview();
      App.toast("Analisis frekuensi berhasil diperbarui!", "success");
    } catch (err) {
      App.toast("Kesalahan analisis: " + err.message, "error");
    }
  },

  renderAnalysisResults(data) {
    // 1. Stats
    document.getElementById('ca-total-chars').textContent = data.total_chars;
    document.getElementById('ca-ioc-val').textContent = data.ioc.toFixed(4);
    document.getElementById('ca-ioc-note').textContent = data.ioc_note;

    // 2. Render Frequency Bars
    this.renderFrequencyChart(data.unigrams, data.language);

    // 3. Render N-Grams
    this.renderNGramTables(data.top_bigrams, data.reference_bigrams, data.top_trigrams, data.reference_trigrams);
  },

  renderFrequencyChart(unigrams, lang) {
    const container = document.getElementById('ca-freq-bars-container');
    if (!container) return;

    let html = '';
    // Find max percentage to scale
    let maxPct = 20;
    unigrams.forEach(u => {
      if (u.percentage > maxPct) maxPct = u.percentage;
      if (u.expected_percentage > maxPct) maxPct = u.expected_percentage;
    });

    unigrams.forEach(u => {
      const hObs = Math.min(100, Math.max(2, (u.percentage / maxPct) * 100));
      const hExp = Math.min(100, Math.max(2, (u.expected_percentage / maxPct) * 100));

      html += `
        <div class="freq-bar-group" title="${u.letter}: Cipher=${u.percentage}% (${u.count}x) | Ref(${lang})=${u.expected_percentage}%">
          <div style="display: flex; gap: 2px; align-items: flex-end; width: 100%; height: 100%; justify-content: center;">
            <div class="freq-bar cipher" style="height: ${hObs}%; width: 45%;"></div>
            <div class="freq-bar reference" style="height: ${hExp}%; width: 45%;"></div>
          </div>
          <span class="freq-label">${u.letter}</span>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  renderNGramTables(topBg, refBg, topTg, refTg) {
    const bgContainer = document.getElementById('ca-bigram-tbody');
    const tgContainer = document.getElementById('ca-trigram-tbody');

    if (bgContainer) {
      let bgHtml = '';
      const len = Math.max(topBg.length, 6);
      for (let i = 0; i < Math.min(len, 8); i++) {
        const obs = topBg[i] || { ngram: '-', count: 0, percentage: 0 };
        const ref = refBg[i] || '-';
        bgHtml += `
          <tr>
            <td><strong>${obs.ngram}</strong> (${obs.count}x)</td>
            <td style="color: var(--accent-cyan); font-weight: bold;">${ref}</td>
          </tr>
        `;
      }
      bgContainer.innerHTML = bgHtml;
    }

    if (tgContainer) {
      let tgHtml = '';
      const len = Math.max(topTg.length, 6);
      for (let i = 0; i < Math.min(len, 8); i++) {
        const obs = topTg[i] || { ngram: '-', count: 0, percentage: 0 };
        const ref = refTg[i] || '-';
        tgHtml += `
          <tr>
            <td><strong>${obs.ngram}</strong> (${obs.count}x)</td>
            <td style="color: #c084fc; font-weight: bold;">${ref}</td>
          </tr>
        `;
      }
      tgContainer.innerHTML = tgHtml;
    }
  },

  renderMappingGrid() {
    const grid = document.getElementById('ca-substitution-grid');
    if (!grid) return;

    let html = '';
    for (let c = 65; c <= 90; c++) {
      const ch = String.fromCharCode(c);
      const val = this.mapping[ch] || '';
      const isMapped = val !== '';

      html += `
        <div class="sub-pair-card">
          <span class="sub-cipher-letter">${ch}</span>
          <span class="sub-arrow">&darr;</span>
          <input type="text" maxlength="1" 
            class="sub-plain-input ${isMapped ? 'mapped' : ''}" 
            data-cipher="${ch}" 
            value="${val}" 
            placeholder="_">
        </div>
      `;
    }

    grid.innerHTML = html;

    // Bind inputs
    const inputs = grid.querySelectorAll('.sub-plain-input');
    inputs.forEach(inp => {
      inp.addEventListener('input', (e) => {
        const cipherChar = inp.dataset.cipher;
        const plainChar = (e.target.value || '').toUpperCase().replace(/[^A-Z]/g, '');
        inp.value = plainChar;
        this.mapping[cipherChar] = plainChar;
        if (plainChar) {
          inp.classList.add('mapped');
        } else {
          inp.classList.remove('mapped');
        }
        this.updateLivePreview();
      });
    });
  },

  updateLivePreview() {
    const previewBox = document.getElementById('ca-live-preview');
    if (!previewBox) return;

    const raw = (this.ciphertext || '').toUpperCase();
    if (!raw) {
      previewBox.innerHTML = '<span style="color: var(--text-subtle);">Plaintext hasil tebakan akan muncul di sini secara real-time...</span>';
      return;
    }

    let html = '';
    for (let i = 0; i < raw.length; i++) {
      const ch = raw[i];
      if (ch >= 'A' && ch <= 'Z') {
        const guessed = this.mapping[ch];
        if (guessed) {
          html += `<span class="mapped-char">${guessed}</span>`;
        } else {
          html += `<span class="unmapped-char">${ch.toLowerCase()}</span>`;
        }
      } else {
        html += ch;
      }
    }

    previewBox.innerHTML = html;
  },

  async runAutoCrack() {
    const text = (document.getElementById('ca-ciphertext-input')?.value || '').trim();
    if (!text) {
      App.toast("Masukkan ciphertext terlebih dahulu untuk di-crack!", "error");
      return;
    }

    const btn = document.getElementById('btn-ca-autocrack');
    const statusBox = document.getElementById('ca-autocrack-result');
    if (btn) btn.disabled = true;
    if (btn) btn.textContent = '⏳ Menjalankan Heuristic Optimization (Hill Climbing)...';

    try {
      const resp = await fetch('/api/cryptanalysis/auto-crack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ciphertext: text, language: this.currentLang, iterations: 2000 })
      });

      const res = await resp.json();
      if (!res.success) {
        App.toast(res.error || "Gagal melakukan kriptanalisis otomatis.", "error");
        return;
      }

      const data = res.data;
      this.lastDiscoveredMapping = data.mapping;

      if (statusBox) {
        statusBox.style.display = 'block';
        document.getElementById('ca-auto-key').textContent = data.best_key;
        document.getElementById('ca-auto-score').textContent = data.fitness_score;
        document.getElementById('ca-auto-time').textContent = `${data.execution_time_ms} ms`;
        document.getElementById('ca-auto-preview').textContent = data.decrypted_text.substring(0, 300) + (data.decrypted_text.length > 300 ? '...' : '');
      }

      App.toast(`Auto-Crack berhasil dalam ${data.execution_time_ms} ms! Klik 'Terapkan Kunci' untuk visualisasi.`, "success");
    } catch (err) {
      App.toast("Kesalahan auto-crack: " + err.message, "error");
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = '🚀 Jalankan Kriptanalisis Otomatis (Hill Climbing)';
      }
    }
  }
};

window.Cryptanalysis = Cryptanalysis;
