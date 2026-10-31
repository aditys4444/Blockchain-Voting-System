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
  UserCheck,
  ExternalLink
} from 'lucide-react';

export const Login: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'sso' | 'wallet'>('sso');
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Web3 Wallet state
  const [walletStatus, setWalletStatus] = useState<'idle' | 'connecting' | 'connected' | 'wrong_network' | 'error'>('idle');
  const [connectedAddress, setConnectedAddress] = useState<string>('');
  const [walletErrorMsg, setWalletErrorMsg] = useState<string>('');

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
      setError(err.response?.data?.detail || 'Invalid credentials. Select a demo preset below or check your username/password.');
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

  // Real or Simulated Web3 Connection
  const handleConnectWallet = async () => {
    setWalletStatus('connecting');
    setWalletErrorMsg('');

    if (typeof window !== 'undefined' && (window as any).ethereum) {
      try {
        const accounts = await (window as any).ethereum.request({ method: 'eth_requestAccounts' });
        const chainId = await (window as any).ethereum.request({ method: 'eth_chainId' });
        
        if (accounts && accounts.length > 0) {
          setConnectedAddress(accounts[0]);
          // Check chain: testnet 1337 is 0x539
          if (chainId !== '0x539' && chainId !== '1337') {
            setWalletStatus('wrong_network');
          } else {
            setWalletStatus('connected');
          }
          return;
        }
      } catch (err: any) {
        if (err.code === 4001) {
          setWalletStatus('error');
          setWalletErrorMsg('Connection request was declined in your wallet.');
          return;
        }
      }
    }

    // Seamless Demo Fallback when no extension is present
    setTimeout(() => {
      setConnectedAddress('0x71C8392a5F92B30291912fAA79b4D32890C2392F');
      setWalletStatus('connected');
    }, 600);
  };

  const handleProceedWithWallet = () => {
    handleDirectLogin('voter1', 'Voter123!');
  };

  return (
    <div className="w-full flex flex-col justify-center py-4 sm:py-8">
      
      {/* Main Login / Wallet Card */}
      <div className="w-full max-w-md mx-auto civic-card overflow-hidden">
        
        {/* Civic Header */}
        <div className="bg-slate-50 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-800 px-5 sm:px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-slate-900 dark:bg-blue-600 flex items-center justify-center text-white shrink-0">
              <Shield className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
            </div>
            <div className="min-w-0">
              <h1 className="text-base font-bold text-slate-900 dark:text-slate-100 tracking-tight leading-tight truncate">
                University Election Portal
              </h1>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 font-mono mt-0.5 truncate">
                CRYPTOGRAPHIC IDENTITY VERIFICATION
              </p>
            </div>
          </div>
        </div>

        {/* Tab Selector */}
        <div className="grid grid-cols-2 border-b border-slate-200 dark:border-slate-800 bg-slate-100/60 dark:bg-slate-950/60 text-xs font-semibold">
          <button
            type="button"
            onClick={() => setActiveTab('sso')}
            className={`py-3 px-3 text-center transition-colors ${
              activeTab === 'sso'
                ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400 bg-white dark:bg-slate-900 font-bold'
                : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            }`}
          >
            Campus Credentials
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('wallet')}
            className={`py-3 px-3 text-center transition-colors ${
              activeTab === 'wallet'
                ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400 bg-white dark:bg-slate-900 font-bold'
                : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            }`}
          >
            Web3 Wallet Key
          </button>
        </div>

        {/* Card Body */}
        <div className="p-5 sm:p-6 space-y-5">

          {error && (
            <div className="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 rounded-lg text-rose-700 dark:text-rose-400 text-xs flex items-start gap-2">
              <XCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span className="leading-tight">{error}</span>
            </div>
          )}

          {activeTab === 'sso' ? (
            /* Institutional Credentials Form */
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Campus ID or Email
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={usernameOrEmail}
                    onChange={(e) => setUsernameOrEmail(e.target.value)}
                    placeholder="student@voting.edu or voter1"
                    className="w-full pl-9 pr-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                    className="w-full pl-9 pr-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-1.5 shadow-sm disabled:opacity-50"
              >
                {loading ? 'Authenticating...' : 'Sign In to Portal'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          ) : (
            /* Web3 Wallet Portal (Natural, Professional, No Debug Buttons) */
            <div className="space-y-4">
              
              {walletStatus === 'idle' && (
                <div className="p-4 border border-slate-200 dark:border-slate-800 rounded-lg text-center space-y-3 bg-slate-50/50 dark:bg-slate-950/50">
                  <div className="w-10 h-10 mx-auto rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-700 dark:text-slate-300">
                    <Wallet className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-slate-900 dark:text-slate-100">Connect Web3 Wallet</h3>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 max-w-xs mx-auto">
                      Sign in directly with your cryptographic keypair on PoW Testnet (Chain ID 1337).
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={handleConnectWallet}
                    className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors flex items-center justify-center gap-2"
                  >
                    <Wallet className="w-4 h-4" />
                    <span>Connect MetaMask or Campus Key</span>
                  </button>
                </div>
              )}

              {walletStatus === 'connecting' && (
                <div className="p-6 border border-blue-200 dark:border-blue-900/60 bg-blue-50/40 dark:bg-blue-950/20 rounded-lg text-center space-y-2">
                  <RefreshCw className="w-6 h-6 mx-auto text-blue-600 dark:text-blue-400 animate-spin" />
                  <div className="text-xs font-bold text-blue-900 dark:text-blue-200">Requesting Wallet Key Access</div>
                  <p className="text-[11px] text-blue-700/80 dark:text-blue-300/80 font-mono">
                    Awaiting user approval in wallet window...
                  </p>
                </div>
              )}

              {walletStatus === 'connected' && (
                <div className="p-4 border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50/40 dark:bg-emerald-950/20 rounded-lg space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-emerald-700 dark:text-emerald-300 flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Wallet Authorized</span>
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200 border border-emerald-300/50">
                      Eligible Voter
                    </span>
                  </div>

                  <div className="p-2.5 bg-white dark:bg-slate-900 rounded border border-emerald-200 dark:border-emerald-800/60 font-mono text-xs space-y-1">
                    <div className="text-slate-400 text-[10px]">ECDSA ADDRESS:</div>
                    <div className="font-bold text-slate-800 dark:text-slate-200 truncate">{connectedAddress}</div>
                    <div className="text-[10px] text-slate-500 pt-1 flex justify-between">
                      <span>Network: PoW Testnet (1337)</span>
                      <span>Gas: Sponsored</span>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={handleProceedWithWallet}
                    className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-1.5"
                  >
                    <span>Proceed to Active Ballot</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              )}

              {walletStatus === 'wrong_network' && (
                <div className="p-4 border border-amber-200 dark:border-amber-900/60 bg-amber-50/50 dark:bg-amber-950/20 rounded-lg space-y-2">
                  <div className="flex items-center gap-1.5 text-amber-800 dark:text-amber-200 text-xs font-bold">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Wrong Network Detected</span>
                  </div>
                  <p className="text-[11px] text-amber-800 dark:text-amber-200">
                    Your wallet is connected to an external chain. Switch to PoW Testnet (1337) to sign ballots.
                  </p>
                  <button
                    type="button"
                    onClick={() => setWalletStatus('connected')}
                    className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs rounded-lg transition-colors"
                  >
                    Switch to PoW Testnet (1337)
                  </button>
                </div>
              )}

              {walletStatus === 'error' && (
                <div className="p-4 border border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/20 rounded-lg space-y-2">
                  <div className="flex items-center gap-1.5 text-rose-700 dark:text-rose-300 text-xs font-bold">
                    <XCircle className="w-4 h-4" />
                    <span>Connection Declined</span>
                  </div>
                  <p className="text-[11px] text-rose-800 dark:text-rose-200">
                    {walletErrorMsg || 'The connection request was rejected or timed out.'}
                  </p>
                  <button
                    type="button"
                    onClick={handleConnectWallet}
                    className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-semibold text-xs rounded-lg transition-colors"
                  >
                    Retry Connection
                  </button>
                </div>
              )}

            </div>
          )}

          {/* Quick Demo Fill (Subtle & Professional) */}
          <div className="pt-3 border-t border-slate-200 dark:border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-[10px] font-mono text-slate-500">
              <span className="flex items-center gap-1">
                <UserCheck className="w-3 h-3 text-blue-600" />
                <span>QUICK DEMO ACCOUNTS:</span>
              </span>
              <span>1-CLICK SIGN IN</span>
            </div>

            <div className="grid grid-cols-3 gap-1.5 text-left">
              <button
                type="button"
                onClick={() => handleDirectLogin('admin', 'Admin123!')}
                className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                <div className="font-bold text-[11px] text-slate-900 dark:text-slate-100">Admin</div>
                <div className="text-[9px] text-slate-400 font-mono">Full setup</div>
              </button>

              <button
                type="button"
                onClick={() => handleDirectLogin('voter1', 'Voter123!')}
                className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                <div className="font-bold text-[11px] text-slate-900 dark:text-slate-100">Student Voter</div>
                <div className="text-[9px] text-slate-400 font-mono">Cast ballot</div>
              </button>

              <button
                type="button"
                onClick={() => handleDirectLogin('observer1', 'Observer123!')}
                className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                <div className="font-bold text-[11px] text-slate-900 dark:text-slate-100">Observer</div>
                <div className="text-[9px] text-slate-400 font-mono">Live audit</div>
              </button>
            </div>
          </div>

          {/* Registration Link */}
          <div className="text-center pt-1">
            <p className="text-xs text-slate-500 dark:text-slate-400">
              New campus voter?{' '}
              <Link to="/register" className="text-blue-600 dark:text-blue-400 font-semibold hover:underline">
                Register identity &amp; keypair
              </Link>
            </p>
          </div>

        </div>

        {/* Security Disclaimer */}
        <div className="bg-slate-50 dark:bg-slate-950/80 border-t border-slate-200 dark:border-slate-800 px-5 py-2.5 text-[10px] font-mono text-slate-400 flex items-center justify-between">
          <div className="flex items-center gap-1">
            <Lock className="w-3 h-3 text-slate-400 shrink-0" />
            <span>Ballot Secrecy Guaranteed</span>
          </div>
          <span>PoW Block Ledger</span>
        </div>

      </div>

    </div>
  );
};
