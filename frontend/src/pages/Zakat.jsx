import React, {useState, useEffect} from 'react';
import ZakatRingkasan from './ZakatRingkasan';
import ZakatAsset from './ZakatAsset';
import ZakatCalculator from './ZakatCalculator';
import ZakatNisab from './ZakatNisab';
import ZakatLiabiliti from './ZakatLiabiliti';
import Zakatbleamount from './Zakatbleamount';
import './Zakat.css';
import '../shared.css';

export default function Zakat() {

  const [nisabAmount, setNisabAmount] = useState(0);
  const [totalAsset, setTotalAsset] = useState(0);
  const [totalLiability, setTotalLiability] = useState(0);

  useEffect(() => {
    const fetchNisabAmount = async () => {
      try {
        // TODO: Replace this with your actual Axios/Fetch call later
        // const response = await fetch('https://your-api.com/nisab');
        // const data = await response.json();
        // setNisabAmount(data.currentNisab);
        
        // Simulating the API response for now so your UI doesn't break
        const simulatedApiResponse = 24320.50; 
        setNisabAmount(simulatedApiResponse);
      } catch (error) {
        console.error("Error fetching Nisab amount:", error);
      }
    };

    fetchNisabAmount();
  }, []);

  return (
    <div className="zakat-page">
      <div className="zakat-header">
        <h1 className="zakat-main-title">Ringkasan Zakat</h1>
        <p className="zakat-subtitle">Pantau dan kira zakat anda dengan mudah</p>
      </div>

      {/*Section 1: Nisab */}
      <ZakatNisab nisabAmount={nisabAmount} />

      {/* Section 2: Jumlah Bersih (Aset - Liabiliti) */}
      <Zakatbleamount totalAsset={totalAsset} totalLiability={totalLiability} nisabAmount={nisabAmount} />
      {/* Section 5: Ringkasan Zakat */}
      <ZakatRingkasan 
        nisabAmount={nisabAmount}
        totalAsset={totalAsset} 
        totalLiability={totalLiability} 
      />

      {/* Section 3: Jumlah Asset */}
      <ZakatAsset onTotalChange={setTotalAsset}/>

      {/* Section 4: Jumlah Liabiliti */}
      <ZakatLiabiliti onTotalChange={setTotalLiability} />

    </div>
  );
}