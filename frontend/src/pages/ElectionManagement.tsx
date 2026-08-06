import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Election } from '../types';
import { Plus, UserPlus, Upload, Vote, Calendar, CheckCircle2, AlertCircle } from 'lucide-react';

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

  const fetchElections = async () => {
    try {
      const res = await api.get('/elections');
      setElections(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchElections();
  }, []);

  const handleCreateElection = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/elections', { title, description, status: 'active' });
      setTitle('');
      setDescription('');
      setShowCreateModal(false);
      fetchElections();
    } catch (err) {
      alert('Failed to create election');
    }
  };

  const handleAddCandidate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedElectionId) return;
    try {
      await api.post(`/elections/${selectedElectionId}/candidates`, {
        name: candName,
        party: candParty,
        manifesto: candManifesto
      });
      setCandName('');
      setCandParty('');
      setCandManifesto('');
      setSelectedElectionId(null);
      fetchElections();
    } catch (err) {
      alert('Failed to add candidate');
    }
  };

  const handleStatusChange = async (electionId: number, newStatus: string) => {
    try {
      await api.put(`/elections/${electionId}/status?status_val=${newStatus}`);
      fetchElections();
    } catch (err) {
      alert('Failed to change status');
    }
  };

  const handleCsvImport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!csvFile) return;
    const formData = new FormData();
    formData.append('file', csvFile);

    try {
      const res = await api.post('/admin/import-voters-csv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setImportResult(res.data.message);
      setCsvFile(null);
    } catch (err: any) {
      setImportResult(err.response?.data?.detail || 'Import failed');
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <div>
          <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">ADMIN MANAGEMENT</span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Election & Candidate Studio</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Configure elections, register candidates, and bulk import voters</p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition-all"
        >
          <Plus className="w-4 h-4" /> Create Election
        </button>
      </div>

      {/* CSV Bulk Import Box */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <Upload className="w-5 h-5 text-cyan-500" /> Bulk Voter CSV Import
        </h3>
        <form onSubmit={handleCsvImport} className="flex flex-col sm:flex-row items-center gap-3">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setCsvFile(e.target.files?.[0] || null)}
            className="text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-cyan-500/10 file:text-cyan-500 hover:file:bg-cyan-500/20"
          />
          <button
            type="submit"
            disabled={!csvFile}
            className="px-4 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 text-xs font-semibold rounded-xl disabled:opacity-40"
          >
            Upload CSV
          </button>
        </form>
        {importResult && (
          <p className="text-xs font-mono text-cyan-500">{importResult}</p>
        )}
      </div>

      {/* Elections List */}
      <div className="space-y-4">
        {elections.map((ele) => (
          <div key={ele.id} className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <span className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase ${
                  ele.status === 'active' ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30' : 'bg-slate-500/10 text-slate-500'
                }`}>
                  Status: {ele.status}
                </span>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-1">
                  #{ele.id} • {ele.title}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">{ele.description}</p>
              </div>

              {/* Status Actions */}
              <div className="flex items-center gap-2">
                {ele.status !== 'active' && (
                  <button
                    onClick={() => handleStatusChange(ele.id, 'active')}
                    className="px-3 py-1.5 bg-emerald-600 text-white rounded-xl text-xs font-semibold hover:bg-emerald-500 transition-colors"
                  >
                    Activate
                  </button>
                )}
                {ele.status === 'active' && (
                  <button
                    onClick={() => handleStatusChange(ele.id, 'closed')}
                    className="px-3 py-1.5 bg-rose-600 text-white rounded-xl text-xs font-semibold hover:bg-rose-500 transition-colors"
                  >
                    Close Election
                  </button>
                )}
                <button
                  onClick={() => setSelectedElectionId(ele.id)}
                  className="px-3 py-1.5 bg-cyan-600/10 text-cyan-500 border border-cyan-500/30 rounded-xl text-xs font-semibold hover:bg-cyan-500/20 transition-colors flex items-center gap-1"
                >
                  <UserPlus className="w-3.5 h-3.5" /> Add Candidate
                </button>
              </div>
            </div>

            {/* Candidates Listing */}
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono mb-2">Registered Candidates ({ele.candidates.length})</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                {ele.candidates.map((cand) => (
                  <div key={cand.id} className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-2xl border border-slate-200 dark:border-slate-800 flex items-center gap-3">
                    <img src={cand.avatar_url || 'https://via.placeholder.com/100'} alt={cand.name} className="w-10 h-10 rounded-full object-cover border border-cyan-500/30" />
                    <div>
                      <h5 className="text-xs font-bold text-slate-900 dark:text-white">{cand.name}</h5>
                      <p className="text-[10px] text-cyan-500 font-semibold">{cand.party || 'Independent'}</p>
                      <span className="text-[10px] font-mono text-slate-400">Total Votes: {cand.vote_count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        ))}
      </div>

      {/* Create Election Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="w-full max-w-md p-6 glass-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Create New Election</h3>
            <form onSubmit={handleCreateElection} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Student Council Election 2026"
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Details regarding this election..."
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button type="button" onClick={() => setShowCreateModal(false)} className="px-4 py-2 text-xs font-semibold text-slate-400">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-cyan-600 text-white text-xs font-semibold rounded-xl">Save & Launch</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Candidate Modal */}
      {selectedElectionId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="w-full max-w-md p-6 glass-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Add Candidate to Election #{selectedElectionId}</h3>
            <form onSubmit={handleAddCandidate} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Candidate Full Name</label>
                <input
                  type="text"
                  required
                  value={candName}
                  onChange={(e) => setCandName(e.target.value)}
                  placeholder="e.g. Sarah Connor"
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Party / Organization</label>
                <input
                  type="text"
                  value={candParty}
                  onChange={(e) => setCandParty(e.target.value)}
                  placeholder="e.g. Innovation Alliance"
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Manifesto</label>
                <textarea
                  value={candManifesto}
                  onChange={(e) => setCandManifesto(e.target.value)}
                  placeholder="Candidate manifesto goals..."
                  className="w-full px-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button type="button" onClick={() => setSelectedElectionId(null)} className="px-4 py-2 text-xs font-semibold text-slate-400">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-cyan-600 text-white text-xs font-semibold rounded-xl">Add Candidate</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
