import React from 'react';
import './Zakat.css';

export default function ZakatNisab({ nisabAmount }) {
  // Safe fallback to a placeholder value if the parent hasn't provided the prop yet
  const displayAmount = nisabAmount !== undefined ? nisabAmount : 24320.50;

  return (
    <section className="zakat-section">
      <div className="ringkasan-grid">

        {/* Card: Nisab */}
        <div className="zakat-card card--due">
          <div className="card-amount" style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
            <div className="card-label" style={{ margin: 0 }}>Nisab Semasa (85g Emas)</div>
            
            <span className="price-container">
              <span className="currencyz">RM</span>
              <span className="amountz">{displayAmount.toFixed(2)}</span>
            </span>
          </div>
        </div>

      </div>
    </section>
  );
}