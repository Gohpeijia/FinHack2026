import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
// IMPORT YOUR FIREBASE AUTH HERE (adjust the path if needed)
import { auth } from '../firebase'; 

const AIAdvisorContext = createContext(null);

const INITIAL_MESSAGES = [
  {
    role: 'assistant',
    content: 'Assalamualaikum. Saya AI Penasihat Shariah anda.',
  },
];

export function AIAdvisorProvider({ children }) {
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [loading, setLoading]   = useState(false);
  const [highlightedContext, setHighlightedContext] = useState(null);

  // Grouping messages into a daily session (matches backend fallback)
  const [conversationId] = useState(() => {
    return new Date().toISOString().split('T')[0]; // e.g., "2026-05-23"
  });

  // ── Load Chat History on Login ──
  useEffect(() => {
    const fetchHistory = async (user) => {
      try {
        const token = await user.getIdToken();
        const response = await fetch(`http://localhost:5000/api/aiagent/ai/history?session_id=${conversationId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        const data = await response.json();
        if (data.success && data.history && data.history.length > 0) {
          // Format backend history to match frontend expectations
          const formattedHistory = data.history.map(msg => ({
            role: msg.role, // 'user' or 'ai/assistant'
            content: msg.content
          }));
          setMessages([...INITIAL_MESSAGES, ...formattedHistory]);
        }
      } catch (error) {
        console.error("Failed to load chat history:", error);
      }
    };

    // Listen for auth state changes so history loads right after login
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        fetchHistory(user);
      } else {
        setMessages(INITIAL_MESSAGES); // Clear if logged out
      }
    });

    return () => unsubscribe();
  }, [conversationId]);

  const sendMessage = useCallback(async ({ text, fileData, fileName }) => {
    if (!text && !fileData && !highlightedContext) return;

    const userMsg = {
      role: 'user',
      content: text,
      fileName: fileName || null,
      highlightedText: highlightedContext || null, 
    };

    const textContextSnapshot = highlightedContext;
    setHighlightedContext(null);

    setMessages(prev => [...prev, userMsg]);

    _callBackend(
      conversationId,
      { text, fileData, fileName, highlightedText: textContextSnapshot },
      setMessages,
      setLoading
    );
    
  }, [conversationId, highlightedContext]);

  const clearMessages = useCallback(() => {
    setMessages(INITIAL_MESSAGES);
    setHighlightedContext(null);
    // Optional: Add logic here to call the DELETE /history backend route if you want to wipe the DB too
  }, []);

  return (
    <AIAdvisorContext.Provider value={{ 
      messages, 
      loading, 
      sendMessage, 
      clearMessages, 
      highlightedContext, 
      setHighlightedContext 
    }}>
      {children}
    </AIAdvisorContext.Provider>
  );
}

/** Internal helper — Server communication handler */
async function _callBackend(conversationId, { text, fileData, fileName, highlightedText }, setMessages, setLoading) {
  setLoading(true);
  try {
    const user = auth.currentUser;
    if (!user) throw new Error("Sila log masuk terlebih dahulu. (Please log in)");

    const token = await user.getIdToken();

    const payload = {
      session_id: conversationId,
      message: text,
      pageContext: highlightedText || "Unknown Page", 
      fileData: fileData,  
      fileName: fileName
    };

    // Make sure the URL matches your Flask server port (usually 5000)
    const response = await fetch('http://localhost:5000/api/aiagent/ai/chat', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` // Sends auth to @require_auth
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Server error');
    }

    if (data.success && data.data && data.data.final_advice) {
      setMessages(prev => [...prev, { role: 'assistant', content: data.data.final_advice }]);
    } else {
      throw new Error("Invalid response format from server.");
    }
    
  } catch (error) {
    console.error("AI Advisor Error:", error);
    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: 'Ralat berlaku. Sila semak sambungan anda dan cuba lagi.' },
    ]);
  } finally {
    setLoading(false);
  }
}

export const useAIAdvisor = () => useContext(AIAdvisorContext);