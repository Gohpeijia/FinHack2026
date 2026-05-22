import React, { useState } from 'react';
import './Zakat.css';

const NISAB_EMAS = 85; // grams of gold
const GOLD_PRICE_PER_GRAM = 380; // RM per gram (approximate, update as needed)
const NISAB_RM = NISAB_EMAS * GOLD_PRICE_PER_GRAM;
const ZAKAT_RATE = 0.025;

export default function ZakatCalculator() {
  const [income, setIncome] = useState('');
  const [savings, setSavings] = useState('');
  const [investments, setInvestments] = useState('');
  const [gold, setGold] = useState('');
  const [result, setResult] = useState(null);

  const calculate = () => {
    const total =
      (parseFloat(income) || 0) +
      (parseFloat(savings) || 0) +
      (parseFloat(investments) || 0) +
      (parseFloat(gold) || 0);

    if (total >= NISAB_RM) {
      setResult({
        total,
        zakatDue: total * ZAKAT_RATE,
        nisabMet: true,
      });
    } else {
      setResult({ total, zakatDue: 0, nisabMet: false });
    }
  };

  const reset = () => {
    setIncome('');
    setSavings('');
    setInvestments('');
    setGold('');
    setResult(null);
  };

  return (
    <section className="zakat-section">
      <h2 className="section-title">Kalkulator Zakat</h2>
      <p className="section-desc">
        Nisab semasa: <strong>RM {NISAB_RM.toLocaleString('en-MY')}</strong> (85g emas × RM {GOLD_PRICE_PER_GRAM}/g)
      </p>

      <div className="calc-card">
        <div className="calc-grid">
          <div className="calc-field">
            <label className="calc-label">Pendapatan Tahunan</label>
            <div className="asset-input-wrap">
              <span className="input-prefix">RM</span>
              <input
                className="asset-input"
                type="number"
                min="0"
                placeholder="0.00"
                value={income}
                onChange={(e) => setIncome(e.target.value)}
              />
            </div>
          </div>

          <div className="calc-field">
            <label className="calc-label">Simpanan</label>
            <div className="asset-input-wrap">
              <span className="input-prefix">RM</span>
              <input
                className="asset-input"
                type="number"
                min="0"
                placeholder="0.00"
                value={savings}
                onChange={(e) => setSavings(e.target.value)}
              />
            </div>
          </div>

          <div className="calc-field">
            <label className="calc-label">Pelaburan & Saham</label>
            <div className="asset-input-wrap">
              <span className="input-prefix">RM</span>
              <input
                className="asset-input"
                type="number"
                min="0"
                placeholder="0.00"
                value={investments}
                onChange={(e) => setInvestments(e.target.value)}
              />
            </div>
          </div>

          <div className="calc-field">
            <label className="calc-label">Nilai Emas (RM)</label>
            <div className="asset-input-wrap">
              <span className="input-prefix">RM</span>
              <input
                className="asset-input"
                type="number"
                min="0"
                placeholder="0.00"
                value={gold}
                onChange={(e) => setGold(e.target.value)}
              />
            </div>
          </div>
        </div>

        <div className="calc-actions">
          <button className="btn-calc" onClick={calculate}>Kira Zakat</button>
          <button className="btn-reset" onClick={reset}>Set Semula</button>
        </div>

        {result && (
          <div className={`calc-result ${result.nisabMet ? 'result--due' : 'result--none'}`}>
            <div className="result-row">
              <span>Jumlah Aset:</span>
              <strong>RM {result.total.toLocaleString('en-MY', { minimumFractionDigits: 2 })}</strong>
            </div>
            <div className="result-row">
              <span>Status Nisab:</span>
              <span className={`nisab-badge ${result.nisabMet ? 'nisab--met' : 'nisab--not'}`}>
                {result.nisabMet ? '✓ Cukup Nisab' : '✗ Tidak Cukup Nisab'}
              </span>
            </div>
            {result.nisabMet && (
              <div className="result-row result-highlight">
                <span>Zakat Wajib Dibayar (2.5%):</span>
                <strong className="highlight-amount">
                  RM {result.zakatDue.toLocaleString('en-MY', { minimumFractionDigits: 2 })}
                </strong>
              </div>
            )}
            {!result.nisabMet && (
              <p className="no-zakat-msg">Aset anda belum mencapai nisab. Zakat tidak wajib pada masa ini.</p>
            )}
          </div>
        )}
      </div>
    </section>
  );
}