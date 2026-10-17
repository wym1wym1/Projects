import random 
import csv
from tabulate import tabulate


numbers_specialcharacters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$']
characters = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
    ]


def main():
    choices = {
        '1': show_object,
        '2': add_object,
        '3': remove_object,
        '4': update_object
    }

    print(
    "What would you like to do?\n"
    "Show your accounts: 1\n"
    "Add a new account: 2\n"
    "Remove an account: 3\n"
    "Update an account: 4")

    choice = input("- ")

    user_choice = choices.get(choice)

    if user_choice:
        user_choice()
    else:
        print('Invalid choice!')




def add_object():
    website = input('Enter Website: ')
    email = input('Enter Email: ')
    username = input('Enter Username: ')
    password = check_password(input('Enter Password: '))




    with open("accounts.csv", "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            website,
            email,
            username,
            password
        ])

    

def show_object():
    with open("accounts.csv", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    
            print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
    if not rows:
        print('No accounts found!')


def check_password(password):
    length = len(password)
    rules = [
    length >= 5,
    any(char.isdigit() for char in password),
    any(char.isupper() for char in password),
    ]

    if password.lower() == 'hangman':  # this is the condition to play hangman, if u like to change it tell
        play = input('Play hangman? Y/N: ').lower()
        if play == 'y':
            hangman()
        
            


    if all(rules):
         return password
    else:
        _ = input('We detected your password might be weak. Would you like a stronger one?\n(Y/N)- ').lower()
        if _ == 'y':
            newpass = ''
            for i in range(4):
                newpass += random.choice(numbers_specialcharacters)
                newpass += random.choice(characters)
            return newpass
        else:
            return password
         

def remove_object():
    show_object()

    with open("accounts.csv", newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    to_remove = input('Enter the website to remove: ')

    new_rows = [row for row in rows if row["website"].lower() != to_remove.lower()]

    if len(new_rows) == len(rows):
         print('Website not found!')
         return 

    with open("accounts.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "website", "email", "username", "password"
        ])
        writer.writeheader()
        writer.writerows(new_rows)

        print("Account removed successfully!") 


def update_object():
    show_object()

    with open("accounts.csv", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    to_update = input('Enter the website you want to update: ')
       
    website = [
        row for row in rows
        if row["website"].lower() == to_update.lower()
    ]

    if not website:
        print('Website not found!')
        return 

    row = website[0]

    print("1- Website\n2- Email\n3- Password\n4- Username")

    fields = {
        '1':"website",
        '2':"email",
        '3':"password",
        '4':"username"
    }

    while True:
        choice = input('Field to change: ')
        if choice not in fields:
            print('Invalid choice')
            continue 
        else:
            break

    field = fields[choice]

    row[field] = input(f"Enter the new {field}: ")

    with open("accounts.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "website", "email", "username", "password"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print("Account updated successfully!")



def hangman():
        
    words = (
        'cat', 'dog', 'elephant', 'giraffe', 'lion', 'tiger', 'apple', 'banana', 'carrot', 
        'pizza', 'burger', 'chocolate', 'table', 'chair', 'lamp', 'phone', 'bottle', 'book', 
        'pen', 'notebook', 'bicycle', 'train', 'airplane', 'hat', 'shoe', 'watch', 'spoon', 
        'fork', 'mouse', 'keyboard'
    )


    word = random.choice(words)
    display = ['_'] * len(word)
    guessed_lets = []
    wrong_lets = []


    def guess():
        guess = input('Guess a letter\n- ')
        if guess.isalpha() and len(guess) == 1:
            return guess
        else:
            print('Invalid input')
            return False


    def correctguess(word, guess):
        if guess in guessed_lets:
            print('Already Guessed! \n')
            print(' '.join(display))
            return 'repeat'
        
        if guess in word:
            for indx, letter in enumerate(word):
                if letter == guess:
                    display[indx] = guess
            print('Correct!\n')
            print(' '.join(display))
            guessed_lets.append(guess)
            return True
        else:
            return False
        
                
                    


    def wrongguess(guess):
            if guess in wrong_lets:
                print ('Already guessed that, and its wrong.\n')
                print(' '.join(display), f" \nWrong Guesses {wrong_lets}")
                return 'repeat2'
            else:
                print('Wrong Guess!')
                wrong_lets.append(guess)

                print(' '.join(display), f" \nWrong Guesses {wrong_lets}")



    def solved(display):
        if '_' not in display:
            return True


    def Play_H():
        attempts = 6
        win = False
        while not win:
            word_guess = guess()
            if word_guess == False:
                continue
            result = correctguess(word, word_guess)
            if result == False:
                w = wrongguess(word_guess)
                if w == 'repeat2':
                    print (f'\nAttempts left: {attempts}')
                    continue
                elif attempts == 0:
                    print (f'you lost! the word was:\n{word}')
                    exit()

                else:
                    attempts -= 1
                    print (f'\nAttempts left:{attempts}')

            elif result == True:
                print (f'\nAttempts left: {attempts}')
            
                continue
            elif result == 'repeat':
                continue

            win = solved(display)
            if win:
                print('You win!')
    Play_H()

 
if __name__ == "__main__":
    main()


