import React, { useState } from 'react';
import './Zakat.css';

export default function Zakatbleamount({ totalAsset = 0, totalLiability = 0, nisabAmount = 0 }) {
  const [isEditing, setIsEditing] = useState(false);
  const [haulDate, setHaulDate] = useState('2026-01-01'); // Default fallback date

  const netAmount = totalAsset - totalLiability;
  const displayAmount = netAmount > 0 ? netAmount : 0.00;

  // Triggers automatically as soon as a user selects a date
  const handleDateChange = (e) => {
    const selectedDate = e.target.value;
    setHaulDate(selectedDate);
    
    // Your backend friend's saving routine can be triggered here instantly
    console.log("Auto-saving Haul Date to database:", selectedDate);
    
    // Automatically close the editing state
    setIsEditing(false);
  };

  const formatDateDisplay = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    
    return date.toLocaleDateString('en-MY', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    }).replace(/ /g, '-');
  };

  return (
    <section className="zakat-section">
      <div className="ringkasan-grid">

        {/* Card: Zakatble Amount (Strictly Read-Only - No Edit Button Here) */}
        <div className="zakat-card card--history">
          <div >
            <div className="card-label" >Jumlah Bersih <br/>(Aset - Liabiliti)</div>
            
            <span className="price-container">
              <span className="currencyz">RM</span>
              <span className="amountz">{displayAmount.toLocaleString('en-MY', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </span>
          </div>
        </div>

        {/* Card: Haul Date (The only card with the edit button functionality) */}
        <div className="zakat-card card--history" style={{ position: 'relative' }}>
          <div className="card-label">Haul</div>
          <div className="card-amount">
            {isEditing ? (
              <div className="asset-input-wrap">
                <input 
                  type="date" 
                  className="asset-input" 
                  value={haulDate} 
                  onChange={handleDateChange} 
                  onBlur={() => setIsEditing(false)} 
                  autoFocus 
                  style={{ width: '100%' }}
                />
              </div>
            ) : (
              <span className="date">{formatDateDisplay(haulDate)}</span>
            )}
          </div>
          
          {/* Edit button is localized explicitly inside the Haul card context */}
          {!isEditing && (
            <button 
              className="edit-fab" 
              onClick={() => setIsEditing(true)}
              title="Edit Haul"
            >
              ✎
            </button>
          )}
        </div>

      </div>
    </section>
  );
}