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
  Wallet,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  RefreshCw,
  Lock,
  Cpu,
  UserCheck
} from 'lucide-react';

type WalletState = 'disconnected' | 'connecting' | 'connected' | 'wrong-network' | 'failed';

export const Login: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'sso' | 'wallet'>('sso');
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Web3 Wallet Simulation State
  const [walletState, setWalletState] = useState<WalletState>('disconnected');
  const [walletAddress] = useState('0x71C8392a5F92B30291912fAA79b4D32890C2392F');

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
      setError(err.response?.data?.detail || 'Invalid credentials. Use demo accounts below or check input.');
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
    }, 700);
  };

  const proceedWithConnectedWallet = () => {
    handleDirectLogin('voter1', 'Voter123!');
  };

  return (
    <div className="min-h-[82vh] flex flex-col justify-center py-6 px-4 sm:px-6 lg:px-8">
      
      {/* Main Login / Wallet Card */}
      <div className="max-w-lg w-full mx-auto civic-card overflow-hidden">
        
        {/* Civic Header */}
        <div className="bg-slate-50 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-800 px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-slate-900 dark:bg-blue-600 flex items-center justify-center text-white shrink-0">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-base font-bold text-slate-900 dark:text-slate-100 tracking-tight leading-tight">
                University Election Portal
              </h1>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-mono mt-0.5">
                SECURE IDENTITY AUTHENTICATION &amp; BALLOT ACCESS
              </p>
            </div>
          </div>
        </div>

        {/* Tab Selector: Institutional SSO vs Web3 Wallet */}
        <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-800 bg-slate-100/60 dark:bg-slate-950/60 text-xs font-semibold">
          <button
            type="button"
            onClick={() => setActiveTab('sso')}
            className={`py-3 px-4 flex items-center justify-center gap-2 border-b-2 transition-colors ${
              activeTab === 'sso'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-white dark:bg-slate-900 font-bold'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
            }`}
          >
            <Mail className="w-4 h-4" />
            <span>Campus ID / Email</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('wallet')}
            className={`py-3 px-4 flex items-center justify-center gap-2 border-b-2 transition-colors ${
              activeTab === 'wallet'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-white dark:bg-slate-900 font-bold'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
            }`}
          >
            <Wallet className="w-4 h-4" />
            <span>Web3 Wallet Key</span>
          </button>
        </div>

        {/* Card Body */}
        <div className="p-6 sm:p-7 space-y-6">

          {error && (
            <div className="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 rounded-lg text-rose-700 dark:text-rose-400 text-xs font-medium flex items-center gap-2">
              <XCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {activeTab === 'sso' ? (
            /* Institutional Credentials Form */
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Institutional Email or Username
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={usernameOrEmail}
                    onChange={(e) => setUsernameOrEmail(e.target.value)}
                    placeholder="voter1@voting.edu or admin"
                    className="w-full pl-9 pr-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
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
                    className="w-full pl-9 pr-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {loading ? 'Authenticating...' : 'Sign In with Credentials'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          ) : (
            /* Web3 Wallet Connection Portal */
            <div className="space-y-4">
              
              {/* Wallet State Simulator */}
              <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg text-xs space-y-2">
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
                <div className="p-5 border border-dashed border-slate-300 dark:border-slate-700 rounded-lg text-center space-y-3">
                  <div className="w-10 h-10 mx-auto rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-300">
                    <Wallet className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-slate-900 dark:text-slate-100">Wallet Disconnected</h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-xs mx-auto">
                      Connect your MetaMask or Hardware Key to sign voting transactions on PoW Testnet (Chain ID 1337).
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={connectWalletSimulation}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors inline-flex items-center gap-1.5"
                  >
                    <Wallet className="w-4 h-4" />
                    <span>Connect MetaMask</span>
                  </button>
                </div>
              )}

              {/* State 2: Connecting */}
              {walletState === 'connecting' && (
                <div className="p-5 border border-blue-200 dark:border-blue-900/60 bg-blue-50/40 dark:bg-blue-950/20 rounded-lg text-center space-y-3">
                  <RefreshCw className="w-6 h-6 mx-auto text-blue-600 dark:text-blue-400 animate-spin" />
                  <div>
                    <h3 className="text-xs font-bold text-blue-900 dark:text-blue-200">Awaiting Signature</h3>
                    <p className="text-xs text-blue-700/80 dark:text-blue-300/80 mt-1 font-mono">
                      Requesting eth_requestAccounts authorization...
                    </p>
                  </div>
                </div>
              )}

              {/* State 3: Connected */}
              {walletState === 'connected' && (
                <div className="p-4 border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/40 dark:bg-emerald-950/20 rounded-lg space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5 text-emerald-700 dark:text-emerald-300 text-xs font-bold">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Wallet Verified &amp; Whitelisted</span>
                    </div>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-200 border border-emerald-300/50">
                      Eligible Voter
                    </span>
                  </div>
                  <div className="p-2.5 bg-white dark:bg-slate-900 rounded border border-emerald-200 dark:border-emerald-800/60 font-mono text-xs space-y-1">
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
                    className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors flex items-center justify-center gap-1.5"
                  >
                    <span>Proceed to Active Ballot</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              )}

              {/* State 4: Wrong Network */}
              {walletState === 'wrong-network' && (
                <div className="p-4 border border-amber-200 dark:border-amber-900/60 bg-amber-50/50 dark:bg-amber-950/20 rounded-lg space-y-2">
                  <div className="flex items-center gap-1.5 text-amber-700 dark:text-amber-300 text-xs font-bold">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Wrong Network (Chain ID 1 - Ethereum Mainnet)</span>
                  </div>
                  <p className="text-xs text-amber-800 dark:text-amber-200">
                    CivicVote operates on PoW Testnet (Chain ID 1337). Switch network to authorize transactions.
                  </p>
                  <button
                    type="button"
                    onClick={() => setWalletState('connected')}
                    className="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs rounded-lg transition-colors inline-flex items-center gap-1.5"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>Switch to PoW Testnet (1337)</span>
                  </button>
                </div>
              )}

              {/* State 5: Failed */}
              {walletState === 'failed' && (
                <div className="p-4 border border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/20 rounded-lg space-y-2">
                  <div className="flex items-center gap-1.5 text-rose-700 dark:text-rose-400 text-xs font-bold">
                    <XCircle className="w-4 h-4" />
                    <span>Connection Request Denied</span>
                  </div>
                  <p className="text-xs text-rose-800 dark:text-rose-300">
                    The signature request was declined or timed out.
                  </p>
                  <div className="flex items-center gap-2 pt-1">
                    <button
                      type="button"
                      onClick={connectWalletSimulation}
                      className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-semibold text-xs rounded-lg transition-colors"
                    >
                      Retry Connection
                    </button>
                    <button
                      type="button"
                      onClick={() => setActiveTab('sso')}
                      className="px-3 py-1.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-semibold text-xs rounded-lg hover:bg-slate-50 transition-colors"
                    >
                      Use Campus Password
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
                <UserCheck className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                <span>DEMO CREDENTIALS:</span>
              </span>
              <span>1-CLICK SIGN IN</span>
            </div>

            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => handleDirectLogin('admin', 'Admin123!')}
                className="p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-left"
              >
                <div className="font-bold text-xs text-slate-900 dark:text-slate-100">
                  Administrator
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">admin / Admin123!</div>
              </button>

              <button
                type="button"
                onClick={() => handleDirectLogin('voter1', 'Voter123!')}
                className="p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-left"
              >
                <div className="font-bold text-xs text-slate-900 dark:text-slate-100">
                  Student Voter
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">voter1 / Voter123!</div>
              </button>

              <button
                type="button"
                onClick={() => handleDirectLogin('observer1', 'Observer123!')}
                className="p-2.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-left"
              >
                <div className="font-bold text-xs text-slate-900 dark:text-slate-100">
                  Public Observer
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">observer1 / Obs123!</div>
              </button>
            </div>
          </div>

          {/* Registration Link */}
          <div className="text-center pt-1">
            <p className="text-xs text-slate-500 dark:text-slate-400">
              New campus voter?{' '}
              <Link to="/register" className="text-blue-600 dark:text-blue-400 font-semibold hover:underline">
                Register voter identity &amp; keypair
              </Link>
            </p>
          </div>

        </div>

        {/* Security & Ledger Disclaimer */}
        <div className="bg-slate-50 dark:bg-slate-950/80 border-t border-slate-200 dark:border-slate-800 px-6 py-3 flex flex-wrap items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 gap-2 font-mono">
          <div className="flex items-center gap-1.5">
            <Lock className="w-3.5 h-3.5 text-slate-400" />
            <span>Ballot Secrecy: Selections encrypted</span>
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
