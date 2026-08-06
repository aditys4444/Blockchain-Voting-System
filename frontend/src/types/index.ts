export type UserRole = 'admin' | 'voter' | 'observer';

export interface User {
  id: number;
  email: string;
  username: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface Candidate {
  id: number;
  election_id: number;
  name: string;
  party?: string;
  manifesto?: string;
  avatar_url?: string;
  vote_count: number;
  percentage?: number;
}

export interface Election {
  id: number;
  title: string;
  description?: string;
  status: 'draft' | 'scheduled' | 'active' | 'closed';
  start_time?: string;
  end_time?: string;
  created_by: number;
  created_at: string;
  candidates: Candidate[];
}

export interface VoteReceipt {
  vote_id: number;
  election_id: number;
  candidate_id: number;
  voter_hash: string;
  tx_hash: string;
  block_index: number;
  receipt_hash: string;
  created_at: string;
}

export interface Block {
  index: number;
  timestamp: number;
  previous_hash: string;
  hash: string;
  nonce: number;
  merkle_root: string;
  signature: string;
  transactions: any[];
}

export interface ChainStatus {
  is_valid: boolean;
  total_blocks: number;
  difficulty: number;
  pending_transactions_count: number;
  message: string;
}

export interface FraudAnalysis {
  fraud_risk_score: number;
  risk_level: 'Low' | 'Medium' | 'High' | 'Critical';
  flagged_anomalies: string[];
  details: {
    total_votes: number;
    rapid_burst_count: number;
    duplicate_ip_count: number;
    double_voting_attempts: number;
  };
}

export interface AuditLog {
  id: number;
  user_id?: number;
  user_email?: string;
  action: string;
  details?: string;
  ip_address?: string;
  timestamp: string;
}
