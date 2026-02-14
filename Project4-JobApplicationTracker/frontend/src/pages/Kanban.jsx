import React, { useState, useEffect } from 'react';
import api from '../api/axios';

const KanbanBoard = () => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const columns = ['To Apply', 'Applied', 'Interview', 'Offer', 'Rejected'];

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const response = await api.get('/applications/');
            // Map backend fields to frontend expected fields if needed, or use directly
            // Backend: job_title, company_name, status, id
            // Frontend previously used: title, company, status, id
            const mappedTasks = response.data.map(app => ({
                id: app.id,
                title: app.job_title,
                company: app.company_name,
                status: app.status || 'To Apply', // Default to 'To Apply' if null
                work_model: app.work_model
            }));
            setTasks(mappedTasks);
            setLoading(false);
        } catch (err) {
            console.error('Failed to fetch tasks:', err);
            setError('Failed to load applications.');
            setLoading(false);
        }
    };

    const getTasksByStatus = (status) => tasks.filter(task => task.status === status);

    const onDrop = async (e, status) => {
        e.preventDefault();
        const id = parseInt(e.dataTransfer.getData("taskId"));

        // Optimistic update
        const originalTasks = [...tasks];
        setTasks(tasks.map(task => {
            if (task.id === id) {
                return { ...task, status };
            }
            return task;
        }));

        try {
            // Find the task to get its current data, though we only update status here
            // We need to send the required fields or just the field we want to update if backend supports partial updates
            // The backend update_application expects ApplicationCreate schema which has all fields optional except title/company? 
            // no, ApplicationCreate has job_title and company_name as required.
            // Let's check backend/main.py again. create_application expects ApplicationCreate. update_application expects ApplicationCreate.

            // Wait, looking at main.py:
            // class ApplicationCreate(BaseModel):
            //     job_title: str
            //     company_name: str
            // ...

            // And update_application:
            // def update_application(application_id: int, application: ApplicationCreate...

            // This suggests I need to send job_title and company_name even if I only want to update status.
            // That's a bit annoying in the backend design, but I can work with it by finding the task first.

            const taskToUpdate = tasks.find(t => t.id === id);
            if (!taskToUpdate) return;

            // We need to construct the payload matching ApplicationCreate
            // efficiently, we should probably fetch the single application details to be safe, 
            // but since we have basic info likely sufficient for the required fields:
            const payload = {
                job_title: taskToUpdate.title,
                company_name: taskToUpdate.company,
                status: status,
                // include other fields if we had them in state, but essentially we just need to satisfy the required fields
            };

            // However, the backend update implementation:
            // for key, value in application.dict(exclude_unset=True).items():
            //    setattr(db_app, key, value)

            // If I send only status, pydantic might complain about missing required fields for ApplicationCreate if I don't provide them.
            // Let's try sending the required fields we know.

            await api.put(`/applications/${id}`, payload);

        } catch (err) {
            console.error('Failed to update task status:', err);
            // Revert on error
            setTasks(originalTasks);
            alert('Failed to update status. Please try again.');
        }
    };

    const onDragStart = (e, id) => {
        e.dataTransfer.setData("taskId", id);
    };

    if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading applications...</div>;
    if (error) return <div style={{ padding: '2rem', textAlign: 'center', color: 'red' }}>{error}</div>;

    return (
        <div style={{ height: 'calc(100vh - 100px)', paddingBottom: '2rem' }}>
            <h1 style={{ marginBottom: '2rem', fontSize: '2rem', fontWeight: 800 }}>Application Board</h1>

            <div className="kanban-board">
                {columns.map(status => (
                    <div
                        key={status}
                        className="kanban-column"
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => onDrop(e, status)}
                    >
                        <div className="column-header">
                            {status}
                            <span className="badge badge-medium">{getTasksByStatus(status).length}</span>
                        </div>
                        <div className="column-content">
                            {getTasksByStatus(status).map(task => (
                                <div
                                    key={task.id}
                                    className="kanban-card"
                                    draggable
                                    onDragStart={(e) => onDragStart(e, task.id)}
                                >
                                    <div style={{ fontWeight: 600 }}>{task.title}</div>
                                    <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{task.company}</div>
                                    <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.5rem' }}>
                                        {task.work_model && <span className="badge badge-low">{task.work_model}</span>}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default KanbanBoard;
