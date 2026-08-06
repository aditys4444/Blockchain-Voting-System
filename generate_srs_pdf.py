import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page count in footer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4B5563"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Software Requirements Specification — Blockchain Voting System")
            self.setStrokeColor(colors.HexColor("#E5E7EB"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, footer_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — IEEE 830 STANDARD SPECIFICATION")
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * inch - 54, 48)
        
        self.restoreState()

def create_srs_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1E3A8A")    # Navy Blue
    SECONDARY = colors.HexColor("#2563EB")  # Accent Blue
    TEXT_DARK = colors.HexColor("#1F2937")  # Dark Slate
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Light background
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    
    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        leftIndent=15,
        spaceAfter=4
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []

    # Title Block
    story.append(Paragraph("Software Requirements Specification (SRS)", title_style))
    story.append(Paragraph("Full-Stack Cryptographic Blockchain Voting System", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=12))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Project Title:</b> Cryptographic Blockchain Voting System", meta_style), Paragraph("<b>Status:</b> Approved", meta_style)],
        [Paragraph("<b>Document Version:</b> 1.0.0", meta_style), Paragraph("<b>Standard:</b> IEEE Std 830-1998", meta_style)],
        [Paragraph("<b>Target Audience:</b> Engineers, Auditors, Cryptographers", meta_style), Paragraph("<b>Date:</b> July 2026", meta_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Section 1
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=SECONDARY, spaceAfter=8))
    
    story.append(Paragraph("1.1 Purpose", h2_style))
    story.append(Paragraph(
        "The purpose of this Software Requirements Specification (SRS) document is to define the functional, "
        "non-functional, security, and architectural requirements for the Full-Stack Cryptographic Blockchain Voting System. "
        "This document serves as the formal baseline for development, verification, and independent auditing.", body_style
    ))

    story.append(Paragraph("1.2 Scope", h2_style))
    story.append(Paragraph(
        "The Blockchain Voting System is a production-grade digital voting platform engineered to guarantee end-to-end "
        "confidentiality, immutability, transparency, and anti-fraud detection. The system features:", body_style
    ))
    story.append(Paragraph("• <b>AES-256 GCM Payload Encryption:</b> Ensures vote secrecy before transaction broadcast.", bullet_style))
    story.append(Paragraph("• <b>ECDSA SECP256R1 Signatures:</b> Provides mathematical proof of vote authenticity.", bullet_style))
    story.append(Paragraph("• <b>SHA-256 Merkle Tree Ledger:</b> Aggregates transactions into verifiable binary hash trees.", bullet_style))
    story.append(Paragraph("• <b>Proof-of-Work (PoW) Consensus:</b> Requires zero-prefix nonce calculation to prevent tampering.", bullet_style))
    story.append(Paragraph("• <b>AI Fraud Radar Module:</b> Computes dynamic threat risk scores (0-100%) based on velocity bursts.", bullet_style))
    story.append(Paragraph("• <b>QR Code Verification Receipts:</b> Enables voter auditability without revealing vote selection.", bullet_style))

    story.append(Paragraph("1.3 Definitions & Acronyms", h2_style))
    def_data = [
        [Paragraph("Term / Acronym", table_header_style), Paragraph("Definition", table_header_style)],
        [Paragraph("AES-256 GCM", table_cell_style), Paragraph("Advanced Encryption Standard with 256-bit key in Galois/Counter Mode.", table_cell_style)],
        [Paragraph("ECDSA", table_cell_style), Paragraph("Elliptic Curve Digital Signature Algorithm (SECP256R1 curve).", table_cell_style)],
        [Paragraph("PoW", table_cell_style), Paragraph("Proof-of-Work consensus algorithm requiring nonce discovery.", table_cell_style)],
        [Paragraph("Merkle Tree", table_cell_style), Paragraph("Binary hash tree for efficient transaction payload integrity verification.", table_cell_style)],
        [Paragraph("RBAC", table_cell_style), Paragraph("Role-Based Access Control (Admin, Voter, Observer).", table_cell_style)],
        [Paragraph("JWT", table_cell_style), Paragraph("JSON Web Token standard for stateless session authorization.", table_cell_style)]
    ]
    def_table = Table(def_data, colWidths=[120, 384])
    def_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(def_table)
    story.append(Spacer(1, 10))

    # Section 2
    story.append(Paragraph("2. Overall Description", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=SECONDARY, spaceAfter=8))
    
    story.append(Paragraph("2.1 Product Perspective", h2_style))
    story.append(Paragraph(
        "The application operates as a decoupled full-stack architecture comprising a React 19 single-page client, "
        "an asynchronous FastAPI backend server, a SQLite relational database, and an embedded custom Python cryptographic blockchain.", body_style
    ))

    story.append(Paragraph("2.2 User Classes & Characteristics", h2_style))
    story.append(Paragraph("<b>1. Admin:</b> Manages election lifecycles, candidates, voter CSV rosters, audit logs, and AI risk metrics.", bullet_style))
    story.append(Paragraph("<b>2. Voter:</b> Views active elections, submits encrypted 1-click votes, receives QR code receipts, and verifies block inclusion.", bullet_style))
    story.append(Paragraph("<b>3. Observer:</b> Inspects public blockchain explorer, Merkle roots, live WebSockets tallies, and block signatures.", bullet_style))

    # Section 3
    story.append(PageBreak())
    story.append(Paragraph("3. Specific System Requirements", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=SECONDARY, spaceAfter=8))

    story.append(Paragraph("3.1 Functional Requirements", h2_style))
    
    req_data = [
        [Paragraph("Req ID", table_header_style), Paragraph("Module", table_header_style), Paragraph("Specification Description", table_header_style)],
        [Paragraph("FR-AUTH-01", table_cell_style), Paragraph("Authentication", table_cell_style), Paragraph("Supports login via username or email with bcrypt password verification.", table_cell_style)],
        [Paragraph("FR-AUTH-03", table_cell_style), Paragraph("Authentication", table_cell_style), Paragraph("Issues short-lived access JWT and refresh JWT tokens for stateless RBAC.", table_cell_style)],
        [Paragraph("FR-ELEC-01", table_cell_style), Paragraph("Elections", table_cell_style), Paragraph("Admin CRUD operations and state transitions (Draft -> Active -> Completed).", table_cell_style)],
        [Paragraph("FR-VOTE-01", table_cell_style), Paragraph("Voting Engine", table_cell_style), Paragraph("Strict 1-vote constraint per user per election backed by database indices.", table_cell_style)],
        [Paragraph("FR-VOTE-02", table_cell_style), Paragraph("Voting Engine", table_cell_style), Paragraph("AES-256 GCM encryption of vote selection payload before transaction queueing.", table_cell_style)],
        [Paragraph("FR-VOTE-03", table_cell_style), Paragraph("Voting Engine", table_cell_style), Paragraph("ECDSA SECP256R1 digital keypair generation and transaction signing per vote.", table_cell_style)],
        [Paragraph("FR-BC-02", table_cell_style), Paragraph("Blockchain", table_cell_style), Paragraph("Proof-of-Work mining with difficulty zero-prefix hash validation.", table_cell_style)],
        [Paragraph("FR-BC-03", table_cell_style), Paragraph("Blockchain", table_cell_style), Paragraph("Computes and verifies binary Merkle Tree Root for all transactions in a block.", table_cell_style)],
        [Paragraph("FR-RCPT-01", table_cell_style), Paragraph("Receipts", table_cell_style), Paragraph("Generates downloadable PDF/PNG QR Receipts with receipt SHA-256 hash.", table_cell_style)],
        [Paragraph("FR-AI-01", table_cell_style), Paragraph("AI Fraud Radar", table_cell_style), Paragraph("Detects velocity bursts (<2s apart) and IP address concentration (>5 votes).", table_cell_style)],
        [Paragraph("FR-AI-04", table_cell_style), Paragraph("AI Fraud Radar", table_cell_style), Paragraph("Computes unified threat score (0-100%) categorized as Low/Med/High/Critical.", table_cell_style)]
    ]
    req_table = Table(req_data, colWidths=[75, 95, 334])
    req_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (2,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(req_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.2 Non-Functional Requirements (NFR)", h2_style))
    story.append(Paragraph("• <b>NFR-SEC-01:</b> Zero plaintext candidate selections or user identities in mined blocks.", bullet_style))
    story.append(Paragraph("• <b>NFR-PERF-01:</b> API endpoint response latencies under 200ms.", bullet_style))
    story.append(Paragraph("• <b>NFR-PERF-02:</b> Proof-of-Work mining completes in 1.0 - 3.0s (difficulty = 2).", bullet_style))
    story.append(Paragraph("• <b>NFR-PERF-03:</b> Real-time WebSockets tally broadcast latency under 100ms.", bullet_style))
    story.append(Paragraph("• <b>NFR-REL-01:</b> Block payload immutability; downstream chain fails validation on tampering.", bullet_style))

    # Section 4
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Verification & Compliance Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=SECONDARY, spaceAfter=8))
    
    matrix_data = [
        [Paragraph("Req ID", table_header_style), Paragraph("Verification Method", table_header_style), Paragraph("Acceptance Criteria / Status", table_header_style)],
        [Paragraph("FR-AUTH-02", table_cell_style), Paragraph("Pytest Unit Test", table_cell_style), Paragraph("Passwords hashed via bcrypt (salt cost >= 12). Passed.", table_cell_style)],
        [Paragraph("FR-VOTE-01", table_cell_style), Paragraph("Integration Test", table_cell_style), Paragraph("Duplicate vote rejected with HTTP 400 Bad Request. Passed.", table_cell_style)],
        [Paragraph("FR-VOTE-02", table_cell_style), Paragraph("Crypto Audit", table_cell_style), Paragraph("Payload unreadable without 256-bit AES GCM key. Passed.", table_cell_style)],
        [Paragraph("FR-BC-05", table_cell_style), Paragraph("Ledger Audit Endpoint", table_cell_style), Paragraph("is_chain_valid returns true with 0 anomalies. Passed.", table_cell_style)]
    ]
    matrix_table = Table(matrix_data, colWidths=[80, 140, 284])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (2,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(matrix_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated SRS PDF document at: {output_filename}")

if __name__ == "__main__":
    output_path = sys.argv[1] if len(sys.argv) > 1 else "Blockchain_Voting_System_SRS.pdf"
    create_srs_pdf(output_path)
