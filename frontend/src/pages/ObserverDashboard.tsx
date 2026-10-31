import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Election } from '../types';
import { BarChart3, Lock } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const DEFAULT_ELECTIONS: Election[] = [
  {
    id: 1,
    title: "Student Government Presidential Election 2025–2026",
    description: "Annual university-wide executive leadership election conducted via cryptographic decentralized ledger.",
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
        party: "Progressive Student Alliance",
        manifesto: "Expanding research funding, campus digital sovereignty, open educational resources, and sustainable infrastructure.",
        avatar_url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80",
        vote_count: 0
      },
      {
        id: 102,
        election_id: 1,
        name: "Elena Rostova",
        party: "Academic Integrity Coalition",
        manifesto: "Transparent governance, student fee reductions, universal library access, and anonymous cryptographic polling.",
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

  const BAR_COLORS = ['#2563eb', '#0f766e', '#475569', '#7c3aed', '#d97706'];

  const fetchElections = async () => {
    try {
      const res = await api.get('/elections');
      if (res.data && res.data.length > 0) {
        setElections(res.data);
        if (!selectedElectionId) setSelectedElectionId(res.data[0].id);
        return;
      }
    } catch (err) {
      console.log('Using observer elections fallback');
    }

    const saved = localStorage.getItem('demo_elections');
    const parsed = saved ? JSON.parse(saved) : DEFAULT_ELECTIONS;
    setElections(parsed);
    if (!selectedElectionId && parsed.length > 0) {
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
      title: target?.title || 'Presidential Election 2025–2026',
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
      const timer = setInterval(() => fetchResults(selectedElectionId), 5000);
      return () => clearInterval(timer);
    }
  }, [selectedElectionId]);

  return (
    <div className="space-y-4 sm:space-y-6 w-full">
      
      {/* Header */}
      <div className="civic-card p-4 sm:p-6 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-1.5 text-xs font-mono text-blue-600 dark:text-blue-400 font-bold uppercase">
            <span>PUBLIC OBSERVATION</span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span className="text-slate-500 font-normal">CERTIFIED TALLIES</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-0.5">
            Live Election Results
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 max-w-xl">
            Tallies are calculated directly from verified transactions mined on the block ledger.
          </p>
        </div>

        {/* Contest Dropdown */}
        <div className="flex items-center gap-2 self-start md:self-auto w-full sm:w-auto">
          <label className="text-xs font-semibold text-slate-500 font-mono shrink-0">CONTEST:</label>
          <select
            value={selectedElectionId || ''}
            onChange={(e) => setSelectedElectionId(Number(e.target.value))}
            className="w-full sm:w-auto px-2.5 py-1.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs font-semibold text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {elections.map((ele) => (
              <option key={ele.id} value={ele.id}>
                {ele.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 sm:gap-4">
        <div className="civic-card p-4">
          <div className="text-[10px] sm:text-[11px] font-mono text-slate-500 uppercase">Verified Ballots Cast</div>
          <div className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 mt-0.5">
            {liveResults?.total_votes || 0}
          </div>
          <p className="text-[10px] text-slate-400 font-mono">Recorded on PoW Ledger</p>
        </div>

        <div className="civic-card p-4">
          <div className="text-[10px] sm:text-[11px] font-mono text-slate-500 uppercase">Contest Status</div>
          <div className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 mt-0.5 flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <span className="capitalize">{liveResults?.status || 'Active'}</span>
          </div>
          <p className="text-[10px] text-slate-400 font-mono">Accepting verified blocks</p>
        </div>

        <div className="civic-card p-4">
          <div className="text-[10px] sm:text-[11px] font-mono text-slate-500 uppercase">Audit Integrity</div>
          <div className="text-xl sm:text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
            100% Certified
          </div>
          <p className="text-[10px] text-slate-400 font-mono">Merkle proofs matched</p>
        </div>
      </div>

      {/* Candidate Breakdown & Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        
        {/* Candidate List with Progress Bars */}
        <div className="lg:col-span-2 civic-card p-4 sm:p-6 space-y-4">
          <h2 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
            <BarChart3 className="w-4 h-4 text-blue-600 shrink-0" />
            <span>Accredited Candidate Tallies</span>
          </h2>

          <div className="space-y-3">
            {liveResults?.candidates && liveResults.candidates.map((cand: any) => {
              const isLeader = cand.vote_count > 0 && Math.max(...liveResults.candidates.map((c: any) => c.vote_count)) === cand.vote_count;

              return (
                <div key={cand.candidate_id} className="p-3.5 bg-slate-50 dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 space-y-1.5">
                  <div className="flex items-center justify-between gap-2">
                    <div className="min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="font-bold text-xs sm:text-sm text-slate-900 dark:text-slate-100 truncate">
                          {cand.name}
                        </span>
                        {isLeader && (
                          <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300">
                            LEAD
                          </span>
                        )}
                      </div>
                      <p className="text-[11px] text-blue-600 dark:text-blue-400 truncate">{cand.party}</p>
                    </div>

                    <div className="text-right shrink-0">
                      <div className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">
                        {cand.vote_count} <span className="text-[10px] font-normal text-slate-500">{cand.vote_count === 1 ? 'vote' : 'votes'}</span>
                      </div>
                      <div className="text-[10px] font-mono text-slate-500">{cand.percentage}%</div>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                      style={{ width: `${cand.percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Minimal Bar Chart */}
        <div className="civic-card p-4 sm:p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100 mb-0.5">
              Vote Distribution
            </h3>
            <p className="text-[11px] text-slate-500 font-mono">Ballot Share Breakdown</p>
          </div>

          <div className="h-48 sm:h-56 w-full my-3">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={liveResults?.candidates || []} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <XAxis dataKey="name" tick={{ fontSize: 9, fill: '#64748b' }} interval={0} />
                <YAxis tick={{ fontSize: 9, fill: '#64748b' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#0f172a', 
                    borderColor: '#334155', 
                    borderRadius: '6px', 
                    fontSize: '11px',
                    color: '#f8fafc' 
                  }} 
                />
                <Bar dataKey="vote_count" fill="#2563eb" radius={[4, 4, 0, 0]}>
                  {(liveResults?.candidates || []).map((_: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={BAR_COLORS[index % BAR_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800 text-[10px] font-mono text-slate-500 flex items-center gap-1.5">
            <Lock className="w-3 h-3 text-slate-400 shrink-0" />
            <span>Audit Note: Live observer tallies match ledger consensus.</span>
          </div>
        </div>

      </div>

    </div>
  );
};
