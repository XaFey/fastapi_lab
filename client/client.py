import argparse
import json
import requests

BASE_URL = "http://localhost:8000"

def get_all_books():
    response = requests.get(f"{BASE_URL}/books/all")
    print_response(response)

def get_book(book_id):
    response = requests.get(f"{BASE_URL}/books/get/{book_id}")
    print_response(response)

def create_book(title, author_name, author_email, year, genre, ratings):
    book= {
        "id": len(requests.get(f"{BASE_URL}/books").json()) + 1,
        "title": title,
        "author": {
            "name": author_name,
            "email": author_email
        },
        "year": year,
        "genre": genre,
        "ratings": ratings


    }
    response = requests.post(f"{BASE_URL}/books/create", json=book)
    print_response(response)

def update_book(book_id, title, author_name, author_email, year, genre, ratings=None):
    book = {
        "title": title,
        "author": {
            "name": author_name,
            "email": author_email
        },
        "year": year,
        "genre": genre,
        "ratings": ratings
    }
    response = requests.put(f"{BASE_URL}/books/update/{book_id}", json=book)
    print_response(response)

def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/delete/{book_id}")
    print_response(response)

#Search Books by Genre
def search_books_by_genre(genre):
    response = requests.get(f"{BASE_URL}/books/search?genre={genre}")
    print_response(response)

#Count
def count_books():
    response = requests.get(f"{BASE_URL}/books/count")
    print_response(response)


def print_response(response):
    try:
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(f"Status Code: {response.status_code}")
        print(response.text)

def main():
    parser = argparse.ArgumentParser(description="Book API Client")
    subparsers = parser.add_subparsers(dest="command", help= "API command")

    #List all books
    subparsers.add_parser("list", help="List all books")

    #Get a book
    get_parser = subparsers.add_parser("get", help="Get a book by ID")
    get_parser.add_argument("id", type=int, help="Book ID")


    #Create a book
    create_parser =  subparsers.add_parser("create", help="Create a new book")
    create_parser.add_argument("title", type=str, help="Create a new book")
    create_parser.add_argument("author_name", type=str, help="Book title")
    create_parser.add_argument("--author_email", type=str, default=None, help="Author email")
    create_parser.add_argument("year", type=int, help= "Publication Year")
    create_parser.add_argument("genre", type=str, help="Book genre")
    create_parser.add_argument("ratings", type=int, help="Book ratings", nargs="+", default=[])

    #Update a book
    update_parser= subparsers.add_parser("update", help="Update a book by ID")
    update_parser.add_argument("id", type=int, help="Book ID")
    update_parser.add_argument("title", type=str, help="Update a book")
    update_parser.add_argument("author_name", type=str, help="Book title")
    update_parser.add_argument("--author_email", type=str, default=None, help="Author email")
    update_parser.add_argument("year", type=int, help= "Publication Year")
    update_parser.add_argument("genre", type=str, help="Book genre")
    update_parser.add_argument("ratings", type=int, help="Book ratings", nargs="+", default=[])


    #Delete a book
    delete_parser = subparsers.add_parser("delete", help="Delete a book")
    delete_parser.add_argument("id", type=int, help="Book ID")

    #Search a book by genre
    search_parser = subparsers.add_parser("search", help="Search books by genre")
    search_parser.add_argument("genre", type=str, help="Book genre")

    #Count books
    count_parser = subparsers.add_parser("count", help="Count all books")
    count_parser.add_argument("count", type=int, help="Count all books")

    args = parser.parse_args()

    if args.command == "list":
        get_all_books()
    elif args.command == "get":
        get_book(args.id)
    elif args.command == "create":
        create_book(args.title, args.author_name, args.author_email, args.year, args.genre, args.ratings)
    elif args.command == "update":
        update_book(args.id, args.title, args.author_name, args.author_email, args.year, args.genre, args.ratings)
    elif args.command == "delete":
        delete_book(args.id)
    #Search Books by Genre
    elif args.command == "search":
        search_books_by_genre(args.genre)
    #Count Books
    elif args.command == "count":
        count_books(args.count)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
