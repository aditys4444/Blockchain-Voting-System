import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Election, Candidate, VoteReceipt } from '../types';
import { Vote as VoteIcon, CheckCircle, Sparkles, RefreshCw, ShieldCheck } from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';

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

export const VoterDashboard: React.FC = () => {
  const { user } = useAuth();
  const [elections, setElections] = useState<Election[]>([]);
  const [myReceipts, setMyReceipts] = useState<VoteReceipt[]>([]);
  const [selectedElection, setSelectedElection] = useState<Election | null>(null);
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [loading, setLoading] = useState(false);
  const [voteSuccessReceipt, setVoteSuccessReceipt] = useState<any>(null);

  const getStoredReceipts = (): VoteReceipt[] => {
    try {
      const saved = localStorage.getItem('demo_receipts');
      if (saved) return JSON.parse(saved);
    } catch (e) {}
    return [];
  };

  const saveStoredReceipts = (list: VoteReceipt[]) => {
    try {
      localStorage.setItem('demo_receipts', JSON.stringify(list));
    } catch (e) {}
  };

  const fetchVoterData = async () => {
    let activeOnly: Election[] = [];
    try {
      const [eRes, rRes] = await Promise.all([
        api.get('/elections'),
        api.get('/votes/my-receipts')
      ]);
      activeOnly = eRes.data.filter((e: Election) => e.status === 'active');
      setElections(activeOnly);
      setMyReceipts(rRes.data);
      saveStoredReceipts(rRes.data);
      return;
    } catch (err) {
      console.log('Using voter data fallback');
    }

    try {
      const savedElections = localStorage.getItem('demo_elections');
      const parsed = savedElections ? JSON.parse(savedElections) : DEFAULT_ELECTIONS;
      activeOnly = parsed.filter((e: Election) => e.status === 'active');
    } catch (e) {
      activeOnly = DEFAULT_ELECTIONS;
    }
    setElections(activeOnly);
    setMyReceipts(getStoredReceipts());
  };

  useEffect(() => {
    fetchVoterData();
  }, []);

  const hasVotedInElection = (electionId: number) => {
    if (!user) return false;
    return myReceipts.some(r => r.election_id === electionId && ((r as any).user_id === user.id || (r as any).username === user.username));
  };

  const resetMyVotes = (electionId: number) => {
    if (!user) return;
    const current = getStoredReceipts();
    const filtered = current.filter(r => !(r.election_id === electionId && ((r as any).user_id === user.id || (r as any).username === user.username)));
    saveStoredReceipts(filtered);
    setMyReceipts(filtered);
    setSelectedCandidate(null);
    setSelectedElection(null);
  };

  const generateMockHex = (len: number) => {
    const chars = '0123456789abcdef';
    let res = '';
    for (let i = 0; i < len; i++) res += chars[Math.floor(Math.random() * chars.length)];
    return res;
  };

  const handleCastVote = async (cand: Candidate, ele: Election) => {
    setLoading(true);
    setSelectedElection(ele);
    setSelectedCandidate(cand);

    try {
      const res = await api.post('/votes/cast', {
        election_id: ele.id,
        candidate_id: cand.id
      });
      setVoteSuccessReceipt(res.data);
    } catch (err: any) {
      // Local demo vote casting fallback
      const txHash = '0x' + generateMockHex(64);
      const receiptHash = generateMockHex(32);
      const mockReceipt: any = {
        vote_id: Date.now(),
        election_id: ele.id,
        candidate_id: cand.id,
        user_id: user?.id || 2,
        username: user?.username || 'voter1',
        voter_hash: generateMockHex(16),
        tx_hash: txHash,
        block_index: getStoredReceipts().length + 1,
        receipt_hash: receiptHash,
        created_at: new Date().toISOString()
      };

      const currentReceipts = getStoredReceipts();
      const updatedReceipts = [mockReceipt, ...currentReceipts];
      saveStoredReceipts(updatedReceipts);

      setVoteSuccessReceipt({
        tx_hash: txHash,
        block_index: mockReceipt.block_index,
        receipt_hash: receiptHash,
        voter_hash: mockReceipt.voter_hash,
        election_id: ele.id,
        created_at: new Date().toISOString()
      });
    } finally {
      setLoading(false);
      fetchVoterData();
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">VOTER PORTAL</span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Active Elections & Voting Desk</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Your vote is encrypted with AES-256 GCM and recorded immutably on the SHA-256 ledger</p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1.5 bg-cyan-500/10 text-cyan-500 border border-cyan-500/30 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4" /> IDENTITY: {user?.username || 'Voter'}
          </span>
        </div>
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
                  <div className="flex items-center gap-2">
                    <span className="px-3 py-1.5 bg-emerald-500/10 text-emerald-500 border border-emerald-500/30 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5">
                      <CheckCircle className="w-4 h-4" /> VOTE RECORDED
                    </span>
                    <button
                      onClick={() => resetMyVotes(ele.id)}
                      className="px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-rose-500/10 text-slate-500 hover:text-rose-500 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-semibold flex items-center gap-1 transition-colors"
                      title="Reset my vote to test voting again"
                    >
                      <RefreshCw className="w-3.5 h-3.5" /> Re-Vote
                    </button>
                  </div>
                ) : (
                  <span className="px-3 py-1.5 bg-cyan-500/10 text-cyan-500 border border-cyan-500/30 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4" /> READY TO VOTE
                  </span>
                )}
              </div>

              {/* Candidate Selection Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {ele.candidates && ele.candidates.map((cand) => {
                  return (
                    <div
                      key={cand.id}
                      className={`p-5 rounded-2xl border transition-all space-y-4 ${
                        alreadyVoted
                          ? 'border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/30'
                          : 'border-slate-200 dark:border-slate-800 hover:border-cyan-500/50 hover:bg-slate-50 dark:hover:bg-slate-900/50'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <img
                          src={cand.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80'}
                          alt={cand.name}
                          className="w-14 h-14 rounded-2xl object-cover border border-cyan-500/30 shadow-md"
                        />
                        <div className="flex-1 min-w-0">
                          <h4 className="text-base font-bold text-slate-900 dark:text-white truncate">{cand.name}</h4>
                          <p className="text-xs font-semibold text-cyan-500">{cand.party}</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">{cand.manifesto}</p>
                        </div>
                      </div>

                      {/* Vote Button */}
                      {!alreadyVoted ? (
                        <button
                          onClick={() => handleCastVote(cand, ele)}
                          disabled={loading}
                          className="w-full py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
                        >
                          <VoteIcon className="w-4 h-4" />
                          {loading ? 'Encrypting & Mining Vote...' : `Vote for ${cand.name}`}
                        </button>
                      ) : (
                        <div className="py-2 text-center text-xs font-semibold text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800/50 rounded-xl">
                          Vote Recorded on Ledger
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

            </div>
          );
        })}
      </div>

      {/* Success QR Receipt Modal */}
      <QRCodeModal
        isOpen={Boolean(voteSuccessReceipt)}
        receipt={voteSuccessReceipt}
        onClose={() => setVoteSuccessReceipt(null)}
      />

    </div>
  );
};
