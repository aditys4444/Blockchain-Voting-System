import docx

doc = docx.Document('PROJECT_REPORT_75_PAGES.docx')
page_breaks = 0
for p in doc.paragraphs:
    if 'w:type="page"' in p._element.xml:
        page_breaks += 1

print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")
print(f"Total Embedded Images: {len(doc.inline_shapes)}")
print(f"Total Page Breaks: {page_breaks}")
print(f"Total Physical Pages in MS Word: {page_breaks + 1}")
words = sum(len(p.text.split()) for p in doc.paragraphs) + sum(len(c.text.split()) for t in doc.tables for r in t.rows for c in r.cells)
print(f"Total Word Count: {words}")

