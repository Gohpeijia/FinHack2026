import React, {useState, useEffect} from 'react';
import ZakatRingkasan from './ZakatRingkasan';
import ZakatAsset from './ZakatAsset';
import ZakatCalculator from './ZakatCalculator';
import ZakatNisab from './ZakatNisab';
import ZakatLiabiliti from './ZakatLiabiliti';
import Zakatbleamount from './Zakatbleamount';
import ZakatGoals from './ZakatGoals';   
import './Zakat.css';
import '../shared.css';

export default function Zakat() {

  const [nisabAmount, setNisabAmount] = useState(0);
  const [totalAsset, setTotalAsset] = useState(0);
  const [totalLiability, setTotalLiability] = useState(0);
  const [dbData, setDbData] = useState({});

  useEffect(() => {
    const fetchZakatData = async () => {
      try {
        const user = auth.currentUser;
        if (!user) return;
        const token = await user.getIdToken();
        const headers = { Authorization: `Bearer ${token}` };
        // 1. Fetch live Nisab (Gold API)
        const nisabRes = await axios.get('http://127.0.0.1:5000/api/zakat/nisab', { headers });
        if (nisabRes.data.success) {
          setNisabAmount(nisabRes.data.data.nisab_value);
        }

        // 2. Fetch saved User Profile data
        const profileRes = await axios.get('http://127.0.0.1:5000/api/zakat/data', { headers });
        if (profileRes.data.success && profileRes.data.data) {
          setDbData(profileRes.data.data);
        }

      } catch (error) {
        console.error("Error fetching Zakat data:", error);
      }
    };

    fetchZakatData();
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

      {/* Section 6: Matlamat Kewangan ← NEW */}
      <ZakatGoals />
    </div>
  );
}