import requests
from bs4 import BeautifulSoup
from os import getcwd

search_again = "y"
urls_clean = []
listsLocation = (getcwd())
urls = open(listsLocation + "\\URL List.txt", "r").readlines()
for y in urls:
    urls_clean.append(y.strip("\n"))
urls = urls_clean


def automatic_search():
    global check, doc, search_again
    search = input("\nPlease enter a search term: ")
    for x in urls:
        url = x
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        h3_tag = doc.findChildren("h3")

        for a in h3_tag:
            a_tag = a.find(["a"])
            a_tags.append(a_tag)
            headline = a_tag.find(text=True)
            all_headlines.append(headline)
            if search in headline.lower():
                searched_headlines.append(headline)
            else:
                check = check + 1
        for a in doc.find_all("h3"):
            for link in a.find_all("a"):
                link = link.get("href")
                link = link[1:]
                links.append(link)

    print("\nToday's Headlines:\n")
    for x in all_headlines:
        print('"' + x + '"')

    if check == len(searched_headlines) or len(searched_headlines) < 1:
        print("\nNo headlines found. ")
    else:

        print("\nSearch Found:\n")
        for x in searched_headlines:
            print('"' + x + '"')
            link_find = all_headlines.index(x)
            print(' - https://news.google.com' + links[link_find] + "\n")

    search_again = input("\nWould you like to Search again? [Y/N]\n").lower()


def manual_search():
    global search_again, check
    manual_choice = input(
        "Would you like to check: Google News Top Stories [a], Google Covid News [b],"
        " or Google Market News [c]?").lower()
    if manual_choice == "a":
        url = urls[1]
    elif manual_choice == "b":
        url = urls[2]
    else:
        url = urls[3]

    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    search = input("\nPlease enter a search term: ")
    h3_tag = doc.findChildren("h3")

    print("\nToday's Headlines:\n")
    for x in h3_tag:
        a_tag = x.find(["a"])
        a_tags.append(a_tag)
        headline = a_tag.find(text=True)
        print('"' + headline + '"')
        all_headlines.append(headline)
        if search in headline.lower():
            searched_headlines.append(headline)
        else:
            check = check + 1

    if check == len(searched_headlines) or len(searched_headlines) < 1:
        print("\nNo headlines found. ")
    else:
        for a in doc.find_all("h3"):
            for link in a.find_all("a"):
                link = link.get("href")
                link = link[1:]
                links.append(link)

        print("\nSearch Found:\n")
        for x in searched_headlines:
            print('"' + x + '"')
            link_find = all_headlines.index(x)
            print(' - https://news.google.com' + links[link_find] + "\n")
    search_again = input("\nWould you like to Search again? [Y/N]\n").lower()


choice = input("Would you like Automated_Search engaged?: [Y/N]\n").lower()
if choice != 'y':
    manual_mode = True
else:
    manual_mode = False

while search_again == "y":
    all_headlines = []
    searched_headlines = []
    links = []
    a_tags = []
    check = 0
    print("Web Scrapper mk1\n")

    if manual_mode:
        manual_search()
    else:
        automatic_search()
