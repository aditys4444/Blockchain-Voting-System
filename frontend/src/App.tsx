import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { AdminDashboard } from './pages/AdminDashboard';
import { ElectionManagement } from './pages/ElectionManagement';
import { VoterDashboard } from './pages/VoterDashboard';
import { VoteReceipt } from './pages/VoteReceipt';
import { BlockchainExplorer } from './pages/BlockchainExplorer';
import { ObserverDashboard } from './pages/ObserverDashboard';
import { AIFraudDashboard } from './pages/AIFraudDashboard';

const RequireAuth: React.FC<{ children: React.ReactNode; allowedRoles?: string[] }> = ({ children, allowedRoles }) => {
  const { user, isAuthenticated } = useAuth();
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/explorer" replace />;
  }
  return <>{children}</>;
};

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className={`flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex gap-6 ${user ? 'pb-20 md:pb-6' : ''}`}>
        {user && <Sidebar />}
        <main className="flex-1 min-w-0">{children}</main>
      </div>
    </div>
  );
};

export function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <MainLayout>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/explorer" element={<BlockchainExplorer />} />
              <Route path="/observer" element={<ObserverDashboard />} />
              <Route path="/ai-fraud" element={<AIFraudDashboard />} />

              {/* Admin Routes */}
              <Route
                path="/admin"
                element={
                  <RequireAuth allowedRoles={['admin']}>
                    <AdminDashboard />
                  </RequireAuth>
                }
              />
              <Route
                path="/admin/elections"
                element={
                  <RequireAuth allowedRoles={['admin']}>
                    <ElectionManagement />
                  </RequireAuth>
                }
              />

              {/* Voter Routes */}
              <Route
                path="/voter"
                element={
                  <RequireAuth allowedRoles={['voter', 'admin']}>
                    <VoterDashboard />
                  </RequireAuth>
                }
              />
              <Route
                path="/voter/receipts"
                element={
                  <RequireAuth allowedRoles={['voter', 'admin']}>
                    <VoteReceipt />
                  </RequireAuth>
                }
              />

              {/* Default Redirect */}
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </MainLayout>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
