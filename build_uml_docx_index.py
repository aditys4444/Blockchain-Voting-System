import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def build_uml_index_docx():
    doc = docx.Document()

    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.0)

    COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Navy
    COLOR_SECONDARY = RGBColor(0, 128, 128)  # Teal Accent
    COLOR_DARK = RGBColor(15, 23, 42)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(24)
    p_title.paragraph_format.space_after = Pt(12)
    run_t = p_title.add_run("UML DIAGRAM SET SPECIFICATION & MASTER INDEX")
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(20)
    run_t.bold = True
    run_t.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(20)
    run_s = p_sub.add_run("Decentralized Blockchain Voting System with AI Fraud Radar\nAuthor: Aditya Yadav (B.Sc Computer Science) • Academic Year 2026-2027")
    run_s.font.name = "Times New Roman"
    run_s.font.size = Pt(12)
    run_s.font.color.rgb = COLOR_SECONDARY

    # Summary Table
    headers = ["Diagram #", "File Name", "Diagram Title", "Related Chapter", "Requirements"]
    rows = [
        ["Figure 5.1", "01_System_Context.png", "System Context Diagram", "Ch 1 & Ch 5", "System Boundaries & Actors"],
        ["Figure 5.2", "02_Use_Case.png", "System Use Case Diagram", "Ch 3 & Ch 5", "FR-01 to FR-25 Mapping"],
        ["Figure 5.3", "03_Class_Diagram.png", "System Class Diagram Architecture", "Ch 5 & Ch 7", "SQLAlchemy & Crypto Classes"],
        ["Figure 5.4", "04_Login_Sequence.png", "Sequence: User Authentication", "Ch 3 & Ch 5", "FR-01 (Bcrypt & JWT)"],
        ["Figure 5.5", "05_Registration_Sequence.png", "Sequence: Voter Self-Registration", "Ch 3 & Ch 5", "FR-02 (Identity Registration)"],
        ["Figure 5.6", "06_Main_Workflow_Sequence.png", "Sequence: Encrypted Vote & Mining", "Ch 3 & Ch 5", "FR-09, FR-10, FR-15, FR-16"],
        ["Figure 5.7", "07_API_Sequence.png", "Sequence: API & AI Telemetry", "Ch 5 & Ch 6", "FR-21 to FR-25 (AI Radar)"],
        ["Figure 5.8", "08_Login_Activity.png", "Activity: User Login & Role Guard", "Ch 5", "FR-01, FR-03 (Routing)"],
        ["Figure 5.9", "09_Main_Workflow_Activity.png", "Activity: Voter Main Lifecycle", "Ch 5", "FR-09 to FR-12 (Voter Journey)"],
        ["Figure 5.10", "10_ER_Diagram.png", "Entity-Relationship (ER) Data Model", "Ch 5 & Ch 7", "users, elections, candidates"],
        ["Figure 5.11", "11_Deployment.png", "System Deployment Diagram", "Ch 6", "Vercel CDN, Render, SQLite WAL"],
        ["Figure 5.12", "12_Component.png", "UML Component Diagram", "Ch 6 & Ch 7", "UI, API, Engine, Database"],
        ["Figure 5.13", "13_Module.png", "Package & Directory Module Diagram", "Ch 7", "frontend, backend, blockchain"],
        ["Figure 5.14", "14_DFD_Level_0.png", "Data Flow Diagram (Level 0 Context)", "Ch 5 & Ch 6", "Entity Data Transformations"],
        ["Figure 5.15", "15_DFD_Level_1.png", "Data Flow Diagram (Level 1 Decomposition)", "Ch 5 & Ch 6", "Functional Sub-Process Data Flow"]
    ]

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    for i, h_text in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h_text
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, r_data in enumerate(rows):
        cells = table.rows[r_idx + 1].cells
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cells[c_idx].text = str(val)
            set_cell_background(cells[c_idx], bg_col)
            set_cell_margins(cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = cells[c_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9)
                r.font.color.rgb = COLOR_DARK

    set_table_borders(table, "CBD5E1")

    # Col Widths
    col_w = [1.1, 1.6, 2.0, 1.1, 1.4]
    for row in table.rows:
        for c_idx, w in enumerate(col_w):
            row.cells[c_idx].width = Inches(w)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Detailed Descriptions
    descriptions = [
        ("Figure 5.1: System Context Diagram", "Demarcates external entities (Administrator, Voter, Observer) from internal services (React SPA, FastAPI, SECP256R1 ECDSA, Proof-of-Work Miner, AI Radar) and persistence stores (SQLite WAL and Blockchain Ledger)."),
        ("Figure 5.2: System Use Case Diagram", "Formalizes functional interactions between human and automated actors and the 12 core system use cases with <<include>> and <<extend>> relationships."),
        ("Figure 5.3: System Class Diagram Architecture", "Defines the object-oriented structure, class attributes, method signatures, and cardinalities for User, Election, Candidate, VoteReceipt, Block, and BlockchainService classes."),
        ("Figure 5.4: Sequence Diagram for User Login", "Visualizes the synchronous authentication sequence between the client, FastAPI Auth Router, Bcrypt security service, SQLite database, and JWT signer."),
        ("Figure 5.5: Sequence Diagram for Voter Registration", "Models the registration sequence verifying input formatting, enforcing duplicate identity checks, salting passwords, and creating user records."),
        ("Figure 5.6: Sequence Diagram for Encrypted Voting & Mining", "Traces ballot submission, AES-256 GCM encryption, Merkle tree root computation, Proof-of-Work mining, SECP256R1 digital signing, and QR receipt generation."),
        ("Figure 5.7: Sequence Diagram for API Interaction & AI Fraud Telemetry", "Models how API requests feed the arrival velocity engine, calculate burst scores (<500ms), and push WebSocket live tallies to observers."),
        ("Figure 5.8: Activity Diagram for User Login", "Illustrates decision branches, credential checks, error toasts, and role-based redirects across `/admin/elections`, `/voter`, and `/observer`."),
        ("Figure 5.9: Activity Diagram for Voter Main Workflow", "Outlines the voter lifecycle from ballot selection and double-vote validation to AES encryption, block mining, and QR receipt download."),
        ("Figure 5.10: Entity-Relationship (ER) Diagram", "Defines the relational data schema in SQLite with primary keys, foreign keys, and 1:N cardinalities across users, elections, candidates, vote_receipts, and audit_logs."),
        ("Figure 5.11: System Deployment Diagram", "Maps software artifacts across execution nodes: Client Browser Node (React SPA + fallback), Vercel Global Edge CDN, Render Cloud Container (FastAPI ASGI), and SQLite Storage Volume."),
        ("Figure 5.12: UML Component Diagram", "Details modular component dependencies between UI Presentation, REST API Layer, Security Service, Blockchain Engine, AI Fraud Radar, and Database Storage."),
        ("Figure 5.13: Package & Directory Module Diagram", "Maps physical repository organization across `frontend/src/`, `backend/app/`, and `backend/blockchain/`."),
        ("Figure 5.14: Data Flow Diagram (Level 0 Context)", "Visualizes high-level data inputs, transformations, and outputs flowing between external actors, Process 0.0, and data stores (D1 SQLite, D2 Blockchain Ledger)."),
        ("Figure 5.15: Data Flow Diagram (Level 1 Decomposition)", "Decomposes Process 0.0 into five functional sub-processes: 1.0 Auth, 2.0 Election Management, 3.0 Ballot Encryption, 4.0 Block Mining, and 5.0 AI Fraud Telemetry.")
    ]

    for title, desc in descriptions:
        p_h = doc.add_paragraph()
        p_h.paragraph_format.space_before = Pt(8)
        p_h.paragraph_format.space_after = Pt(2)
        p_h.paragraph_format.keep_with_next = True
        run_h = p_h.add_run(title)
        run_h.font.name = "Times New Roman"
        run_h.font.size = Pt(11)
        run_h.bold = True
        run_h.font.color.rgb = COLOR_PRIMARY

        p_d = doc.add_paragraph()
        p_d.paragraph_format.space_after = Pt(6)
        p_d.paragraph_format.line_spacing = 1.3
        run_d = p_d.add_run(desc)
        run_d.font.name = "Times New Roman"
        run_d.font.size = Pt(10)
        run_d.font.color.rgb = COLOR_DARK

    out_file = os.path.join("UML_Diagrams", "UML_Diagram_Index.docx")
    doc.save(out_file)
    print(f"Index document successfully saved to: {out_file}")

if __name__ == "__main__":
    build_uml_index_docx()
