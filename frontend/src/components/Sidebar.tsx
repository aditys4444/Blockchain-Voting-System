import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  LayoutDashboard, 
  Vote, 
  Database, 
  ShieldAlert, 
  Eye, 
  FileCheck2
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { user } = useAuth();
  if (!user) return null;

  const role = user.role;

  const adminLinks = [
    { to: '/admin', label: 'Command Center', icon: LayoutDashboard },
    { to: '/admin/elections', label: 'Elections & Candidates', icon: Vote },
    { to: '/explorer', label: 'Blockchain Ledger', icon: Database },
    { to: '/observer', label: 'Observer Tallies', icon: Eye },
    { to: '/ai-fraud', label: 'Audit & Fraud Radar', icon: ShieldAlert },
  ];

  const voterLinks = [
    { to: '/voter', label: 'Active Elections', icon: Vote },
    { to: '/voter/receipts', label: 'My Vote Receipts', icon: FileCheck2 },
    { to: '/explorer', label: 'Blockchain Ledger', icon: Database },
    { to: '/observer', label: 'Election Results', icon: Eye },
  ];

  const observerLinks = [
    { to: '/observer', label: 'Certified Results', icon: Eye },
    { to: '/explorer', label: 'Blockchain Ledger', icon: Database },
    { to: '/ai-fraud', label: 'Audit Radar', icon: ShieldAlert },
  ];

  const links = role === 'admin' ? adminLinks : role === 'voter' ? voterLinks : observerLinks;

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="w-60 shrink-0 hidden md:block">
        <div className="sticky top-28 p-3 civic-card">
          <p className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 font-mono">
            {role} Navigation
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
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 font-semibold border-l-2 border-blue-600'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{link.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>
      </aside>

      {/* Mobile Sticky Bottom Navigation Dock */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 p-2 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 shadow-lg">
        <div className="flex items-center justify-around max-w-md mx-auto">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === '/admin' || link.to === '/voter' || link.to === '/observer'}
                className={({ isActive }) =>
                  `flex flex-col items-center justify-center p-2 rounded-lg text-[11px] font-medium transition-colors ${
                    isActive
                      ? 'text-blue-600 dark:text-blue-400 font-bold'
                      : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  }`
                }
              >
                <Icon className="w-4 h-4 mb-0.5" />
                <span className="truncate max-w-[70px]">{link.label.split(' ')[0]}</span>
              </NavLink>
            );
          })}
        </div>
      </div>
    </>
  );
};
