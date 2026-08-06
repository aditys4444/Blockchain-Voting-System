import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { AuditLog } from '../types';
import { Vote, Users, Database, ShieldCheck, Activity, ArrowUpRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const AdminDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [mRes, aRes] = await Promise.all([
        api.get('/admin/metrics'),
        api.get('/admin/audit-logs')
      ]);
      setMetrics(mRes.data);
      setAuditLogs(aRes.data);
    } catch (err) {
      console.error('Failed to load admin metrics', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const timer = setInterval(fetchData, 5000);
    return () => clearInterval(timer);
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Loading admin metrics...</div>;
  }

  const statCards = [
    { label: 'Total Elections', value: metrics?.total_elections || 0, icon: Vote, color: 'from-blue-600 to-indigo-600' },
    { label: 'Active Elections', value: metrics?.active_elections || 0, icon: Activity, color: 'from-emerald-500 to-teal-600' },
    { label: 'Registered Voters', value: metrics?.total_voters || 0, icon: Users, color: 'from-cyan-500 to-blue-600' },
    { label: 'Blockchain Votes', value: metrics?.total_votes || 0, icon: ShieldCheck, color: 'from-violet-600 to-purple-600' },
  ];

  return (
    <div className="space-y-8">
      
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <div>
          <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">ADMIN CONTROL DESK</span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">System Command & Overview</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Real-time monitoring of custom SHA-256 cryptographic chain & election status</p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/admin/elections"
            className="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold rounded-xl text-xs flex items-center gap-1.5 shadow-lg shadow-cyan-500/20 transition-all"
          >
            Manage Elections <ArrowUpRight className="w-4 h-4" />
          </Link>
          <Link
            to="/ai-fraud"
            className="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-semibold rounded-xl text-xs flex items-center gap-1.5 transition-colors"
          >
            AI Fraud Radar
          </Link>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div key={i} className="p-5 glass-card rounded-2xl border border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-slate-500 dark:text-slate-400">{card.label}</p>
                <h3 className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">{card.value}</h3>
              </div>
              <div className={`p-3 rounded-2xl bg-gradient-to-tr ${card.color} text-white shadow-md`}>
                <Icon className="w-5 h-5" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Blockchain Status Banner */}
      <div className="p-5 glass-card rounded-2xl border border-emerald-500/30 bg-emerald-500/5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Database className="w-6 h-6 text-emerald-500" />
          <div>
            <h4 className="text-sm font-bold text-slate-900 dark:text-white">Blockchain Ledger Health</h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">
              Status: <span className="text-emerald-500 font-bold">{metrics?.blockchain_status}</span> • Total Mined Blocks: #{metrics?.chain_length}
            </p>
          </div>
        </div>
        <Link to="/explorer" className="text-xs font-semibold text-cyan-500 hover:underline">
          Open Ledger Explorer &rarr;
        </Link>
      </div>

      {/* Audit Logs */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 className="text-lg font-bold text-slate-900 dark:text-white">Immutable Audit Trail</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-slate-400 dark:text-slate-500 uppercase font-mono border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="pb-3 px-2">ID</th>
                <th className="pb-3 px-2">Action</th>
                <th className="pb-3 px-2">User Email</th>
                <th className="pb-3 px-2">Details</th>
                <th className="pb-3 px-2">IP Address</th>
                <th className="pb-3 px-2">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-mono text-slate-700 dark:text-slate-300">
              {auditLogs.slice(0, 10).map((log) => (
                <tr key={log.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                  <td className="py-2.5 px-2 font-bold text-cyan-500">#{log.id}</td>
                  <td className="py-2.5 px-2 font-semibold">{log.action}</td>
                  <td className="py-2.5 px-2 text-slate-500">{log.user_email || 'System'}</td>
                  <td className="py-2.5 px-2 truncate max-w-xs">{log.details}</td>
                  <td className="py-2.5 px-2 text-slate-400">{log.ip_address}</td>
                  <td className="py-2.5 px-2 text-slate-400">{new Date(log.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
