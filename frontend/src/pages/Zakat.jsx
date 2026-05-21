import React from 'react';
import ZakatRingkasan from './ZakatRingkasan';
import ZakatAsset from './ZakatAsset';
import ZakatCalculator from './ZakatCalculator';
import './Zakat.css';

export default function Zakat() {
  return (
    <div className="zakat-page">
      <div className="zakat-header">
        <h1 className="zakat-main-title">Ringkasan Zakat</h1>
        <p className="zakat-subtitle">Pantau dan kira zakat anda dengan mudah</p>
      </div>

      {/* Section 1: Ringkasan Zakat */}
      <ZakatRingkasan />

      {/* Section 2: Jumlah Asset */}
      <ZakatAsset />

      {/* Section 3: Zakat Calculator */}
      <ZakatCalculator />
    </div>
  );
}