from search_service import search

query = input("Search product: ")
results = search(query)

for r in results:
    print(r["name"], " | Score:", r["score"])
