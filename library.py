def start(all_books=None, borrowed_ISBNs=None):  # Two parameters, list of all books and list of borrowed books
    # If there is no assigned value, then the previous values from the given instructions for the assignment are used
    # This is done through assigning both parameters as None if parameters aren't defined and then the values for the
    # parameters are reassigned as seen below
    if borrowed_ISBNs is None:
        borrowed_ISBNs = []
    # Although all books is a dictionary, I will refer to it as a list, not as the datatype list but when referred to
    # as a list of books, I mean it is the list of books in the library
    if all_books is None:
        all_books = {  # ISBN (key) : [Book Name, Author, Edition, [All previous borrowers]]
            '9780596007126': ["The Earth Inside Out", "Mike B", 2, ['Ali']],
            '9780134494166': ["The Human Body", "Dave R", 1, []],
            '9780321125217': ["Human on Earth", "Jordan P", 1, ['David', 'b1', 'user123']]
        }

    printMenu()  # Print the menu

    selection = input("Your Selection> ")  # User selects which function to call

    if selection == "1" or selection == "A" or selection == "a":  # Inputs to add a new book
        output = add_New()  # Output will be an array with all needed values for the book
        all_books[output[0]] = output[1]  # ISBN is key of new entry and the value is an array (values mentioned above)
    elif selection == "2" or selection == "R" or selection == "r":  # Inputs to borrow a book

        # Result will be the new list for borrowed books and new dictionary for all books
        result = borrow(all_books, borrowed_ISBNs)

        # Reassigning new updated values for all_books and borrowed ISBNs
        all_books = result[0]
        borrowed_ISBNs = result[1]

    elif selection == "3" or selection == "T" or selection == "t":  # Inputs to return a book

        result = return_book(borrowed_ISBNs, all_books)  # Returns updated list of borrowed ISBNs of books
        borrowed_ISBNs = result  # Reassigning new updated value to list of borrowed ISBNs of books

    elif selection == "4" or selection == "L" or selection == "l":  # Inputs to list the books
        list_books(all_books, borrowed_ISBNs)  # Calls list function
    elif selection == "5" or selection == "X" or selection == "x":  # Inputs to exit the program
        exit_program(all_books, borrowed_ISBNs)  # Calls exit program function
        return 1  # Exit library by returning a value of 1
    else:  # If input doesn't match any condition above, then just print out error statement and restart
        print("Wrong selection! Please select a valid option.")
        start(all_books, borrowed_ISBNs)

    start(all_books, borrowed_ISBNs)  # Restart function to perform other functions


def valid_ISBN(num):
    # This program checks if an ISBN is valid, this is essentially being done by doing the dot product of
    # [1,2,3,4,5,6,7,8,9,10,11,12,13] (ISBN value) and [1,3,1,3,1,3,1,3,1,3,1,3,1] (check vector), the result of which
    # should be evenly divisible by 10
    sum = 0  # Sum of dot product

    for i in range(0, 13, 2):  # Add all digits being multiplied by 1
        sum += int(num[i])

    for i in range(1, 13, 2):  # Add all digits being multiplied by 3
        sum += (int(num[i]) * 3)

    return sum % 10 == 0  # Return if sum is divisible by 10


def borrow(books_list, rented):
    # This function takes the variables from the start() function and then modifies them so that the books that are
    # borrowed are added into the two variables, this is done in by adding the borrower's name to book's logged history
    # and the ISBN of the borrowed book is added to a list
    borrow_name = input("Enter the borrower name> ")  # Get borrowed name
    search = (input("Search term> ")).lower()  # Take input and make it lowercase
    # Make a new list which is the list of currently rented books to compare with what's been rented after
    initial = rented[:]

    # The if statements check below if the last digit is a "*", "%", or neither and filters based of those
    # All checks are done in lowercase so everything is converted to lowercase
    if search[-1] == "*":
        # Search by checking if search term is within name of book

        search = search[0:-1]  # Take entire string except last letter
        for book in books_list:  # Iterate through each book
            if book not in rented and search in books_list[book][0].lower():
                # If book is not currently borrowed and search term is within name of book, then the following commands
                # are executed
                books_list[book][3] += [borrow_name]  # Add name of borrower to book's logged history
                rented += [book]  # Add ISBN to the list of books already rented

    elif search[-1] == "%":
        # Search by checking if the search term matches with the first letters of any book name

        search = search[0:-1]  # Take entire string except last letter
        for book in books_list:  # Iterate through each book
            if (book not in rented) and search == books_list[book][0][:len(search)].lower():
                # If book is not currently borrowed and search term matches with beginning of the name of book,
                # then the following commands are executed
                books_list[book][3] += [borrow_name]  # Add name of borrower to book's logged history
                rented += [book]  # Add ISBN to the list of books already rented

    else:
        # Search by exact match of book name

        for book in books_list:  # Iterate through each book
            if book not in rented and search == books_list[book][0].lower():
                # If book is not currently borrowed and search term is exact match with name of book,
                # then the following commands are executed
                books_list[book][3] += [borrow_name]  # Add name of borrower to book's logged history
                rented += [book]  # Add ISBN to the list of books already rented

    # If no changes between the list of ISBNs of borrowed books from before and then after, then say
    # that no such books were found, otherwise print the books that were borrowed
    if initial == rented:
        print("No books found!")
    else:
        for book in rented:
            if book not in initial:
                print('-"{}" is borrowed!'.format(books_list[book][0]))

    return [books_list, rented]  # Return the new list of books and the list of


