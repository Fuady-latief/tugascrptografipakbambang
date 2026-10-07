// ===================================================================
// Math Explorer Controller (Kalkulator Aljabar Kriptografi & Modulo 26)
// ===================================================================

const MathExplorer = {
  init() {
    this.bindEgcd();
    this.bindMatrixCalc();
  },

  bindEgcd() {
    const btn = document.getElementById('btn-calc-egcd');
    if (!btn) return;

    btn.addEventListener('click', async () => {
      const a = parseInt(document.getElementById('egcd-a').value, 10);
      const m = parseInt(document.getElementById('egcd-m').value, 10);

      try {
        const resp = await fetch('/api/math/egcd', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ a, m })
        });
        const res = await resp.json();
        if (res.success) {
          const resBox = document.getElementById('egcd-result-box');
          resBox.style.display = 'block';
          document.getElementById('egcd-gcd-val').textContent = res.gcd;
          document.getElementById('egcd-equation').textContent = `${a} * (${res.x}) + ${m} * (${res.y}) = ${res.gcd}`;
          document.getElementById('egcd-inv-val').textContent = res.inverse !== null ? `${res.inverse}` : 'Tidak Ada (Bukan Koprima)';
          document.getElementById('egcd-coprime-status').textContent = res.coprime ? 'Ya (Relatif Prima / Koprima)' : 'Tidak (Mempunyai Faktor Bersama)';
          App.toast("Kalkulasi Extended Euclidean selesai!", "success");
        }
      } catch (err) {
        App.toast("Kesalahan: " + err.message, "error");
      }
    });
  },

  bindMatrixCalc() {
    const btn = document.getElementById('btn-calc-matrix-inv');
    if (!btn) return;

    btn.addEventListener('click', async () => {
      const dim = parseInt(document.querySelector('input[name="math-mat-dim"]:checked')?.value || '2', 10);
      const mat = [];

      for (let r = 0; r < dim; r++) {
        const row = [];
        for (let c = 0; c < dim; c++) {
          const val = parseInt(document.getElementById(`mm-${r}-${c}`)?.value || '0', 10);
          row.push(val);
        }
        mat.push(row);
      }

      try {
        const resp = await fetch('/api/cipher/hill/validate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ matrix: mat })
        });
        const res = await resp.json();
        const resBox = document.getElementById('matrix-calc-result-box');
        resBox.style.display = 'block';

        if (res.success) {
          const d = res.data;
          document.getElementById('mcalc-det-raw').textContent = d.det;
          document.getElementById('mcalc-det-mod').textContent = d.det_mod;
          document.getElementById('mcalc-det-inv').textContent = d.det_inv;
          document.getElementById('mcalc-adj-matrix').textContent = JSON.stringify(d.adjugate);
          document.getElementById('mcalc-inv-matrix').textContent = JSON.stringify(d.inverse_matrix);
          document.getElementById('mcalc-status').innerHTML = '<span class="badge badge-green">✓ Invertible pada Modulo 26</span>';
          App.toast("Invers matriks modulo 26 berhasil dihitung!", "success");
        } else {
          document.getElementById('mcalc-status').innerHTML = `<span class="badge badge-amber">✗ ${res.error || 'Matriks tidak dapat diinvers'}</span>`;
          document.getElementById('mcalc-det-raw').textContent = '-';
          document.getElementById('mcalc-det-mod').textContent = '-';
          document.getElementById('mcalc-det-inv').textContent = 'Tidak Ada';
          document.getElementById('mcalc-adj-matrix').textContent = '-';
          document.getElementById('mcalc-inv-matrix').textContent = '-';
        }
      } catch (err) {
        App.toast("Kesalahan matriks: " + err.message, "error");
      }
    });

    // Dimension toggle
    const radioDims = document.querySelectorAll('input[name="math-mat-dim"]');
    radioDims.forEach(rd => {
      rd.addEventListener('change', () => {
        const dim = parseInt(rd.value, 10);
        const container = document.getElementById('math-matrix-grid-container');
        if (dim === 2) {
          container.innerHTML = `
            <div class="matrix-grid-2x2">
              <input type="number" class="matrix-cell" id="mm-0-0" value="3">
              <input type="number" class="matrix-cell" id="mm-0-1" value="3">
              <input type="number" class="matrix-cell" id="mm-1-0" value="2">
              <input type="number" class="matrix-cell" id="mm-1-1" value="5">
            </div>
          `;
        } else {
          container.innerHTML = `
            <div class="matrix-grid-3x3">
              <input type="number" class="matrix-cell" id="mm-0-0" value="6">
              <input type="number" class="matrix-cell" id="mm-0-1" value="24">
              <input type="number" class="matrix-cell" id="mm-0-2" value="1">
              <input type="number" class="matrix-cell" id="mm-1-0" value="13">
              <input type="number" class="matrix-cell" id="mm-1-1" value="16">
              <input type="number" class="matrix-cell" id="mm-1-2" value="10">
              <input type="number" class="matrix-cell" id="mm-2-0" value="20">
              <input type="number" class="matrix-cell" id="mm-2-1" value="17">
              <input type="number" class="matrix-cell" id="mm-2-2" value="15">
            </div>
          `;
        }
      });
    });
  }
};

window.MathExplorer = MathExplorer;
