from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET

def fetch_pubmed_papers(query, max_results=10):
    """PubMedから論文を取得する"""
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    # 日付を取得
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "datetype": "pdat",
        "mindate": yesterday.strftime('%Y/%m/%d'),
        "maxdate": today.strftime('%Y/%m/%d'),
    }
    search_response = requests.get(search_url, params=params)
    if search_response.status_code == 200:
        ids = search_response.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            print("No papers found in PubMed")
            return []
        
        # 論文の詳細情報を取得
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        summary_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
        }    
        summary_response = requests.get(summary_url, params=summary_params)
        if summary_response.status_code == 200:
            papers = []
            for id, details in summary_response.json().get("result", {}).items():
                if id == "uids":
                    continue
                papers.append({
                    "id": id,
                    "title": details.get("title", "タイトルなし"),
                    "source": details.get("source", "雑誌なし"),
                    "pubdate": details.get("pubdate", "日付なし"),
                    "link": f"https://pubmed.ncbi.nlm.nih.gov/{id}",
                })
            return papers
    else:
        print(f"Failed to fetch summary (PubMed): {search_response.status_code}")
        return []

def fetch_arxiv_papers(query, max_results=5):
    """Arxivから論文を取得する"""
    base_url = "https://arxiv.org/api/query"

    # 日付を取得
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    # フィルタリングクエリの作成
    date_range = f"{yesterday.strftime('%Y%m%d')} TO {today.strftime('%Y%m%d')}"
    search_query = f"all:{query} AND submittedDate:[{date_range}]"

    # パラメータの設定
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        papers = []
        root = ET.fromstring(response.text)
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            link = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
            pubdate = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
            papers.append({"title": title, "summary": summary, "link": link, "pubdate": pubdate})
        return papers
    else:
        print(f"Failed to fetch papers (Arxiv): {response.status_code}")
        return []


# テスト用コード
if __name__ == "__main__":
    print("=== PubMed ===")
    pubmed_results = fetch_pubmed_papers("Bioinformatics", 3)
    for result in pubmed_results:
        print(f" - {result['title']} ({result['source']}, {result['pubdate']})")
        print(f"   {result['link']}")

    print("\n=== Arxiv ===")
    arxiv_results = fetch_arxiv_papers("Genomics", 3)
    for result in arxiv_results:
        print(f" - {result['title']} ({result['pubdate']})")
        print(f"   {result['link']}")
