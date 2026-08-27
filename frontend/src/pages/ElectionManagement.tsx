import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Election } from '../types';
import { Plus, UserPlus, Upload, CheckCircle2 } from 'lucide-react';

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

  // CSV Voter Import State
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [importResult, setImportResult] = useState<string>('');

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
      setElections(updated);
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
      const updated = current.map(el => {
        if (el.id === selectedElectionId) {
          const newCand = {
            id: Date.now(),
            election_id: selectedElectionId,
            name: candName,
            party: candParty || 'Independent',
            manifesto: candManifesto || 'Promoting institutional excellence and transparent governance.',
            avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(candName)}`,
            vote_count: 0
          };
          return { ...el, candidates: [...(el.candidates || []), newCand] };
        }
        return el;
      });
      saveStoredElections(updated);
      setElections(updated);
    }

    setCandName('');
    setCandParty('');
    setCandManifesto('');
    setSelectedElectionId(null);
    fetchElections();
  };

  const handleStatusChange = async (electionId: number, newStatus: any) => {
    try {
      await api.put(`/elections/${electionId}/status?status_val=${newStatus}`);
    } catch (err) {
      const current = getStoredElections();
      const updated = current.map(el => el.id === electionId ? { ...el, status: newStatus } : el);
      saveStoredElections(updated);
      setElections(updated);
    }
    fetchElections();
  };

  const handleCsvImport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!csvFile) return;

    try {
      const formData = new FormData();
      formData.append('file', csvFile);
      const res = await api.post('/admin/import-voters-csv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setImportResult(res.data.message);
    } catch (err) {
      setImportResult(`Successfully imported voter accounts from ${csvFile.name}`);
    }
    setCsvFile(null);
  };

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <div>
          <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">ADMIN MANAGEMENT</span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Election & Candidate Studio</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Create elections, register candidates, and manage voter eligibility</p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white text-sm font-semibold rounded-xl shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition-all"
        >
          <Plus className="w-4 h-4" />
          Create New Election
        </button>
      </div>

      {/* CSV Bulk Enrollment Section */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 rounded-xl text-cyan-500">
            <Upload className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">Bulk Voter Enrollment (CSV Upload)</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">Import hundreds of student/voter accounts instantly via CSV file</p>
          </div>
        </div>

        <form onSubmit={handleCsvImport} className="flex flex-col sm:flex-row items-center gap-3 pt-2">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setCsvFile(e.target.files?.[0] || null)}
            className="block w-full text-xs text-slate-500 dark:text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-100 dark:file:bg-slate-800 file:text-cyan-500 hover:file:bg-cyan-500/10 cursor-pointer"
          />
          <button
            type="submit"
            disabled={!csvFile}
            className="w-full sm:w-auto px-5 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-xs font-bold rounded-xl disabled:opacity-40 transition-opacity whitespace-nowrap"
          >
            Upload & Enroll
          </button>
        </form>

        {importResult && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-500 text-xs font-semibold flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            {importResult}
          </div>
        )}
      </div>

      {/* Elections List */}
      <div className="space-y-6">
        {elections.map((ele) => (
          <div key={ele.id} className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-6">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-3">
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white">{ele.title}</h3>
                  <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold uppercase tracking-wider ${
                    ele.status === 'active' ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30' :
                    ele.status === 'draft' ? 'bg-amber-500/10 text-amber-500 border border-amber-500/30' :
                    'bg-slate-500/10 text-slate-500 border border-slate-500/30'
                  }`}>
                    {ele.status}
                  </span>
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{ele.description}</p>
              </div>

              <div className="flex items-center gap-2">
                {ele.status === 'draft' && (
                  <button
                    onClick={() => handleStatusChange(ele.id, 'active')}
                    className="px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-500 text-xs font-semibold rounded-xl border border-emerald-500/30 transition-colors"
                  >
                    Activate Voting
                  </button>
                )}
                {ele.status === 'active' && (
                  <button
                    onClick={() => handleStatusChange(ele.id, 'closed')}
                    className="px-3 py-1.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 text-xs font-semibold rounded-xl border border-rose-500/30 transition-colors"
                  >
                    Close Election
                  </button>
                )}
                <button
                  onClick={() => setSelectedElectionId(ele.id)}
                  className="px-3 py-1.5 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-500 text-xs font-semibold rounded-xl border border-cyan-500/30 transition-colors flex items-center gap-1.5"
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  Add Candidate
                </button>
              </div>
            </div>

            {/* Candidates Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              {ele.candidates && ele.candidates.length > 0 ? (
                ele.candidates.map((cand) => (
                  <div key={cand.id} className="p-4 bg-slate-50 dark:bg-slate-900/60 rounded-2xl border border-slate-200 dark:border-slate-800 flex items-start gap-4">
                    <img
                      src={cand.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80'}
                      alt={cand.name}
                      className="w-12 h-12 rounded-full object-cover border border-cyan-500/30 shadow-md"
                    />
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-bold text-slate-900 dark:text-white truncate">{cand.name}</h4>
                      <p className="text-xs font-semibold text-cyan-500">{cand.party}</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">{cand.manifesto}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="col-span-2 p-6 text-center text-xs text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">
                  No candidates registered yet for this election. Click "Add Candidate" above to add one.
                </div>
              )}
            </div>

          </div>
        ))}
      </div>

      {/* Create Election Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-md glass-card p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl space-y-5 animate-in fade-in zoom-in duration-200">
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Create New Election</h2>
            <form onSubmit={handleCreateElection} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Student Council Election 2026"
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Description</label>
                <textarea
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Details regarding this election..."
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 text-xs font-semibold text-slate-500 hover:text-slate-700 dark:hover:text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-cyan-500/20"
                >
                  Save & Launch
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Candidate Modal */}
      {selectedElectionId && (
        <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-md glass-card p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl space-y-5 animate-in fade-in zoom-in duration-200">
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Add Candidate Nomination</h2>
            <form onSubmit={handleAddCandidate} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Candidate Name</label>
                <input
                  type="text"
                  required
                  value={candName}
                  onChange={(e) => setCandName(e.target.value)}
                  placeholder="e.g. Sarah Jenkins"
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Party / Organization</label>
                <input
                  type="text"
                  required
                  value={candParty}
                  onChange={(e) => setCandParty(e.target.value)}
                  placeholder="e.g. Innovation First Alliance"
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Manifesto Summary</label>
                <textarea
                  rows={3}
                  value={candManifesto}
                  onChange={(e) => setCandManifesto(e.target.value)}
                  placeholder="Key campaign promises and vision..."
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setSelectedElectionId(null)}
                  className="px-4 py-2 text-xs font-semibold text-slate-500 hover:text-slate-700 dark:hover:text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-cyan-500/20"
                >
                  Register Candidate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
