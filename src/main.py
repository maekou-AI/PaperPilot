from utils.fetch_papers import fetch_pubmed_papers, fetch_arxiv_papers
from utils.send_line_notification import send_line_notification


def main():
    # PubMedからの論文収集
    query_pubmed = "Bioinformatics"
    pubmed_papers = fetch_pubmed_papers(query_pubmed, max_results=10)
    pubmed_message = "PubMed:\n"
    if pubmed_papers:
        for paper in pubmed_papers:
            pubmed_message += (
                f"- {paper['title']} ({paper['source']}, {paper['pubdate']})\n"
                f"  {paper['link']}\n"
            )
    else:
        pubmed_message += (f"PubMedから本日の論文は見つかりませんでした。")

    # Arxivからの論文収集
    query_arxiv = "Genomics"
    arxiv_papers = fetch_arxiv_papers(query_arxiv, max_results=3)
    arxiv_message = "Arxiv:\n"
    if arxiv_papers:
        for paper in arxiv_papers:
            arxiv_message += (
                f"- {paper['title']} ({paper['pubdate']})\n"
                f"  {paper['link']}\n"
            )
    else:
        arxiv_message += (f"Arxivから本日の論文は見つかりませんでした。")

    message = "今日の論文:\n\n" + pubmed_message + "\n" + arxiv_message
    
    # メッセージ送信
    send_line_notification(message)

if __name__ == "__main__":
    main()
