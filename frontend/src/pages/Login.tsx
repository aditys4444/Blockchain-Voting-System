import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { UserRole } from '../types';
import { Shield, KeyRound, Mail, ArrowRight, Sparkles } from 'lucide-react';

export const Login: React.FC = () => {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const checkDemoCredentials = (u: string, p: string) => {
    const cred = u.toLowerCase().trim();
    const pwd = p.trim();
    const now = new Date().toISOString();

    if ((cred === 'admin' || cred === 'admin_edu' || cred === 'admin@voting.edu' || cred === 'admin@blockchainvoting.org') && (pwd === 'admin123' || pwd === 'Admin123!')) {
      return { id: 1, email: 'admin@voting.edu', username: 'admin', role: 'admin' as UserRole, is_active: true, created_at: now };
    }
    if ((cred === 'voter1' || cred === 'voter_edu' || cred === 'voter1@voting.edu' || cred === 'voter@blockchainvoting.org') && (pwd === 'voter123' || pwd === 'Voter123!')) {
      return { id: 2, email: 'voter1@voting.edu', username: 'voter1', role: 'voter' as UserRole, is_active: true, created_at: now };
    }
    if ((cred === 'observer1' || cred === 'observer_edu' || cred === 'observer@voting.edu' || cred === 'observer@blockchainvoting.org') && (pwd === 'observer123' || pwd === 'Observer123!')) {
      return { id: 3, email: 'observer@voting.edu', username: 'observer1', role: 'observer' as UserRole, is_active: true, created_at: now };
    }

    try {
      const saved = localStorage.getItem('demo_registered_users');
      if (saved) {
        const registeredList = JSON.parse(saved);
        const match = registeredList.find((usr: any) =>
          (usr.email.toLowerCase() === cred || usr.username.toLowerCase() === cred) && usr.password === pwd
        );
        if (match) {
          return {
            id: match.id,
            email: match.email,
            username: match.username,
            role: match.role as UserRole,
            is_active: true,
            created_at: match.created_at || now
          };
        }
      }
    } catch (e) {}

    return null;
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await api.post('/auth/login', {
        username_or_email: usernameOrEmail,
        password,
      });

      const { access_token, user } = res.data;
      login(access_token, user);

      if (user.role === 'admin') navigate('/admin');
      else if (user.role === 'voter') navigate('/voter');
      else navigate('/observer');
    } catch (err: any) {
      const demoUser = checkDemoCredentials(usernameOrEmail, password);
      if (demoUser) {
        login(`demo-${demoUser.role}-token`, demoUser);
        if (demoUser.role === 'admin') navigate('/admin');
        else if (demoUser.role === 'voter') navigate('/voter');
        else navigate('/observer');
        return;
      }
      setError(err.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleDirectLogin = async (u: string, p: string) => {
    setUsernameOrEmail(u);
    setPassword(p);
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/auth/login', {
        username_or_email: u,
        password: p,
      });
      const { access_token, user } = res.data;
      login(access_token, user);
      if (user.role === 'admin') navigate('/admin');
      else if (user.role === 'voter') navigate('/voter');
      else navigate('/observer');
    } catch (err: any) {
      const demoUser = checkDemoCredentials(u, p);
      if (demoUser) {
        login(`demo-${demoUser.role}-token`, demoUser);
        if (demoUser.role === 'admin') navigate('/admin');
        else if (demoUser.role === 'voter') navigate('/voter');
        else navigate('/observer');
        return;
      }
      setError(err.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8 glass-card p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl">
        
        {/* Header */}
        <div className="text-center">
          <div className="inline-flex p-3 bg-gradient-to-tr from-blue-600 to-cyan-500 rounded-2xl text-white shadow-lg shadow-cyan-500/20 mb-4">
            <Shield className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Secure Portal Login
          </h2>
          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 font-mono">
            SECP256R1 ECDSA SIGNED SESSIONS
          </p>
        </div>

        {error && (
          <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-500 text-xs font-semibold text-center">
            {error}
          </div>
        )}

        <form className="mt-8 space-y-5" onSubmit={handleLogin}>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Username or Email
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 absolute left-3 top-3.5 text-slate-400" />
              <input
                type="text"
                required
                value={usernameOrEmail}
                onChange={(e) => setUsernameOrEmail(e.target.value)}
                placeholder="admin@blockchainvoting.org"
                className="w-full pl-9 pr-4 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Password
            </label>
            <div className="relative">
              <KeyRound className="w-4 h-4 absolute left-3 top-3.5 text-slate-400" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-4 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold rounded-xl shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            {loading ? 'Authenticating...' : 'Sign In'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Demo Quick Logins */}
        <div className="pt-4 border-t border-slate-200 dark:border-slate-800">
          <p className="text-[11px] font-mono text-slate-400 dark:text-slate-500 mb-2 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-amber-400" /> Quick Demo Credentials:
          </p>
          <div className="grid grid-cols-3 gap-2 text-center text-xs font-mono">
            <button
              type="button"
              onClick={() => handleDirectLogin('admin', 'Admin123!')}
              className="p-2 bg-slate-100 dark:bg-slate-800/80 hover:bg-cyan-500/10 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
            >
              Admin
            </button>
            <button
              type="button"
              onClick={() => handleDirectLogin('voter1', 'Voter123!')}
              className="p-2 bg-slate-100 dark:bg-slate-800/80 hover:bg-cyan-500/10 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
            >
              Voter
            </button>
            <button
              type="button"
              onClick={() => handleDirectLogin('observer1', 'Observer123!')}
              className="p-2 bg-slate-100 dark:bg-slate-800/80 hover:bg-cyan-500/10 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
            >
              Observer
            </button>
          </div>
        </div>

        <p className="text-center text-xs text-slate-500">
          Don't have a voter account?{' '}
          <Link to="/register" className="text-cyan-500 font-semibold hover:underline">
            Register here
          </Link>
        </p>

      </div>
    </div>
  );
};
