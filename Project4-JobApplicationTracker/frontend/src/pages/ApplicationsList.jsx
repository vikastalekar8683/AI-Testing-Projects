import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const ApplicationsList = () => {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchApplications = async () => {
            try {
                const response = await api.get('/applications/');
                setApplications(response.data);
                setLoading(false);
            } catch (err) {
                console.error("Error fetching applications:", err);
                setError("Failed to load applications");
                setLoading(false);
            }
        };

        fetchApplications();
    }, []);

    const handleDelete = async (id) => {
        if (window.confirm("Are you sure you want to delete this application?")) {
            try {
                await api.delete(`/applications/${id}`);
                setApplications(applications.filter(app => app.id !== id));
            } catch (err) {
                console.error("Error deleting application:", err);
                alert("Failed to delete application");
            }
        }
    };

    if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading applications...</div>;
    if (error) return <div style={{ padding: '2rem', textAlign: 'center', color: 'red' }}>{error}</div>;

    const getStatusBadgeClass = (status) => {
        switch (status) {
            case 'Offer': return 'badge badge-success';
            case 'Rejected': return 'badge badge-danger';
            case 'Interview': return 'badge badge-warning';
            default: return 'badge badge-medium';
        }
    };

    return (
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '2rem', fontWeight: 800 }}>Applications List</h1>
                <button
                    onClick={() => navigate('/add-job')}
                    className="btn btn-primary"
                >
                    + Add New Job
                </button>
            </div>

            <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead style={{ backgroundColor: 'var(--background-color)', borderBottom: '1px solid var(--border-color)' }}>
                            <tr>
                                <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Job Title</th>
                                <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Company</th>
                                <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Status</th>
                                <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Date Applied</th>
                                <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Work Model</th>
                                <th style={{ padding: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {applications.length > 0 ? (
                                applications.map((app) => (
                                    <tr key={app.id} style={{ borderBottom: '1px solid var(--border-color)', transition: 'background-color 0.1s' }} className="table-row">
                                        <td style={{ padding: '1rem', fontWeight: 500 }}>{app.job_title}</td>
                                        <td style={{ padding: '1rem' }}>{app.company_name}</td>
                                        <td style={{ padding: '1rem' }}>
                                            <span className={getStatusBadgeClass(app.status)} style={{ padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.875rem' }}>
                                                {app.status}
                                            </span>
                                        </td>
                                        <td style={{ padding: '1rem', color: 'var(--text-secondary)' }}>{new Date(app.created_at).toLocaleDateString()}</td>
                                        <td style={{ padding: '1rem' }}>{app.work_model || '-'}</td>
                                        <td style={{ padding: '1rem' }}>
                                            <button
                                                onClick={() => handleDelete(app.id)}
                                                style={{ color: 'var(--danger-color)', fontWeight: 500, cursor: 'pointer' }}
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="6" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                                        No applications found. Start by adding a new job!
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default ApplicationsList;
