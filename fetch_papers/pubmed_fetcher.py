import requests
import csv
import re
from typing import List, Dict

class PubMedClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def fetch_paper_ids(self, query: str) -> List[str]:
        """Fetches paper IDs based on the given query."""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": 100,
            "retmode": "json",
        }
        if self.api_key:
            params["api_key"] = self.api_key
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    
    def fetch_paper_details(self, paper_ids: List[str]) -> List[Dict]:
        """Fetches details of papers by their IDs."""
        if not paper_ids:
            return []
        params = {
            "db": "pubmed",
            "id": ",".join(paper_ids),
            "retmode": "json",
        }
        if self.api_key:
            params["api_key"] = self.api_key
        response = requests.get(self.SUMMARY_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("result", {})

def filter_papers(details: List[Dict]) -> List[Dict]:
    """Filters papers with at least one non-academic author."""
    results = []
    for paper_id, info in details.items():
        if not isinstance(info, dict) or "uid" not in info:
            continue
        authors = info.get("authors", [])
        non_academic_authors = []
        company_affiliations = []
        for author in authors:
            affiliation = author.get("affiliation", "").lower()
            if "university" not in affiliation and "institute" not in affiliation:
                non_academic_authors.append(author.get("name", ""))
                company_affiliations.append(affiliation)
        if non_academic_authors:
            results.append({
                "PubmedID": info.get("uid"),
                "Title": info.get("title", "N/A"),
                "Publication Date": info.get("pubdate", "N/A"),
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": extract_email(info.get("title", "")),
            })
    return results

def extract_email(text: str) -> str:
    """Extracts email addresses from text."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "N/A"

def save_to_csv(filename: str, data: List[Dict]):
    """Saves the filtered data to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
