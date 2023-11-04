import wikipediaapi

def search_wiki(query):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='wikipiki')
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        print("Page - Title: %s" % page_py.title)
        print("Page - Summary: %s" % page_py.summary)
        return page_py.summary
    else:
        print("No page with this title found")
        return "No page with this title found"

if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        search_wiki(query)
        print("\n\n")
        print("Do you want to search again? y/n")
        choice = input()
        if choice == 'y':
            continue
        else:
            break
