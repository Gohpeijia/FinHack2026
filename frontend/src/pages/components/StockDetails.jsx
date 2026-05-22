import React, { memo } from 'react';

/**
 * StockDetails — fundamentals panel: sector, market cap, PE, dividend, etc.
 *
 * Props:
 *  details: {
 *    sector, industry, marketCap, peRatio, dividendYield,
 *    eps, beta, avgVolume, fiftyTwoWeekHigh, fiftyTwoWeekLow,
 *    ... any extra key-value pairs
 *  }
 *  loading: bool
 */
const FIELDS = [
  { key: 'sector',          label: 'Sektor' },
  { key: 'industry',        label: 'Industri' },
  { key: 'marketCap',       label: 'Modal Pasaran' },
  { key: 'peRatio',         label: 'Nisbah PE' },
  { key: 'dividendYield',   label: 'Hasil Dividen' },
  { key: 'eps',             label: 'EPS' },
  { key: 'beta',            label: 'Beta' },
  { key: 'avgVolume',       label: 'Purata Volum' },
  { key: 'fiftyTwoWeekHigh',label: 'Tinggi 52M' },
  { key: 'fiftyTwoWeekLow', label: 'Rendah 52M' },
];

const StockDetails = memo(function StockDetails({ details, loading }) {
  return (
    <div className="stock-details-card">
      <h3 className="details-title">Company Details</h3>
      <div className="details-grid">
        {FIELDS.map(({ key, label }) => (
          <div className="detail-item" key={key}>
            <span className="detail-label">{label}</span>
            <span className={`detail-value${loading ? ' loading' : ''}`}>
              {loading ? '' : (details?.[key] ?? '—')}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
});

export default StockDetails;