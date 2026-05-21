import React from 'react';
import '../shared.css';

// The "export default" right here is what Vite is looking for!
export default function Advisor() {
    return (
        <div className="app-container">
            <div className="page-header">
                <h1 className="page-title">AI Shariah Advisor</h1>
            </div>

            <div className="ui-card">
                <div className="alert-box-neutral">
                    <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>
                        Chat interface loading...
                    </p>
                </div>
            </div>
        </div>
    );
}