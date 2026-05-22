import React, { useState } from 'react';
import './Zakat.css';

const assetTypes = [
  { key: 'simpanan', label: 'Simpanan Tunai', icon: '🏦' },
  { key: 'pelaburan', label: 'Pelaburan & Saham', icon: '📈' },
  { key: 'emas', label: 'Emas & Perak', icon: '🪙' },
  { key: 'perniagaan', label: 'Aset Perniagaan', icon: '💼' },
];

export default function ZakatAsset() {
  const [assets, setAssets] = useState({
    simpanan: '',
    pelaburan: '',
    emas: '',
    perniagaan: '',
  });

  const total = Object.values(assets)
    .map((v) => parseFloat(v) || 0)
    .reduce((a, b) => a + b, 0);

  const handleChange = (key, value) => {
    setAssets((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <section className="zakat-section">
      <h2 className="section-title">Jumlah Asset</h2>
      <p className="section-desc">Masukkan nilai semasa aset anda untuk pengiraan yang tepat.</p>

      <div className="asset-card">
        <div className="asset-rows">
          {assetTypes.map(({ key, label, icon }) => (
            <div className="asset-row" key={key}>
              <div className="asset-row-label">
                <span className="asset-icon">{icon}</span>
                <span>{label}</span>
              </div>
              <div className="asset-input-wrap">
                <span className="input-prefix">RM</span>
                <input
                  className="asset-input"
                  type="number"
                  min="0"
                  placeholder="0.00"
                  value={assets[key]}
                  onChange={(e) => handleChange(key, e.target.value)}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="asset-total-row">
          <span className="total-label">Jumlah Keseluruhan</span>
          <span className="total-amount">
            RM {total.toLocaleString('en-MY', { minimumFractionDigits: 2 })}
          </span>
        </div>

        <button className="edit-fab" title="Edit Aset">✎</button>
      </div>
    </section>
  );
}