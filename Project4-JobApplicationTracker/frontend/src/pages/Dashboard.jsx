import React, { useEffect, useState } from 'react';
import api from '../api/axios';

const Dashboard = () => {
    const [stats, setStats] = useState({
        total: 0,
        interviews: 0,
        offers: 0,
        responseRate: 0,
    });
    const [recentActivity, setRecentActivity] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.get('/applications/');
                const applications = response.data;

                // Calculate stats
                const total = applications.length;
                const interviews = applications.filter(app => app.status === 'Interview').length;
                const offers = applications.filter(app => app.status === 'Offer').length;
                const responded = applications.filter(app => ['Interview', 'Offer', 'Rejected'].includes(app.status)).length;
                const responseRate = total > 0 ? Math.round((responded / total) * 100) : 0;

                setStats({
                    total,
                    interviews,
                    offers,
                    responseRate
                });

                // Get recent activity (last 5 applications, sorted by ID descending as proxy for date if created_at not strictly ordered or just use reverse)
                // Assuming higher ID means newer
                const sortedApps = [...applications].sort((a, b) => b.id - a.id).slice(0, 5);
                setRecentActivity(sortedApps);

            } catch (error) {
                console.error("Error fetching dashboard data:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return <div style={{ padding: '2rem' }}>Loading dashboard...</div>;
    }

    return (
        <div className="dashboard-container">
            <h1 style={{ marginBottom: '2rem', fontSize: '2rem', fontWeight: 800, color: 'var(--text-primary)' }}>Welcome Back! 👋</h1>

            <div className="grid-cols-4" style={{ marginBottom: '2rem' }}>
                <div className="card stat-card">
                    <span className="stat-value">{stats.total}</span>
                    <span className="stat-label">Total Applications</span>
                </div>
                <div className="card stat-card">
                    <span className="stat-value">{stats.interviews}</span>
                    <span className="stat-label">Interviews Scheduled</span>
                </div>
                <div className="card stat-card">
                    <span className="stat-value">{stats.offers}</span>
                    <span className="stat-label">Offers Received</span>
                </div>
                <div className="card stat-card">
                    <span className="stat-value">{stats.responseRate}%</span>
                    <span className="stat-label">Response Rate</span>
                </div>
            </div>

            <div className="card" style={{ minHeight: '400px' }}>
                <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: 600 }}>Recent Activity</h3>
                {recentActivity.length > 0 ? (
                    <div className="recent-activity-list">
                        {recentActivity.map(app => (
                            <div key={app.id} style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: '1rem',
                                borderBottom: '1px solid var(--border-color)',
                                transition: 'background-color 0.2s'
                            }}>
                                <div>
                                    <div style={{ fontWeight: 600, fontSize: '1.1rem' }}>{app.job_title}</div>
                                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{app.company_name} • {app.status}</div>
                                </div>
                                <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                    {new Date(app.created_at).toLocaleDateString()}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p style={{ color: 'var(--text-secondary)' }}>No recent activity to show yet. Start applying!</p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
