import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Shield, Sun, Moon, LogOut, User as UserIcon } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { darkMode, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="sticky top-0 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="p-2 bg-gradient-to-tr from-cyan-500 to-blue-600 rounded-xl text-white shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-slate-900 via-blue-900 to-cyan-600 dark:from-white dark:via-blue-200 dark:to-cyan-400 bg-clip-text text-transparent">
                BLOCKCHAIN<span className="font-mono text-cyan-500 text-sm ml-1">VOTE</span>
              </span>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 font-mono leading-none">SECP256R1 • SHA-256 LEDGER</p>
            </div>
          </Link>

          {/* Right Actions */}
          <div className="flex items-center gap-3">
            
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title="Toggle Theme"
            >
              {darkMode ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-slate-600" />}
            </button>

            {user ? (
              <div className="flex items-center gap-3 pl-3 border-l border-slate-200 dark:border-slate-800">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-cyan-500/10 text-cyan-500 dark:bg-cyan-400/20 dark:text-cyan-400 flex items-center justify-center font-bold text-sm">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="hidden sm:block text-left">
                    <p className="text-xs font-semibold text-slate-800 dark:text-slate-200 leading-tight">{user.username}</p>
                    <span className="inline-block text-[10px] font-mono capitalize px-1.5 py-0.5 rounded bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-800">
                      {user.role}
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleLogout}
                  className="p-2 rounded-xl text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-colors"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 rounded-xl shadow-lg shadow-cyan-500/20 transition-all"
              >
                Sign In
              </Link>
            )}

          </div>

        </div>
      </div>
    </nav>
  );
};
