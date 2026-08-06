import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Block, ChainStatus } from '../types';
import { Database, Search, ShieldCheck, Cpu, Key, Layers, RefreshCw } from 'lucide-react';

export const BlockchainExplorer: React.FC = () => {
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [status, setStatus] = useState<ChainStatus | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResult, setSearchResult] = useState<any>(null);
  const [auditResult, setAuditResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchBlockchainData = async () => {
    try {
      const [bRes, sRes] = await Promise.all([
        api.get('/blockchain/blocks'),
        api.get('/blockchain/status')
      ]);
      setBlocks(bRes.data);
      setStatus(sRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBlockchainData();
    const interval = setInterval(fetchBlockchainData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;
    try {
      const res = await api.get(`/blockchain/blocks/${searchTerm.trim()}`);
      setSearchResult(res.data);
    } catch (err) {
      try {
        const txRes = await api.get(`/blockchain/transactions/${searchTerm.trim()}`);
        setSearchResult(txRes.data);
      } catch (txErr) {
        setSearchResult({ error: 'Block or Transaction hash not found on ledger.' });
      }
    }
  };

  const runFullAudit = async () => {
    try {
      const res = await api.get('/blockchain/verify-chain');
      setAuditResult(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <div>
          <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">PUBLIC TRANSPARENCY</span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Blockchain Ledger Explorer</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Inspect blocks, verify Merkle root integrity, and audit digital signatures</p>
        </div>

        <button
          onClick={runFullAudit}
          className="px-4 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-emerald-500/20 transition-all"
        >
          <ShieldCheck className="w-4 h-4" /> Run Cryptographic Chain Audit
        </button>
      </div>

      {/* Chain Status Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 glass-card rounded-2xl border border-slate-200 dark:border-slate-800 flex items-center gap-3">
          <Layers className="w-8 h-8 text-cyan-500" />
          <div>
            <p className="text-[10px] font-mono uppercase text-slate-400">Total Blocks Mined</p>
            <h4 className="text-xl font-bold text-slate-900 dark:text-white">#{status?.total_blocks || 0}</h4>
          </div>
        </div>
        <div className="p-4 glass-card rounded-2xl border border-slate-200 dark:border-slate-800 flex items-center gap-3">
          <Cpu className="w-8 h-8 text-indigo-500" />
          <div>
            <p className="text-[10px] font-mono uppercase text-slate-400">Proof-of-Work Target</p>
            <h4 className="text-xl font-bold text-slate-900 dark:text-white">{status?.difficulty} Zero-Prefix Hash</h4>
          </div>
        </div>
        <div className="p-4 glass-card rounded-2xl border border-slate-200 dark:border-slate-800 flex items-center gap-3">
          <ShieldCheck className="w-8 h-8 text-emerald-500" />
          <div>
            <p className="text-[10px] font-mono uppercase text-slate-400">Ledger Integrity</p>
            <h4 className="text-xl font-bold text-emerald-500">{status?.is_valid ? '100% VALID' : 'ALERT'}</h4>
          </div>
        </div>
      </div>

      {/* Full Audit Result Banner */}
      {auditResult && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl font-mono text-xs text-emerald-500 space-y-1">
          <p className="font-bold">&gt; AUDIT PASSED: {auditResult.audit_details}</p>
          <p>Blocks Audited: #{auditResult.total_blocks_audited} • Verified Algorithms: {auditResult.crypto_algorithms.join(', ')}</p>
        </div>
      )}

      {/* Search Input Box */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-3">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white">Search Ledger by Block Index, Block Hash, or Transaction Hash</h3>
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Paste block index (e.g. 1) or SHA256 Hash..."
            className="flex-1 px-4 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-xs font-mono"
          />
          <button type="submit" className="px-6 py-2.5 bg-cyan-600 text-white rounded-xl text-xs font-semibold">
            Search Ledger
          </button>
        </form>

        {searchResult && (
          <div className="p-4 bg-slate-900 text-cyan-400 font-mono text-xs rounded-2xl overflow-x-auto">
            <pre>{JSON.stringify(searchResult, null, 2)}</pre>
          </div>
        )}
      </div>

      {/* Blocks List */}
      <div className="space-y-4">
        <h3 className="text-base font-bold text-slate-900 dark:text-white">Mined Block Ledger ({blocks.length})</h3>

        {blocks.map((block) => (
          <div key={block.index} className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 font-mono text-xs space-y-3">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3 gap-2">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-1 bg-cyan-500/10 text-cyan-500 font-bold rounded-lg border border-cyan-500/30">
                  BLOCK #{block.index}
                </span>
                <span className="text-slate-400 text-[10px]">
                  {new Date(block.timestamp * 1000).toLocaleString()}
                </span>
              </div>
              <span className="text-[10px] text-slate-500">Nonce: {block.nonce}</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
              <div>
                <span className="text-slate-400">Block Hash:</span>
                <p className="text-cyan-500 font-semibold truncate">{block.hash}</p>
              </div>
              <div>
                <span className="text-slate-400">Previous Hash:</span>
                <p className="text-slate-400 truncate">{block.previous_hash}</p>
              </div>
              <div>
                <span className="text-slate-400">Merkle Root:</span>
                <p className="text-emerald-500 font-semibold truncate">{block.merkle_root}</p>
              </div>
              <div>
                <span className="text-slate-400">ECDSA Block Signature:</span>
                <p className="text-slate-400 truncate">{block.signature || 'N/A'}</p>
              </div>
            </div>

            {/* Transactions */}
            <div className="pt-2">
              <span className="text-[10px] uppercase font-bold text-slate-400">Encrypted Transactions ({block.transactions.length})</span>
              <div className="mt-1 space-y-1">
                {block.transactions.map((tx: any, idx: number) => (
                  <div key={idx} className="p-2 bg-slate-50 dark:bg-slate-900/60 rounded-xl border border-slate-200 dark:border-slate-800 flex items-center justify-between text-[10px]">
                    <span className="text-cyan-500">Tx: {tx.tx_hash?.substring(0, 16)}...</span>
                    <span className="text-slate-400">Voter: {tx.voter_hash?.substring(0, 12)}...</span>
                    <span className="text-emerald-500">Encrypted Vote: {tx.encrypted_vote?.substring(0, 12)}...</span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
};
