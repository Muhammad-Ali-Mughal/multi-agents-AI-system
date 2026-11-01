from src.tools.tools import web_search_tool, scrape_url

# result = web_search_tool.invoke("What is the capital of France?")

result = scrape_url("https://news.google.com/topics/CAAqIAgKIhpDQkFTRFFvSEwyMHZNRzFyZWhJQ1pXNG9BQVAB?hl=en-US&gl=US&ceid=US%3Aen")

def main():
    print(result)