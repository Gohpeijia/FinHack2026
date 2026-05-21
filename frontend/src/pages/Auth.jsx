import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../shared.css';

export default function Auth() {
    const navigate = useNavigate();

    // State to hold the user's input
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        
        // Later, you will connect this to a real database (like Firebase or Supabase).
        // For now, clicking Login just securely routes them to the Dashboard!
        console.log("Authenticating user:", email);
        navigate('/'); 
    };

    return (
        <div className="app-container">
            {/* Centered Header for the Welcome Screen */}
            <div className="page-header" style={{ justifyContent: 'center', marginTop: '40px' }}>
                <h1 className="page-title" style={{ fontSize: '32px' }}>Welcome</h1>
            </div>

            <div className="ui-card">
                <form onSubmit={handleLogin}>
                    
                    <div className="form-group">
                        <label className="form-label">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email"
                            className="form-input"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            className="form-input"
                            required
                        />
                    </div>

                    <button type="submit" className="btn-primary" style={{ marginTop: '12px' }}>
                        Log In
                    </button>
                </form>

                {/* Divider Line */}
                <div style={{ 
                    textAlign: 'center', 
                    margin: '28px 0', 
                    color: '#64748b', 
                    fontSize: '14px',
                    position: 'relative'
                }}>
                    <span style={{ backgroundColor: '#ffffff', padding: '0 10px' }}>
                        or continue with
                    </span>
                </div>

                {/* Google Login Button Mockup */}
                <button
                    type="button"
                    style={{
                        width: '100%',
                        padding: '12px',
                        backgroundColor: '#ffffff',
                        border: '1px solid #e2e8f0',
                        borderRadius: '12px',
                        color: '#334155',
                        fontWeight: '600',
                        fontSize: '16px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '12px',
                        transition: 'background-color 0.2s'
                    }}
                    onMouseOver={(e) => e.target.style.backgroundColor = '#f8fafc'}
                    onMouseOut={(e) => e.target.style.backgroundColor = '#ffffff'}
                >
                    {/* A simple text-based placeholder for the Google 'G' icon */}
                    <span style={{ 
                        fontWeight: 'bold', 
                        fontSize: '20px', 
                        color: '#ea4335' 
                    }}>
                        G
                    </span> 
                    Google
                </button>

            </div>
        </div>
    );
}