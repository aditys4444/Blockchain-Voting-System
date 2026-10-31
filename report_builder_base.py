import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="334155"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="8" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def set_frame_border(table, color="000000", sz="12"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="none"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

class AcademicReportBuilder:
    def __init__(self, filename="PROJECT_REPORT_75_PAGES.docx"):
        self.filename = filename
        self.doc = docx.Document()
        self.setup_palette()
        self.setup_page_geometry()
        self.setup_page_borders()
        self.setup_heading_styles()
        self.setup_header_footer()

    def setup_palette(self):
        self.COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Navy #1B365D
        self.COLOR_SECONDARY = RGBColor(0, 128, 128)  # Teal Accent #008080
        self.COLOR_DARK = RGBColor(0, 0, 0)           # Pure Black for maximum contrast
        self.COLOR_MUTED = RGBColor(71, 85, 105)      # Slate Muted #475569

    def setup_page_geometry(self):
        section = self.doc.sections[0]
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)

    def setup_page_borders(self):
        for section in self.doc.sections:
            sectPr = section._sectPr
            existing = sectPr.xpath('./w:pgBorders')
            for e in existing:
                sectPr.remove(e)
            pb = parse_xml(
                f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page" w:zOrder="front">'
                f'<w:top w:val="single" w:sz="12" w:space="30" w:color="000000"/>'
                f'<w:bottom w:val="single" w:sz="12" w:space="30" w:color="000000"/>'
                f'<w:left w:val="single" w:sz="12" w:space="30" w:color="000000"/>'
                f'<w:right w:val="single" w:sz="12" w:space="30" w:color="000000"/>'
                f'</w:pgBorders>'
            )
            sectPr.append(pb)

    def setup_heading_styles(self):
        # Heading 1: Chapter Title (16 pt Bold, Navy #1B365D)
        try:
            h1 = self.doc.styles['Heading 1']
            h1.font.name = 'Times New Roman'
            h1.font.size = Pt(16)
            h1.font.bold = True
            h1.font.color.rgb = self.COLOR_PRIMARY
            h1.paragraph_format.space_before = Pt(20)
            h1.paragraph_format.space_after = Pt(12)
            h1.paragraph_format.keep_with_next = True
        except Exception:
            pass

        # Heading 2: Section Heading (14 pt Bold, Teal #008080)
        try:
            h2 = self.doc.styles['Heading 2']
            h2.font.name = 'Times New Roman'
            h2.font.size = Pt(14)
            h2.font.bold = True
            h2.font.color.rgb = self.COLOR_SECONDARY
            h2.paragraph_format.space_before = Pt(14)
            h2.paragraph_format.space_after = Pt(6)
            h2.paragraph_format.keep_with_next = True
        except Exception:
            pass

        # Heading 3: Subsection Heading (12 pt Bold, Deep Dark)
        try:
            h3 = self.doc.styles['Heading 3']
            h3.font.name = 'Times New Roman'
            h3.font.size = Pt(12)
            h3.font.bold = True
            h3.font.color.rgb = self.COLOR_PRIMARY
            h3.paragraph_format.space_before = Pt(10)
            h3.paragraph_format.space_after = Pt(4)
            h3.paragraph_format.keep_with_next = True
        except Exception:
            pass

    def setup_header_footer(self):
        section = self.doc.sections[0]
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "DECENTRALIZED BLOCKCHAIN VOTING SYSTEM WITH AI FRAUD RADAR"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.style.font.name = "Times New Roman"
        hp.style.font.size = Pt(8.5)
        hp.style.font.color.rgb = self.COLOR_MUTED

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = ""
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_inst = fp.add_run("Department of B.Sc Computer Science • Academic Project Report")
        r_inst.font.name = "Times New Roman"
        r_inst.font.size = Pt(8.5)
        r_inst.font.color.rgb = self.COLOR_MUTED

        fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.02), WD_TAB_ALIGNMENT.RIGHT)
        r_pg = fp.add_run("\tPage ")
        r_pg.font.name = "Times New Roman"
        r_pg.font.size = Pt(8.5)
        r_pg.font.color.rgb = self.COLOR_MUTED

        # Insert dynamic Word PAGE field
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        r_pg._r.append(fld)

    def add_title(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(28)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(20)
        run.bold = True
        run.font.color.rgb = self.COLOR_PRIMARY
        return p

    def add_subtitle(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(20)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.italic = True
        run.font.color.rgb = self.COLOR_MUTED
        return p

    def add_chapter_title(self, text):
        p = self.doc.add_paragraph(style='Heading 1')
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.bold = True
        run.font.color.rgb = self.COLOR_PRIMARY
        return p

    def add_section_heading(self, text):
        p = self.doc.add_paragraph(style='Heading 2')
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = self.COLOR_SECONDARY
        return p

    def add_subsection_heading(self, text):
        p = self.doc.add_paragraph(style='Heading 3')
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = self.COLOR_PRIMARY
        return p

    def add_p(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = self.COLOR_DARK
        return p

    def add_bullet_item(self, lead, text):
        p = self.doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run_lead = p.add_run(lead + ": ")
        run_lead.font.name = 'Times New Roman'
        run_lead.font.size = Pt(12)
        run_lead.bold = True
        run_lead.font.color.rgb = self.COLOR_PRIMARY
        run_text = p.add_run(text)
        run_text.font.name = 'Times New Roman'
        run_text.font.size = Pt(12)
        run_text.font.color.rgb = self.COLOR_DARK
        return p

    def add_code_block(self, code_text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(code_text)
        run.font.name = 'Courier New'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_diagram_box(self, fig_num, fig_title, diagram_type, details_list, image_filename=None, img_width=4.6):
        if image_filename:
            image_path = os.path.join(os.getcwd(), "UML_Diagrams", image_filename)
            if os.path.exists(image_path):
                img_table = self.doc.add_table(rows=1, cols=1)
                img_table.alignment = WD_TABLE_ALIGNMENT.CENTER
                img_table.autofit = False
                trPr = img_table.rows[0]._tr.get_or_add_trPr()
                trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
                cell_img = img_table.rows[0].cells[0]
                cell_img.width = Inches(5.8)
                set_cell_background(cell_img, "FFFFFF")
                set_cell_margins(cell_img, top=30, bottom=30, left=30, right=30)
                p_img = cell_img.paragraphs[0]
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(0)
                p_img.paragraph_format.space_after = Pt(0)
                run_img = p_img.add_run()
                run_img.add_picture(image_path, width=Inches(img_width))
                set_frame_border(img_table, color="000000", sz="10")

        p_caption = self.doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_before = Pt(4)
        p_caption.paragraph_format.space_after = Pt(4)
        p_caption.paragraph_format.keep_with_next = True
        run_cap = p_caption.add_run(f"Figure {fig_num}: {fig_title}")
        run_cap.font.name = 'Times New Roman'
        run_cap.font.size = Pt(10.5)
        run_cap.bold = True
        run_cap.font.color.rgb = self.COLOR_PRIMARY

        table = self.doc.add_table(rows=2, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        cell_hdr = table.rows[0].cells[0]
        cell_hdr.width = Inches(6.0)
        cell_hdr.text = f"ARCHITECTURAL SPECIFICATION & DIAGRAM SCHEMA — {diagram_type.upper()}"
        set_cell_background(cell_hdr, "1B365D")
        set_cell_margins(cell_hdr, top=40, bottom=40, left=80, right=80)
        p_hdr = cell_hdr.paragraphs[0]
        p_hdr.paragraph_format.space_before = Pt(0)
        p_hdr.paragraph_format.space_after = Pt(0)
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p_hdr.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

        cell_body = table.rows[1].cells[0]
        cell_body.width = Inches(6.0)
        set_cell_background(cell_body, "F8FAFC")
        set_cell_margins(cell_body, top=40, bottom=40, left=80, right=80)
        p_b = cell_body.paragraphs[0]
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(2)
        p_b.text = "Architectural Composition & Structural Logic:"
        p_b.runs[0].font.bold = True
        p_b.runs[0].font.size = Pt(8.5)

        for item in details_list:
            p_item = cell_body.add_paragraph(style='List Bullet')
            p_item.paragraph_format.space_before = Pt(0)
            p_item.paragraph_format.space_after = Pt(1)
            p_item.paragraph_format.line_spacing = 1.05
            run_item = p_item.add_run(item)
            run_item.font.name = 'Times New Roman'
            run_item.font.size = Pt(8)
            run_item.font.color.rgb = self.COLOR_DARK

        set_table_borders(table, "94A3B8")
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def add_styled_table(self, headers, rows, col_widths=None, caption=None):
        if caption:
            p_caption = self.doc.add_paragraph()
            p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_caption.paragraph_format.space_before = Pt(6)
            p_caption.paragraph_format.space_after = Pt(3)
            p_caption.paragraph_format.keep_with_next = True
            run_cap = p_caption.add_run(caption)
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(10.5)
            run_cap.bold = True
            run_cap.font.color.rgb = self.COLOR_PRIMARY

        table = self.doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header row configuration
        hdr_tr = table.rows[0]._tr.get_or_add_trPr()
        hdr_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        hdr_tr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "1B365D")
            set_cell_margins(hdr_cells[i], top=60, bottom=60, left=100, right=100)
            p = hdr_cells[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

        for row_idx, row_data in enumerate(rows):
            row = table.rows[row_idx + 1]
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            row_cells = row.cells
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                set_cell_background(row_cells[col_idx], bg_color)
                set_cell_margins(row_cells[col_idx], top=50, bottom=50, left=100, right=100)
                p = row_cells[col_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(1.5)
                p.paragraph_format.line_spacing = 1.05
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9)
                    r.font.color.rgb = self.COLOR_DARK

        set_table_borders(table, "334155")

        if col_widths:
            for row in table.rows:
                for col_idx, w in enumerate(col_widths):
                    row.cells[col_idx].width = Inches(w)

        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return table

    def add_page_break(self):
        self.doc.add_page_break()

    def save(self):
        self.setup_page_borders()
        self.doc.save(self.filename)
        print(f"Document successfully written to {self.filename}")
