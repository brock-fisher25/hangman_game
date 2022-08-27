import PySimpleGUI as sg
import pygame
from random import seed
from random import randint

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
    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    (width, height) = (1000,1000)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Hangman Game')
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Guess the word below', True, black, white)
    textRect = text.get_rect()
    textRect.center = (500, 50)
    pygame.display.flip()
    running = True
    while running:
        screen.fill(white)
        screen.blit(text, textRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


def getRandomWord(difficulty):
    easyStrings = ['Wench', 'Divot', 'Rough', 'Bless', 'Hello', 'Leapt', 'Fluke', 'Steal', 'Penis']
    medStrings = ['abroad', 'accept', 'demand', 'degree', 'easily', 'series', 'silver', 'single', 'slight']
    hardStrings = ['alleged', 'anxious', 'counter', 'general', 'healthy', 'library', 'massive', 'quarter', 'reflect']
    seed(1)
    value = randint(0,8)
    if difficulty == "Easy":
        return easyStrings[value]
    elif difficulty == "Medium":
        return medStrings[value]
    else:
        return hardStrings[value]
    


if __name__ == "__main__":
    start()