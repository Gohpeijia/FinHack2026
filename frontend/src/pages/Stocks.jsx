import React, { useState, useCallback, useEffect, useRef } from 'react';
import './stocks.css';

// 🟢 Import Firebase tools
import { db, auth } from '../firebase'; // Adjust this path if your firebase.js is somewhere else
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { onAuthStateChanged } from 'firebase/auth';

import StockSidePanel from './components/StockSidePanel';
import StockSearchBar from './components/StockSearchBar';
import StockHeader    from './components/StockHeader';
import StockChart     from './components/StockChart';
import StockDetails   from './components/StockDetails';

/* ──────────────────────────────────────────────────────────────
   API INTEGRATION POINTS (Mock Data so UI doesn't crash)
   ────────────────────────────────────────────────────────────── */
async function apiSearchStocks(query) {
  // Mock search result
  return [
    { ticker: 'MAYBANK', name: 'Malayan Banking Bhd', exchange: 'KLSE' },
    { ticker: 'TENAGA', name: 'Tenaga Nasional Bhd', exchange: 'KLSE' }
  ].filter(s => s.ticker.includes(query.toUpperCase()) || s.name.toLowerCase().includes(query.toLowerCase()));
}

async function apiFetchQuote(ticker) {
  return { ticker, name: ticker, exchange: 'KLSE', price: 9.85, change: 0.12, changePct: 1.23 };
}

async function apiFetchChart(ticker, period) {
  let dataLength = 30;
  let labelPrefix = 'Day';

  // Generate different mock data based on the chosen period
  switch (period) {
    case '1D':  dataLength = 24; labelPrefix = 'Hour'; break;
    case '1W':  dataLength = 7;  labelPrefix = 'Day'; break;
    case '1M':  dataLength = 30; labelPrefix = 'Day'; break;
    case '3M':  dataLength = 12; labelPrefix = 'Week'; break;
    case '1Y':  dataLength = 12; labelPrefix = 'Month'; break;
    case 'ALL': dataLength = 5;  labelPrefix = 'Year'; break;
    default:    dataLength = 30; labelPrefix = 'Day'; break;
  }

  const data = Array.from({length: dataLength}, (_, i) => ({ 
    label: `${labelPrefix} ${i + 1}`, 
    price: 9.00 + Math.random() 
  }));
  
  return { data, high: 10.00, low: 9.00 };
}

async function apiFetchDetails(ticker) {
  return { sector: 'Kewangan', marketCap: 'RM 118B', peRatio: 12.5, dividendYield: '5.8%' };
}

/* ──────────────────────────────────────────────────────────────
   MAIN STOCKS PAGE
   ────────────────────────────────────────────────────────────── */
