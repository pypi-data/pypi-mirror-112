from src.wikisearch.wikisearcher import WikiSearcher

searcher = WikiSearcher()
search_result = searcher.search('React.js', verbose=True)
print(search_result)