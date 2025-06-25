from fpdf import FPDF
import datetime

class PDFExporter:
    def __init__(self, output_data):
        self.output = output_data
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "AI Project Plan Report", ln=True, align="C")
        self.pdf.set_font("Arial", "", 12)
        self.pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%d-%b-%Y')}", ln=True, align="R")
        self.pdf.ln(5)

    def add_section(self, title, content):
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font("Arial", "", 11)
        self.pdf.multi_cell(0, 8, content)
        self.pdf.ln(4)

    def export(self, filename="AI_Project_Report.pdf"):
        self.pdf.add_page()
        self.header()
        self.add_section("Title", self.output.get("title", ""))
        self.add_section("Purpose", self.output.get("purpose", ""))
        self.add_section("Project Flow", self.output.get("flow", ""))
        self.add_section("Diagram (Mermaid)", self.output.get("diagram", ""))
        self.add_section("Expert Feedback", self.output.get("feedback_out", ""))
        self.add_section("Market Insights", self.output.get("market_insights", ""))
        self.pdf.output(filename)
        print(f"✅ Exported PDF to: {filename}")
