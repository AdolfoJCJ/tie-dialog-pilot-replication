
import os, json
from fpdf import FPDF

def build_pdf(fig_paths, tables, out_pdf):
    # Minimal PDF builder to keep dependencies light; install fpdf if needed.
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, "TIE–Dialog Pilot — Replication Report", ln=True)
    pdf.set_font("Arial", size=10)
    for title, table_path in tables.items():
        pdf.cell(0, 8, f"{title}: {table_path}", ln=True)
    for fp in fig_paths:
        pdf.add_page()
        pdf.image(fp, w=180)
    pdf.output(out_pdf)
    return out_pdf
