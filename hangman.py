import PySimpleGUI as sg
import pygame
from random import randint
import csv

def start():
    event, values = sg.Window('Choose an option', [[sg.Text('Select a difficulty level'), sg.Listbox(['Easy', 'Medium', 'Hard'], size=(20, 3), key='LB')],
        [sg.Button('Ok'), sg.Button('Cancel')]]).read(close=True)

    if event == 'Ok':
        difficulty = values["LB"][0]
        sg.popup(f'You chose ' + difficulty + '. Lets begin!')
        begin_game(difficulty)
    
    else:
        sg.popup_cancel('User aborted')

def begin_game(difficulty):
    wordToGuess = getRandomWord(difficulty)
    wordToGuess = wordToGuess[0].lower() + wordToGuess[1:]
    letterGuessedCorrect = [False for i in range(len(wordToGuess))]
    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    (width, height) = (1000,1000)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Hangman Game')
    font = pygame.font.Font('freesansbold.ttf', 32)
    lettersFont = pygame.font.Font('freesansbold.ttf', 20)
    titleText = font.render('Guess the word below', True, black, white)
    titleTextSpot = titleText.get_rect()
    titleTextSpot.center = (width / 2, height / 20)
    gallowSpot = pygame.image.load('pics/1_img.JPG')
    gallowSpot = pygame.transform.scale(gallowSpot, (350, 350))
    numLetters = len(wordToGuess)
    underscore = pygame.image.load('pics/Underscore.JPG')
    underscore = pygame.transform.scale(underscore, (100, 100))
    pygame.display.flip()
    running = True
    listOfLetters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
    gallowCounter = 1
    letterCounter = 0
    
    while running:
        letters = lettersFont.render(listOfLetters, True, black, white)
        lettersSpot = letters.get_rect()
        lettersSpot.center = (700, 300)
        screen.fill(white)
        screen.blit(titleText, titleTextSpot)
        screen.blit(letters, lettersSpot)
        screen.blit(gallowSpot, (width / 20, height / 5))
        for i in range(numLetters):
            screen.blit(underscore, (i * 100, 800))
        for i in range(len(wordToGuess)):
            if letterGuessedCorrect[i] == True:
                picToLoad = 'pics/alphabet/' + wordToGuess[i].upper() + '.JPG'
                correctLetter = pygame.image.load(picToLoad)
                correctLetter = pygame.transform.scale(correctLetter, (100,100))
                screen.blit(correctLetter, (i * 100, 770))
        if letterCounter == len(wordToGuess):
            wonGame(wordToGuess)
            return
        if gallowCounter == 7:
            lostGame(wordToGuess)
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                guessedLetter = event.key
                guessedLetter = chr(guessedLetter)
                if guessedLetter in wordToGuess:
                    for i in range(len(wordToGuess)):
                        if wordToGuess[i] == guessedLetter:
                            letterGuessedCorrect[i] = True
                            letterCounter += 1
                    listOfLetters = updateLetters(listOfLetters, guessedLetter)
                else:
                    gallowCounter += 1
                    gallowSpot = missedUpdate(gallowCounter)
                    listOfLetters = updateLetters(listOfLetters, guessedLetter)
        pygame.display.update()


def updateLetters(listOfLetters, guessedLetter):
    for i in range(len(listOfLetters)):
        if listOfLetters[i] == guessedLetter:
            listOfLetters = listOfLetters[:i] + listOfLetters[i+1:]
            break
    listOfLetters.strip()
    index = 0
    for i in range(len(listOfLetters) - 1):
        if i == len(listOfLetters) - 1:
            break
        if listOfLetters[i] == " " and listOfLetters[i+1] == " ":
            listOfLetters = listOfLetters[:i] + listOfLetters[i+1:]
    return listOfLetters

def getRandomWord(difficulty):
    listOfWords = []
    with open("./" + difficulty + "_words.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            listOfWords.append(row[0])
        value = randint(0, len(listOfWords))
        return listOfWords[value]

def lostGame(wordToGuess):
    event, values = sg.Window('Loser', [[sg.Text('You lost the game. The word was ' + wordToGuess + '. Would you like to play again?'), sg.Listbox(['Yes', 'No'], size=(20, 3), key='LB')],
        [sg.Button('Ok'), sg.Button('Cancel')]]).read(close=True)
    if event == 'Ok':
        playAgain = values["LB"][0]
        if playAgain == "Yes":
            start()
        else:
            sg.popup_cancel('User aborted')
    else:
        sg.popup_cancel('User aborted')

def wonGame(wordToGuess):
    event, values = sg.Window('Winner!', [[sg.Text('You won the game! The word was ' + wordToGuess + '. Would you like to play again?'), sg.Listbox(['Yes', 'No'], size=(20, 3), key='LB')],
        [sg.Button('Ok'), sg.Button('Cancel')]]).read(close=True)
    if event == 'Ok':
        playAgain = values["LB"][0]
        if playAgain == "Yes":
            start()
        else:
            sg.popup_cancel('User aborted')
    else:
        sg.popup_cancel('User aborted')

def missedUpdate(gallowCounter):
    fileNum = 'pics/' + str(gallowCounter) + "_img.JPG"
    gallowSpot = pygame.image.load(fileNum)
    gallowSpot = pygame.transform.scale(gallowSpot, (350, 350))
    return gallowSpot


if __name__ == "__main__":
    start()