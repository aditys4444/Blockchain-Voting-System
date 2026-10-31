import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

OUTPUT_DIR = os.path.join(os.getcwd(), "UML_Diagrams")
SOURCES_DIR = os.path.join(OUTPUT_DIR, "sources")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SOURCES_DIR, exist_ok=True)

# Palette Constants
NAVY = "#1B365D"
TEAL = "#008080"
LIGHT_BG = "#F8FAFC"
WHITE = "#FFFFFF"
DARK_TEXT = "#0F172A"
BORDER_BLUE = "#3B82F6"
BORDER_GRAY = "#94A3B8"
ACCENT_GREEN = "#10B981"
ACCENT_AMBER = "#F59E0B"
ACCENT_RED = "#EF4444"

def setup_canvas(width=14, height=10, title=""):
    fig, ax = plt.subplots(figsize=(width, height), dpi=300)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    if title:
        ax.text(50, 96, title, ha='center', va='center', fontsize=15, fontweight='bold', color=NAVY)
        ax.plot([10, 90], [93, 93], color=TEAL, lw=1.5)
    return fig, ax

def draw_box(ax, x, y, w, h, title="", lines=None, bg=LIGHT_BG, border=BORDER_BLUE, title_color=NAVY, lw=1.5):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.0",
                          linewidth=lw, edgecolor=border, facecolor=bg)
    ax.add_patch(rect)
    if title:
        ax.text(x + w/2, y + h - 2.5, title, ha='center', va='top', fontsize=10, fontweight='bold', color=title_color)
    if lines:
        start_y = y + h - 6.5
        for i, line in enumerate(lines):
            ax.text(x + 2, start_y - (i * 3.2), line, ha='left', va='top', fontsize=8.5, color=DARK_TEXT)

def draw_arrow(ax, x1, y1, x2, y2, text="", color=NAVY, style="->", dashed=False, lw=1.5, text_offset=(0, 1.5)):
    ls = '--' if dashed else '-'
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, linestyle=ls, shrinkA=3, shrinkB=3))
    if text:
        mid_x = (x1 + x2) / 2 + text_offset[0]
        mid_y = (y1 + y2) / 2 + text_offset[1]
        ax.text(mid_x, mid_y, text, ha='center', va='center', fontsize=8, color=color,
                bbox=dict(boxstyle="round,pad=0.2", fc=WHITE, ec="none", alpha=0.9))

