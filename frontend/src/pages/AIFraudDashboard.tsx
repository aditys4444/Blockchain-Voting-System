import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { FraudAnalysis, Election } from '../types';
import { ShieldAlert, Cpu, AlertTriangle, CheckCircle, Zap } from 'lucide-react';

export const AIFraudDashboard: React.FC = () => {
  const [elections, setElections] = useState<Election[]>([]);
  const [selectedElectionId, setSelectedElectionId] = useState<number | null>(null);
  const [fraudData, setFraudData] = useState<FraudAnalysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/elections').then(res => {
      setElections(res.data);
      if (res.data.length > 0) setSelectedElectionId(res.data[0].id);
    });
  }, []);

  const analyzeElection = async (id: number) => {
    setLoading(true);
    try {
      const res = await api.get(`/ai/fraud-analysis/${id}`);
      setFraudData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedElectionId) {
      analyzeElection(selectedElectionId);
    }
  }, [selectedElectionId]);

  return (
    <div className="space-y-8">
      
      {/* Top Banner */}
      <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800">
        <span className="text-xs font-mono text-cyan-500 uppercase tracking-widest font-semibold">AI BONUS MODULE</span>
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">AI Fraud Radar & Anomaly Prediction</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Machine learning engine analyzing vote velocity, duplicate IP vectors, and timing anomalies</p>
      </div>

      {/* Select Election Tabs */}
      <div className="flex flex-wrap gap-2">
        {elections.map((ele) => (
          <button
            key={ele.id}
            onClick={() => setSelectedElectionId(ele.id)}
            className={`px-4 py-2 rounded-xl text-xs font-bold font-mono transition-all ${
              selectedElectionId === ele.id
                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-lg shadow-cyan-500/20'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'
            }`}
          >
            Election #{ele.id}
          </button>
        ))}
      </div>

      {fraudData && (
        <div className="space-y-6">
          
          {/* Main Risk Score Card */}
          <div className="p-8 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-2 text-center md:text-left">
              <span className="text-xs font-mono text-slate-400 uppercase">SYNTHETIC RISK ASSESSMENT</span>
              <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white">
                Fraud Risk Index: <span className="text-cyan-500">{fraudData.fraud_risk_score}%</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Statistical Confidence Score computed via timing burst clustering & IP vector analysis
              </p>
            </div>

            <div className={`px-6 py-4 rounded-2xl border text-center font-mono font-extrabold uppercase ${
              fraudData.risk_level === 'Low' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-500' :
              fraudData.risk_level === 'Medium' ? 'bg-amber-500/10 border-amber-500/30 text-amber-500' :
              'bg-rose-500/10 border-rose-500/30 text-rose-500'
            }`}>
              <p className="text-[10px] text-slate-400">RISK LEVEL</p>
              <p className="text-2xl mt-0.5">{fraudData.risk_level}</p>
            </div>
          </div>

          {/* Anomaly Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Flagged Anomalies Box */}
            <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-500" /> Flagged Security Anomalies
              </h3>
              <div className="space-y-2">
                {fraudData.flagged_anomalies.map((anom, idx) => (
                  <div key={idx} className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl border border-slate-200 dark:border-slate-800 text-xs font-mono text-slate-700 dark:text-slate-300">
                    &bull; {anom}
                  </div>
                ))}
              </div>
            </div>

            {/* Velocity & Cluster Metrics */}
            <div className="p-6 glass-card rounded-3xl border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Zap className="w-5 h-5 text-cyan-500" /> Velocity & Cluster Signals
              </h3>
              <div className="space-y-3 font-mono text-xs">
                <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl flex justify-between">
                  <span className="text-slate-400">Total Analyzed Votes:</span>
                  <span className="font-bold text-slate-900 dark:text-white">{fraudData.details.total_votes}</span>
                </div>
                <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl flex justify-between">
                  <span className="text-slate-400">Rapid Burst Votes (&lt; 2s):</span>
                  <span className="font-bold text-cyan-500">{fraudData.details.rapid_burst_count}</span>
                </div>
                <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl flex justify-between">
                  <span className="text-slate-400">Suspicious Duplicate IPs:</span>
                  <span className="font-bold text-amber-500">{fraudData.details.duplicate_ip_count}</span>
                </div>
                <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl flex justify-between">
                  <span className="text-slate-400">Blocked Double-Vote Attempts:</span>
                  <span className="font-bold text-rose-500">{fraudData.details.double_voting_attempts}</span>
                </div>
              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  );
};
