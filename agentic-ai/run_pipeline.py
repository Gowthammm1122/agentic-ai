from pipeline_graph import build_graph
from export_to_pdf import PDFExporter  # ✅ Import the PDF exporter

# Build LangGraph
graph = build_graph()

# Dummy input (can modify)
inputs = {
    "title": "AI-Powered Academic Planner",
    "goals": "Help students generate structured project plans",
    "feedback": "Should be fast, visual, and helpful"
}

# Run the pipeline
result = graph.invoke(inputs)

# Print result to console
print("\nFinal Output:")
print(result)

# ✅ Export the result to PDF
exporter = PDFExporter(result)
exporter.export("AI_Project_Report.pdf")
