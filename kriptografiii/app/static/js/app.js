// ===================================================================
// App Coordinator (Navigation, Files, Toasts, Persistence)
// ===================================================================

const App = {
  init() {
    this.bindNavigation();
    this.bindModeSwitcher();
    this.bindFileInputs();
    this.bindExportButtons();
    this.bindTeamPersistence();
    this.bindMathAccordion();

    // Initialize sub-modules
    if (window.Ciphers) window.Ciphers.init();
    if (window.FileCiphers) window.FileCiphers.init();
    if (window.Cryptanalysis) window.Cryptanalysis.init();
    if (window.MathExplorer) window.MathExplorer.init();
  },

  bindModeSwitcher() {
    const btnText = document.getElementById('btn-mode-text');
    const btnBin = document.getElementById('btn-mode-binary');
    const subText = document.getElementById('subview-text-mode');
    const subBin = document.getElementById('subview-binary-mode');

    if (btnText && btnBin && subText && subBin) {
      btnText.addEventListener('click', () => {
        btnText.classList.add('active');
        btnBin.classList.remove('active');
        subText.classList.add('active');
        subBin.classList.remove('active');
      });

      btnBin.addEventListener('click', () => {
        btnBin.classList.add('active');
        btnText.classList.remove('active');
        subBin.classList.add('active');
        subText.classList.remove('active');
      });
    }
  },

  bindNavigation() {
    const tabButtons = document.querySelectorAll('.nav-tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTabId = btn.dataset.tab;
        tabButtons.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        const targetContent = document.getElementById(targetTabId);
        if (targetContent) targetContent.classList.add('active');
      });
    });
  },

  bindFileInputs() {
    // 1. Plaintext file input for Cipher section
    const cipherDropzone = document.getElementById('cipher-dropzone');
    const cipherFileInput = document.getElementById('cipher-file-input');
    const cipherTextArea = document.getElementById('cipher-input-text');
    const cipherFilename = document.getElementById('cipher-dropzone-filename');
    const cipherCharCount = document.getElementById('cipher-input-char-count');

    const updateCharCount = () => {
      const len = cipherTextArea?.value?.length || 0;
      if (cipherCharCount) cipherCharCount.textContent = `${len} Karakter`;
    };

    if (cipherTextArea) {
      cipherTextArea.addEventListener('input', updateCharCount);
      updateCharCount();
    }

    if (cipherDropzone && cipherFileInput) {
      cipherDropzone.addEventListener('click', () => cipherFileInput.click());

      cipherFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          cipherFilename.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
          const reader = new FileReader();
          reader.onload = (evt) => {
            cipherTextArea.value = evt.target.result;
            updateCharCount();
            App.toast(`File ${file.name} berhasil dibaca ke input teks!`, "success");
          };
          reader.readAsText(file);
        }
      });

      // Drag and drop events
      ['dragenter', 'dragover'].forEach(eventName => {
        cipherDropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          cipherDropzone.classList.add('dragover');
        });
      });
      ['dragleave', 'drop'].forEach(eventName => {
        cipherDropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          cipherDropzone.classList.remove('dragover');
        });
      });
      cipherDropzone.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        if (file) {
          cipherFilename.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
          const reader = new FileReader();
          reader.onload = (evt) => {
            cipherTextArea.value = evt.target.result;
            updateCharCount();
            App.toast(`File ${file.name} berhasil dimuat!`, "success");
          };
          reader.readAsText(file);
        }
      });
    }

    // Cryptanalysis file upload
    const btnCaUpload = document.getElementById('btn-ca-upload-file');
    const caFileInput = document.getElementById('ca-file-input');
    const caTextArea = document.getElementById('ca-ciphertext-input');

    if (btnCaUpload && caFileInput && caTextArea) {
      btnCaUpload.addEventListener('click', () => caFileInput.click());
      caFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (evt) => {
            caTextArea.value = evt.target.result;
            if (window.Cryptanalysis) {
              window.Cryptanalysis.ciphertext = evt.target.result.trim();
              window.Cryptanalysis.runFrequencyAnalysis();
            }
            App.toast(`Berkas ciphertext ${file.name} berhasil dimuat & dianalisis!`, "success");
          };
          reader.readAsText(file);
        }
      });
    }

    // Input mode toggle (Keyboard vs File Upload)
    const btnModeKeyboard = document.getElementById('btn-mode-keyboard');
    const btnModeFile = document.getElementById('btn-mode-file');
    const dropzoneContainer = document.getElementById('cipher-dropzone-container');

    if (btnModeKeyboard && btnModeFile && dropzoneContainer) {
      btnModeKeyboard.addEventListener('click', () => {
        btnModeKeyboard.classList.add('active');
        btnModeFile.classList.remove('active');
        dropzoneContainer.style.display = 'none';
      });
      btnModeFile.addEventListener('click', () => {
        btnModeFile.classList.add('active');
        btnModeKeyboard.classList.remove('active');
        dropzoneContainer.style.display = 'block';
      });
    }
  },

  bindExportButtons() {
    // Copy result
    const btnCopy = document.getElementById('btn-copy-result');
    if (btnCopy) {
      btnCopy.addEventListener('click', () => {
        const text = document.getElementById('cipher-output-display')?.textContent || '';
        if (text && text !== 'Hasil enkripsi/dekripsi akan tampil di sini...') {
          navigator.clipboard.writeText(text);
          App.toast("Hasil berhasil disalin ke clipboard!", "success");
        } else {
          App.toast("Tidak ada teks hasil untuk disalin.", "error");
        }
      });
    }

    // Download result as .txt file
    const btnDownload = document.getElementById('btn-download-result');
    if (btnDownload) {
      btnDownload.addEventListener('click', () => {
        const text = document.getElementById('cipher-output-display')?.textContent || '';
        if (text && text !== 'Hasil enkripsi/dekripsi akan tampil di sini...') {
          App.downloadFile(text, "ciphertext_output.txt");
          App.toast("File ciphertext_output.txt berhasil diunduh!", "success");
        } else {
          App.toast("Tidak ada teks hasil untuk diunduh.", "error");
        }
      });
    }
  },

  bindMathAccordion() {
    const accordion = document.getElementById('cipher-math-accordion');
    const header = document.querySelector('.math-accordion-header');
    if (accordion && header) {
      header.addEventListener('click', () => {
        accordion.classList.toggle('open');
      });
    }
  },

  bindTeamPersistence() {
    // Load saved team member details from localStorage
    const saved = localStorage.getItem('kripto_team_members');
    if (saved) {
      try {
        const members = JSON.parse(saved);
        members.forEach((m, idx) => {
          const nameEl = document.getElementById(`team-name-${idx}`);
          const nimEl = document.getElementById(`team-nim-${idx}`);
          const roleEl = document.getElementById(`team-role-${idx}`);
          if (nameEl && m.name) nameEl.value = m.name;
          if (nimEl && m.nim) nimEl.value = m.nim;
          if (roleEl && m.role) roleEl.value = m.role;
        });
      } catch (e) {
        console.error(e);
      }
    }

    const btnSaveTeam = document.getElementById('btn-save-team');
    if (btnSaveTeam) {
      btnSaveTeam.addEventListener('click', () => {
        const members = [];
        for (let idx = 0; idx < 4; idx++) {
          const nameEl = document.getElementById(`team-name-${idx}`);
          const nimEl = document.getElementById(`team-nim-${idx}`);
          const roleEl = document.getElementById(`team-role-${idx}`);
          members.push({
            name: nameEl?.value || '',
            nim: nimEl?.value || '',
            role: roleEl?.value || ''
          });
        }
        localStorage.setItem('kripto_team_members', JSON.stringify(members));
        App.toast("Data anggota kelompok berhasil disimpan!", "success");
      });
    }
  },

  downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  toast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? '✓' : type === 'error' ? '⚠️' : 'ℹ️';
    toast.innerHTML = `<span style="font-weight: bold;">${icon}</span><span>${message}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.4s ease';
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});

window.App = App;
