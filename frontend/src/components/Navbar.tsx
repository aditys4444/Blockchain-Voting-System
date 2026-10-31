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
    <header className="sticky top-0 z-40 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 transition-colors w-full">
      
      {/* Top Network Sub-banner (Clean, responsive) */}
      <div className="bg-slate-100/90 dark:bg-slate-950/90 border-b border-slate-200/80 dark:border-slate-800/80 px-3 sm:px-6 py-1 text-[11px] font-mono text-slate-500 dark:text-slate-400">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 truncate">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shrink-0"></span>
            <span className="font-medium text-slate-700 dark:text-slate-300 truncate">
              PoW Testnet (1337)
            </span>
            <span className="hidden sm:inline text-slate-300 dark:text-slate-700">•</span>
            <span className="hidden sm:inline">Block #1,402</span>
          </div>

          <div className="flex items-center gap-2 sm:gap-3 shrink-0 text-[10px] sm:text-[11px]">
            <Link to="/explorer" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center gap-1">
              <Terminal className="w-3 h-3" />
              <span className="hidden xs:inline">Ledger</span>
            </Link>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <Link to="/observer" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center gap-1">
              <Activity className="w-3 h-3" />
              <span className="hidden xs:inline">Results</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Navbar Bar */}
      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16">
          
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2.5 sm:gap-3 group shrink-0">
            <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-slate-900 dark:bg-blue-600 flex items-center justify-center text-white shadow-sm shrink-0">
              <Shield className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-base sm:text-lg tracking-tight text-slate-900 dark:text-slate-100">
                  CivicVote
                </span>
                <span className="text-[9px] sm:text-[10px] uppercase font-mono font-semibold px-1 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                  Campus
                </span>
              </div>
              <p className="hidden sm:block text-[10px] text-slate-500 dark:text-slate-400 font-mono leading-none">
                VERIFIED BLOCKCHAIN VOTING
              </p>
            </div>
          </Link>

          {/* Right Actions */}
          <div className="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
            
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-1.5 sm:p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title="Toggle theme"
              aria-label="Toggle Theme"
            >
              {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
            </button>

            {user ? (
              <div className="flex items-center gap-2 pl-2 border-l border-slate-200 dark:border-slate-800">
                <div className="flex items-center gap-1.5">
                  <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 flex items-center justify-center font-bold text-xs shrink-0">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="hidden sm:block text-left max-w-[120px]">
                    <p className="text-xs font-semibold text-slate-900 dark:text-slate-100 truncate">
                      {user.username}
                    </p>
                    <span className="text-[9px] font-mono capitalize text-slate-500">
                      {user.role}
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleLogout}
                  className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/30 rounded-lg transition-colors"
                  title="Sign Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              location.pathname !== '/login' && (
                <Link
                  to="/login"
                  className="px-3 py-1.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors shrink-0"
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
