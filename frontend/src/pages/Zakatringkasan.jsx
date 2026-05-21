import React from 'react';
import './Zakat.css';

export default function ZakatRingkasan() {
  return (
    <section className="zakat-section">
      <div className="ringkasan-grid">

        {/* Card 1: Zakat Perlu Dibayar */}
        <div className="zakat-card card--due">
          <div className="card-label">Zakat Perlu Dibayar</div>
          <div className="card-amount">
            <span className="currency">RM</span>
            <span className="amount">0.00</span>
          </div>
          <div className="card-badge badge--warning">Belum Dibayar</div>
          <button className="card-action-btn">Bayar Sekarang</button>
        </div>

        {/* Card 2: Sejarah Sumbangan */}
        <div className="zakat-card card--history">
          <div className="card-label">Sejarah Sumbangan</div>
          <div className="card-amount">
            <span className="currency">RM</span>
            <span className="amount">0.00</span>
          </div>
          <div className="card-badge badge--success">Jumlah Dibayar</div>
          <button className="card-action-btn card-action-btn--secondary">
            <span className="edit-icon">✎</span> Lihat Rekod
          </button>
        </div>

      </div>
    </section>
  );
}