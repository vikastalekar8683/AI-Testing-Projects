import React, { useEffect, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import api from '../api/axios';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement
);

const Analytics = () => {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.get('/applications/');
                setApplications(response.data);
                setLoading(false);
            } catch (err) {
                console.error("Error fetching analytics data:", err);
                setError("Failed to load analytics data");
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading analytics...</div>;
    if (error) return <div style={{ padding: '2rem', textAlign: 'center', color: 'red' }}>{error}</div>;

    // Process data for charts

    // 1. Status Distribution
    const statusCounts = applications.reduce((acc, app) => {
        acc[app.status] = (acc[app.status] || 0) + 1;
        return acc;
    }, {});

    const statusData = {
        labels: Object.keys(statusCounts),
        datasets: [
            {
                label: '# of Applications',
                data: Object.values(statusCounts),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    // 2. Applications Over Time (Grouping by Month-Year)
    const jobsByDate = applications.reduce((acc, app) => {
        const date = new Date(app.created_at);
        const monthYear = date.toLocaleString('default', { month: 'short', year: 'numeric' });
        acc[monthYear] = (acc[monthYear] || 0) + 1;
        return acc;
    }, {});

    // Sort properly (can be expanded, for now assuming basic chronological order if keys are inserted in order or we sort manually)
    // For simplicity using keys directly
    const timelineData = {
        labels: Object.keys(jobsByDate),
        datasets: [
            {
                label: 'Applications per Month',
                data: Object.values(jobsByDate),
                borderColor: 'rgb(99, 102, 241)',
                backgroundColor: 'rgba(99, 102, 241, 0.5)',
                tension: 0.3
            }
        ]
    };

    // 3. Work Model Distribution
    const workModelCounts = applications.reduce((acc, app) => {
        const model = app.work_model || 'Unspecified';
        acc[model] = (acc[model] || 0) + 1;
        return acc;
    }, {});

    const workModelData = {
        labels: Object.keys(workModelCounts),
        datasets: [
            {
                label: 'Work Model',
                data: Object.values(workModelCounts),
                backgroundColor: ['#6366f1', '#ec4899', '#10b981', '#f59e0b'],
            }
        ]

    };

    return (
        <div style={{ maxWidth: '1200px', margin: '0 auto', paddingBottom: '2rem' }}>
            <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '2rem' }}>Analytics Dashboard</h1>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '2rem' }}>

                {/* Status Chart */}
                <div className="card" style={{ padding: '1.5rem' }}>
                    <h3 style={{ marginBottom: '1rem', fontWeight: 600 }}>Application Status</h3>
                    <div style={{ height: '300px', display: 'flex', justifyContent: 'center' }}>
                        <Doughnut data={statusData} options={{ responsive: true, maintainAspectRatio: false }} />
                    </div>
                </div>

                {/* Timeline Chart */}
                <div className="card" style={{ padding: '1.5rem' }}>
                    <h3 style={{ marginBottom: '1rem', fontWeight: 600 }}>Application Timeline</h3>
                    <div style={{ height: '300px' }}>
                        <Line data={timelineData} options={{ responsive: true, maintainAspectRatio: false }} />
                    </div>
                </div>

                {/* Work Model Chart */}
                <div className="card" style={{ padding: '1.5rem' }}>
                    <h3 style={{ marginBottom: '1rem', fontWeight: 600 }}>Work Model Preference</h3>
                    <div style={{ height: '300px' }}>
                        <Bar data={workModelData} options={{ responsive: true, maintainAspectRatio: false }} />
                    </div>
                </div>
            </div>

            <div className="card" style={{ marginTop: '2rem', padding: '1.5rem' }}>
                <h3 style={{ marginBottom: '1rem', fontWeight: 600 }}>Quick Insights</h3>
                <ul style={{ listStyleType: 'disc', paddingLeft: '1.5rem', lineHeight: '1.8' }}>
                    <li>Total Applications: <strong>{applications.length}</strong></li>
                    <li>Most Common Status: <strong>{Object.keys(statusCounts).sort((a, b) => statusCounts[b] - statusCounts[a])[0] || 'N/A'}</strong></li>
                    <li>Conversion Rate (Interview/Total): <strong>{applications.length > 0 ? Math.round(((statusCounts['Interview'] || 0) / applications.length) * 100) : 0}%</strong></li>
                </ul>
            </div>

        </div>
    );
};

export default Analytics;
