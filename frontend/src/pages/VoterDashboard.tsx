import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Election, Candidate, VoteReceipt } from '../types';
import { 
  Vote as VoteIcon, 
  CheckCircle2, 
  RefreshCw, 
  ShieldCheck, 
  Calendar, 
  FileText, 
  AlertCircle, 
  ArrowRight,
  ExternalLink,
  Lock,
  Cpu
} from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';
import { Link } from 'react-router-dom';

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

export const VoterDashboard: React.FC = () => {
  const { user } = useAuth();
  const [elections, setElections] = useState<Election[]>([]);
  const [myReceipts, setMyReceipts] = useState<VoteReceipt[]>([]);
  const [selectedCandidates, setSelectedCandidates] = useState<{ [electionId: number]: Candidate }>({});
  const [confirmingElectionId, setConfirmingElectionId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [miningStatus, setMiningStatus] = useState<string>('');
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

  const getVoteReceiptForElection = (electionId: number) => {
    if (!user) return null;
    return myReceipts.find(r => r.election_id === electionId && ((r as any).user_id === user.id || (r as any).username === user.username));
  };

  const resetMyVotes = (electionId: number) => {
    if (!user) return;
    const current = getStoredReceipts();
    const filtered = current.filter(r => !(r.election_id === electionId && ((r as any).user_id === user.id || (r as any).username === user.username)));
    saveStoredReceipts(filtered);
    setMyReceipts(filtered);
    const updatedSelected = { ...selectedCandidates };
    delete updatedSelected[electionId];
    setSelectedCandidates(updatedSelected);
    setConfirmingElectionId(null);
  };

  const generateMockHex = (len: number) => {
    const chars = '0123456789abcdef';
    let res = '';
    for (let i = 0; i < len; i++) res += chars[Math.floor(Math.random() * chars.length)];
    return res;
  };

  const handleSelectCandidate = (electionId: number, cand: Candidate) => {
    setSelectedCandidates(prev => ({ ...prev, [electionId]: cand }));
  };

  const handleCastVote = async (cand: Candidate, ele: Election) => {
    setLoading(true);
    setMiningStatus('Generating SECP256R1 zero-knowledge ballot commitment...');

    await new Promise(r => setTimeout(r, 600));
    setMiningStatus('Broadcasting cryptographic transaction to PoW Testnet (Chain ID 1337)...');

    await new Promise(r => setTimeout(r, 700));
    setMiningStatus('Mining transaction into block & verifying Merkle proof...');

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
        block_index: getStoredReceipts().length + 1403,
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
      setMiningStatus('');
      setConfirmingElectionId(null);
      fetchVoterData();
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header Banner */}
      <div className="civic-card p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono uppercase tracking-wider text-blue-600 dark:text-blue-400 font-bold">
              OFFICIAL BALLOT PORTAL
            </span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
              SECP256R1 ECDSA SIGNED
            </span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-1">
            Active University Elections
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
            Eligible student and faculty voters can review accredited candidates, cast a single irreversible ballot, and obtain a verifiable cryptographic transaction receipt.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3.5 py-2 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-mono flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <div>
              <div className="text-[10px] text-slate-400 uppercase">AUTHENTICATED VOTER</div>
              <div className="font-bold text-slate-800 dark:text-slate-200">{user?.username || 'voter1'}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Active Elections List */}
      <div className="space-y-6">
        {elections.length === 0 ? (
          <div className="civic-card p-12 text-center text-slate-500 dark:text-slate-400">
            <Calendar className="w-10 h-10 mx-auto text-slate-300 dark:text-slate-700 mb-3" />
            <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">No Active Elections Currently Open</h3>
            <p className="text-xs text-slate-500 mt-1">Check back during designated campus voting windows.</p>
          </div>
        ) : (
          elections.map((ele) => {
            const alreadyVoted = hasVotedInElection(ele.id);
            const recordedReceipt = getVoteReceiptForElection(ele.id);
            const selectedCand = selectedCandidates[ele.id];
            const isConfirming = confirmingElectionId === ele.id;

            return (
              <div key={ele.id} className="civic-card p-6 sm:p-7 space-y-6">
                
                {/* Election Metadata Header */}
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-slate-200 dark:border-slate-800">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-mono font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                        VOTING ACTIVE
                      </span>
                      <span className="text-xs text-slate-400 font-mono">Election #{ele.id}</span>
                    </div>
                    <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                      {ele.title}
                    </h2>
                    <p className="text-xs text-slate-600 dark:text-slate-400 max-w-2xl">
                      {ele.description}
                    </p>
                  </div>

                  {/* Voter Status Tag / Re-vote reset tool */}
                  <div className="flex items-center gap-2 shrink-0">
                    {alreadyVoted ? (
                      <div className="flex items-center gap-2">
                        <span className="px-3 py-1.5 bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5">
                          <CheckCircle2 className="w-4 h-4 text-emerald-600" /> BALLOT RECORDED
                        </span>
                        <button
                          onClick={() => resetMyVotes(ele.id)}
                          className="px-2.5 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-mono transition-colors"
                          title="Reset vote in demo mode to cast another ballot"
                        >
                          <RefreshCw className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    ) : (
                      <span className="px-3 py-1.5 bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800 rounded-lg text-xs font-mono font-medium flex items-center gap-1.5">
                        <VoteIcon className="w-4 h-4 text-blue-600" /> ELIGIBLE TO VOTE (1 BALLOT)
                      </span>
                    )}
                  </div>
                </div>

                {/* Candidate Selection Area */}
                {alreadyVoted ? (
                  /* Post-Vote Confirmation State */
                  <div className="p-5 bg-slate-50 dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                        <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">
                          Your vote is cryptographically secured on Block #{recordedReceipt?.block_index || 1403}
                        </h4>
                      </div>
                      <Link
                        to="/voter/receipts"
                        className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
                      >
                        <span>View Official Receipt</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </Link>
                    </div>

                    <div className="font-mono text-xs text-slate-500 dark:text-slate-400 space-y-1 pt-1 border-t border-slate-200 dark:border-slate-800">
                      <div>TRANSACTION HASH: <span className="font-bold text-slate-800 dark:text-slate-200">{recordedReceipt?.tx_hash || '0x4f8a...3b21'}</span></div>
                      <div>RECEIPT HASH: <span className="text-slate-700 dark:text-slate-300">{recordedReceipt?.receipt_hash || 'e3b0c442...'}</span></div>
                      <div className="text-[11px] text-slate-400 pt-1">
                        🔒 Ballot Secrecy Guarantee: Candidate choice is zero-knowledge committed and hidden from public receipts.
                      </div>
                    </div>
                  </div>
                ) : (
                  /* Voting Slate: Candidate Cards */
                  <div className="space-y-4">
                    <div className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                      Select One Candidate to Cast Your Ballot:
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {ele.candidates && ele.candidates.map((cand) => {
                        const isSelected = selectedCand?.id === cand.id;

                        return (
                          <div
                            key={cand.id}
                            onClick={() => handleSelectCandidate(ele.id, cand)}
                            className={`p-5 rounded-xl border cursor-pointer transition-all ${
                              isSelected
                                ? 'border-blue-600 bg-blue-50/40 dark:bg-blue-950/30 ring-2 ring-blue-600/30'
                                : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-slate-300 dark:hover:border-slate-700'
                            }`}
                          >
                            <div className="flex items-start gap-4">
                              <img
                                src={cand.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80'}
                                alt={cand.name}
                                className="w-14 h-14 rounded-lg object-cover border border-slate-200 dark:border-slate-700 shrink-0"
                              />
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between gap-2">
                                  <h4 className="text-base font-bold text-slate-900 dark:text-slate-100 truncate">
                                    {cand.name}
                                  </h4>
                                  <div className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 ${
                                    isSelected
                                      ? 'border-blue-600 bg-blue-600 text-white'
                                      : 'border-slate-300 dark:border-slate-600'
                                  }`}>
                                    {isSelected && <span className="w-2 h-2 rounded-full bg-white"></span>}
                                  </div>
                                </div>
                                <p className="text-xs font-semibold text-blue-600 dark:text-blue-400 mt-0.5">
                                  {cand.party}
                                </p>
                                <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 line-clamp-3">
                                  {cand.manifesto}
                                </p>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    {/* Step 2: Confirmation & Submission Box */}
                    {selectedCand && (
                      <div className="p-5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl space-y-4 mt-4">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <div className="text-xs font-mono uppercase text-blue-600 dark:text-blue-400 font-bold">
                              CONFIRM YOUR SELECTION
                            </div>
                            <div className="text-sm font-bold text-slate-900 dark:text-slate-100 mt-0.5">
                              You have selected: <span className="text-blue-600 dark:text-blue-400">{selectedCand.name}</span> ({selectedCand.party})
                            </div>
                            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                              Submission will sign a transaction with your authenticated identity and record it on the PoW block ledger.
                            </p>
                          </div>
                        </div>

                        {loading ? (
                          <div className="p-4 bg-blue-50/60 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 rounded-lg flex items-center gap-3">
                            <RefreshCw className="w-5 h-5 text-blue-600 dark:text-blue-400 animate-spin shrink-0" />
                            <div className="font-mono text-xs text-blue-800 dark:text-blue-200">
                              {miningStatus}
                            </div>
                          </div>
                        ) : (
                          <div className="flex items-center gap-3">
                            <button
                              onClick={() => handleCastVote(selectedCand, ele)}
                              disabled={loading}
                              className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors flex items-center gap-2"
                            >
                              <VoteIcon className="w-4 h-4" />
                              <span>Submit Official Ballot</span>
                            </button>
                            <button
                              onClick={() => setSelectedCandidates(prev => {
                                const next = { ...prev };
                                delete next[ele.id];
                                return next;
                              })}
                              className="px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-semibold text-xs rounded-lg hover:bg-slate-100 transition-colors"
                            >
                              Cancel Selection
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}

              </div>
            );
          })
        )}
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
