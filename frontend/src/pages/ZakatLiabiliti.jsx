import React, { useState , useEffect } from 'react';
import './Zakat.css';

const liabilitiTypes = [
  { key: 'hutangperibadi', label: 'Hutang Peribadi', icon: '👤' },
  { key: 'pinjamankenderaan', label: 'Pinjaman Kenderaan', icon: '🚗' },
  { key: 'pinjamanrumah', label: 'Pinjaman Rumah', icon: '🏠' },
  { key: 'lain', label: 'Liabiliti Lain-lain', icon: '📋' },
];

export default function ZakatLiabiliti({ onTotalChange }) {

  // 1. Declare state FIRST
  const [liabiliti, setLiabiliti] = useState({
    hutangperibadi: [
      { id: 'hp-1', label: 'Kad Kredit', amount: '' },
      { id: 'hp-2', label: 'Hutang Peribadi', amount: '' }
    ],
    pinjamankenderaan: [
      { id: 'pk-1', label: 'Ansuran Kereta', amount: '' }
    ],
    pinjamanrumah: [
      { id: 'pr-1', label: 'Ansuran Rumah', amount: '' }
    ],
    lain: [
      { id: 'lain-1', label: 'Liabiliti Lain', amount: '' }
    ]
  });

  const [expanded, setExpanded] = useState({
    hutangperibadi: true,
    pinjamankenderaan: false,
    pinjamanrumah: false,
    lain: false
  });

  const [isEditing, setIsEditing] = useState(false);

  // 2. Declare helper functions SECOND
  const getCategoryTotal = (key) => {
    return liabiliti[key].reduce((sum, item) => sum + (parseFloat(item.amount) || 0), 0);
  };

  // 3. Perform calculations that depend on state and helpers THIRD
  const grandTotal = liabilitiTypes.reduce((sum, type) => sum + getCategoryTotal(type.key), 0);

  // 4. Run effects FOURTH
  useEffect(() => {
    if (onTotalChange) {
      onTotalChange(grandTotal);
    }
  }, [grandTotal, onTotalChange]);

  // ... (The rest of your handler functions and return statement remain exactly the same)
  const toggleExpand = (key) => {
    setExpanded((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleItemChange = (categoryKey, itemId, field, value) => {
    setLiabiliti((prev) => ({
      ...prev,
      [categoryKey]: prev[categoryKey].map((item) =>
        item.id === itemId ? { ...item, [field]: value } : item
      )
    }));
  };

  const handleAddItem = (categoryKey) => {
    const newItem = {
      id: `${categoryKey}-${Date.now()}`,
      label: '',
      amount: ''
    };
    setLiabiliti((prev) => ({
      ...prev,
      [categoryKey]: [...prev[categoryKey], newItem]
    }));
  };

  const handleDeleteItem = (categoryKey, itemId) => {
    setLiabiliti((prev) => ({
      ...prev,
      [categoryKey]: prev[categoryKey].filter((item) => item.id !== itemId)
    }));
  };

  const handleActionClick = async () => {
    if (isEditing) {
      try {
        console.log("Saving liabiliti to database...", liabiliti);
        // Tempat letak panggilan API/Axios anda nanti
        setIsEditing(false);
      } catch (error) {
        console.error("Gagal menyimpan data:", error);
      }
    } else {
      setIsEditing(true);
    }
  };

  return (
    <section className="zakat-section">
      <h2 className="section-title">Jumlah Liabiliti</h2>
      <p className="section-desc">Masukkan nilai semasa liabiliti anda untuk pengiraan yang tepat.</p>

      <div className="asset-card">
        <div className="edit-hint-banner">
          <span>Sila klik butang ikon pen (✎) di penjuru kanan bawah untuk mula mengemas kini atau menambah sub-kategori liabiliti anda.</span>
        </div>

        <div className="asset-rows">
          {liabilitiTypes.map(({ key, label, icon }) => {
            const isCategoryOpen = expanded[key];
            const catTotal = getCategoryTotal(key);

            return (
              <div key={key} className="asset-category-group">
                <div
                  className={`asset-row clickable ${isCategoryOpen ? 'active-row' : ''}`}
                  onClick={() => toggleExpand(key)}
                  title="Klik untuk melihat pecahan"
                >
                  <div className="asset-row-label">
                    <span className={`dropdown-chevron ${isCategoryOpen ? 'open' : ''}`}>▶</span>
                    <span className="asset-icon">{icon}</span>
                    <span className="category-main-text">{label}</span>
                  </div>
                  <div className="category-total-display liabiliti-total">
                    RM {catTotal.toLocaleString('en-MY', { minimumFractionDigits: 2 })}
                  </div>
                </div>

                {isCategoryOpen && (
                  <div className="sub-items-container">
                    {liabiliti[key].map((item) => (
                      <div className="sub-item-row" key={item.id}>
                        <input
                          className="sub-item-name-input"
                          type="text"
                          placeholder="Nama item (cth: CIMB Kad Kredit, Pinjaman ASB)"
                          value={item.label}
                          onChange={(e) => handleItemChange(key, item.id, 'label', e.target.value)}
                          disabled={!isEditing}
                        />

                        <div className={`asset-input-wrap ${!isEditing ? 'disabled-wrap' : ''}`}>
                          <span className="input-prefix liabiliti-prefix">RM</span>
                          <input
                            className="asset-input"
                            type="number"
                            min="0"
                            placeholder="0.00"
                            value={item.amount}
                            onChange={(e) => handleItemChange(key, item.id, 'amount', e.target.value)}
                            disabled={!isEditing}
                          />
                        </div>

                        {isEditing && (
                          <button
                            type="button"
                            className="btn-delete-sub"
                            onClick={() => handleDeleteItem(key, item.id)}
                            title="Padam sub-kategori"
                          >
                            🗑️
                          </button>
                        )}
                      </div>
                    ))}

                    {isEditing && (
                      <button
                        type="button"
                        className="btn-add-sub"
                        onClick={() => handleAddItem(key)}
                      >
                        ＋ Tambah Item Baru
                      </button>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Bar Jumlah Keseluruhan */}
        <div className="asset-total-row liabiliti-total-row">
          <span className="total-label">Jumlah Keseluruhan Liabiliti</span>
          <span className="total-amount liabiliti-total-amount">
            RM {grandTotal.toLocaleString('en-MY', { minimumFractionDigits: 2 })}
          </span>
        </div>

        {/* Floating Action Button */}
        <button
          className={`edit-fab ${isEditing ? 'save-mode' : ''}`}
          onClick={handleActionClick}
          title={isEditing ? "Simpan Liabiliti ke Database" : "Edit Liabiliti"}
        >
          {isEditing ? '💾' : '✎'}
        </button>
      </div>
    </section>
  );
}