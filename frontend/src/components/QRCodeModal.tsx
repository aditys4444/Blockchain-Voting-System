import React from 'react';
import { X, CheckCircle, ShieldCheck, Download, Copy } from 'lucide-react';

interface QRCodeModalProps {
  isOpen: boolean;
  onClose: () => void;
  receipt: {
    tx_hash: string;
    block_index: number;
    receipt_hash: string;
    voter_hash: string;
    election_id: number;
    created_at?: string;
  } | null;
}

export const QRCodeModal: React.FC<QRCodeModalProps> = ({ isOpen, onClose, receipt }) => {
  if (!isOpen || !receipt) return null;

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied hash to clipboard!');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-md p-6 glass-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-flex p-3 bg-emerald-500/10 text-emerald-500 rounded-2xl mb-3">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white">Cryptographic Receipt</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-mono">
            BLOCKCHAIN PROOF OF VOTE #B{receipt.block_index}
          </p>
        </div>

        {/* Simulated SVG QR Code */}
        <div className="flex flex-col items-center justify-center p-6 bg-slate-50 dark:bg-slate-950 rounded-2xl border border-slate-200 dark:border-slate-800 mb-6">
          <svg className="w-44 h-44 text-slate-900 dark:text-slate-100" viewBox="0 0 100 100" fill="currentColor">
            <rect width="100" height="100" fill="none" />
            <path d="M0,0 h30 v30 h-30 z M10,10 h10 v10 h-10 z" />
            <path d="M70,0 h30 v30 h-30 z M80,10 h10 v10 h-10 z" />
            <path d="M0,70 h30 v30 h-30 z M10,80 h10 v10 h-10 z" />
            <rect x="40" y="40" width="20" height="20" className="text-cyan-500" />
            <rect x="35" y="10" width="10" height="15" />
            <rect x="55" y="15" width="10" height="10" />
            <rect x="10" y="45" width="15" height="10" />
            <rect x="75" y="45" width="15" height="20" />
            <rect x="45" y="75" width="20" height="15" />
          </svg>
          <span className="text-[11px] font-mono text-cyan-600 dark:text-cyan-400 font-semibold mt-3">
            SHA256 • {receipt.receipt_hash.substring(0, 16)}...
          </span>
        </div>

        {/* Details Grid */}
        <div className="space-y-3 font-mono text-xs mb-6">
          <div className="p-2.5 bg-slate-100 dark:bg-slate-800/60 rounded-xl flex items-center justify-between">
            <span className="text-slate-500">Transaction Hash:</span>
            <div className="flex items-center gap-1">
              <span className="font-semibold text-slate-700 dark:text-slate-300">
                {receipt.tx_hash.substring(0, 12)}...
              </span>
              <button onClick={() => copyToClipboard(receipt.tx_hash)} className="text-slate-400 hover:text-cyan-500">
                <Copy className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <div className="p-2.5 bg-slate-100 dark:bg-slate-800/60 rounded-xl flex items-center justify-between">
            <span className="text-slate-500">Block Index:</span>
            <span className="font-bold text-cyan-600 dark:text-cyan-400">#{receipt.block_index}</span>
          </div>

          <div className="p-2.5 bg-slate-100 dark:bg-slate-800/60 rounded-xl flex items-center justify-between">
            <span className="text-slate-500">Voter Hash:</span>
            <span className="text-slate-700 dark:text-slate-300">{receipt.voter_hash.substring(0, 12)}...</span>
          </div>
        </div>

        {/* Download Button */}
        <button
          onClick={() => window.print()}
          className="w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold rounded-2xl shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition-all"
        >
          <Download className="w-4 h-4" />
          Download / Print Receipt
        </button>

      </div>
    </div>
  );
};
