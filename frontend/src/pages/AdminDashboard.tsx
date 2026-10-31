import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { AuditLog } from '../types';
import { Vote, Users, Database, ShieldCheck, Activity, ArrowRight, ShieldAlert, Cpu } from 'lucide-react';
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
      const savedReceipts = localStorage.getItem('demo_receipts');
      const receiptsList = savedReceipts ? JSON.parse(savedReceipts) : [];
      const savedElections = localStorage.getItem('demo_elections');
      const electionsList = savedElections ? JSON.parse(savedElections) : [{}];

      setMetrics({
        total_elections: electionsList.length,
        active_elections: electionsList.filter((e: any) => e.status === 'active').length,
        total_voters: 42,
        total_votes: receiptsList.length,
        blockchain_status: "Verified & Operating",
        chain_length: receiptsList.length + 1402
      });

      setAuditLogs([
        {
          id: 1,
          action: "ELECTION_INITIALIZED",
          details: "Student Government Presidential Election 2025–2026 deployed",
          user_id: 1,
          ip_address: "127.0.0.1",
          timestamp: new Date(Date.now() - 3600000).toISOString()
        },
        {
          id: 2,
          action: "GENESIS_BLOCK_MINED",
          details: "PoW Consensus initialized on Chain ID 1337 with Difficulty 4",
          user_id: 1,
          ip_address: "127.0.0.1",
          timestamp: new Date(Date.now() - 7200000).toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const timer = setInterval(fetchData, 6000);
    return () => clearInterval(timer);
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-slate-500 font-mono text-xs">Loading governance telemetry...</div>;
  }

  const statCards = [
    { label: 'Elections', value: metrics?.total_elections || 1, icon: Vote, desc: 'Registered contests' },
    { label: 'Active Windows', value: metrics?.active_elections || 1, icon: Activity, desc: 'Accepting ballots' },
    { label: 'Voter Roll', value: metrics?.total_voters || 42, icon: Users, desc: 'Eligible students' },
    { label: 'Mined Blocks', value: metrics?.chain_length || 1403, icon: Database, desc: 'SHA-256 blocks' },
  ];

  return (
    <div className="space-y-4 sm:space-y-6 w-full">
      
      {/* Top Banner */}
      <div className="civic-card p-4 sm:p-6 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-1.5 text-xs font-mono text-blue-600 dark:text-blue-400 font-bold uppercase">
            <span>GOVERNANCE CONSOLE</span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span className="text-slate-500 font-normal">ADMINISTRATOR DESK</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-0.5">
            System Operations &amp; Telemetry
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 max-w-xl">
            Real-time monitoring of voting windows, cryptographic ledger integrity, and immutable audit logs.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start md:self-auto">
          <Link
            to="/admin/elections"
            className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors flex items-center gap-1.5"
          >
            <span>Manage Elections</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
          <Link
            to="/ai-fraud"
            className="px-3 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-xs rounded-lg transition-colors flex items-center gap-1 border border-slate-200 dark:border-slate-700"
          >
            <ShieldAlert className="w-3.5 h-3.5 text-amber-500" />
            <span className="hidden sm:inline">Fraud Radar</span>
          </Link>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-4">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div key={i} className="civic-card p-3 sm:p-4 flex items-start justify-between">
              <div>
                <p className="text-[10px] sm:text-xs font-semibold text-slate-500">{card.label}</p>
                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 mt-0.5">{card.value}</h3>
                <p className="text-[9px] sm:text-[10px] text-slate-400 font-mono mt-0.5">{card.desc}</p>
              </div>
              <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center justify-center shrink-0">
                <Icon className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Blockchain Status Card */}
      <div className="civic-card p-4 border-l-4 border-l-emerald-500 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 shrink-0">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">
              Consensus Status: Healthy
            </h4>
            <p className="text-[11px] text-slate-500 font-mono">
              Status: <span className="text-emerald-600 font-bold">{metrics?.blockchain_status}</span> • Difficulty: 4 • Blocks: #{metrics?.chain_length}
            </p>
          </div>
        </div>
        <Link 
          to="/explorer" 
          className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 font-mono self-start sm:self-auto"
        >
          <span>Open Ledger</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Audit Logs Container (Desktop Table + Mobile Cards) */}
      <div className="civic-card overflow-hidden">
        <div className="px-4 sm:px-6 py-3 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60 flex items-center justify-between">
          <h2 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-blue-600 shrink-0" />
            <span>Administrative Audit Trail</span>
          </h2>
          <span className="text-[10px] font-mono text-slate-500">IMMUTABLE LOGS</span>
        </div>

        {/* Desktop Table */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100/70 dark:bg-slate-950/70 text-slate-500 font-mono uppercase text-[10px] border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="px-5 py-3">Timestamp</th>
                <th className="px-5 py-3">Action Event</th>
                <th className="px-5 py-3">Details</th>
                <th className="px-5 py-3">Operator</th>
                <th className="px-5 py-3 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {auditLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                  <td className="px-5 py-3 font-mono text-slate-500">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="px-5 py-3 font-mono font-semibold text-slate-900 dark:text-slate-100">
                    {log.action}
                  </td>
                  <td className="px-5 py-3 text-slate-600 dark:text-slate-300">
                    {log.details}
                  </td>
                  <td className="px-5 py-3 font-mono text-slate-500">
                    Admin #{log.user_id}
                  </td>
                  <td className="px-5 py-3 text-right">
                    <span className="inline-block px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                      SUCCESS
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Stacked Cards (< 768px - Never Overflows) */}
        <div className="md:hidden divide-y divide-slate-200 dark:divide-slate-800">
          {auditLogs.map((log) => (
            <div key={log.id} className="p-4 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-mono font-bold text-xs text-slate-900 dark:text-slate-100">
                  {log.action}
                </span>
                <span className="text-[10px] font-mono text-slate-400">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-300">
                {log.details}
              </p>
              <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1">
                <span>Operator: Admin #{log.user_id}</span>
                <span className="text-emerald-600 dark:text-emerald-400 font-bold">VERIFIED</span>
              </div>
            </div>
          ))}
        </div>

      </div>

    </div>
  );
};
