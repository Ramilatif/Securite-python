from src.tp1.utils.capture import Capture
from src.tp1.utils.config import DOC_DIR
from scapy.all import IP
import pygal
from fpdf import FPDF


class Report:
    def __init__(self, capture: Capture, filename: str, summary: str):
        self.capture = capture
        self.filename = filename
        self.title = "TITRE DU RAPPORT"
        self.summary = summary
        self.array = ""
        self.graph = ""

    def concat_report(self) -> str:
        """
        Concat all data in report
        """
        content = ""
        content += self.title
        content += self.summary
        content += self.array
        content += self.graph

        return content

    def save(self, filename: str) -> None:
        """
        Save report as a PDF file
        :param filename:
        :return:
        """
        pdf = FPDF()
        pdf.add_page()

        # Titre
        pdf.set_font("Helvetica", "B", size=16)
        pdf.cell(0, 10, self.title, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(5)

        # Résumé
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 7, self.summary)
        pdf.ln(5)

        # Tableau
        if self.array:
            pdf.set_font("Courier", size=9)
            pdf.multi_cell(0, 5, self.array)
            pdf.ln(5)

        # Référence au graphique
        if self.graph:
            pdf.set_font("Helvetica", "I", size=10)
            pdf.multi_cell(0, 7, f"Graphique enregistré dans : {self.graph}")

        pdf.output(filename)

    def generate(self, param: str) -> None:
        """
        Generate graph and array
        """
        if param == "graph":
            protocols: dict[str, int] = {}
            for pkt in self.capture.packets:
                proto = pkt.lastlayer().name
                protocols[proto] = protocols.get(proto, 0) + 1

            graph_file = str(DOC_DIR / "protocols_chart.svg")
            bar_chart = pygal.Bar(title="Distribution des protocoles réseau")
            for proto, count in sorted(protocols.items(), key=lambda x: x[1], reverse=True):
                bar_chart.add(proto, count)
            bar_chart.render_to_file(graph_file)
            self.graph = graph_file

        elif param == "array":
            lines = ["Protocole    | Source IP           | Destination IP      | Taille"]
            lines.append("-" * 68)
            for pkt in self.capture.packets:
                proto = pkt.lastlayer().name
                src = pkt[IP].src if IP in pkt else "N/A"
                dst = pkt[IP].dst if IP in pkt else "N/A"
                size = len(pkt)
                lines.append(f"{proto:<12} | {src:<19} | {dst:<19} | {size}")
            self.array = "\n".join(lines)
