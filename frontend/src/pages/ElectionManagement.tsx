import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Election } from '../types';
import { Plus, UserPlus, CheckCircle2, AlertCircle, X, Vote, Users, Calendar, ArrowRight } from 'lucide-react';

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

export const ElectionManagement: React.FC = () => {
  const [elections, setElections] = useState<Election[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Candidate Modal State
  const [selectedElectionId, setSelectedElectionId] = useState<number | null>(null);
  const [candName, setCandName] = useState('');
  const [candParty, setCandParty] = useState('');
  const [candManifesto, setCandManifesto] = useState('');

  const getStoredElections = (): Election[] => {
    try {
      const saved = localStorage.getItem('demo_elections');
      if (saved) return JSON.parse(saved);
    } catch (e) {}
    localStorage.setItem('demo_elections', JSON.stringify(DEFAULT_ELECTIONS));
    return DEFAULT_ELECTIONS;
  };

  const saveStoredElections = (list: Election[]) => {
    try {
      localStorage.setItem('demo_elections', JSON.stringify(list));
    } catch (e) {}
  };

  const fetchElections = async () => {
    try {
      const res = await api.get('/elections');
      if (res.data && res.data.length > 0) {
        setElections(res.data);
        saveStoredElections(res.data);
        return;
      }
    } catch (err) {
      console.log('Using local elections storage fallback');
    }
    setElections(getStoredElections());
  };

  useEffect(() => {
    fetchElections();
  }, []);

  const handleCreateElection = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    try {
      await api.post('/elections', { title, description, status: 'active' });
    } catch (err) {
      const current = getStoredElections();
      const newElection: Election = {
        id: Date.now(),
        title,
        description: description || 'Decentralized blockchain election',
        status: 'active',
        start_time: new Date().toISOString(),
        end_time: new Date(Date.now() + 7 * 86400000).toISOString(),
        created_by: 1,
        created_at: new Date().toISOString(),
        candidates: []
      };
      const updated = [newElection, ...current];
      saveStoredElections(updated);
    }

    setTitle('');
    setDescription('');
    setShowCreateModal(false);
    fetchElections();
  };

  const handleAddCandidate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedElectionId || !candName.trim()) return;

    try {
      await api.post(`/elections/${selectedElectionId}/candidates`, {
        name: candName,
        party: candParty,
        manifesto: candManifesto
      });
    } catch (err) {
      const current = getStoredElections();
      const target = current.find(e => e.id === selectedElectionId);
      if (target) {
        if (!target.candidates) target.candidates = [];
        target.candidates.push({
          id: Date.now(),
          election_id: selectedElectionId,
          name: candName,
          party: candParty || 'Independent',
          manifesto: candManifesto || 'Official platform',
          avatar_url: `https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80`,
          vote_count: 0
        });
        saveStoredElections(current);
      }
    }

    setCandName('');
    setCandParty('');
    setCandManifesto('');
    setSelectedElectionId(null);
    fetchElections();
  };

  const toggleElectionStatus = (id: number) => {
    const current = getStoredElections();
    const updated: Election[] = current.map(e => {
      if (e.id === id) {
        const nextStatus: 'active' | 'closed' = e.status === 'active' ? 'closed' : 'active';
        return { ...e, status: nextStatus };
      }
      return e;
    });
    saveStoredElections(updated);
    setElections(updated);
  };

  return (
    <div className="space-y-6">
      
      {/* Header Banner */}
      <div className="civic-card p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono uppercase tracking-wider text-blue-600 dark:text-blue-400 font-bold">
              CONTEST GOVERNANCE
            </span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
              ELECTION &amp; CANDIDATE ROSTER
            </span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-1">
            Elections &amp; Ballot Setup
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
            Create new election contests, manage accredited candidate profiles, open or close voting windows, and audit candidate eligibility.
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors flex items-center gap-1.5 shrink-0"
        >
          <Plus className="w-4 h-4" />
          <span>Create New Election</span>
        </button>
      </div>

      {/* Elections List */}
      <div className="space-y-5">
        {elections.map((ele) => (
          <div key={ele.id} className="civic-card p-6 space-y-5">
            
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-mono font-bold ${
                    ele.status === 'active'
                      ? 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700'
                  }`}>
                    {ele.status === 'active' ? '● VOTING ACTIVE' : '○ CONTEST CLOSED'}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">Contest #{ele.id}</span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  {ele.title}
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 max-w-2xl">
                  {ele.description}
                </p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => setSelectedElectionId(ele.id)}
                  className="px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-semibold flex items-center gap-1 transition-colors"
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  <span>Add Candidate</span>
                </button>
                <button
                  onClick={() => toggleElectionStatus(ele.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-colors ${
                    ele.status === 'active'
                      ? 'bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800 hover:bg-amber-100'
                      : 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100'
                  }`}
                >
                  {ele.status === 'active' ? 'Close Voting' : 'Open Voting'}
                </button>
              </div>
            </div>

            {/* Candidates Roster */}
            <div>
              <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 font-mono uppercase mb-3">
                Approved Candidates ({ele.candidates?.length || 0})
              </div>

              {(!ele.candidates || ele.candidates.length === 0) ? (
                <div className="p-4 bg-slate-50 dark:bg-slate-950 rounded-lg border border-dashed border-slate-300 dark:border-slate-700 text-center text-xs text-slate-500">
                  No candidates accredited for this contest yet. Click "Add Candidate" above.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {ele.candidates.map((cand) => (
                    <div key={cand.id} className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg flex items-start gap-3">
                      <img
                        src={cand.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80'}
                        alt={cand.name}
                        className="w-10 h-10 rounded-md object-cover border border-slate-200 dark:border-slate-700 shrink-0"
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <h4 className="font-bold text-xs text-slate-900 dark:text-slate-100 truncate">{cand.name}</h4>
                          <span className="text-[10px] font-mono text-slate-500">Candidate #{cand.id}</span>
                        </div>
                        <p className="text-[11px] text-blue-600 dark:text-blue-400 font-medium">{cand.party}</p>
                        <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">{cand.manifesto}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

          </div>
        ))}
      </div>

      {/* Modal: Create Election */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 flex items-center justify-center p-4">
          <div className="civic-card max-w-md w-full p-6 space-y-4 shadow-xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
              <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-2">
                <Vote className="w-4 h-4 text-blue-600" />
                <span>Create New Election Contest</span>
              </h3>
              <button onClick={() => setShowCreateModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleCreateElection} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Election Title
                </label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Faculty Senate General Election 2026"
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Description &amp; Scope
                </label>
                <textarea
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Explain eligibility, term limits, and voting criteria..."
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-600 border rounded-lg hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg"
                >
                  Publish Election Contest
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Add Candidate */}
      {selectedElectionId && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 flex items-center justify-center p-4">
          <div className="civic-card max-w-md w-full p-6 space-y-4 shadow-xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
              <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 flex items-center gap-2">
                <UserPlus className="w-4 h-4 text-blue-600" />
                <span>Accredit Candidate Profile</span>
              </h3>
              <button onClick={() => setSelectedElectionId(null)} className="text-slate-400 hover:text-slate-600">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleAddCandidate} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Candidate Full Name
                </label>
                <input
                  type="text"
                  required
                  value={candName}
                  onChange={(e) => setCandName(e.target.value)}
                  placeholder="e.g. Maya Lin"
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Party or Affiliation
                </label>
                <input
                  type="text"
                  value={candParty}
                  onChange={(e) => setCandParty(e.target.value)}
                  placeholder="e.g. University Green Coalition"
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Candidate Platform &amp; Manifesto
                </label>
                <textarea
                  rows={3}
                  value={candManifesto}
                  onChange={(e) => setCandManifesto(e.target.value)}
                  placeholder="Summary of campaign priorities..."
                  className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setSelectedElectionId(null)}
                  className="px-3 py-1.5 text-xs text-slate-600 border rounded-lg hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg"
                >
                  Add to Ballot Slate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
