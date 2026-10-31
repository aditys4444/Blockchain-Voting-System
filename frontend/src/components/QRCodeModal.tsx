import React, { useState } from 'react';
import { X, ShieldCheck, Download, Copy, Check, Lock } from 'lucide-react';

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
  const [copied, setCopied] = useState(false);

  if (!isOpen || !receipt) return null;

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-none">
      <div className="relative w-full max-w-md p-6 civic-card shadow-2xl">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="text-center mb-5">
          <div className="w-12 h-12 mx-auto rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 dark:text-emerald-400 mb-2">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
            Official Cryptographic Receipt
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 font-mono mt-0.5">
            BLOCKCHAIN PROOF OF BALLOT • BLOCK #{receipt.block_index}
          </p>
        </div>

        {/* Simulated SVG QR Code */}
        <div className="flex flex-col items-center justify-center p-5 bg-slate-50 dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 mb-5">
          <svg className="w-40 h-40 text-slate-900 dark:text-slate-100" viewBox="0 0 100 100" fill="currentColor">
            <rect width="100" height="100" fill="none" />
            <path d="M0,0 h30 v30 h-30 z M10,10 h10 v10 h-10 z" />
            <path d="M70,0 h30 v30 h-30 z M80,10 h10 v10 h-10 z" />
            <path d="M0,70 h30 v30 h-30 z M10,80 h10 v10 h-10 z" />
            <rect x="40" y="40" width="20" height="20" className="text-blue-600" />
            <rect x="35" y="10" width="10" height="15" />
            <rect x="55" y="15" width="10" height="10" />
            <rect x="10" y="45" width="15" height="10" />
            <rect x="75" y="45" width="15" height="20" />
            <rect x="45" y="75" width="20" height="15" />
          </svg>
          <span className="text-[11px] font-mono text-slate-600 dark:text-slate-400 font-semibold mt-2.5">
            SHA-256: {receipt.receipt_hash.substring(0, 16)}...
          </span>
        </div>

        {/* Details Grid */}
        <div className="space-y-2 font-mono text-xs mb-5">
          <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <span className="text-slate-500">Transaction Hash:</span>
            <div className="flex items-center gap-1.5">
              <span className="font-semibold text-slate-800 dark:text-slate-200">
                {receipt.tx_hash.substring(0, 12)}...
              </span>
              <button 
                onClick={() => copyToClipboard(receipt.tx_hash)} 
                className="p-1 text-slate-400 hover:text-blue-600"
                title="Copy full hash"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
            </div>
          </div>

          <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <span className="text-slate-500">Block Height:</span>
            <span className="font-bold text-blue-600 dark:text-blue-400">Block #{receipt.block_index}</span>
          </div>

          <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <span className="text-slate-500">Voter Key Hash:</span>
            <span className="text-slate-700 dark:text-slate-300">{receipt.voter_hash.substring(0, 12)}...</span>
          </div>
        </div>

        {/* Ballot Secrecy Guarantee */}
        <div className="text-[11px] font-mono text-slate-400 mb-4 flex items-center gap-1.5">
          <Lock className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <span>Ballot choice is cryptographically encrypted and hidden from this receipt.</span>
        </div>

        {/* Print Button */}
        <button
          onClick={() => window.print()}
          className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm flex items-center justify-center gap-2 transition-colors"
        >
          <Download className="w-4 h-4" />
          <span>Print / Save Cryptographic Receipt</span>
        </button>

      </div>
    </div>
  );
};
