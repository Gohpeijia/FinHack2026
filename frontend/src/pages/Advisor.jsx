import React, { useState, useRef, useEffect } from 'react';
import '../shared.css';
import './Advisor.css';
import { FaPaperPlane, FaPaperclip, FaTimes, FaFileAlt, FaRobot } from 'react-icons/fa';

export default function Advisor() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Assalamualaikum. Saya AI Penasihat Shariah anda.",
    },
  ]);
  const [input, setInput] = useState('');
  const [attachedFile, setAttachedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 160) + 'px';
  }, [input]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setAttachedFile(file);

    const reader = new FileReader();
    reader.onload = (ev) => setFileContent(ev.target.result.split(',')[1]);
    reader.readAsDataURL(file);
    e.target.value = '';
  };

  const removeFile = () => {
    setAttachedFile(null);
    setFileContent(null);
  };

  const sendMessage = async () => {
    const text = input.trim();
    if (!text && !attachedFile) return;

    const userMsg = {
      role: 'user',
      content: text,
      fileName: attachedFile?.name || null,
    };

    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);

    const b64 = fileContent;
    const fname = attachedFile?.name;
    
    setAttachedFile(null);
    setFileContent(null);

    try {
      const response = await fetch('/api/shariah-advisor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          fileData: b64,
          fileName: fname,
          history: updatedMessages
        }),
      });

      if (!response.ok) throw new Error('Server responded with an error');

      const data = await response.json();
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'An error occurred. Please check your connection and try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="advisor-page">
      {/* Header */}
      <div className="advisor-header">
        <div>
          <h1 className="advisor-main-title">AI Shariah Advisor</h1>
          <p className="advisor-subtitle">Islamic Finance &amp; Zakat Guidance</p>
        </div>
        {/* Status indicator badge block completely removed from here */}
      </div>

      {/* Chat Window */}
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message-row ${msg.role === 'user' ? 'message-row--user' : 'message-row--assistant'}`}>
            {msg.role === 'assistant' && (
              <div className="avatar avatar--assistant">
                <FaRobot size={16} />
              </div>
            )}

            <div className={`bubble ${msg.role === 'user' ? 'bubble--user' : 'bubble--assistant'}`}>
              {msg.fileName && (
                <div className="bubble-file-tag">
                  <FaFileAlt size={12} />
                  <span>{msg.fileName}</span>
                </div>
              )}
              <span className="bubble-text">{msg.content}</span>
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row message-row--assistant">
            <div className="avatar avatar--assistant">
              <FaRobot size={16} />
            </div>
            <div className="bubble bubble--assistant bubble--typing">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Attached File Preview */}
      {attachedFile && (
        <div className="file-preview-bar">
          <FaFileAlt size={14} />
          <span className="file-preview-name">{attachedFile.name}</span>
          <button className="file-preview-remove" onClick={removeFile} aria-label="Remove file">
            <FaTimes size={12} />
          </button>
        </div>
      )}

      {/* Input Bar */}
      <div className="input-bar">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.png,.jpg,.jpeg,.webp"
          style={{ display: 'none' }}
        />

        <button
          className="input-btn input-btn--attach"
          onClick={() => fileInputRef.current?.click()}
          aria-label="Attach file"
          title="Attach PDF or image"
        >
          <FaPaperclip size={16} />
        </button>

        <textarea
          ref={textareaRef}
          className="input-textarea"
          placeholder="Ask about halal investing, zakat, Shariah compliance…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
        />

        <button
          className={`input-btn input-btn--send ${(input.trim() || attachedFile) && !loading ? 'input-btn--send-active' : ''}`}
          onClick={sendMessage}
          disabled={(!input.trim() && !attachedFile) || loading}
          aria-label="Send message"
        >
          <FaPaperPlane size={15} />
        </button>
      </div>

      <p className="input-hint">Press Enter to send · Shift+Enter for new line · PDF &amp; image uploads supported</p>
    </div>
  );
}