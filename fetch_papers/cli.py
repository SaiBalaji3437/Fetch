import typer
import requests
import csv
from typing import Optional

app = typer.Typer()

@app.command()
def get_papers_list(
    query: str,
    file: Optional[str] = typer.Option(None, "--file", "-f", help="File name to save results"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Print debug information")
):
    # Debugging output
    if debug:
        typer.echo(f"Query: {query}")
        typer.echo(f"Output file: {file}")

    # Fetch papers (this is a simplified example, you'll use the PubMed API here)
    papers = [
        {"PubmedID": "12345", "Title": "Pharmaceutical Research 101", "Publication Date": "2023-01-01", "Non-academic Author(s)": "Dr. John Doe", "Company Aliation(s)": "PharmaCo", "Corresponding Author Email": "john.doe@pharmaco.com"},
        {"PubmedID": "67890", "Title": "Biotech Advances in 2023", "Publication Date": "2023-05-15", "Non-academic Author(s)": "Dr. Jane Smith", "Company Aliation(s)": "BioTechCorp", "Corresponding Author Email": "jane.smith@biotechcorp.com"}
    ]

    # Output to CSV or console
    if file:
        with open(file, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
        typer.echo(f"Results saved to {file}")
    else:
        for paper in papers:
            typer.echo(f"PubmedID: {paper['PubmedID']}, Title: {paper['Title']}, Publication Date: {paper['Publication Date']}")

if __name__ == "__main__":
    app()