# ----------------------------------------------------------------------
# 1. System Context Diagram
# ----------------------------------------------------------------------
def generate_system_context():
    fig, ax = setup_canvas(14, 10, "Figure 5.1 — System Context Diagram")
    
    # External Users (Left)
    draw_box(ax, 4, 68, 22, 18, "System Administrator", 
             ["• Creates elections", "• Registers candidates", "• Imports voter rosters", "• Closes election"], bg="#EFF6FF", border=BORDER_BLUE)
    
    draw_box(ax, 4, 40, 22, 18, "Registered Voter", 
             ["• Authenticates identity", "• Reviews candidate bios", "• Casts AES encrypted vote", "• Downloads QR receipt"], bg="#EFF6FF", border=BORDER_BLUE)
    
    draw_box(ax, 4, 12, 22, 18, "Independent Observer", 
             ["• Monitors live standings", "• Audits block transactions", "• Inspects Merkle proofs", "• Reviews AI fraud score"], bg="#EFF6FF", border=BORDER_BLUE)

    # Core System (Center)
    draw_box(ax, 38, 28, 26, 44, "DECENTRALIZED BLOCKCHAIN\nVOTING SYSTEM",
             ["Core Engine Architecture:",
              "• React 19 Frontend SPA",
              "• FastAPI Asynchronous API",
              "• SECP256R1 ECDSA Signer",
              "• SHA-256 Merkle Tree Engine",
              "• Proof-of-Work Miner (Diff 4)",
              "• AI Anomaly Telemetry",
              "• Dynamic QR Generator"], bg="#F0FDF4", border=ACCENT_GREEN, title_color=TEAL, lw=2.0)

    # External Systems & Storage (Right)
    draw_box(ax, 74, 68, 22, 18, "Relational Database Engine", 
             ["• SQLite 3 with WAL Mode", "• SQLAlchemy 2.0 ORM", "• Parameterized queries", "• Identity & Candidate store"], bg="#FDF4FF", border="#C084FC")
    
    draw_box(ax, 74, 40, 22, 18, "AI Fraud Radar Service", 
             ["• Request velocity engine", "• <500ms burst detector", "• IP clustering analytics", "• Dynamic Risk Scoring"], bg="#FFFBEB", border=ACCENT_AMBER)
    
    draw_box(ax, 74, 12, 22, 18, "Public Ledger & Audit Service", 
             ["• Immutable block store", "• SECP256R1 key validator", "• SHA-256 hash continuity", "• Public audit desk"], bg="#F1F5F9", border=BORDER_GRAY)

    # Connecting Arrows
    draw_arrow(ax, 26, 77, 38, 60, "Config & CSV Data")
    draw_arrow(ax, 26, 49, 38, 49, "AES-256 Encrypted Vote")
    draw_arrow(ax, 38, 45, 26, 45, "QR Code Receipt")
    draw_arrow(ax, 26, 21, 38, 38, "Telemetry & Audit Queries")

    draw_arrow(ax, 64, 60, 74, 77, "SQL Operations")
    draw_arrow(ax, 64, 50, 74, 49, "Vote Timestamps & IPs")
    draw_arrow(ax, 74, 45, 64, 45, "Risk Score (0-100%)")
    draw_arrow(ax, 64, 38, 74, 21, "Mined Blocks & Signatures")

    plt.savefig(os.path.join(OUTPUT_DIR, "01_System_Context.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 2. Use Case Diagram
# ----------------------------------------------------------------------
def generate_use_case():
    fig, ax = setup_canvas(14, 10, "Figure 5.2 — System Use Case Diagram")
    
    # Actors (Standard text boxes instead of Unicode glyphs)
    draw_box(ax, 2, 72, 14, 8, "<<actor>>\nAdministrator", bg="#EFF6FF", border=BORDER_BLUE)
    draw_box(ax, 2, 45, 14, 8, "<<actor>>\nRegistered Voter", bg="#EFF6FF", border=BORDER_BLUE)
    draw_box(ax, 2, 18, 14, 8, "<<actor>>\nObserver / Auditor", bg="#EFF6FF", border=BORDER_BLUE)
    draw_box(ax, 84, 45, 14, 8, "<<actor: system>>\nAI Fraud Radar", bg="#FFFBEB", border=ACCENT_AMBER)

    # System Boundary Box
    rect = FancyBboxPatch((18, 5), 64, 85, boxstyle="round,pad=0.8", linewidth=1.5, edgecolor=BORDER_BLUE, facecolor="#F8FAFC")
    ax.add_patch(rect)
    ax.text(50, 87, "Decentralized Voting System Boundary", ha='center', fontsize=10, fontweight='bold', color=NAVY)

    # Use Cases (Ellipses)
    uc_list = [
        (33, 78, "UC-01: User Login & JWT Auth", "#DBEAFE"),
        (33, 68, "UC-02: Create Election Instance", "#DBEAFE"),
        (33, 58, "UC-03: Register Candidate Profile", "#DBEAFE"),
        (33, 48, "UC-04: Bulk CSV Voter Import", "#DBEAFE"),
        (63, 78, "UC-05: Browse Active Ballots", "#FEF3C7"),
        (63, 66, "UC-06: Cast Encrypted Ballot", "#D1FAE5"),
        (63, 54, "UC-07: Download QR Receipt", "#D1FAE5"),
        (33, 34, "UC-08: Mine PoW Block (Diff 4)", "#E0E7FF"),
        (63, 34, "UC-09: Sign Block with SECP256R1", "#E0E7FF"),
        (33, 20, "UC-10: Verify Individual Receipt Hash", "#F3E8FF"),
        (63, 20, "UC-11: Full Chain Integrity Audit", "#F3E8FF"),
        (63, 10, "UC-12: AI Fraud Telemetry Scoring", "#FEE2E2")
    ]

    for x, y, label, bg in uc_list:
        p = patches.FancyBboxPatch((x - 12, y - 3), 24, 6, boxstyle="round,pad=0.4,rounding_size=3.0",
                                   ec=NAVY, fc=bg, lw=1.2)
        ax.add_patch(p)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.2, fontweight='bold', color=DARK_TEXT)

    # Connections
    draw_arrow(ax, 16, 76, 21, 78, "")
    draw_arrow(ax, 16, 76, 21, 68, "")
    draw_arrow(ax, 16, 76, 21, 58, "")
    draw_arrow(ax, 16, 76, 21, 48, "")

    draw_arrow(ax, 16, 49, 21, 78, "")
    draw_arrow(ax, 16, 49, 51, 78, "")
    draw_arrow(ax, 16, 49, 51, 66, "")
    draw_arrow(ax, 16, 49, 51, 54, "")

    draw_arrow(ax, 16, 22, 21, 20, "")
    draw_arrow(ax, 16, 22, 51, 20, "")

    # Include / Extend links
    draw_arrow(ax, 63, 63, 63, 57, "<<include>>", color=TEAL, style="->", dashed=True, lw=1.2)
    draw_arrow(ax, 63, 63, 33, 37, "<<include>>", color=TEAL, style="->", dashed=True, lw=1.2)
    draw_arrow(ax, 33, 31, 63, 34, "<<include>>", color=TEAL, style="->", dashed=True, lw=1.2)
    draw_arrow(ax, 84, 45, 75, 12, "<<extend>>", color=ACCENT_RED, style="->", dashed=True, lw=1.2)

    plt.savefig(os.path.join(OUTPUT_DIR, "02_Use_Case.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 3. Class Diagram
# ----------------------------------------------------------------------
def generate_class_diagram():
    fig, ax = setup_canvas(15, 11, "Figure 5.3 — System Class Diagram Architecture")

    # User Class
    draw_box(ax, 3, 62, 28, 30, "User (SQLAlchemy Entity)",
             ["+ id: int [PK]",
              "+ email: str [Unique]",
              "+ username: str [Unique]",
              "+ hashed_password: str",
              "+ role: str (admin/voter/observer)",
              "+ is_active: bool",
              "+ created_at: datetime",
              "------------------------------------",
              "+ authenticate(password): bool",
              "+ generate_jwt_token(): str",
              "+ verify_role(role): bool"], bg="#EFF6FF", border=BORDER_BLUE)

    # Election Class
    draw_box(ax, 37, 62, 28, 30, "Election (SQLAlchemy Entity)",
             ["+ id: int [PK]",
              "+ title: str",
              "+ description: str",
              "+ status: str (draft/active/closed)",
              "+ start_time: datetime",
              "+ end_time: datetime",
              "+ created_by: int [FK -> users.id]",
              "------------------------------------",
              "+ activate(): void",
              "+ close(): void",
              "+ add_candidate(c: Candidate): void",
              "+ get_results(): Dict"], bg="#EFF6FF", border=BORDER_BLUE)

    # Candidate Class
    draw_box(ax, 71, 62, 26, 30, "Candidate (Entity)",
             ["+ id: int [PK]",
              "+ election_id: int [FK]",
              "+ name: str",
              "+ party: str",
              "+ manifesto: str",
              "+ avatar_url: str",
              "+ vote_count: int = 0",
              "------------------------------------",
              "+ increment_vote(): void",
              "+ get_tally_percentage(): float"], bg="#EFF6FF", border=BORDER_BLUE)

    # VoteReceipt Class
    draw_box(ax, 3, 15, 28, 38, "VoteReceipt (Entity)",
             ["+ id: int [PK]",
              "+ user_id: int [FK -> users.id]",
              "+ election_id: int [FK -> elections.id]",
              "+ candidate_id: int [FK]",
              "+ voter_hash: str [Unique]",
              "+ encrypted_vote: str [AES-256]",
              "+ tx_hash: str [SHA-256]",
              "+ block_index: int",
              "+ receipt_hash: str [Unique]",
              "+ created_at: datetime",
              "------------------------------------",
              "+ verify_signature(pub_key): bool",
              "+ generate_qr_matrix(): Image"], bg="#FEF3C7", border=ACCENT_AMBER)

    # Block Class (Cryptographic)
    draw_box(ax, 37, 15, 28, 38, "Block (Cryptographic Object)",
             ["+ index: int",
              "+ timestamp: float",
              "+ previous_hash: str",
              "+ hash: str [SHA-256]",
              "+ nonce: int",
              "+ merkle_root: str",
              "+ signature: str [SECP256R1]",
              "+ transactions: List[Dict]",
              "------------------------------------",
              "+ calculate_hash(): str",
              "+ mine_pow(difficulty=4): void",
              "+ sign(private_key): str",
              "+ verify_ecdsa(public_key): bool"], bg="#D1FAE5", border=ACCENT_GREEN)

    # BlockchainService Class
    draw_box(ax, 71, 15, 26, 38, "BlockchainService (Core)",
             ["+ chain: List[Block]",
              "+ pending_txs: List[Dict]",
              "+ difficulty: int = 4",
              "+ target_prefix: str = '0000'",
              "------------------------------------",
              "+ create_genesis_block(): Block",
              "+ add_transaction(tx): void",
              "+ compute_merkle_root(txs): str",
              "+ mine_block(): Block",
              "+ is_chain_valid(): bool",
              "+ verify_receipt_hash(h): Dict"], bg="#F3E8FF", border="#A855F7")

    # Cardinality Relationships
    draw_arrow(ax, 31, 77, 37, 77, "1        creates        *", style="->", text_offset=(0, 2))
    draw_arrow(ax, 65, 77, 71, 77, "1       has       *", style="->", text_offset=(0, 2))
    draw_arrow(ax, 17, 62, 17, 53, "1\ncasts\n*", style="->", text_offset=(2, 0))
    draw_arrow(ax, 51, 62, 28, 53, "1  secures  *", style="->", text_offset=(0, 2))
    draw_arrow(ax, 31, 34, 37, 34, "*      mined into      1", style="->", text_offset=(0, 2))
    draw_arrow(ax, 65, 34, 71, 34, "*      managed by      1", style="->", text_offset=(0, 2))

    plt.savefig(os.path.join(OUTPUT_DIR, "03_Class_Diagram.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 4. Sequence Diagram: Login
# ----------------------------------------------------------------------
def generate_login_sequence():
    fig, ax = setup_canvas(14, 10, "Figure 5.4 — Sequence Diagram for User Login")
    
    lifelines = [
        (10, "User / Browser"),
        (30, "Auth Router\n(/auth/login)"),
        (52, "SecurityService\n(Bcrypt)"),
        (72, "Database\n(SQLite)"),
        (90, "JWT Service\n(HS256)")
    ]

    for x, label in lifelines:
        ax.text(x, 88, label, ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY,
                bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec=BORDER_BLUE))
        ax.plot([x, x], [12, 84], color=BORDER_GRAY, linestyle='--', lw=1.2)

    # Activations
    ax.add_patch(patches.Rectangle((29.3, 24), 1.4, 55, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((71.3, 62), 1.4, 12, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((51.3, 44), 1.4, 12, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((89.3, 28), 1.4, 12, fc="#DBEAFE", ec=BORDER_BLUE))

    # Messages
    draw_arrow(ax, 10, 79, 29.3, 79, "1: POST /api/v1/auth/login {email, password}")
    draw_arrow(ax, 30.7, 72, 71.3, 72, "2: SELECT * FROM users WHERE email = ?")
    draw_arrow(ax, 71.3, 64, 30.7, 64, "3: Return User Record (hashed_password)", dashed=True, color=TEAL)
    
    draw_arrow(ax, 30.7, 54, 51.3, 54, "4: verify_password(password, hash)")
    draw_arrow(ax, 51.3, 46, 30.7, 46, "5: Password Valid (True)", dashed=True, color=TEAL)

    draw_arrow(ax, 30.7, 38, 89.3, 38, "6: create_access_token({sub: id, role})")
    draw_arrow(ax, 89.3, 30, 30.7, 30, "7: Return Signed JWT Bearer Token", dashed=True, color=TEAL)

    draw_arrow(ax, 29.3, 24, 10, 24, "8: 200 OK {access_token, user_profile}", dashed=True, color=ACCENT_GREEN)

    plt.savefig(os.path.join(OUTPUT_DIR, "04_Login_Sequence.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 5. Sequence Diagram: Registration
# ----------------------------------------------------------------------
def generate_registration_sequence():
    fig, ax = setup_canvas(14, 10, "Figure 5.5 — Sequence Diagram for Voter Self-Registration")
    
    lifelines = [
        (10, "Voter UI\n(Register.tsx)"),
        (35, "Auth Router\n(/auth/register)"),
        (60, "SecurityService\n(Bcrypt Cost 12)"),
        (85, "Database\n(SQLite Engine)")
    ]

    for x, label in lifelines:
        ax.text(x, 88, label, ha='center', va='center', fontsize=9.5, fontweight='bold', color=NAVY,
                bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec=BORDER_BLUE))
        ax.plot([x, x], [12, 84], color=BORDER_GRAY, linestyle='--', lw=1.2)

    # Activations
    ax.add_patch(patches.Rectangle((34.3, 22), 1.4, 58, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((84.3, 62), 1.4, 12, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((59.3, 42), 1.4, 12, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((84.3, 26), 1.4, 12, fc="#DBEAFE", ec=BORDER_BLUE))

    # Messages
    draw_arrow(ax, 10, 80, 34.3, 80, "1: Submit Form {email, username, password}")
    draw_arrow(ax, 35.7, 72, 84.3, 72, "2: Check Duplicate (email / username)")
    draw_arrow(ax, 84.3, 64, 35.7, 64, "3: No Duplicate Found (None)", dashed=True, color=TEAL)
    
    draw_arrow(ax, 35.7, 52, 59.3, 52, "4: hash_password(password, cost=12)")
    draw_arrow(ax, 59.3, 44, 35.7, 44, "5: Return Hashed String", dashed=True, color=TEAL)

    draw_arrow(ax, 35.7, 36, 84.3, 36, "6: INSERT INTO users (role='voter')")
    draw_arrow(ax, 84.3, 28, 35.7, 28, "7: Commit OK & Return user_id", dashed=True, color=TEAL)

    draw_arrow(ax, 34.3, 22, 10, 22, "8: 201 Created & Auto-Login Redirect", dashed=True, color=ACCENT_GREEN)

    plt.savefig(os.path.join(OUTPUT_DIR, "05_Registration_Sequence.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 6. Sequence Diagram: Main Vote Casting & Receipt
# ----------------------------------------------------------------------
def generate_main_vote_sequence():
    fig, ax = setup_canvas(15, 11, "Figure 5.6 — Sequence Diagram for Encrypted Voting & Block Mining")
    
    lifelines = [
        (8, "Voter Desk\n(VoterDashboard)"),
        (26, "Vote Router\n(/votes/cast)"),
        (46, "Crypto Service\n(AES-256 GCM)"),
        (66, "Blockchain Miner\n(PoW Diff 4)"),
        (84, "Signer\n(SECP256R1)"),
        (96, "Database\n(SQLite)")
    ]

    for x, label in lifelines:
        ax.text(x, 89, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY,
                bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec=BORDER_BLUE))
        ax.plot([x, x], [10, 85], color=BORDER_GRAY, linestyle='--', lw=1.2)

    # Activations
    ax.add_patch(patches.Rectangle((25.3, 18), 1.4, 64, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((45.3, 62), 1.4, 10, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((65.3, 40), 1.4, 18, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((83.3, 32), 1.4, 8, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((95.3, 22), 1.4, 8, fc="#DBEAFE", ec=BORDER_BLUE))

    # Messages
    draw_arrow(ax, 8, 82, 25.3, 82, "1: Click 'Vote for Candidate' {election_id, candidate_id}")
    draw_arrow(ax, 25.3, 76, 8, 76, "2: Verify Voter Not Already Voted in election", dashed=True, color=TEAL)
    
    draw_arrow(ax, 26.7, 70, 45.3, 70, "3: encrypt_vote(candidate_id, secret_key)")
    draw_arrow(ax, 45.3, 63, 26.7, 63, "4: Return Ciphertext + Auth Tag", dashed=True, color=TEAL)

    draw_arrow(ax, 26.7, 56, 65.3, 56, "5: mine_block(transactions, prev_hash, diff=4)")
    draw_arrow(ax, 66.7, 48, 66.7, 44, "Compute SHA-256 Merkle Root")
    draw_arrow(ax, 66.7, 40, 83.3, 40, "6: sign_block_header(hash, private_key)")
    draw_arrow(ax, 83.3, 34, 66.7, 34, "7: Return DER ECDSA Signature", dashed=True, color=TEAL)
    draw_arrow(ax, 65.3, 30, 26.7, 30, "8: Block Mined (Nonce, BlockHash, TxHash)", dashed=True, color=TEAL)

    draw_arrow(ax, 26.7, 26, 95.3, 26, "9: INSERT INTO vote_receipts (tx_hash, receipt_hash)")
    draw_arrow(ax, 95.3, 20, 26.7, 20, "10: Commit OK", dashed=True, color=TEAL)

    draw_arrow(ax, 25.3, 16, 8, 16, "11: 200 OK -> Render QRCodeModal with Receipt Hash", dashed=True, color=ACCENT_GREEN)

    plt.savefig(os.path.join(OUTPUT_DIR, "06_Main_Workflow_Sequence.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 7. Sequence Diagram: API Interaction & Telemetry
# ----------------------------------------------------------------------
def generate_api_sequence():
    fig, ax = setup_canvas(14, 10, "Figure 5.7 — Sequence Diagram for API Interaction & AI Fraud Telemetry")
    
    lifelines = [
        (10, "Client Browser\n(Axios Client)"),
        (38, "API Gateway\n(FastAPI ASGI)"),
        (66, "AI Fraud Radar\n(Velocity Engine)"),
        (90, "Observer Portal\n(WebSockets)")
    ]

    for x, label in lifelines:
        ax.text(x, 88, label, ha='center', va='center', fontsize=9.5, fontweight='bold', color=NAVY,
                bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec=BORDER_BLUE))
        ax.plot([x, x], [12, 84], color=BORDER_GRAY, linestyle='--', lw=1.2)

    # Activations
    ax.add_patch(patches.Rectangle((37.3, 20), 1.4, 62, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((65.3, 38), 1.4, 30, fc="#DBEAFE", ec=BORDER_BLUE))
    ax.add_patch(patches.Rectangle((89.3, 24), 1.4, 14, fc="#DBEAFE", ec=BORDER_BLUE))

    # Messages
    draw_arrow(ax, 10, 80, 37.3, 80, "1: API Request + Bearer JWT Header")
    draw_arrow(ax, 38.7, 72, 65.3, 72, "2: Log Request Timestamp (t) & Client IP")
    draw_arrow(ax, 66.7, 64, 66.7, 60, "Evaluate arrival interval Δt = t - t_prev")
    draw_arrow(ax, 66.7, 54, 66.7, 50, "Check Burst Threshold (<500ms)")
    draw_arrow(ax, 65.3, 44, 37.3, 44, "3: Return Fraud Risk Score (0-100%)", dashed=True, color=TEAL)

    draw_arrow(ax, 38.7, 34, 89.3, 34, "4: Broadcast WebSocket Event {type: 'VOTE_EVENT'}")
    draw_arrow(ax, 89.3, 26, 89.3, 24, "Update Recharts Live Standings")

    draw_arrow(ax, 37.3, 20, 10, 20, "5: Return HTTP JSON Response (200 OK)", dashed=True, color=ACCENT_GREEN)

    plt.savefig(os.path.join(OUTPUT_DIR, "07_API_Sequence.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 8. Activity Diagram: Login
# ----------------------------------------------------------------------
def generate_login_activity():
    fig, ax = setup_canvas(12, 11, "Figure 5.8 — Activity Diagram for User Login & Role Guard")

    # Start Node
    ax.add_patch(patches.Circle((50, 91), 1.8, fc=NAVY, ec=NAVY))
    ax.text(50, 94.5, "Start", ha='center', fontsize=9, fontweight='bold', color=NAVY)

    # Activity 1: Enter Credentials
    draw_arrow(ax, 50, 89.2, 50, 84, "")
    draw_box(ax, 35, 78, 30, 6, "Enter Email & Password", bg="#EFF6FF", border=BORDER_BLUE)

    # Activity 2: Submit Form
    draw_arrow(ax, 50, 78, 50, 72, "")
    draw_box(ax, 35, 66, 30, 6, "Transmit POST /api/v1/auth/login", bg="#EFF6FF", border=BORDER_BLUE)

    # Decision 1: Credentials Valid?
    draw_arrow(ax, 50, 66, 50, 60, "")
    diamond = patches.Polygon([[50, 60], [58, 55], [50, 50], [42, 55]], fc="#FEF3C7", ec=ACCENT_AMBER, lw=1.5)
    ax.add_patch(diamond)
    ax.text(50, 55, "Valid Hash?", ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)

    # Invalid Branch (Right)
    draw_arrow(ax, 58, 55, 80, 55, "[No]")
    draw_box(ax, 72, 45, 22, 6, "Display HTTP 401\nError Toast", bg="#FEE2E2", border=ACCENT_RED)
    draw_arrow(ax, 83, 51, 83, 81, "")
    draw_arrow(ax, 83, 81, 65, 81, "Retry")

    # Valid Branch (Down)
    draw_arrow(ax, 50, 50, 50, 43, "[Yes]")
    draw_box(ax, 35, 37, 30, 6, "Issue OAuth2 JWT Bearer Token", bg="#D1FAE5", border=ACCENT_GREEN)

    # Decision 2: Role Check
    draw_arrow(ax, 50, 37, 50, 31, "")
    diamond2 = patches.Polygon([[50, 31], [58, 26], [50, 21], [42, 26]], fc="#FEF3C7", ec=ACCENT_AMBER, lw=1.5)
    ax.add_patch(diamond2)
    ax.text(50, 26, "User Role?", ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY)

    # Admin Branch
    draw_arrow(ax, 42, 26, 22, 26, "[admin]")
    draw_box(ax, 10, 16, 24, 6, "Redirect /admin/elections", bg="#EFF6FF", border=BORDER_BLUE)

    # Voter Branch
    draw_arrow(ax, 50, 21, 50, 16, "[voter]")
    draw_box(ax, 38, 10, 24, 6, "Redirect /voter", bg="#EFF6FF", border=BORDER_BLUE)

    # Observer Branch
    draw_arrow(ax, 58, 26, 78, 26, "[observer]")
    draw_box(ax, 66, 16, 24, 6, "Redirect /observer", bg="#EFF6FF", border=BORDER_BLUE)

    # End Node
    ax.add_patch(patches.Circle((50, 3), 1.8, fc=WHITE, ec=NAVY, lw=1.5))
    ax.add_patch(patches.Circle((50, 3), 1.0, fc=NAVY, ec=NAVY))
    ax.text(50, 0, "Session Established", ha='center', fontsize=8, color=NAVY)

    plt.savefig(os.path.join(OUTPUT_DIR, "08_Login_Activity.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 9. Activity Diagram: Voter Main Workflow
# ----------------------------------------------------------------------
def generate_voter_activity():
    fig, ax = setup_canvas(13, 11, "Figure 5.9 — Activity Diagram for Voter Main Voting Lifecycle")

    # Start
    ax.add_patch(patches.Circle((50, 92), 1.8, fc=NAVY, ec=NAVY))
    
    # 1. Login & Auth
    draw_arrow(ax, 50, 90.2, 50, 85, "")
    draw_box(ax, 35, 79, 30, 6, "Authenticate & Load Voter Portal", bg="#EFF6FF", border=BORDER_BLUE)

    # 2. Fetch active elections
    draw_arrow(ax, 50, 79, 50, 73, "")
    draw_box(ax, 35, 67, 30, 6, "Retrieve Active Elections List", bg="#EFF6FF", border=BORDER_BLUE)

    # Decision 1: Already Voted?
    draw_arrow(ax, 50, 67, 50, 60, "")
    diamond1 = patches.Polygon([[50, 60], [58, 55], [50, 50], [42, 55]], fc="#FEF3C7", ec=ACCENT_AMBER, lw=1.5)
    ax.add_patch(diamond1)
    ax.text(50, 55, "Already Voted?", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)

    # Already Voted -> Receipts
    draw_arrow(ax, 58, 55, 78, 55, "[Yes]")
    draw_box(ax, 72, 45, 24, 6, "Display 'Already Voted'\nNavigate to /receipts", bg="#FEF3C7", border=ACCENT_AMBER)
    draw_arrow(ax, 84, 45, 84, 18, "")

    # Not Voted -> Select Candidate
    draw_arrow(ax, 50, 50, 50, 43, "[No]")
    draw_box(ax, 35, 37, 30, 6, "Select Candidate & Confirm Vote", bg="#EFF6FF", border=BORDER_BLUE)

    # Encrypt & Mine Block
    draw_arrow(ax, 50, 37, 50, 31, "")
    draw_box(ax, 32, 25, 36, 6, "Encrypt AES-256 & Mine PoW Block", bg="#D1FAE5", border=ACCENT_GREEN)

    # Display QR Modal
    draw_arrow(ax, 50, 25, 50, 19, "")
    draw_box(ax, 32, 13, 36, 6, "Display QRCodeModal & TxHash", bg="#D1FAE5", border=ACCENT_GREEN)

    # End
    draw_arrow(ax, 50, 13, 50, 7, "")
    draw_arrow(ax, 84, 18, 52, 5, "")
    ax.add_patch(patches.Circle((50, 4), 1.8, fc=WHITE, ec=NAVY, lw=1.5))
    ax.add_patch(patches.Circle((50, 4), 1.0, fc=NAVY, ec=NAVY))

    plt.savefig(os.path.join(OUTPUT_DIR, "09_Main_Workflow_Activity.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 10. Entity-Relationship (ER) Diagram
# ----------------------------------------------------------------------
def generate_er_diagram():
    fig, ax = setup_canvas(15, 11, "Figure 5.10 — Entity-Relationship (ER) Data Model Diagram")

    # Table: USERS
    draw_box(ax, 4, 60, 26, 28, "USERS (Table)",
             ["PK  id: INTEGER",
              "UQ  email: VARCHAR(255)",
              "UQ  username: VARCHAR(100)",
              "    hashed_password: VARCHAR(255)",
              "    role: VARCHAR(50)",
              "    is_active: BOOLEAN",
              "    created_at: DATETIME"], bg="#EFF6FF", border=BORDER_BLUE)

    # Table: ELECTIONS
    draw_box(ax, 37, 60, 26, 28, "ELECTIONS (Table)",
             ["PK  id: INTEGER",
              "    title: VARCHAR(255)",
              "    description: TEXT",
              "    status: VARCHAR(50)",
              "    start_time: DATETIME",
              "    end_time: DATETIME",
              "FK  created_by: INTEGER"], bg="#EFF6FF", border=BORDER_BLUE)

    # Table: CANDIDATES
    draw_box(ax, 70, 60, 26, 28, "CANDIDATES (Table)",
             ["PK  id: INTEGER",
              "FK  election_id: INTEGER",
              "    name: VARCHAR(255)",
              "    party: VARCHAR(100)",
              "    manifesto: TEXT",
              "    avatar_url: VARCHAR(255)",
              "    vote_count: INTEGER"], bg="#EFF6FF", border=BORDER_BLUE)

    # Table: VOTE_RECEIPTS
    draw_box(ax, 20, 12, 30, 36, "VOTE_RECEIPTS (Table)",
             ["PK  id: INTEGER",
              "FK  user_id: INTEGER",
              "FK  election_id: INTEGER",
              "FK  candidate_id: INTEGER",
              "UQ  voter_hash: VARCHAR(64)",
              "    encrypted_vote: TEXT",
              "UQ  tx_hash: VARCHAR(64)",
              "    block_index: INTEGER",
              "UQ  receipt_hash: VARCHAR(64)",
              "    created_at: DATETIME"], bg="#FEF3C7", border=ACCENT_AMBER)

    # Table: AUDIT_LOGS
    draw_box(ax, 62, 12, 28, 36, "AUDIT_LOGS (Table)",
             ["PK  id: INTEGER",
              "FK  user_id: INTEGER",
              "    user_email: VARCHAR(255)",
              "    action: VARCHAR(100)",
              "    details: TEXT",
              "    ip_address: VARCHAR(45)",
              "    timestamp: DATETIME"], bg="#F1F5F9", border=BORDER_GRAY)

    # Foreign Key Connectors with Crow's Foot notation
    draw_arrow(ax, 30, 74, 37, 74, "1 : N (created_by)", style="->", text_offset=(0, 2))
    draw_arrow(ax, 63, 74, 70, 74, "1 : N (election_id)", style="->", text_offset=(0, 2))
    draw_arrow(ax, 17, 60, 25, 48, "1 : N (user_id)", style="->", text_offset=(-2, 0))
    draw_arrow(ax, 50, 60, 42, 48, "1 : N (election_id)", style="->", text_offset=(0, 2))
    draw_arrow(ax, 83, 60, 48, 48, "1 : N (candidate_id)", style="->", text_offset=(4, 0))
    draw_arrow(ax, 17, 60, 68, 48, "1 : N (audit user)", style="->", text_offset=(0, 2))

    plt.savefig(os.path.join(OUTPUT_DIR, "10_ER_Diagram.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 11. Deployment Diagram
# ----------------------------------------------------------------------
def generate_deployment_diagram():
    fig, ax = setup_canvas(15, 11, "Figure 5.11 — System Deployment Architecture Diagram")

    # Node 1: Client Workstation
    draw_box(ax, 4, 52, 26, 36, "<<device>> Client Machine\n[Workstation / Smartphone]",
             ["<<executionEnvironment>>",
              "Modern Web Browser",
              "------------------------------",
              "• React 19 SPA (Client DOM)",
              "• LocalStorage (Fallback Store)",
              "• Web Crypto API (AES/SHA)",
              "• HTML5 / Canvas QR Viewer",
              "• WSS WebSocket Client"], bg="#EFF6FF", border=BORDER_BLUE)

    # Node 2: Vercel CDN Edge
    draw_box(ax, 37, 52, 26, 36, "<<cloud node>>\nVercel Global Edge CDN",
             ["<<infrastructure>>",
              "Edge Proxy & Static Cache",
              "------------------------------",
              "• Compiled JS/CSS Dist Bundles",
              "• Client SPA URL Rewrites",
              "• Automated TLS 1.3 Termination",
              "• DDoS Mitigation Filter",
              "• Edge Asset Invalidation"], bg="#F0FDF4", border=ACCENT_GREEN)

    # Node 3: Render Cloud Application Server
    draw_box(ax, 70, 52, 26, 36, "<<cloud node>>\nRender / Railway Container",
             ["<<executionEnvironment>>",
              "Linux Container (Python 3.12)",
              "------------------------------",
              "• Uvicorn ASGI Server (Port 8000)",
              "• FastAPI Async Worker Pool",
              "• Cryptographic Engine (`chain.py`)",
              "• AI Fraud Service (`ai_fraud`)",
              "• SECP256R1 Key Management"], bg="#FEF3C7", border=ACCENT_AMBER)

    # Node 4: Database Storage Node
    draw_box(ax, 70, 10, 26, 32, "<<database node>>\nPersistent Storage Volume",
             ["<<storageVolume>>",
              "SQLite 3 Engine",
              "------------------------------",
              "• `voting_system.db` (Schema)",
              "• `voting_system.db-wal` (Journal)",
              "• Parameterized Query Engine",
              "• ACID Compliance WAL Mode"], bg="#FDF4FF", border="#C084FC")

    # Node 5: Client Offline Fallback (Under Client)
    draw_box(ax, 4, 10, 26, 32, "<<executionEnvironment>>\nClient Smart Fallback Node",
             ["<<browserSandbox>>",
              "IndexedDB / LocalStorage",
              "------------------------------",
              "• Client SHA-256 Block Miner",
              "• Local Receipt Store",
              "• Standalone Demo Execution",
              "• Zero Network Downtime"], bg="#F1F5F9", border=BORDER_GRAY)

    # Network Links
    draw_arrow(ax, 30, 70, 37, 70, "HTTPS (TLS 1.3)")
    draw_arrow(ax, 63, 70, 70, 70, "Reverse Proxy / API")
    draw_arrow(ax, 83, 52, 83, 42, "SQLAlchemy / WAL")
    draw_arrow(ax, 17, 52, 17, 42, "Sync on Disconnect", dashed=True, color=BORDER_GRAY)

    plt.savefig(os.path.join(OUTPUT_DIR, "11_Deployment.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 12. Component Diagram
# ----------------------------------------------------------------------
def generate_component_diagram():
    fig, ax = setup_canvas(15, 11, "Figure 5.12 — UML Component Architecture Diagram")

    # Presentation Tier
    draw_box(ax, 4, 60, 26, 30, "<<component>>\nUI Presentation Layer",
             ["• VoterDashboard.tsx",
              "• ElectionManagement.tsx",
              "• BlockchainExplorer.tsx",
              "• ObserverDashboard.tsx",
              "• QRCodeModal.tsx"], bg="#EFF6FF", border=BORDER_BLUE)

    # API & Route Tier
    draw_box(ax, 37, 60, 26, 30, "<<component>>\nREST API Layer (FastAPI)",
             ["• /api/v1/auth Router",
              "• /api/v1/elections Router",
              "• /api/v1/votes Router",
              "• /api/v1/blockchain Router",
              "• /api/v1/ai Router"], bg="#F0FDF4", border=ACCENT_GREEN)

    # Security & Auth Component
    draw_box(ax, 70, 60, 26, 30, "<<component>>\nSecurity & Auth Service",
             ["• JWT Token Manager",
              "• Bcrypt Password Hasher",
              "• Role Guard Dependency",
              "• CORS Security Handler"], bg="#FEF3C7", border=ACCENT_AMBER)

    # Core Blockchain Engine Component
    draw_box(ax, 4, 15, 26, 35, "<<component>>\nBlockchain Ledger Engine",
             ["• Proof-of-Work Miner",
              "• SHA-256 Merkle Root Tree",
              "• SECP256R1 Digital Signer",
              "• Chain Audit Verifier"], bg="#F3E8FF", border="#A855F7")

    # AI Fraud Radar Component
    draw_box(ax, 37, 15, 26, 35, "<<component>>\nAI Fraud Radar Service",
             ["• Ingestion Velocity Tracker",
              "• <500ms Burst Bot Filter",
              "• Duplicate IP Cluster Log",
              "• Dynamic Risk Score Model"], bg="#FEE2E2", border=ACCENT_RED)

    # Database Component
    draw_box(ax, 70, 15, 26, 35, "<<component>>\nDatabase Storage Layer",
             ["• SQLAlchemy 2.0 Engine",
              "• SQLite WAL Connection Pool",
              "• Relational Entity Models",
              "• Parameterized SQL Binder"], bg="#FDF4FF", border="#C084FC")

    # Dependencies
    draw_arrow(ax, 30, 75, 37, 75, "<<use>> Axios HTTP", dashed=True)
    draw_arrow(ax, 63, 75, 70, 75, "<<delegate>>", dashed=True)
    draw_arrow(ax, 50, 60, 17, 50, "<<call>> Mining", dashed=True)
    draw_arrow(ax, 50, 60, 50, 50, "<<telemetry>>", dashed=True)
    draw_arrow(ax, 50, 60, 83, 50, "<<persist>>", dashed=True)

    plt.savefig(os.path.join(OUTPUT_DIR, "12_Component.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 13. Module / Package Diagram
# ----------------------------------------------------------------------
def generate_module_diagram():
    fig, ax = setup_canvas(15, 11, "Figure 5.13 — Package & Directory Module Diagram")

    # Root Package
    draw_box(ax, 2, 8, 96, 84, "Package: blockchain-voting-system (Root)", [], bg="#F8FAFC", border=NAVY, lw=2.0)

    # Frontend Package
    draw_box(ax, 5, 52, 43, 36, "Package: frontend/src/",
             ["+ components/ (Navbar, Sidebar, QRCodeModal)",
              "+ context/ (AuthContext, ThemeContext)",
              "+ pages/ (Login, Voter, Admin, Explorer, Observer)",
              "+ services/ (api.ts - Axios + Fallback)",
              "+ types/ (User, Election, Block, Receipt)"], bg="#EFF6FF", border=BORDER_BLUE)

    # Backend App Package
    draw_box(ax, 51, 52, 44, 36, "Package: backend/app/",
             ["+ api/ (auth.py, elections.py, votes.py, ai.py)",
              "+ core/ (config.py, database.py, security.py)",
              "+ models/ (models.py - SQLAlchemy Schemas)",
              "+ schemas/ (schemas.py - Pydantic Validators)",
              "+ services/ (blockchain_service, ai_fraud_service)",
              "+ main.py (FastAPI Startup & Seeds)"], bg="#F0FDF4", border=ACCENT_GREEN)

    # Blockchain Core Package
    draw_box(ax, 51, 12, 44, 34, "Package: backend/blockchain/",
             ["+ chain.py (Proof-of-Work & Merkle Tree)",
              "+ block.py (Block Header & SHA-256 Hashing)",
              "+ cryptography.py (SECP256R1 ECDSA Signatures)",
              "+ wallet.py (Asymmetric Key Generation)"], bg="#F3E8FF", border="#A855F7")

    # Database Store
    draw_box(ax, 5, 12, 43, 34, "Package: backend/storage/",
             ["+ voting_system.db (SQLite Database File)",
              "+ voting_system.db-wal (WAL Concurrency Journal)",
              "+ start_project.bat (Windows Concurrent Launcher)",
              "+ vercel.json (SPA Edge Configuration)"], bg="#FEF3C7", border=ACCENT_AMBER)

    # Package Import Links
    draw_arrow(ax, 48, 70, 51, 70, "<<HTTP REST / WSS>>")
    draw_arrow(ax, 73, 52, 73, 46, "<<import / invoke>>")
    draw_arrow(ax, 73, 46, 48, 29, "<<persist block records>>", dashed=True)

    plt.savefig(os.path.join(OUTPUT_DIR, "13_Module.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 14. DFD Level 0 (Context Level)
# ----------------------------------------------------------------------
def generate_dfd_level_0():
    fig, ax = setup_canvas(14, 10, "Figure 5.14 — Data Flow Diagram (DFD Level 0 — Context)")

    # External Entities (Rectangles)
    draw_box(ax, 5, 65, 20, 15, "Administrator", ["• Election Setup Data", "• Candidate Bios", "• Voter CSV Roster"], bg="#EFF6FF", border=BORDER_BLUE)
    draw_box(ax, 5, 38, 20, 15, "Registered Voter", ["• User Credentials", "• Candidate Choice"], bg="#EFF6FF", border=BORDER_BLUE)
    draw_box(ax, 5, 10, 20, 15, "Observer / Auditor", ["• Receipt Hash", "• Chain Audit Query"], bg="#EFF6FF", border=BORDER_BLUE)

    # Process 0.0 (Circle)
    p_circle = patches.Circle((52, 45), 18, fc="#D1FAE5", ec=ACCENT_GREEN, lw=2)
    ax.add_patch(p_circle)
    ax.text(52, 48, "0.0\nDECENTRALIZED\nBLOCKCHAIN VOTING\nPLATFORM", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=NAVY)

    # External Stores & Output (Right)
    draw_box(ax, 78, 55, 18, 20, "D1: SQLite Database", ["• users", "• elections", "• candidates"], bg="#FEF3C7", border=ACCENT_AMBER)
    draw_box(ax, 78, 15, 18, 20, "D2: Blockchain Ledger", ["• Mined Blocks", "• Merkle Roots", "• ECDSA Signatures"], bg="#F3E8FF", border="#A855F7")

    # Data Flows
    draw_arrow(ax, 25, 72, 40, 56, "Elections & Candidates")
    draw_arrow(ax, 25, 45, 34, 45, "Encrypted Ballots")
    draw_arrow(ax, 34, 42, 25, 42, "QR Receipts", color=TEAL)
    draw_arrow(ax, 25, 18, 40, 34, "Audit Inquiries")
    draw_arrow(ax, 40, 31, 25, 15, "Tally & Audit Reports", color=TEAL)

    draw_arrow(ax, 68, 52, 78, 62, "CRUD User/Candidate")
    draw_arrow(ax, 68, 38, 78, 28, "Commit Signed Block")

    plt.savefig(os.path.join(OUTPUT_DIR, "14_DFD_Level_0.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# 15. DFD Level 1 (Detailed Functional Decomposition)
# ----------------------------------------------------------------------
def generate_dfd_level_1():
    fig, ax = setup_canvas(15, 11, "Figure 5.15 — Data Flow Diagram (DFD Level 1 — Functional Decomposition)")

    # Processes (Circles / Rounded Rects)
    processes = [
        (25, 78, "1.0 User Authentication\n& Role Verification"),
        (25, 52, "2.0 Election & Candidate\nAdministration Studio"),
        (25, 26, "3.0 Ballot Encryption\n& Single Vote Guard"),
        (75, 52, "4.0 Blockchain Mining\n& Proof-of-Work Engine"),
        (75, 26, "5.0 AI Fraud Telemetry\n& Anomaly Radar")
    ]

    for x, y, label in processes:
        p = patches.FancyBboxPatch((x - 14, y - 5), 28, 10, boxstyle="round,pad=0.5,rounding_size=4.0",
                                   ec=ACCENT_GREEN, fc="#D1FAE5", lw=1.8)
        ax.add_patch(p)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY)

    # Data Stores
    draw_box(ax, 45, 75, 20, 14, "D1: Users Store", ["users table (SQLite)"], bg="#FEF3C7", border=ACCENT_AMBER)
    draw_box(ax, 45, 45, 20, 14, "D2: Elections Store", ["elections / candidates"], bg="#FEF3C7", border=ACCENT_AMBER)
    draw_box(ax, 45, 15, 20, 14, "D3: Blockchain Ledger", ["Mined Blocks & Receipts"], bg="#F3E8FF", border="#A855F7")

    # External Entities
    draw_box(ax, 2, 75, 12, 14, "Voter / Admin", ["External Users"], bg="#EFF6FF", border=BORDER_BLUE)
    draw_box(ax, 85, 75, 12, 14, "Observer", ["Independent Auditor"], bg="#EFF6FF", border=BORDER_BLUE)

    # Flows
    draw_arrow(ax, 14, 82, 11, 82, "Credentials")
    draw_arrow(ax, 25, 73, 45, 82, "Validate User")
    draw_arrow(ax, 25, 47, 45, 52, "Store Candidate")
    draw_arrow(ax, 25, 21, 45, 21, "Voter Hash")
    draw_arrow(ax, 39, 26, 61, 52, "Encrypted Vote Payload")
    draw_arrow(ax, 75, 47, 65, 24, "Write Mined Block")
    draw_arrow(ax, 75, 47, 75, 31, "Timestamp & IP")
    draw_arrow(ax, 75, 21, 85, 75, "Fraud Alerts & Risk Score")

    plt.savefig(os.path.join(OUTPUT_DIR, "15_DFD_Level_1.png"), bbox_inches='tight')
    plt.close()

# ----------------------------------------------------------------------
# Generate Mermaid Source Files
# ----------------------------------------------------------------------
def generate_mermaid_sources():
    sources = {
        "01_System_Context.mmd": """graph LR
    Admin[Administrator] -->|Config, Nominations, CSV| App[Decentralized Blockchain Voting System]
    Voter[Registered Voter] -->|Credentials, AES-256 Encrypted Vote| App
    App -->|Cryptographic QR Receipt| Voter
    Observer[Observer / Auditor] -->|Audit Queries, Hash Lookup| App
    App -->|Live Standings, Block Explorer| Observer
    App <-->|SQL Queries| DB[(SQLite 3 Database)]
    App -->|Vote Arrival Telemetry| AI[AI Fraud Radar Service]
    AI -->|Risk Score 0-100%| App
    App <-->|Mined Blocks & Proof-of-Work| Ledger[(SHA-256 Blockchain Ledger)]
""",
        "02_Use_Case.mmd": """graph TD
    Admin((Administrator))
    Voter((Registered Voter))
    Observer((Independent Observer))
    AI((AI Fraud Radar))

    subgraph Decentralized Voting System
        UC1(UC-01: User Login & JWT Auth)
        UC2(UC-02: Create Election Instance)
        UC3(UC-03: Register Candidate Profile)
        UC4(UC-04: Bulk CSV Voter Import)
        UC5(UC-05: Browse Active Ballots)
        UC6(UC-06: Cast Encrypted Ballot)
        UC7(UC-07: Download QR Receipt)
        UC8(UC-08: Mine PoW Block)
        UC9(UC-09: Sign Block with SECP256R1)
        UC10(UC-10: Verify Individual Receipt)
        UC11(UC-11: Full Chain Cryptographic Audit)
        UC12(UC-12: AI Fraud Telemetry Scoring)
    end

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Voter --> UC1
    Voter --> UC5
    Voter --> UC6
    Voter --> UC7
    Observer --> UC10
    Observer --> UC11
    Observer --> UC12

    UC6 -.->|<<include>>| UC8
    UC8 -.->|<<include>>| UC9
    UC6 -.->|<<include>>| UC7
    UC6 -.->|<<extend>>| UC12
""",
        "03_Class_Diagram.mmd": """classDiagram
    class User {
        +int id
        +string email
        +string username
        +string hashed_password
        +string role
        +bool is_active
        +datetime created_at
        +authenticate(password) bool
        +generate_jwt_token() string
    }

    class Election {
        +int id
        +string title
        +string description
        +string status
        +datetime start_time
        +datetime end_time
        +int created_by
        +activate() void
        +close() void
        +get_results() Dict
    }

    class Candidate {
        +int id
        +int election_id
        +string name
        +string party
        +string manifesto
        +string avatar_url
        +int vote_count
        +increment_vote() void
    }

    class VoteReceipt {
        +int id
        +int user_id
        +int election_id
        +int candidate_id
        +string voter_hash
        +string encrypted_vote
        +string tx_hash
        +int block_index
        +string receipt_hash
        +datetime created_at
        +verify_signature() bool
    }

    class Block {
        +int index
        +float timestamp
        +string previous_hash
        +string hash
        +int nonce
        +string merkle_root
        +string signature
        +list transactions
        +calculate_hash() string
        +mine_pow(difficulty) void
    }

    class BlockchainService {
        +list chain
        +list pending_txs
        +int difficulty
        +mine_block() Block
        +is_chain_valid() bool
    }

    User "1" --> "*" Election : creates
    Election "1" --> "*" Candidate : contains
    User "1" --> "*" VoteReceipt : casts
    Election "1" --> "*" VoteReceipt : records
    VoteReceipt "*" --> "1" Block : mined into
    BlockchainService "1" --> "*" Block : manages
""",
        "04_Login_Sequence.mmd": """sequenceDiagram
    autonumber
    actor User as User / Browser
    participant API as Auth Router (/auth/login)
    participant Sec as SecurityService (Bcrypt)
    participant DB as SQLite Database
    participant JWT as JWT Signer (HS256)

    User->>API: POST /api/v1/auth/login {email, password}
    API->>DB: SELECT * FROM users WHERE email = ?
    DB-->>API: Return User Record
    API->>Sec: verify_password(password, hashed_password)
    Sec-->>API: Password Valid (True)
    API->>JWT: create_access_token({sub: id, role})
    JWT-->>API: Return Signed Token String
    API-->>User: 200 OK {access_token, user_profile}
""",
        "05_Registration_Sequence.mmd": """sequenceDiagram
    autonumber
    actor Voter as Voter UI (Register.tsx)
    participant API as Auth Router (/auth/register)
    participant Sec as SecurityService (Bcrypt)
    participant DB as SQLite Database

    Voter->>API: POST /api/v1/auth/register {email, username, password}
    API->>DB: Check Duplicate email or username
    DB-->>API: No Duplicate Found
    API->>Sec: hash_password(password, cost=12)
    Sec-->>API: Return Bcrypt Hash
    API->>DB: INSERT INTO users (role='voter')
    DB-->>API: Commit OK & Return user_id
    API-->>Voter: 201 Created & Automatic Login
""",
        "06_Main_Workflow_Sequence.mmd": """sequenceDiagram
    autonumber
    actor Voter as Voter Dashboard
    participant API as Vote Router (/votes/cast)
    participant AES as Crypto Service (AES-256)
    participant Miner as Blockchain Miner (PoW)
    participant ECDSA as Digital Signer (SECP256R1)
    participant DB as SQLite Database

    Voter->>API: POST /api/v1/votes/cast {election_id, candidate_id}
    API->>DB: Check if Voter already voted
    DB-->>API: Not Voted (Valid)
    API->>AES: encrypt_vote(candidate_id, secret_key)
    AES-->>API: Ciphertext + Auth Tag
    API->>Miner: mine_block(transactions, diff=4)
    Miner->>Miner: Calculate SHA-256 Merkle Root
    Miner->>ECDSA: sign_block_header(block_hash)
    ECDSA-->>Miner: DER-Encoded Signature
    Miner-->>API: Mined Block (Nonce, BlockHash, TxHash)
    API->>DB: INSERT INTO vote_receipts
    DB-->>API: Commit OK
    API-->>Voter: 200 OK -> Render QRCodeModal with Receipt
""",
        "07_API_Sequence.mmd": """sequenceDiagram
    autonumber
    participant Client as Client Browser (Axios)
    participant Gateway as FastAPI ASGI Gateway
    participant AI as AI Fraud Radar Service
    participant WS as WebSockets Broadcaster
    participant Observer as Observer Live Desk

    Client->>Gateway: HTTP Request with Bearer Token
    Gateway->>AI: Log Timestamp (t) & Client IP
    AI->>AI: Check Arrival Interval (<500ms burst)
    AI-->>Gateway: Return Fraud Risk Score (0-100%)
    Gateway->>WS: Broadcast Tally & Risk Score Update
    WS-->>Observer: Real-time Recharts Live Update
    Gateway-->>Client: HTTP JSON Response (200 OK)
""",
        "08_Login_Activity.mmd": """stateDiagram-v2
    [*] --> EnterCredentials
    EnterCredentials --> TransmitRequest: Submit Form
    TransmitRequest --> VerifyHash: Query Database
    state CheckCredentials <<choice>>
    VerifyHash --> CheckCredentials
    CheckCredentials --> ErrorToast: [Invalid]
    ErrorToast --> EnterCredentials: Retry
    CheckCredentials --> IssueToken: [Valid]
    state CheckRole <<choice>>
    IssueToken --> CheckRole
    CheckRole --> AdminStudio: [role == 'admin']
    CheckRole --> VoterPortal: [role == 'voter']
    CheckRole --> ObserverDesk: [role == 'observer']
    AdminStudio --> [*]
    VoterPortal --> [*]
    ObserverDesk --> [*]
""",
        "09_Main_Workflow_Activity.mmd": """stateDiagram-v2
    [*] --> Authenticate
    Authenticate --> FetchElections
    FetchElections --> CheckVoted
    state CheckVoted <<choice>>
    CheckVoted --> AlreadyVoted: [voted == true]
    AlreadyVoted --> ViewReceipts: Navigate /receipts
    CheckVoted --> SelectCandidate: [voted == false]
    SelectCandidate --> EncryptAES256: Confirm Choice
    EncryptAES256 --> MineBlock: PoW Consensus (Diff 4)
    MineBlock --> StoreReceipt: Save to SQLite & Chain
    StoreReceipt --> ShowQRModal: Display Receipt & QR
    ShowQRModal --> [*]
    ViewReceipts --> [*]
""",
        "10_ER_Diagram.mmd": """erDiagram
    USERS ||--o{ ELECTIONS : creates
    ELECTIONS ||--|{ CANDIDATES : contains
    USERS ||--o{ VOTE_RECEIPTS : casts
    ELECTIONS ||--o{ VOTE_RECEIPTS : records
    USERS ||--o{ AUDIT_LOGS : generates

    USERS {
        int id PK
        string email UK
        string username UK
        string hashed_password
        string role
        boolean is_active
        datetime created_at
    }

    ELECTIONS {
        int id PK
        string title
        string description
        string status
        datetime start_time
        datetime end_time
        int created_by FK
    }

    CANDIDATES {
        int id PK
        int election_id FK
        string name
        string party
        string manifesto
        string avatar_url
        int vote_count
    }

    VOTE_RECEIPTS {
        int id PK
        int user_id FK
        int election_id FK
        int candidate_id FK
        string voter_hash UK
        string encrypted_vote
        string tx_hash UK
        int block_index
        string receipt_hash UK
        datetime created_at
    }

    AUDIT_LOGS {
        int id PK
        int user_id FK
        string user_email
        string action
        string details
        string ip_address
        datetime timestamp
    }
""",
        "11_Deployment.mmd": """graph TB
    subgraph ClientDevice [Client Device Workstation / Smartphone]
        Browser[Modern Web Browser]
        SPA[React 19 Single Page App]
        LocalStorage[(LocalStorage Fallback Store)]
    end

    subgraph VercelEdge [Vercel Global Edge CDN]
        CDN[Edge Reverse Proxy & Static Cache]
        Rewrites[Client SPA URL Rewrites]
    end

    subgraph CloudServer [Render Cloud Linux Container]
        ASGI[Uvicorn ASGI Worker Pool]
        FastAPI[FastAPI Application Backend]
        BlockchainCore[Cryptographic Ledger Engine]
        AIRadar[AI Fraud Radar Service]
    end

    subgraph StorageNode [Persistent Database Volume]
        SQLite[(SQLite 3 Database WAL Mode)]
    end

    Browser --> CDN
    CDN --> FastAPI
    FastAPI --> BlockchainCore
    FastAPI --> AIRadar
    FastAPI --> SQLite
    Browser -.->|Offline Fallback| LocalStorage
""",
        "12_Component.mmd": """graph TD
    subgraph Presentation Tier
        UI[VoterDashboard / ElectionStudio / ObserverPortal]
        QR[QRCodeModal Component]
    end

    subgraph Application Tier
        AuthAPI[Auth Router & Bcrypt Service]
        VoteAPI[Vote Processing Router]
        AdminAPI[Election Studio Router]
        AIComponent[AI Fraud Radar Anomaly Engine]
    end

    subgraph Cryptographic Core
        PoWMiner[Proof-of-Work Mining Loop]
        MerkleTree[SHA-256 Merkle Root Engine]
        ECDSASigner[SECP256R1 Digital Signer]
    end

    subgraph Persistence Tier
        DBORM[SQLAlchemy 2.0 ORM Engine]
        SQLiteDB[(SQLite 3 Database File)]
        ChainLedger[(Immutable Blockchain Store)]
    end

    UI --> AuthAPI
    UI --> VoteAPI
    UI --> AdminAPI
    VoteAPI --> PoWMiner
    PoWMiner --> MerkleTree
    PoWMiner --> ECDSASigner
    VoteAPI --> AIComponent
    VoteAPI --> DBORM
    PoWMiner --> ChainLedger
    DBORM --> SQLiteDB
""",
        "13_Module.mmd": """graph TD
    subgraph Root [blockchain-voting-system]
        subgraph Frontend [frontend/src/]
            F_Comp[components/]
            F_Pages[pages/]
            F_Context[context/]
            F_Services[services/api.ts]
        end

        subgraph Backend [backend/app/]
            B_API[api/]
            B_Core[core/]
            B_Models[models/]
            B_Services[services/]
            B_Main[main.py]
        end

        subgraph Blockchain [backend/blockchain/]
            BC_Chain[chain.py]
            BC_Block[block.py]
            BC_Crypto[cryptography.py]
            BC_Wallet[wallet.py]
        end

        subgraph Storage [backend/storage/]
            DB_File[(voting_system.db)]
        end
    end

    F_Services --> B_API
    B_API --> B_Services
    B_Services --> BC_Chain
    BC_Chain --> BC_Block
    BC_Chain --> BC_Crypto
    B_Services --> B_Models
    B_Models --> DB_File
""",
        "14_DFD_Level_0.mmd": """graph LR
    Admin[Administrator] -->|Election Details & Candidates| System((0.0 Decentralized Blockchain Voting System))
    Voter[Registered Voter] -->|Credentials & Encrypted Vote| System
    System -->|Cryptographic QR Receipt| Voter
    Observer[Independent Observer] -->|Tally & Hash Audit Requests| System
    System -->|Live Tallies & Chain Proofs| Observer
    System <-->|Read / Write Records| DB[(D1: SQLite Database)]
    System <-->|Append / Read Blocks| Chain[(D2: Blockchain Ledger)]
""",
        "15_DFD_Level_1.mmd": """graph TD
    Voter[Registered Voter] -->|Credentials| P1((1.0 User Authentication))
    Admin[Administrator] -->|Election Data & Candidates| P2((2.0 Election Management))
    Voter -->|Vote Selection| P3((3.0 Ballot Encryption))
    P3 -->|Encrypted Payload| P4((4.0 Block Mining & Consensus))
    P4 -->|Timestamp & IP| P5((5.0 AI Fraud Telemetry))

    P1 <-->|User Records| D1[(D1: Users Store)]
    P2 <-->|Elections / Candidates| D2[(D2: Elections Store)]
    P3 <-->|Voter Hash Check| D3[(D3: Vote Receipts Store)]
    P4 -->|Mined Block & Receipt| D4[(D4: Blockchain Ledger)]
    P5 -->|Risk Score & Alerts| Observer[Independent Observer]
    P4 -->|QR Receipt Hash| Voter
"""
    }

    for filename, code in sources.items():
        with open(os.path.join(SOURCES_DIR, filename), "w", encoding="utf-8") as f:
            f.write(code)

def main():
    print("Generating 15 Professional High-Resolution PNG Diagrams...")
    generate_system_context()
    generate_use_case()
    generate_class_diagram()
    generate_login_sequence()
    generate_registration_sequence()
    generate_main_vote_sequence()
    generate_api_sequence()
    generate_login_activity()
    generate_voter_activity()
    generate_er_diagram()
    generate_deployment_diagram()
    generate_component_diagram()
    generate_module_diagram()
    generate_dfd_level_0()
    generate_dfd_level_1()
    print("Generating Mermaid editable source files...")
    generate_mermaid_sources()
    print("All diagrams and sources generated successfully in UML_Diagrams/")

if __name__ == "__main__":
    main()
