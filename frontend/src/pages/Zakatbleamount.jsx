import React from 'react';
import './Zakat.css';

// FIX: Added nisabAmount = 0 to the props here!
export default function Zakatbleamount({ totalAsset = 0, totalLiability = 0, nisabAmount = 0 }) {
  // Calculate the net amount (Asset - Liability)
  const netAmount = totalAsset - totalLiability;
  
  // Safe fallback to prevent negative zakatable amounts if liabilities exceed assets
  const displayAmount = netAmount > 0 ? netAmount : 0.00;

  // Now this will work because nisabAmount is passed in
  const isEligible = displayAmount >= nisabAmount;

  return (
    <section className="zakat-section">
      <div className="ringkasan-grid">

        {/* Card: Zakatble Amount */}
        <div className="zakat-card card--due">
          <div className="card-amount" style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
            <div className="card-label" style={{ margin: 0 }}>Jumlah Bersih (Aset - Liabiliti)</div>
            
            <span className="price-container">
              <span className="currencyz">RM</span>
              <span className="amountz">{displayAmount.toLocaleString('en-MY', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </span>
          </div>
        </div>

      </div>
    </section>
  );
}