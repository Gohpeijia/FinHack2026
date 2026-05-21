// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
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
const analytics = getAnalytics(app);
const auth = getAuth(app);