import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import LegalTeam from './pages/LegalTeam';
import Upload from './pages/Upload';
import ClientWorkspace from './pages/ClientWorkspace';
import InviteClient from './pages/InviteClient';
import TemplatesPage from './pages/TemplatesPage';
import DocumentAnalysis from './pages/DocumentAnalysis';
import TemplateAnalysis from './pages/TemplateAnalysis';
import ClauseReview from './pages/ClauseReview';
import { apiFetch } from './utils/api';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const localToken = localStorage.getItem('token');
        const nifoToken = localStorage.getItem('jwtAccessToken');
        const candidateTokens = [
          ...(localToken ? [localToken] : []),
          ...(nifoToken && nifoToken !== localToken ? [nifoToken] : []),
        ];

        for (const candidate of candidateTokens) {
          const res = await apiFetch('/auth/me', {
            headers: {
              Authorization: `Bearer ${candidate}`,
            },
          });

          if (!res.ok) {
            continue;
          }

          const data = await res.json();
          localStorage.setItem('token', data.token || candidate);
          localStorage.setItem('user', JSON.stringify(data.user));
          setIsAuthenticated(true);
          setUser(data.user);
          return;
        }

        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setIsAuthenticated(false);
        setUser(null);
      } catch {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setAuthLoading(false);
      }
    };
    checkSession();
  }, []);

  const clearSession = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router basename="/legal-analyzer">
      <div className="app">
        <div className="bg-animation"></div>
        {authLoading ? (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <span style={{ color: '#a5b4fc', fontSize: '1rem' }}>Loading...</span>
          </div>
        ) : (
          <Routes>
            <Route
              path="/login"
              element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />}
            />
            <Route
              path="/dashboard"
              element={isAuthenticated ? <Dashboard user={user} onLogout={clearSession} /> : <Navigate to="/login" />}
            />
            <Route
              path="/workspace/:clientId"
              element={
                isAuthenticated && (user?.role === 'admin' || user?.role === 'legal_team')
                  ? <ClientWorkspace user={user} onLogout={clearSession} />
                  : <Navigate to="/login" />
              }
            />
            <Route
              path="/legal-team"
              element={
                isAuthenticated && (user?.role === 'admin' || user?.role === 'legal_team')
                  ? <LegalTeam user={user} onLogout={clearSession} />
                  : <Navigate to="/login" />
              }
            />
            <Route
              path="/upload"
              element={isAuthenticated ? <Upload user={user} onLogout={clearSession} /> : <Navigate to="/login" />}
            />
            <Route
              path="/invite-client"
              element={
                isAuthenticated && (user?.role === 'admin' || user?.role === 'legal_team')
                  ? <InviteClient user={user} onLogout={clearSession} />
                  : <Navigate to="/login" />
              }
            />
            <Route
              path="/templates"
              element={
                isAuthenticated && (user?.role === 'admin' || user?.role === 'legal_team')
                  ? <TemplatesPage user={user} onLogout={clearSession} />
                  : <Navigate to="/login" />
              }
            />
            <Route
              path="/analysis/:documentId"
              element={isAuthenticated ? <DocumentAnalysis user={user} onLogout={clearSession} /> : <Navigate to="/login" />}
            />
            <Route
              path="/template-analysis/:templateId"
              element={
                isAuthenticated && (user?.role === 'admin' || user?.role === 'legal_team')
                  ? <TemplateAnalysis user={user} onLogout={clearSession} />
                  : <Navigate to="/login" />
              }
            />
            <Route
              path="/review/:documentId"
              element={isAuthenticated ? <ClauseReview user={user} onLogout={clearSession} /> : <Navigate to="/login" />}
            />
            <Route path="/" element={<Navigate to="/login" />} />
          </Routes>
        )}
      </div>
    </Router>
  );
}

export default App;
