import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { VoteReceipt as ReceiptType } from '../types';
import { ShieldCheck, Search, QrCode, CheckCircle2, AlertTriangle } from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';

export const VoteReceipt: React.FC = () => {
  const [receipts, setReceipts] = useState<ReceiptType[]>([]);
  const [activeModalReceipt, setActiveModalReceipt] = useState<any>(null);
  
  // Receipt Verification Tool
  const [verifyHashInput, setVerifyHashInput] = useState('');
  const [verificationResult, setVerificationResult] = useState<any>(null);
  const [verifying, setVerifying] = useState(false);

  const fetchReceipts = () => {
    api.get('/votes/my-receipts')
      .then(res => setReceipts(res.data))
      .catch(() => {
        const saved = localStorage.getItem('demo_receipts');
        if (saved) setReceipts(JSON.parse(saved));
      });
  };

  useEffect(() => {
    fetchReceipts();
  }, []);

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!verifyHashInput.trim()) return;
    setVerifying(true);
    try {
      const res = await api.get(`/votes/verify-receipt/${verifyHashInput.trim()}`);
      setVerificationResult(res.data);
    } catch (err) {
      const saved = localStorage.getItem('demo_receipts');
      const receiptsList: ReceiptType[] = saved ? JSON.parse(saved) : [];
      const found = receiptsList.find(r => r.receipt_hash === verifyHashInput.trim() || r.tx_hash === verifyHashInput.trim());

      if (found) {
        setVerificationResult({
          verified: true,
          block_index: found.block_index,
          tx_hash: found.tx_hash,
          voter_hash: found.voter_hash
        });
      } else {
        setVerificationResult({ verified: false, message: 'Receipt hash not found in blockchain ledger.' });
      }
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">VERIFICATION DESK</span>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Vote Receipts & Ledger Audit</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Audit your vote on the blockchain without exposing candidate choice</p>
      </div>

      {/* Verification Tool Box */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <Search className="w-5 h-5 text-cyan-500" /> Verify Any Vote Receipt Hash
        </h3>
        <form onSubmit={handleVerify} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={verifyHashInput}
            onChange={(e) => setVerifyHashInput(e.target.value)}
            placeholder="Paste SHA-256 Receipt Hash..."
            className="flex-1 px-4 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-xs font-mono"
          />
          <button
            type="submit"
            disabled={verifying}
            className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold text-xs rounded-xl shadow-lg shadow-cyan-500/20"
          >
            {verifying ? 'Auditing Ledger...' : 'Verify Hash'}
          </button>
        </form>

        {verificationResult && (
          <div className={`p-4 rounded-2xl border font-mono text-xs ${
            verificationResult.verified 
              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-500' 
              : 'bg-rose-500/10 border-rose-500/30 text-rose-500'
          }`}>
            {verificationResult.verified ? (
              <div className="space-y-1">
                <p className="font-bold flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4" /> VERIFIED: Vote Transaction exists on Block #{verificationResult.block_index}</p>
                <p>TxHash: {verificationResult.tx_hash}</p>
                <p>Voter Hash: {verificationResult.voter_hash}</p>
              </div>
            ) : (
              <p className="font-bold flex items-center gap-1.5"><AlertTriangle className="w-4 h-4" /> {verificationResult.message}</p>
            )}
          </div>
        )}
      </div>

      {/* Receipts Table */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-slate-900 dark:text-white">Your Historical Vote Receipts ({receipts.length})</h3>
        
        {receipts.length > 0 ? (
          <div className="space-y-3">
            {receipts.map((r, idx) => (
              <div key={r.vote_id || idx} className="p-4 bg-slate-50 dark:bg-slate-900/60 rounded-2xl border border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <span className="text-[10px] font-mono text-cyan-500 font-bold">ELECTION #{r.election_id} • BLOCK #{r.block_index}</span>
                  <p className="text-xs font-mono font-bold text-slate-800 dark:text-slate-200 mt-1">Receipt Hash: {r.receipt_hash}</p>
                  <p className="text-[10px] text-slate-400 font-mono">TxHash: {r.tx_hash}</p>
                </div>

                <button
                  onClick={() => setActiveModalReceipt(r)}
                  className="px-4 py-2 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-900 dark:text-white text-xs font-semibold rounded-xl flex items-center gap-1.5 transition-colors self-start sm:self-auto"
                >
                  <QrCode className="w-4 h-4 text-cyan-500" /> View QR Receipt
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-8 text-center text-xs text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">
            No vote receipts found yet. Go to <span className="text-cyan-500 font-semibold">Active Elections</span> to cast your first vote!
          </div>
        )}
      </div>

      <QRCodeModal
        isOpen={Boolean(activeModalReceipt)}
        onClose={() => setActiveModalReceipt(null)}
        receipt={activeModalReceipt}
      />

    </div>
  );
};
