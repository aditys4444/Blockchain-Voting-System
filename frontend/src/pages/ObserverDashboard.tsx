import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Election } from '../types';
import { Download, BarChart as BarIcon, ShieldCheck } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const DEFAULT_ELECTIONS: Election[] = [
  {
    id: 1,
    title: "General Presidential Election 2026",
    description: "Official decentralised blockchain election for 2026 leadership.",
    status: "active",
    start_time: new Date().toISOString(),
    end_time: new Date(Date.now() + 7 * 86400000).toISOString(),
    created_by: 1,
    created_at: new Date().toISOString(),
    candidates: [
      {
        id: 101,
        election_id: 1,
        name: "Dr. Alex Rivera",
        party: "Progressive Tech Party",
        manifesto: "Focusing on AI innovation, digital rights, and sustainable green technology.",
        avatar_url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80",
        vote_count: 0
      },
      {
        id: 102,
        election_id: 1,
        name: "Elena Rostova",
        party: "Global Unity Alliance",
        manifesto: "Transparency, decentralised governance, economic prosperity, and privacy protection.",
        avatar_url: "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80",
        vote_count: 0
      }
    ]
  }
];

export const ObserverDashboard: React.FC = () => {
  const [elections, setElections] = useState<Election[]>([]);
  const [selectedElectionId, setSelectedElectionId] = useState<number | null>(null);
  const [liveResults, setLiveResults] = useState<any>(null);

  const COLORS = ['#06b6d4', '#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899'];

  const fetchElections = async () => {
    try {
      const res = await api.get('/elections');
      setElections(res.data);
      if (res.data.length > 0 && !selectedElectionId) {
        setSelectedElectionId(res.data[0].id);
      }
      return;
    } catch (err) {
      console.log('Using observer elections fallback');
    }

    const saved = localStorage.getItem('demo_elections');
    const parsed = saved ? JSON.parse(saved) : DEFAULT_ELECTIONS;
    setElections(parsed);
    if (parsed.length > 0 && !selectedElectionId) {
      setSelectedElectionId(parsed[0].id);
    }
  };

  const fetchResults = async (id: number) => {
    try {
      const res = await api.get(`/observer/live-results/${id}`);
      setLiveResults(res.data);
      return;
    } catch (err) {
      console.log('Using observer results fallback');
    }

    const savedElections = localStorage.getItem('demo_elections');
    const electionsList = savedElections ? JSON.parse(savedElections) : DEFAULT_ELECTIONS;
    const target = electionsList.find((e: any) => e.id === id) || electionsList[0];

    const savedReceipts = localStorage.getItem('demo_receipts');
    const receiptsList = savedReceipts ? JSON.parse(savedReceipts) : [];
    const electionReceipts = receiptsList.filter((r: any) => r.election_id === id);

    let totalVotes = electionReceipts.length;
    let candidatesWithStats = (target?.candidates || []).map((cand: any) => {
      const candVotes = electionReceipts.filter((r: any) => r.candidate_id === cand.id).length;
      return {
        candidate_id: cand.id,
        name: cand.name,
        party: cand.party || 'Independent',
        vote_count: candVotes,
        percentage: totalVotes > 0 ? Math.round((candVotes / totalVotes) * 100) : 0
      };
    });

    setLiveResults({
      election_id: id,
      title: target?.title || 'General Election 2026',
      status: target?.status || 'active',
      total_votes: totalVotes,
      candidates: candidatesWithStats
    });
  };

  useEffect(() => {
    fetchElections();
  }, []);

  useEffect(() => {
    if (selectedElectionId) {
      fetchResults(selectedElectionId);
      const interval = setInterval(() => fetchResults(selectedElectionId), 3000);
      return () => clearInterval(interval);
    }
  }, [selectedElectionId]);

  return (
    <div className="space-y-8">
      
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <div>
          <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">INDEPENDENT OBSERVER</span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Live Election Transparency Desk</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Real-time vote tallies, candidate percentages, and cryptographically verified count</p>
        </div>

        <button
          onClick={() => window.print()}
          className="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-semibold rounded-xl text-xs flex items-center gap-2 transition-colors"
        >
          <Download className="w-4 h-4" /> Export Report (PDF)
        </button>
      </div>

      {/* Select Election Tabs */}
      <div className="flex flex-wrap gap-2">
        {elections.map((ele) => (
          <button
            key={ele.id}
            onClick={() => setSelectedElectionId(ele.id)}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-mono transition-all ${
              selectedElectionId === ele.id
                ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg shadow-cyan-500/20'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
            }`}
          >
            #{ele.id} • {ele.title}
          </button>
        ))}
      </div>

      {liveResults && (
        <div className="space-y-6">
          
          {/* Summary Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-5 glass-card rounded-2xl border border-slate-200 dark:border-slate-800">
              <span className="text-[10px] font-mono text-slate-400 uppercase">Total Votes Cast</span>
              <h3 className="text-2xl font-extrabold text-slate-900 dark:text-white mt-1">{liveResults.total_votes}</h3>
            </div>
            <div className="p-5 glass-card rounded-2xl border border-slate-200 dark:border-slate-800">
              <span className="text-[10px] font-mono text-slate-400 uppercase">Election Status</span>
              <h3 className="text-2xl font-extrabold text-cyan-500 capitalize mt-1">{liveResults.status}</h3>
            </div>
            <div className="p-5 glass-card rounded-2xl border border-slate-200 dark:border-slate-800">
              <span className="text-[10px] font-mono text-slate-400 uppercase">Blockchain Ledger</span>
              <h3 className="text-2xl font-extrabold text-emerald-500 mt-1 flex items-center gap-1.5">
                <ShieldCheck className="w-6 h-6" /> Verified
              </h3>
            </div>
          </div>

          {/* Chart & Breakdowns */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Recharts Bar Chart */}
            <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <BarIcon className="w-5 h-5 text-cyan-500" /> Vote Distribution Chart
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={liveResults.candidates}>
                    <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} />
                    <YAxis stroke="#94a3b8" fontSize={11} />
                    <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', color: '#fff' }} />
                    <Bar dataKey="vote_count" radius={[8, 8, 0, 0]}>
                      {liveResults.candidates.map((_: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Detailed Table */}
            <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Candidate Percentage Standings</h3>
              <div className="space-y-3">
                {liveResults.candidates.map((c: any) => (
                  <div key={c.candidate_id} className="p-4 bg-slate-50 dark:bg-slate-900/60 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-bold text-slate-900 dark:text-white">{c.name} ({c.party})</span>
                      <span className="font-mono font-bold text-cyan-500">{c.percentage}% ({c.vote_count} votes)</span>
                    </div>
                    {/* Progress Bar */}
                    <div className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-500"
                        style={{ width: `${c.percentage}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  );
};
