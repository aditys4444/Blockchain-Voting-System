import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  LayoutDashboard, 
  Vote, 
  Database, 
  ShieldAlert, 
  Eye, 
  CheckCircle2
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { user } = useAuth();
  if (!user) return null;

  const role = user.role;

  const adminLinks = [
    { to: '/admin', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/admin/elections', label: 'Elections & Studio', icon: Vote },
    { to: '/explorer', label: 'Explorer', icon: Database },
    { to: '/ai-fraud', label: 'Fraud Radar', icon: ShieldAlert },
    { to: '/observer', label: 'Observer Live', icon: Eye },
  ];

  const voterLinks = [
    { to: '/voter', label: 'Active Elections', icon: Vote },
    { to: '/voter/receipts', label: 'Vote Receipts', icon: CheckCircle2 },
    { to: '/explorer', label: 'Explorer', icon: Database },
  ];

  const observerLinks = [
    { to: '/observer', label: 'Live Desk', icon: Eye },
    { to: '/explorer', label: 'Ledger', icon: Database },
    { to: '/ai-fraud', label: 'Fraud Radar', icon: ShieldAlert },
  ];

  const links = role === 'admin' ? adminLinks : role === 'voter' ? voterLinks : observerLinks;

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="w-64 shrink-0 hidden md:block">
        <div className="sticky top-20 p-4 glass-card rounded-2xl border border-slate-200 dark:border-slate-800">
          <p className="px-3 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 font-mono">
            {role} Menu
          </p>

          <nav className="space-y-1">
            {links.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  end={link.to === '/admin' || link.to === '/voter' || link.to === '/observer'}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-md shadow-cyan-500/20'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>
      </aside>

      {/* Mobile Sticky Navigation Dock */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 p-2 bg-white/95 dark:bg-slate-900/95 backdrop-blur-lg border-t border-slate-200 dark:border-slate-800 shadow-2xl">
        <div className="flex items-center justify-around max-w-md mx-auto">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === '/admin' || link.to === '/voter' || link.to === '/observer'}
                className={({ isActive }) =>
                  `flex flex-col items-center justify-center p-1.5 rounded-xl text-[10px] font-semibold transition-all ${
                    isActive
                      ? 'text-cyan-500 font-bold'
                      : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  }`
                }
              >
                <Icon className="w-5 h-5 mb-0.5" />
                <span className="truncate max-w-[65px]">{link.label.split(' ')[0]}</span>
              </NavLink>
            );
          })}
        </div>
      </div>
    </>
  );
};
