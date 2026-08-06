import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Election, Candidate, VoteReceipt } from '../types';
import { Vote as VoteIcon, ShieldCheck, Lock, CheckCircle, Sparkles } from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';

export const VoterDashboard: React.FC = () => {
  const [elections, setElections] = useState<Election[]>([]);
  const [myReceipts, setMyReceipts] = useState<VoteReceipt[]>([]);
  const [selectedElection, setSelectedElection] = useState<Election | null>(null);
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [loading, setLoading] = useState(false);
  const [voteSuccessReceipt, setVoteSuccessReceipt] = useState<any>(null);

  const fetchVoterData = async () => {
    try {
      const [eRes, rRes] = await Promise.all([
        api.get('/elections'),
        api.get('/votes/my-receipts')
      ]);
      const activeOnly = eRes.data.filter((e: Election) => e.status === 'active');
      setElections(activeOnly);
      setMyReceipts(rRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchVoterData();
  }, []);

  const hasVotedInElection = (electionId: number) => {
    return myReceipts.some(r => r.election_id === electionId);
  };

  const handleCastVote = async () => {
    if (!selectedElection || !selectedCandidate) return;
    setLoading(true);

    try {
      const res = await api.post('/votes/cast', {
        election_id: selectedElection.id,
        candidate_id: selectedCandidate.id
      });

      setVoteSuccessReceipt(res.data);
      setSelectedCandidate(null);
      setSelectedElection(null);
      fetchVoterData();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to cast vote');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">VOTER PORTAL</span>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Active Elections & Voting Desk</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Your vote is encrypted with AES-256 GCM and recorded immutably on the SHA-256 ledger</p>
      </div>

      {/* Active Elections */}
      <div className="space-y-6">
        {elections.map((ele) => {
          const alreadyVoted = hasVotedInElection(ele.id);

          return (
            <div key={ele.id} className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-6">
              
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white">{ele.title}</h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{ele.description}</p>
                </div>

                {alreadyVoted ? (
                  <span className="px-3 py-1.5 bg-emerald-500/10 text-emerald-500 border border-emerald-500/30 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5">
                    <CheckCircle className="w-4 h-4" /> VOTE RECORDED
                  </span>
                ) : (
                  <span className="px-3 py-1.5 bg-cyan-500/10 text-cyan-500 border border-cyan-500/30 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4" /> READY TO VOTE
                  </span>
                )}
              </div>

              {/* Candidates Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {ele.candidates.map((cand) => {
                  const isSelected = selectedCandidate?.id === cand.id;

                  return (
                    <div
                      key={cand.id}
                      onClick={() => {
                        if (!alreadyVoted) {
                          setSelectedElection(ele);
                          setSelectedCandidate(cand);
                        }
                      }}
                      className={`p-5 rounded-2xl border transition-all cursor-pointer ${
                        alreadyVoted
                          ? 'opacity-60 cursor-not-allowed border-slate-200 dark:border-slate-800'
                          : isSelected
                          ? 'bg-cyan-500/10 border-cyan-500 shadow-lg shadow-cyan-500/10'
                          : 'bg-slate-50 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <img
                          src={cand.avatar_url || 'https://via.placeholder.com/100'}
                          alt={cand.name}
                          className="w-14 h-14 rounded-2xl object-cover border-2 border-cyan-500/30"
                        />
                        <div className="flex-1">
                          <h4 className="text-base font-bold text-slate-900 dark:text-white">{cand.name}</h4>
                          <p className="text-xs font-semibold text-cyan-500">{cand.party || 'Independent'}</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">{cand.manifesto}</p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Cast Vote CTA Bar */}
              {selectedElection?.id === ele.id && selectedCandidate && !alreadyVoted && (
                <div className="p-4 bg-cyan-500/10 border border-cyan-500/30 rounded-2xl flex items-center justify-between animate-fade-in">
                  <div>
                    <span className="text-xs font-mono text-cyan-500 font-bold uppercase">SELECTED CANDIDATE:</span>
                    <p className="text-sm font-bold text-slate-900 dark:text-white">{selectedCandidate.name} ({selectedCandidate.party})</p>
                  </div>

                  <button
                    onClick={handleCastVote}
                    disabled={loading}
                    className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition-all disabled:opacity-50"
                  >
                    <Lock className="w-4 h-4" />
                    {loading ? 'Encrypting & Mining Block...' : 'Confirm & Submit Encrypted Vote'}
                  </button>
                </div>
              )}

            </div>
          );
        })}
      </div>

      {/* QR Code Receipt Modal */}
      <QRCodeModal
        isOpen={!!voteSuccessReceipt}
        onClose={() => setVoteSuccessReceipt(null)}
        receipt={voteSuccessReceipt}
      />

    </div>
  );
};
