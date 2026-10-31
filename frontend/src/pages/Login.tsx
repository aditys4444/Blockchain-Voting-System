import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { UserRole } from '../types';
import {
  Shield,
  KeyRound,
  Mail,
  ArrowRight,
  Sparkles,
  Wallet,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  RefreshCw,
  ExternalLink,
  Layers,
  Lock,
  Cpu
} from 'lucide-react';

type WalletState = 'disconnected' | 'connecting' | 'connected' | 'wrong-network' | 'failed';

export const Login: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'sso' | 'wallet'>('sso');
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Web3 Wallet Simulation State (Screen 1 Spec)
  const [walletState, setWalletState] = useState<WalletState>('disconnected');
  const [walletAddress, setWalletAddress] = useState('0x71C8392a5F92B30291912fAA79b4D32890C2392F');

  const { login } = useAuth();
  const navigate = useNavigate();

  const checkDemoCredentials = (u: string, p: string) => {
    const cred = u.toLowerCase().trim();
    const pwd = p.trim();
    const now = new Date().toISOString();

    if (
      (cred === 'admin' || cred === 'admin_edu' || cred === 'admin@voting.edu' || cred === 'admin@blockchainvoting.org') &&
      (pwd === 'admin123' || pwd === 'Admin123!')
    ) {
      return { id: 1, email: 'admin@voting.edu', username: 'admin', role: 'admin' as UserRole, is_active: true, created_at: now };
    }
    if (
      (cred === 'voter1' || cred === 'voter_edu' || cred === 'voter1@voting.edu' || cred === 'voter@blockchainvoting.org') &&
      (pwd === 'voter123' || pwd === 'Voter123!')
    ) {
      return { id: 2, email: 'voter1@voting.edu', username: 'voter1', role: 'voter' as UserRole, is_active: true, created_at: now };
    }
    if (
      (cred === 'observer1' || cred === 'observer_edu' || cred === 'observer@voting.edu' || cred === 'observer@blockchainvoting.org') &&
      (pwd === 'observer123' || pwd === 'Observer123!')
    ) {
      return { id: 3, email: 'observer@voting.edu', username: 'observer1', role: 'observer' as UserRole, is_active: true, created_at: now };
    }

    try {
      const saved = localStorage.getItem('demo_registered_users');
      if (saved) {
        const registeredList = JSON.parse(saved);
        const match = registeredList.find(
          (usr: any) =>
            (usr.email.toLowerCase() === cred || usr.username.toLowerCase() === cred) && usr.password === pwd
        );
        if (match) {
          return {
            id: match.id,
            email: match.email,
            username: match.username,
            role: match.role as UserRole,
            is_active: true,
            created_at: match.created_at || now
          };
        }
      }
    } catch (e) {}

    return null;
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await api.post('/auth/login', {
        username_or_email: usernameOrEmail,
        password,
      });

      const { access_token, user } = res.data;
      login(access_token, user);

      if (user.role === 'admin') navigate('/admin');
      else if (user.role === 'voter') navigate('/voter');
      else navigate('/observer');
    } catch (err: any) {
      const demoUser = checkDemoCredentials(usernameOrEmail, password);
      if (demoUser) {
        login(`demo-${demoUser.role}-token`, demoUser);
        if (demoUser.role === 'admin') navigate('/admin');
        else if (demoUser.role === 'voter') navigate('/voter');
        else navigate('/observer');
        return;
      }
      setError(err.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleDirectLogin = async (u: string, p: string) => {
    setUsernameOrEmail(u);
    setPassword(p);
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/auth/login', {
        username_or_email: u,
        password: p,
      });
      const { access_token, user } = res.data;
      login(access_token, user);
      if (user.role === 'admin') navigate('/admin');
      else if (user.role === 'voter') navigate('/voter');
      else navigate('/observer');
    } catch (err: any) {
      const demoUser = checkDemoCredentials(u, p);
      if (demoUser) {
        login(`demo-${demoUser.role}-token`, demoUser);
        if (demoUser.role === 'admin') navigate('/admin');
        else if (demoUser.role === 'voter') navigate('/voter');
        else navigate('/observer');
        return;
      }
      setError(err.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const connectWalletSimulation = () => {
    setWalletState('connecting');
    setTimeout(() => {
      setWalletState('connected');
    }, 900);
  };

  const proceedWithConnectedWallet = () => {
    handleDirectLogin('voter1', 'Voter123!');
  };

  return (
    <div className="min-h-[88vh] flex flex-col justify-center py-6 px-4 sm:px-6 lg:px-8">
      
      {/* Top Banner: Civic Redesign Showcase Notice */}
      <div className="max-w-xl w-full mx-auto mb-6">
        <a
          href="/stitch_redesign/index.html"
          className="flex items-center justify-between p-4 rounded-xl bg-slate-900 border border-slate-700/80 hover:border-blue-500/80 text-white shadow-xl transition-all group"
        >
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white shrink-0 font-bold">
              <Layers className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-sm text-slate-100 group-hover:text-blue-300 transition-colors">
                  CivicVote Redesign Suite (8 Screens)
                </span>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-400/30">
                  Interactive
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Voter Dashboard, Ballot, Cryptographic Receipt, Admin &amp; Mobile
              </p>
            </div>
          </div>
          <ArrowRight className="w-5 h-5 text-blue-400 group-hover:translate-x-1 transition-transform shrink-0" />
        </a>
      </div>

      {/* Main Login / Wallet Card */}
      <div className="max-w-xl w-full mx-auto bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden">
        
        {/* Civic Header Bar */}
        <div className="bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-slate-900 dark:bg-slate-100 flex items-center justify-center text-white dark:text-slate-900 shadow-sm">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base font-bold text-slate-900 dark:text-slate-100 tracking-tight leading-tight">
                CivicVote Portal
              </h1>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                COLLEGE DEMO • SECP256R1 CRYPTOGRAPHIC LEDGER
              </p>
            </div>
          </div>
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800/80 text-emerald-700 dark:text-emerald-300 text-xs font-mono font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>Chain ID: 1337</span>
          </div>
        </div>

        {/* Tab Selector: Institutional SSO vs Web3 Wallet */}
        <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-800 bg-slate-100/60 dark:bg-slate-950/40 text-xs font-semibold">
          <button
            type="button"
            onClick={() => setActiveTab('sso')}
            className={`py-3 px-4 flex items-center justify-center gap-2 border-b-2 transition-colors ${
              activeTab === 'sso'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-white dark:bg-slate-900'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200'
            }`}
          >
            <Mail className="w-4 h-4" />
            <span>Institutional SSO / Email</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('wallet')}
            className={`py-3 px-4 flex items-center justify-center gap-2 border-b-2 transition-colors ${
              activeTab === 'wallet'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-white dark:bg-slate-900'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200'
            }`}
          >
            <Wallet className="w-4 h-4" />
            <span>Web3 Wallet Connection</span>
          </button>
        </div>

        {/* Card Body */}
        <div className="p-6 sm:p-8 space-y-6">

          {error && (
            <div className="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 rounded-xl text-rose-700 dark:text-rose-400 text-xs font-medium flex items-center gap-2">
              <XCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {activeTab === 'sso' ? (
            /* Institutional SSO & Password Form */
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  University Email or Username
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={usernameOrEmail}
                    onChange={(e) => setUsernameOrEmail(e.target.value)}
                    placeholder="voter1@voting.edu or admin"
                    className="w-full pl-9 pr-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Password
                </label>
                <div className="relative">
                  <KeyRound className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-9 pr-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 bg-slate-900 hover:bg-slate-800 dark:bg-blue-600 dark:hover:bg-blue-500 text-white font-semibold text-sm rounded-xl shadow-md transition-all disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {loading ? 'Authenticating...' : 'Sign In with Credentials'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          ) : (
            /* Web3 Wallet Connection Portal (Screen 1 Specification) */
            <div className="space-y-5">
              
              {/* Wallet State Selector / Evaluator Tool */}
              <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs space-y-2">
                <div className="flex items-center justify-between text-slate-600 dark:text-slate-400 font-mono text-[11px]">
                  <span>SIMULATE WALLET STATE:</span>
                  <span className="uppercase font-bold text-blue-600 dark:text-blue-400">{walletState}</span>
                </div>
                <div className="grid grid-cols-5 gap-1 text-[10px] font-mono">
                  {(['disconnected', 'connecting', 'connected', 'wrong-network', 'failed'] as WalletState[]).map((st) => (
                    <button
                      key={st}
                      type="button"
                      onClick={() => setWalletState(st)}
                      className={`px-1.5 py-1 rounded border capitalize transition-colors ${
                        walletState === st
                          ? 'bg-blue-600 text-white border-blue-600 font-bold'
                          : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-800'
                      }`}
                    >
                      {st === 'wrong-network' ? 'Wrong Net' : st}
                    </button>
                  ))}
                </div>
              </div>

              {/* State 1: Disconnected */}
              {walletState === 'disconnected' && (
                <div className="p-5 border border-dashed border-slate-300 dark:border-slate-700 rounded-xl text-center space-y-3">
                  <div className="w-12 h-12 mx-auto rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-300">
                    <Wallet className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Wallet Disconnected</h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto">
                      Connect your MetaMask, Coinbase Wallet, or Hardware Key to sign voting transactions on PoW Testnet.
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={connectWalletSimulation}
                    className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs rounded-xl shadow-md transition-all inline-flex items-center gap-2"
                  >
                    <Wallet className="w-4 h-4" />
                    <span>Connect MetaMask / Web3 Key</span>
                  </button>
                </div>
              )}

              {/* State 2: Connecting */}
              {walletState === 'connecting' && (
                <div className="p-5 border border-blue-200 dark:border-blue-900/60 bg-blue-50/50 dark:bg-blue-950/20 rounded-xl text-center space-y-3">
                  <RefreshCw className="w-8 h-8 mx-auto text-blue-600 dark:text-blue-400 animate-spin" />
                  <div>
                    <h3 className="text-sm font-bold text-blue-900 dark:text-blue-200">Requesting Wallet Signature</h3>
                    <p className="text-xs text-blue-700/80 dark:text-blue-300/80 mt-1 font-mono">
                      Awaiting user authorization for eth_requestAccounts...
                    </p>
                  </div>
                </div>
              )}

              {/* State 3: Connected */}
              {walletState === 'connected' && (
                <div className="p-5 border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/40 dark:bg-emerald-950/20 rounded-xl space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-300 text-xs font-bold">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Wallet Authorized &amp; Verified</span>
                    </div>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-200 border border-emerald-300/50">
                      Eligible Voter
                    </span>
                  </div>
                  <div className="p-2.5 bg-white dark:bg-slate-900 rounded-lg border border-emerald-200 dark:border-emerald-800/60 font-mono text-xs space-y-1">
                    <div className="text-slate-500 dark:text-slate-400 text-[10px]">ECDSA PUBLIC ADDRESS:</div>
                    <div className="font-bold text-slate-800 dark:text-slate-200 truncate">{walletAddress}</div>
                    <div className="text-[11px] text-slate-500 dark:text-slate-400 flex items-center justify-between pt-1">
                      <span>Network: PoW Testnet (1337)</span>
                      <span>Gas Sponsoring: Active</span>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={proceedWithConnectedWallet}
                    className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs rounded-xl shadow-md transition-all flex items-center justify-center gap-2"
                  >
                    <span>Proceed to Voter Ballot Dashboard</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              )}

              {/* State 4: Wrong Network */}
              {walletState === 'wrong-network' && (
                <div className="p-5 border border-amber-200 dark:border-amber-900/60 bg-amber-50/50 dark:bg-amber-950/20 rounded-xl space-y-3">
                  <div className="flex items-center gap-2 text-amber-700 dark:text-amber-300 text-xs font-bold">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Wrong Network Detected (Chain ID: 1 - Ethereum Mainnet)</span>
                  </div>
                  <p className="text-xs text-amber-800 dark:text-amber-200">
                    CivicVote elections run on PoW Testnet (Chain ID 1337). Your wallet must switch networks to sign transactions.
                  </p>
                  <button
                    type="button"
                    onClick={() => setWalletState('connected')}
                    className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs rounded-xl shadow transition-all inline-flex items-center gap-2"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>Switch to PoW Testnet (1337)</span>
                  </button>
                </div>
              )}

              {/* State 5: Connection Failed */}
              {walletState === 'failed' && (
                <div className="p-5 border border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/20 rounded-xl space-y-3">
                  <div className="flex items-center gap-2 text-rose-700 dark:text-rose-400 text-xs font-bold">
                    <XCircle className="w-4 h-4" />
                    <span>Connection Request Rejected</span>
                  </div>
                  <p className="text-xs text-rose-800 dark:text-rose-300">
                    The signature request was declined in MetaMask or the session timed out. Check your wallet extension and retry.
                  </p>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={connectWalletSimulation}
                      className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs rounded-xl shadow transition-all inline-flex items-center gap-2"
                    >
                      <RefreshCw className="w-3.5 h-3.5" />
                      <span>Retry Connection</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => setActiveTab('sso')}
                      className="px-4 py-2 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-semibold text-xs rounded-xl hover:bg-slate-50 transition-all"
                    >
                      Use SSO Password Instead
                    </button>
                  </div>
                </div>
              )}

            </div>
          )}

          {/* Quick Demo Credentials Footer */}
          <div className="pt-4 border-t border-slate-200 dark:border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400">
              <span className="flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-blue-500" />
                <span>INSTANT DEMO CREDENTIALS:</span>
              </span>
              <span>1-CLICK SIGN IN</span>
            </div>

            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => handleDirectLogin('admin', 'Admin123!')}
                className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-colors text-left group"
              >
                <div className="font-bold text-xs text-slate-900 dark:text-slate-100 group-hover:text-blue-600">
                  Administrator
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">admin / Admin123!</div>
              </button>

              <button
                type="button"
                onClick={() => handleDirectLogin('voter1', 'Voter123!')}
                className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-colors text-left group"
              >
                <div className="font-bold text-xs text-slate-900 dark:text-slate-100 group-hover:text-emerald-600">
                  Student Voter
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">voter1 / Voter123!</div>
              </button>

              <button
                type="button"
                onClick={() => handleDirectLogin('observer1', 'Observer123!')}
                className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-colors text-left group"
              >
                <div className="font-bold text-xs text-slate-900 dark:text-slate-100 group-hover:text-cyan-600">
                  Public Observer
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">observer1 / Obs123!</div>
              </button>
            </div>
          </div>

          {/* Registration Link */}
          <div className="text-center pt-2">
            <p className="text-xs text-slate-500 dark:text-slate-400">
              New college voter?{' '}
              <Link to="/register" className="text-blue-600 dark:text-blue-400 font-semibold hover:underline">
                Register voter identity &amp; keypair
              </Link>
            </p>
          </div>

        </div>

        {/* Security & Ledger Disclaimer */}
        <div className="bg-slate-50 dark:bg-slate-950/60 border-t border-slate-200 dark:border-slate-800 px-6 py-3 flex flex-wrap items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 gap-2 font-mono">
          <div className="flex items-center gap-1.5">
            <Lock className="w-3.5 h-3.5 text-slate-400" />
            <span>Ballot Secrecy Guarantee: Selection hidden on receipts</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-slate-400" />
            <span>Double-Vote Prevention: Unique Key Constraint</span>
          </div>
        </div>

      </div>

    </div>
  );
};
