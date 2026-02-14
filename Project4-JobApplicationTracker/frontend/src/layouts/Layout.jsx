import React from 'react';
import Sidebar from '../components/Sidebar';

import { useNavigate } from 'react-router-dom';

const Layout = ({ children }) => {
    const navigate = useNavigate();
    return (
        <div className="main-layout">
            <Sidebar />
            <main className="content-area">
                <header className="top-bar">
                    <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Overview</h2>
                    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        <button className="btn btn-primary" onClick={() => navigate('/add-job')}>
                            + Add New Job
                        </button>
                    </div>
                </header>
                <div className="page-content">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