export default function Stocks() {
  const [watchlist, setWatchlist] = useState([]);
  const [activeTicker, setActiveTicker] = useState(null);
  
  // 🟢 NEW: Error state
  const [errorMsg, setErrorMsg] = useState(null);

  const [quote, setQuote] = useState(null);
  const [quoteLoading, setQuoteLoading] = useState(false);

  const [chartData, setChartData]   = useState(null);
  const [chartHigh, setChartHigh]   = useState(null);
  const [chartLow,  setChartLow]    = useState(null);
  const [period, setPeriod]         = useState('1Y');
  const [chartLoading, setChartLoading] = useState(false);

  const [details, setDetails]           = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);

  // 🟢 1. Load Watchlist from Firebase when user logs in
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        try {
          const docRef = doc(db, 'users', user.uid);
          const docSnap = await getDoc(docRef);
          if (docSnap.exists() && docSnap.data().watchlist) {
            setWatchlist(docSnap.data().watchlist);
          }
        } catch (err) {
          console.error("Gagal memuat turun senarai pantauan:", err);
        }
      } else {
        setWatchlist([]); // Clear if logged out
      }
    });
    return () => unsubscribe();
  }, []);

  // 🟢 2. Save Watchlist to Firebase whenever it changes
  useEffect(() => {
    const saveToFirebase = async () => {
      if (auth.currentUser) {
        try {
          const docRef = doc(db, 'users', auth.currentUser.uid);
          await setDoc(docRef, { watchlist }, { merge: true });
        } catch (err) {
          console.error("Gagal menyimpan ke Firebase:", err);
        }
      }
    };
    saveToFirebase();
  }, [watchlist]);

  // ── Load quote + details ──
  useEffect(() => {
    if (!activeTicker) return;
    let cancelled = false;
    setErrorMsg(null); // Reset error

    setQuoteLoading(true);
    setDetailsLoading(true);

    apiFetchQuote(activeTicker)
      .then(data => { if (!cancelled) { setQuote(data); setQuoteLoading(false); } })
      .catch(() => { if (!cancelled) { setQuoteLoading(false); setErrorMsg("Gagal mendapatkan data harga."); } });

    apiFetchDetails(activeTicker)
      .then(data => { if (!cancelled) { setDetails(data); setDetailsLoading(false); } })
      .catch(() => { if (!cancelled) setDetailsLoading(false); });

    return () => { cancelled = true; };
  }, [activeTicker]);

  // ── Load chart ──
  useEffect(() => {
    if (!activeTicker) return;
    let cancelled = false;

    setChartLoading(true);
    apiFetchChart(activeTicker, period)
      .then(({ data, high, low }) => {
        if (!cancelled) {
          setChartData(data); setChartHigh(high); setChartLow(low); setChartLoading(false);
        }
      })
      .catch(() => { if (!cancelled) setChartLoading(false); });

    return () => { cancelled = true; };
  }, [activeTicker, period]);


  // ── Select stock (from search or watchlist) ──
  const handleSelectStock = useCallback((item) => {
    // item: { ticker, name, exchange }
    setActiveTicker(item.ticker);
    setQuote(null);
    setChartData(null);
    setDetails(null);
    setPeriod('1Y');
  }, []);

  // ── Watchlist actions ──
  const isSaved = watchlist.some(s => s.ticker === activeTicker);

  const handleToggleSave = useCallback(() => {
    if (!quote && !activeTicker) return;
    const stock = quote ?? { ticker: activeTicker, name: activeTicker, exchange: '', price: null, change: null, changePct: null };
    setWatchlist(prev => {
      if (prev.some(s => s.ticker === stock.ticker)) {
        return prev.filter(s => s.ticker !== stock.ticker);
      }
      return [...prev, { ticker: stock.ticker, name: stock.name, exchange: stock.exchange, price: stock.price, change: stock.change, changePct: stock.changePct }];
    });
  }, [quote, activeTicker]);

  const handleDeleteFromWatchlist = useCallback((ticker) => {
    setWatchlist(prev => prev.filter(s => s.ticker !== ticker));
  }, []);

  const handleReorder = useCallback((newList) => {
    setWatchlist(newList);
  }, []);

  // ── Derive display data ──
  const displayName     = quote?.name     ?? activeTicker ?? '';
  const displayExchange = quote?.exchange ?? '';
  const displayPrice    = quote?.price    ?? null;
  const displayChange   = quote?.change   ?? null;
  const displayChangePct= quote?.changePct?? null;
  const isPositive      = (displayChange ?? 0) >= 0;

  return (
    <div className="stocks-page">
      {/* ── Watchlist Side Panel ── */}
      <StockSidePanel
        watchlist={watchlist}
        activeTicker={activeTicker}
        onSelect={(ticker) => {
          const stock = watchlist.find(s => s.ticker === ticker);
          handleSelectStock(stock ?? { ticker, name: ticker, exchange: '' });
        }}
        onReorder={handleReorder}
        onDelete={handleDeleteFromWatchlist}
      />

      {/* ── Main Content ── */}
      <main className="stocks-main">
        {/* Search Bar */}
        <StockSearchBar
          onSelect={handleSelectStock}
          fetchSearchResults={apiSearchStocks}
        />

        {/* Empty state */}
        {!activeTicker && (
          <div className="stocks-empty-state">
            <div className="stocks-empty-icon">📈</div>
            <h3 className="stocks-empty-title">Cari saham untuk mula</h3>
            <p className="stocks-empty-sub">
              Gunakan bar carian di atas untuk mencari saham, atau pilih satu daripada senarai pantauan anda
            </p>
          </div>
        )}

        {/* Stock view */}
        {activeTicker && (
          <>
            <StockHeader
              ticker={activeTicker}
              name={displayName}
              exchange={displayExchange}
              price={displayPrice}
              change={displayChange}
              changePct={displayChangePct}
              loading={quoteLoading}
            />

            <StockChart
              chartData={chartData}
              period={period}
              onPeriod={setPeriod}
              high={chartHigh}
              low={chartLow}
              isSaved={isSaved}
              onToggleSave={handleToggleSave}
              loading={chartLoading}
              isPositive={isPositive}
            />

            <StockDetails
              details={details}
              loading={detailsLoading}
            />
          </>
        )}
      </main>
    </div>
  );
}