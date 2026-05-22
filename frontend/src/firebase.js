import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore"; // 🟢 ADDED: Import Firestore

const firebaseConfig = {
  apiKey: "AIzaSyBbZoFjUbJijZp4FiGWP5ifAHwcTY_aPiU",
  authDomain: "finhack2026-b44b3.firebaseapp.com",
  projectId: "finhack2026-b44b3",
  storageBucket: "finhack2026-b44b3.firebasestorage.app",
  messagingSenderId: "1080192879602",
  appId: "1:1080192879602:web:d8e61ad3e0280ed37f396b",
  measurementId: "G-SWG458HFXW"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);

// 🟢 EXPORT auth and db so your components can access them!
export const auth = getAuth(app);
export const db = getFirestore(app);