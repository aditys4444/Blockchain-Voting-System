import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Shield, Sun, Moon, LogOut, Terminal, Activity } from 'lucide-react';
import { useNavigate, Link, useLocation } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { darkMode, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 transition-colors">
      
      {/* Top Network Sub-banner (Institutional context) */}
      <div className="bg-slate-100/80 dark:bg-slate-950/80 border-b border-slate-200/80 dark:border-slate-800/80 px-4 sm:px-6 lg:px-8 py-1 text-[11px] font-mono text-slate-500 dark:text-slate-400">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 font-medium text-slate-700 dark:text-slate-300">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>PoW Testnet (Chain ID: 1337)</span>
            </span>
            <span className="text-slate-300 dark:text-slate-700">|</span>
            <span>Block #1,402</span>
            <span className="text-slate-300 dark:text-slate-700">|</span>
            <span>Avg Block Time: 12s</span>
          </div>

          <div className="hidden sm:flex items-center gap-3">
            <Link to="/explorer" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center gap-1">
              <Terminal className="w-3 h-3" />
              <span>Audit Ledger</span>
            </Link>
            <span className="text-slate-300 dark:text-slate-700">|</span>
            <Link to="/observer" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center gap-1">
              <Activity className="w-3 h-3" />
              <span>Certified Tallies</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Navbar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-lg bg-slate-900 dark:bg-blue-600 flex items-center justify-center text-white shadow-sm transition-transform">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg tracking-tight text-slate-900 dark:text-slate-100">
                  CivicVote
                </span>
                <span className="text-[10px] uppercase font-mono font-semibold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                  College Demo
                </span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 font-mono leading-none">
                ECDSA SECP256R1 • SHA-256 LEDGER
              </p>
            </div>
          </Link>

          {/* Right Actions */}
          <div className="flex items-center gap-3">
            
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors border border-transparent hover:border-slate-200 dark:hover:border-slate-700"
              title="Toggle Light/Dark Theme"
              aria-label="Toggle Theme"
            >
              {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
            </button>

            {user ? (
              <div className="flex items-center gap-3 pl-3 border-l border-slate-200 dark:border-slate-800">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 flex items-center justify-center font-bold text-xs">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="hidden sm:block text-left">
                    <p className="text-xs font-semibold text-slate-900 dark:text-slate-100 leading-tight">
                      {user.username}
                    </p>
                    <span className="inline-block text-[10px] font-mono capitalize px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                      {user.role}
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleLogout}
                  className="p-2 rounded-lg text-slate-500 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-colors"
                  title="Sign Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              location.pathname !== '/login' && (
                <Link
                  to="/login"
                  className="px-4 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm transition-colors"
                >
                  Sign In
                </Link>
              )
            )}

          </div>

        </div>
      </div>
    </header>
  );
};
