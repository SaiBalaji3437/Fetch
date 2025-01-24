import typer
from fetch_papers.pubmed_fetcher import PubMedClient, filter_papers, save_to_csv

app = typer.Typer()

@app.command()
def get_papers_list(
    query: str = typer.Argument(..., help="Search query for PubMed"),
    file: str = typer.Option(None, "-f", "--file", help="Filename to save the results (optional)"),
    debug: bool = typer.Option(False, "--debug", help="Print debug information"),
):
    """
    Fetch a list of papers from PubMed based on the query and optionally save to a file.
    """
    client = PubMedClient()  # Initialize the PubMed client

    if debug:
        typer.echo(f"Fetching papers for query: {query}")

    try:
        # Step 1: Fetch paper IDs
        paper_ids = client.fetch_paper_ids(query)
        if debug:
            typer.echo(f"Fetched Paper IDs: {paper_ids}")

        # Step 2: Fetch paper details
        paper_details = client.fetch_paper_details(paper_ids)
        if debug:
            typer.echo(f"Fetched Paper Details: {paper_details}")

        # Step 3: Filter papers
        filtered_papers = filter_papers(paper_details)
        if debug:
            typer.echo(f"Filtered Papers: {filtered_papers}")

        # Step 4: Save to file or display
        if file:
            save_to_csv(file, filtered_papers)
            typer.echo(f"Results saved to {file}")
        else:
            typer.echo(f"Results: {filtered_papers}")

    except Exception as e:
        typer.echo(f"Error occurred: {e}", err=True)

if __name__ == "__main__":
    app()

