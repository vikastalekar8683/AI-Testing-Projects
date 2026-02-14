import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                🚀 JobTracker
            </div>
            <nav style={{ flex: 1 }}>
                <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    📊 Dashboard
                </NavLink>
                <NavLink to="/board" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    📋 Kanban Board
                </NavLink>
                <NavLink to="/applications" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    📝 Applications
                </NavLink>
                <NavLink to="/analytics" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    📈 Analytics
                </NavLink>
            </nav>
            <div style={{ marginTop: 'auto' }}>
                <NavLink to="/settings" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    ⚙️ Settings
                </NavLink>
            </div>
        </aside>
    );
};

export default Sidebar;