def return_book(borrowed_books, books):
    # What's being done within this function is the currently borrowed are being modified so then later in the start
    # function all that needs to be done is reinstating the value of the borrowed books list with what's being returned
    # by this function

    ISBN = input("ISBN> ")  # ISBN of book being returned

    # If this book has actually been borrowed, then the borrowed_books list will be returned with that book
    # removed from it, otherwise it will just say that there is no such book borrowed and return the original list
    if ISBN in borrowed_books:
        borrowed_books.remove(ISBN)
        print('"{}" is returned'.format(books[ISBN][0]))
        return borrowed_books
    else:
        print("No book is found!")
        return borrowed_books


def list_books(all_books, borrowed_books):
    # We take the parameter of all_books to get the data of all books in storage and borrowed_books to see which of
    # these books currently aren't available
    for book in all_books:  # Iterate through each book in all_books
        print("---------------")  # Print a line to separate data from each book
        # If the book is in borrowed_books, then it's unavailable, otherwise available is printed
        if book in borrowed_books:
            print("[Unavailable]")
        else:
            print("[Available]")

        print("{} - {}".format(all_books[book][0], all_books[book][1]))  # "Book Name" - "Author"
        print("E: {} ISBN: {}".format(all_books[book][2], book))  # E: "Edition Number" ISBN: "ISBN"
        print("Borrowed by: [{}]".format(all_books[book][3]))  # Borrowed by: ["Log of people who borrowed that book"]


def exit_program(all_books, borrowed_books):
    # The string on line 128 is printed and then all books are listed using the list_books() function
    print("$$$$$$$$ FINAL LIST OF BOOKS $$$$$$$$")
    list_books(all_books, borrowed_books)


def add_New():
    book_name = input("Book Name> ")  # Input of Book name

    # If the book name has "*" or "%", it's an invalid book name and will keep asking the user for a valid book name
    # Once a valid book name is given, infinite loop is broken out of
    while True:
        if "*" in book_name or "%" in book_name:
            print("Invalid Book Name!")
            book_name = input("Book Name> ")
        else:
            break

    author = input("Author> ")  # Input of author name

    edition = input("Edition> ")  # Input of edition of book

    # Infinite loop established which will be broken out of if contents of edition are all numbers
    while True:
        if edition.isnumeric():
            edition = int(edition)
            break
        else:
            print("Invalid Author Name!")
            edition = input("Edition> ")

    ISBN = input("International Standard Book Number (ISBN): ")  # Get input of ISBN

    # Infinite loop is established, the loop will keep going until conditions are met
    while True:
        # Until the sequence of characters given are all numbers and 13 digits, the loop will keep asking for a
        # valid ISBN input
        if ISBN.isnumeric() and len(ISBN) == 13:
            # Once the conditions above are met, the valid_ISBN(ISBN) function is used to determine if
            # the ISBN given is valid, if it's valid then the loop will break, otherwise it will be said that
            # the ISBN is invalid and will just go back to the start function and print the menu for another option
            if valid_ISBN(ISBN):
                break
            else:
                print("Invalid ISBN!")
                start()
        else:
            print("Invalid ISBN!")
            ISBN = input("International Standard Book Number (ISBN): ")

    # If this point is reached, then all values are valid and returned
    print("A new book is added successfully.")
    new_book = [ISBN, [book_name, author, edition, []]]
    return new_book


def printMenu():  # Print the menu to give user options
    print('\n######################')
    print('1: (A)dd a new book.')
    print('2: Bo(R)row books.')
    print('3: Re(t)urn a book.')
    print('4: (L)ist all books.')
    print('5: E(x)it.')
    print('######################\n')


start()  # Starting of program and loop
