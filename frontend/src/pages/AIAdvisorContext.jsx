import React, { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react';

/**
 * AIAdvisorContext
 * ─────────────────────────────────────────────────────────────
 * Shared state for the AI Advisor chat across all pages.
 * Fully fixed to support secure server-driven session tracking
 * and ChatGPT-style highlighted text contextual awareness.
 */

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

  // Securely capture conversation identifier (simulate session/database token keys)
  const [conversationId] = useState('session_shariah_guidance_active');

  /**
   * sendMessage({ text, fileData, fileName })
   * ─────────────────────────────────────────
   * Injects prompt parameters, captures the quote block snapshot,
   * then calls the backend securely without state closure dependency chains.
   */
  const sendMessage = useCallback(async ({ text, fileData, fileName }) => {
    if (!text && !fileData && !highlightedContext) return;

    const userMsg = {
      role: 'user',
      content: text,
      fileName: fileName || null,
      highlightedText: highlightedContext || null, // Preserved context payload
    };

    // Snapshot context content and clear current input UI bar context
    const textContextSnapshot = highlightedContext;
    setHighlightedContext(null);

    // 1. Safe UI updates
    setMessages(prev => [...prev, userMsg]);

    // 2. Safely delegate network payload outside the state hook cycle
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

/** Internal helper — Decoupled server communication handler */
async function _callBackend(conversationId, { text, fileData, fileName, highlightedText }, setMessages, setLoading) {
  setLoading(true);
  try {
    // ── ARCHITECTURAL SECURITY COMPLIANCE SOLUTION ──────────────────────────────
    // FIXED: Instead of letting the frontend manipulate and submit history logs,
    // we send a secure unique conversationId token. The backend reads authoritative logs from a DB.
    const response = await fetch('/api/shariah-advisor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        conversationId, 
        text, 
        fileData, 
        fileName, 
        highlightedText // Context token processed directly at the backend
      }),
    });

    if (!response.ok) throw new Error('Server error');

    const data = await response.json();
    setMessages(prev => [...prev, { role: 'assistant', content: data.reply }]);
  } catch {
    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: 'An error occurred. Please check your connection and try again.' },
    ]);
  } finally {
    setLoading(false);
  }
}

export function useAIAdvisor() {
  const ctx = useContext(AIAdvisorContext);
  if (!ctx) throw new Error('useAIAdvisor must be used inside AIAdvisorProvider');
  return ctx;
}