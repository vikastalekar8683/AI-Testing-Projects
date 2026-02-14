import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './layouts/Layout';
import Dashboard from './pages/Dashboard';
import Kanban from './pages/Kanban';
import AddJob from './pages/AddJob';

import ApplicationsList from './pages/ApplicationsList';
import Analytics from './pages/Analytics';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/board" element={<Kanban />} />
          <Route path="/add-job" element={<AddJob />} />
          <Route path="/applications" element={<ApplicationsList />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
