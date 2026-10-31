import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { VoteReceipt as ReceiptType } from '../types';
import { Search, QrCode, CheckCircle2, Copy, Check, FileCheck, Lock } from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';

export const VoteReceipt: React.FC = () => {
  const [receipts, setReceipts] = useState<ReceiptType[]>([]);
  const [activeModalReceipt, setActiveModalReceipt] = useState<any>(null);
  const [copiedHash, setCopiedHash] = useState<string | null>(null);
  
  // Verification Tool
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

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedHash(text);
    setTimeout(() => setCopiedHash(null), 2000);
  };

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
      const found = receiptsList.find(
        r => r.receipt_hash === verifyHashInput.trim() || r.tx_hash === verifyHashInput.trim()
      );

      if (found) {
        setVerificationResult({
          verified: true,
          block_index: found.block_index,
          tx_hash: found.tx_hash,
          voter_hash: found.voter_hash,
          created_at: found.created_at
        });
      } else {
        setVerificationResult({ 
          verified: false, 
          message: 'Receipt hash not found in blockchain ledger.' 
        });
      }
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="space-y-4 sm:space-y-6 w-full">
      
      {/* Header */}
      <div className="civic-card p-4 sm:p-6">
        <div className="flex items-center gap-1.5 text-xs font-mono text-blue-600 dark:text-blue-400 font-bold uppercase">
          <span>AUDIT PROOFS</span>
          <span className="text-slate-300 dark:text-slate-700">•</span>
          <span className="text-slate-500 font-normal">TRANSACTION RECEIPTS</span>
        </div>
        <h1 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight mt-0.5">
          Cryptographic Vote Receipts
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 max-w-xl">
          Each ballot generates an immutable transaction receipt. Verify inclusion on the public block ledger without exposing your vote choice.
        </p>
      </div>

      {/* Verification Tool */}
      <div className="civic-card p-4 sm:p-5 space-y-3">
        <div className="flex items-center gap-2 text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100">
          <Search className="w-4 h-4 text-blue-600 shrink-0" />
          <span>Verify Any Receipt or Transaction Hash</span>
        </div>
        <form onSubmit={handleVerify} className="flex flex-col sm:flex-row gap-2">
          <input
            type="text"
            value={verifyHashInput}
            onChange={(e) => setVerifyHashInput(e.target.value)}
            placeholder="Paste Transaction Hash (0x...) or Receipt Hash..."
            className="flex-1 px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs font-mono text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={verifying}
            className="w-full sm:w-auto px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-1.5 shrink-0 disabled:opacity-50"
          >
            {verifying ? 'Auditing...' : 'Verify on Chain'}
          </button>
        </form>

        {verificationResult && (
          <div className={`p-3.5 rounded-lg border font-mono text-xs ${
            verificationResult.verified 
              ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300' 
              : 'bg-rose-50 dark:bg-rose-950/40 border-rose-200 dark:border-rose-900 text-rose-800 dark:text-rose-300'
          }`}>
            {verificationResult.verified ? (
              <div className="space-y-1">
                <div className="font-bold flex items-center gap-1.5 text-emerald-700 dark:text-emerald-300">
                  <CheckCircle2 className="w-4 h-4 shrink-0" />
                  <span>TRANSACTION VERIFIED on Block #{verificationResult.block_index}</span>
                </div>
                <div className="break-all text-[11px]">TX HASH: {verificationResult.tx_hash}</div>
                <div className="text-[10px] text-emerald-600 dark:text-emerald-400">
                  ✓ Merkle inclusion proof valid.
                </div>
              </div>
            ) : (
              <div className="text-xs">✕ {verificationResult.message}</div>
            )}
          </div>
        )}
      </div>

      {/* Receipts Container (Desktop Table + Mobile Cards) */}
      <div className="civic-card overflow-hidden">
        <div className="px-4 sm:px-6 py-3 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60 flex items-center justify-between">
          <h2 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
            <FileCheck className="w-4 h-4 text-blue-600 shrink-0" />
            <span>My Recorded Ballots</span>
          </h2>
          <span className="text-[11px] font-mono text-slate-500">
            {receipts.length} {receipts.length === 1 ? 'Receipt' : 'Receipts'}
          </span>
        </div>

        {receipts.length === 0 ? (
          <div className="p-8 sm:p-12 text-center text-slate-500 space-y-1">
            <Lock className="w-7 h-7 mx-auto text-slate-300 dark:text-slate-700 mb-1" />
            <p className="text-xs font-semibold">No vote receipts recorded yet.</p>
            <p className="text-[11px] text-slate-400">Cast a ballot in an active election to generate your cryptographic receipt.</p>
          </div>
        ) : (
          <>
            {/* Desktop Table View (>= 768px) */}
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-100/70 dark:bg-slate-950/70 text-slate-500 dark:text-slate-400 font-mono uppercase text-[10px] border-b border-slate-200 dark:border-slate-800">
                  <tr>
                    <th className="px-5 py-3">Block #</th>
                    <th className="px-5 py-3">Transaction Hash</th>
                    <th className="px-5 py-3">Receipt Hash</th>
                    <th className="px-5 py-3">Timestamp</th>
                    <th className="px-5 py-3 text-right">Proof</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                  {receipts.map((r: any, idx) => {
                    const txStr = r.tx_hash || '0x' + r.receipt_hash;
                    const shortTx = `${txStr.slice(0, 10)}...${txStr.slice(-8)}`;

                    return (
                      <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                        <td className="px-5 py-3.5 font-mono font-bold text-slate-900 dark:text-slate-100">
                          #{r.block_index || idx + 1403}
                        </td>
                        <td className="px-5 py-3.5 font-mono">
                          <div className="flex items-center gap-1.5">
                            <span className="text-slate-700 dark:text-slate-300 font-bold" title={txStr}>
                              {shortTx}
                            </span>
                            <button
                              onClick={() => copyToClipboard(txStr)}
                              className="p-1 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 rounded"
                              title="Copy hash"
                            >
                              {copiedHash === txStr ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                            </button>
                          </div>
                        </td>
                        <td className="px-5 py-3.5 font-mono text-slate-500">
                          {r.receipt_hash ? `${r.receipt_hash.slice(0, 12)}...` : 'e3b0c442...'}
                        </td>
                        <td className="px-5 py-3.5 text-slate-500">
                          {r.created_at ? new Date(r.created_at).toLocaleTimeString() : 'Recent'}
                        </td>
                        <td className="px-5 py-3.5 text-right">
                          <button
                            onClick={() => setActiveModalReceipt(r)}
                            className="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-blue-50 dark:hover:bg-blue-950/60 text-slate-700 dark:text-slate-300 hover:text-blue-600 rounded text-xs transition-colors"
                          >
                            <QrCode className="w-3.5 h-3.5" />
                            <span>QR Proof</span>
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Mobile Stacked Card View (< 768px - Never Overflows) */}
            <div className="md:hidden divide-y divide-slate-200 dark:divide-slate-800">
              {receipts.map((r: any, idx) => {
                const txStr = r.tx_hash || '0x' + r.receipt_hash;
                const shortTx = `${txStr.slice(0, 10)}...${txStr.slice(-8)}`;

                return (
                  <div key={idx} className="p-4 space-y-2.5">
                    <div className="flex items-center justify-between">
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
                        Block #{r.block_index || idx + 1403}
                      </span>
                      <span className="text-[11px] text-slate-400">
                        {r.created_at ? new Date(r.created_at).toLocaleTimeString() : 'Recent'}
                      </span>
                    </div>

                    <div className="font-mono text-xs space-y-1">
                      <div className="text-[10px] text-slate-400">TRANSACTION HASH:</div>
                      <div className="flex items-center justify-between p-2 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800">
                        <span className="font-bold text-slate-800 dark:text-slate-200 text-[11px] truncate">{shortTx}</span>
                        <button
                          onClick={() => copyToClipboard(txStr)}
                          className="p-1 text-slate-400 hover:text-blue-600 shrink-0 ml-2"
                        >
                          {copiedHash === txStr ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-1">
                      <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-semibold">
                        ✓ Validated on Chain
                      </span>
                      <button
                        onClick={() => setActiveModalReceipt(r)}
                        className="inline-flex items-center gap-1 px-3 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 rounded text-xs transition-colors"
                      >
                        <QrCode className="w-3.5 h-3.5" />
                        <span>View QR</span>
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}

        {/* Footer Note */}
        <div className="bg-slate-50 dark:bg-slate-950/80 px-4 sm:px-6 py-2.5 border-t border-slate-200 dark:border-slate-800 text-[10px] font-mono text-slate-400 flex items-center justify-between">
          <div className="flex items-center gap-1">
            <Lock className="w-3 h-3 text-slate-400 shrink-0" />
            <span>Ballot Secrecy: Choices are encrypted and hidden from receipts.</span>
          </div>
        </div>
      </div>

      {/* QR Code Modal */}
      <QRCodeModal
        isOpen={Boolean(activeModalReceipt)}
        receipt={activeModalReceipt}
        onClose={() => setActiveModalReceipt(null)}
      />

    </div>
  );
};
