import React, { useState, useRef, useCallback, useEffect, memo } from 'react';

/**
 * StockSearchBar — search input + live dropdown.
 *
 * Props:
 *  onSelect : ({ ticker, name, exchange }) => void
 *  fetchSearchResults : async (query) => [{ ticker, name, exchange }]
 *    — caller supplies this so the component is backend-agnostic.
 *    — should return [] on error.
 */
const StockSearchBar = memo(function StockSearchBar({ onSelect, fetchSearchResults }) {
  const [query,    setQuery]    = useState('');
  const [results,  setResults]  = useState([]);
  const [loading,  setLoading]  = useState(false);
  const [open,     setOpen]     = useState(false);
  const debounceTimer = useRef(null);
  const wrapRef       = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClick(e) {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const handleChange = useCallback((e) => {
    const val = e.target.value;
    setQuery(val);

    clearTimeout(debounceTimer.current);

    if (!val.trim()) {
      setResults([]);
      setOpen(false);
      return;
    }

    setLoading(true);
    setOpen(true);

    debounceTimer.current = setTimeout(async () => {
      try {
        const data = await fetchSearchResults(val.trim());
        setResults(data);
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 350);
  }, [fetchSearchResults]);

  const handleSelect = useCallback((item) => {
    setQuery('');
    setOpen(false);
    setResults([]);
    onSelect(item);
  }, [onSelect]);

  const handleClear = useCallback(() => {
    setQuery('');
    setOpen(false);
    setResults([]);
    clearTimeout(debounceTimer.current);
  }, []);

  return (
    <div className="stock-search-wrap" ref={wrapRef}>
      <div className="stock-search-input-row">
        <span className="stock-search-icon">🔍</span>
        <input
          className="stock-search-input"
          type="text"
          placeholder="Cari saham melalui ticker atau nama…"
          value={query}
          onChange={handleChange}
          onFocus={() => query.trim() && setOpen(true)}
          autoComplete="off"
          spellCheck={false}
        />
        {query && (
          <button className="stock-search-clear" onClick={handleClear} title="Clear">✕</button>
        )}
      </div>

      {open && (
        <div className="stock-search-dropdown">
          {loading ? (
            <div className="search-dropdown-item loading">Searching…</div>
          ) : results.length === 0 ? (
            <div className="search-dropdown-item loading">No results found</div>
          ) : (
            results.map(item => (
              <div
                key={item.ticker}
                className="search-dropdown-item"
                onMouseDown={() => handleSelect(item)}
              >
                <span className="dropdown-ticker">{item.ticker}</span>
                <span className="dropdown-name">{item.name}</span>
                <span className="dropdown-exchange">{item.exchange}</span>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
});

export default StockSearchBar;