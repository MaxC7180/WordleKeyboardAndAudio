from email.mime import audio
from pickle import FALSE
import pygame, sys, random, string

pygame.init()
pygame.display.set_caption("Wordle Clone With Audio Description")
WIDTH, HEIGHT = 1200, 1200
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (255, 108, 108)
COLOR_INCORRECT = (75, 75, 75)
COLOR_MISPLACED = (255, 193, 53)
COLOR_CORRECT = (0, 185, 6)

TEXT_TIMER = 2
NUM_ROWS = 6
NUM_COLS = 5
LETTER_LENGTH = NUM_COLS
RECT_WIDTH = 50
RECT_HEIGHT = 50
# Pixels between each Rect
DX = 10
DY = 10
X_PADDING = 5
Y_PADDING = 5
# Leftmost topmost coordinate where the first rect will be drawn, should be symmetrical. Accounts for number of rects, pixels between rects and rect sizes.
BASE_OFFSET_X = (WIDTH/2)-((NUM_COLS/2)*DX)-((NUM_COLS/2)*RECT_WIDTH)+(((NUM_COLS+1)%2)*(DX/2))
BASE_OFFSET_Y = (HEIGHT/2)-((NUM_ROWS/2)*DY)-((NUM_ROWS/2)*RECT_HEIGHT)+(((NUM_ROWS+1)%2)*(DY/2))

TOP_ROW = ['q','w','e','r','t','y','u','i','o','p']
MIDDLE_ROW = ['a','s','d','f','g','h','j','k','l']
BOTTOM_ROW = ['z','x','c','v','b','n','m']

TOP_ROW_Y = HEIGHT - (65*6) - 20
MIDDLE_ROW_Y = HEIGHT - (65*5) - 20
BOTTOM_ROW_Y = HEIGHT - (65*4) - 20

TOP_ROW_X = []
MIDDLE_ROW_X = []
BOTTOM_ROW_X = []

for let in range(len(TOP_ROW)):
    TOP_ROW_X.append((1200-53*len(TOP_ROW))/2 + let*52)
for let in range(len(MIDDLE_ROW)):
    MIDDLE_ROW_X.append((1200-53*len(MIDDLE_ROW))/2 + let*52)
for let in range(len(BOTTOM_ROW)):
    BOTTOM_ROW_X.append((1200-53*len(BOTTOM_ROW))/2 + let*52)

#Sound effects
SOUNDS = []
for let in range(26):
    link = "audio-alphabet/"
    link += chr(let+65)
    link += ".wav"
    SOUNDS.append(link)
CORRECT_SOUND = pygame.mixer.Sound("audio-other/correct.wav")
MISPLACED_SOUND = pygame.mixer.Sound("audio-other/misplaced.wav")
INCORRECT_SOUND = pygame.mixer.Sound("audio-other/incorrect.wav")
UNUSED_SOUND = pygame.mixer.Sound("audio-other/unused.wav")
ENTER_SOUND = pygame.mixer.Sound("audio-other/enter.wav")
BACKSPACE_SOUND = pygame.mixer.Sound("audio-other/backspace.wav")
SCREENREADER_OFF_SOUND = pygame.mixer.Sound("audio-other/screenreader_off.wav")
SCREENREADER_ON_SOUND = pygame.mixer.Sound("audio-other/screenreader_on.wav")
INVALID_WORD_SOUND = pygame.mixer.Sound("audio-other/invalid_word.wav")
NOT_ENOUGH_LETTERS_SOUND = pygame.mixer.Sound("audio-other/not_enough_letters.wav")
GUESS_RIGHT_SOUND = pygame.mixer.Sound("audio-other/correct_fast.wav")
PRESS_R_SOUND = pygame.mixer.Sound("audio-other/play_again.wav")
TRY_AGAIN_SOUND = pygame.mixer.Sound("audio-other/try_again.wav")
WORDLE_TITLE_SOUND = pygame.mixer.Sound("audio-other/wordle.wav")
ON_OFF_SOUND = pygame.mixer.Sound("audio-other/on_off.wav")

def main():
    clock = pygame.time.Clock()
    letter_font = pygame.font.SysFont(None, 65)
    text = pygame.font.Font(None, 40)
    used_words = []
    curr_word = ""
    word_count = 0
    curr_letter = 0
    rects = []
    flag_win = False
    flag_lose = False
    flag_invalid_word = False
    flag_not_enough_letters = False
    audio_on = False
    timer_flag_1 = 0
    timer_flag_2 = 0
    incorrect_letters = []
    yellow_letters = []
    green_letters = []
    wordlist = [word.replace("\n","") for word in list(open("sgb-words.txt"))]
    guess_word = random.choice(wordlist)
    savedLetter = ';'
    readWin = False
    readLose = False
    #guess_word = "eerie"
    assert(len(guess_word) == LETTER_LENGTH)
    assert(guess_word.islower())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Option to restart game
            if flag_win or flag_lose:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                if event.type == pygame.MOUSEBUTTONDOWN and 195 < event.pos[1] < 255:
                    if flag_win:
                        GUESS_RIGHT_SOUND.play()
                        PRESS_R_SOUND.play()
                    if flag_lose:
                        TRY_AGAIN_SOUND.play()
                        PRESS_R_SOUND.play()
            else:
                # Upon keypress
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # Prevents IndexErrors
                        if curr_word: 
                            curr_word = curr_word[:-1]
                            curr_letter -= 1
                    elif event.key == pygame.K_RETURN:
                        if len(curr_word) == 5:
                            if curr_word.lower() in wordlist:
                                word_count += 1
                                used_words.append(curr_word)
                                curr_word = ""
                                curr_letter = 0
                            else:
                                flag_invalid_word = True
                                if audio_on == True:
                                    INVALID_WORD_SOUND.play()
                                timer_flag_1 = 0
                        else:
                            flag_not_enough_letters = True
                            if audio_on == True:
                                NOT_ENOUGH_LETTERS_SOUND.play()
                            timer_flag_2 = 0
                    else:
                        if len(curr_word) < LETTER_LENGTH:
                            if event.unicode.isalpha():
                                if audio_on == True:
                                    soundObj = pygame.mixer.Sound(SOUNDS[ord(event.unicode.upper())-65])
                                    soundObj.play()
                                curr_word += event.unicode.upper()
                                curr_letter += 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    savedLetter = ';'
                    if BOTTOM_ROW_X[0] - 170 < event.pos[0] < BOTTOM_ROW_X[0] - 10 and BOTTOM_ROW_Y < event.pos[1] < BOTTOM_ROW_Y + RECT_HEIGHT:
                        if audio_on == True:
                            BACKSPACE_SOUND.play()
                        if curr_word: 
                            curr_word = curr_word[:-1]
                            curr_letter -= 1
                        continue
                    if BOTTOM_ROW_X[6] + RECT_WIDTH + 10 < event.pos[0] < BOTTOM_ROW_X[6] + RECT_WIDTH + 90 and BOTTOM_ROW_Y < event.pos[1] < BOTTOM_ROW_Y + 90:
                        if audio_on == True:
                            ENTER_SOUND.play()
                        if len(curr_word) == 5:
                            if curr_word.lower() in wordlist:
                                word_count += 1
                                used_words.append(curr_word)
                                curr_word = ""
                                curr_letter = 0
                            else:
                                flag_invalid_word = True
                                if audio_on == True:
                                    INVALID_WORD_SOUND.play()
                                timer_flag_1 = 0
                        else:
                            flag_not_enough_letters = True
                            if audio_on == True:
                                NOT_ENOUGH_LETTERS_SOUND.play()
                            timer_flag_2 = 0
                    #turn on or off audio
                    if (event.button == 3):
                        if audio_on == False:
                            audio_on = True
                            SCREENREADER_ON_SOUND.play()
                            ON_OFF_SOUND.play()
                        else:
                            audio_on = False
                            SCREENREADER_OFF_SOUND.play()
                        continue
                    if len(curr_word) < LETTER_LENGTH:
                        if TOP_ROW_X[0] < event.pos[0] < TOP_ROW_X[9] + RECT_WIDTH:
                            if TOP_ROW_Y < event.pos[1] < TOP_ROW_Y + RECT_HEIGHT:
                                for let in range(len(TOP_ROW)):
                                    if TOP_ROW_X[let] < event.pos[0] < TOP_ROW_X[let] + RECT_WIDTH:
                                        savedLetter = TOP_ROW[let]
                            elif MIDDLE_ROW_Y < event.pos[1] < MIDDLE_ROW_Y + RECT_HEIGHT:
                                for let in range(len(MIDDLE_ROW)):
                                    if MIDDLE_ROW_X[let] < event.pos[0] < MIDDLE_ROW_X[let] + RECT_WIDTH:
                                        savedLetter = MIDDLE_ROW[let]
                            elif BOTTOM_ROW_Y < event.pos[1] < BOTTOM_ROW_Y + RECT_HEIGHT:
                                for let in range(len(BOTTOM_ROW)):
                                    if BOTTOM_ROW_X[let] < event.pos[0] < BOTTOM_ROW_X[let] + RECT_WIDTH:
                                        savedLetter = BOTTOM_ROW[let]
                    if audio_on == True and savedLetter != ';':
                        soundObj = pygame.mixer.Sound(SOUNDS[ord(savedLetter.upper())-65])
                        soundObj.play()
                        played = False
                        while played == False:
                            for correct in green_letters:
                                if correct == savedLetter:
                                    CORRECT_SOUND.play()
                                    played = True
                                    break
                            for misplaced in yellow_letters:
                                if misplaced == savedLetter and played == False:
                                    MISPLACED_SOUND.play()
                                    played = True
                                    break
                            for incorrect in incorrect_letters:
                                if incorrect == savedLetter and played == False:
                                    INCORRECT_SOUND.play()
                                    played = True
                                    break
                            if played == False:
                                UNUSED_SOUND.play()
                                played = True
                    #wordle title
                    if BASE_OFFSET_X+RECT_WIDTH - 20 < event.pos[0] < BASE_OFFSET_X+RECT_WIDTH + 500 and BASE_OFFSET_Y-(RECT_HEIGHT*2) < event.pos[1] < BASE_OFFSET_Y-(RECT_HEIGHT*2) + 70:
                        if audio_on == True:
                            WORDLE_TITLE_SOUND.play()
                            continue
                    if 0 < event.pos[0] < 500 and 0 < event.pos[1] < 100 and event.button != 3:
                        if audio_on == True:
                            SCREENREADER_ON_SOUND.play()
                    #Screen reader position
                if event.type == pygame.MOUSEBUTTONUP and savedLetter != ';':
                    curr_word += savedLetter.upper()
                    curr_letter += 1
          
        SCREEN.fill(DARK_GREY)
        # Draw title and underline
        draw_title(letter_font)
        # Draws base 5x6 grid for letters
        for y in range(NUM_ROWS):
            row_rects = []  
            for x in range(NUM_COLS):
                x_pos = BASE_OFFSET_X+(x*DX)+(x*RECT_WIDTH)
                y_pos = BASE_OFFSET_Y+(y*DY)+(y*RECT_HEIGHT)
                curr_rect = pygame.Rect((x_pos, y_pos), (RECT_WIDTH, RECT_HEIGHT))
                pygame.draw.rect(SCREEN,GREY,curr_rect,2)
                row_rects.append((x_pos, y_pos))
            rects.append(row_rects)
        
        # Alerts player that word is not in wordlist. Text appears for 2 seconds.
        if flag_invalid_word:
            timer_flag_2 = 0
            flag_not_enough_letters = False
            text_surface = text.render("Not in word list", True, RED)
            # Should be about center aligned. Use of magic numbers, but not serious.
            x_pos = BASE_OFFSET_X + (RECT_WIDTH * (NUM_COLS/5))
            y_pos = BASE_OFFSET_Y - (DY*4)
            SCREEN.blit(text_surface, (x_pos, y_pos))
            timer_flag_1 += 1
        if flag_not_enough_letters:
            timer_flag_1 = 0
            flag_invalid_word = False
            text_surface = text.render("Not enough letters", True, RED)
            x_pos = BASE_OFFSET_X + (RECT_WIDTH * (NUM_COLS/10))
            y_pos = BASE_OFFSET_Y - (DY*4)
            SCREEN.blit(text_surface, (x_pos, y_pos))
            timer_flag_2 += 1
        if timer_flag_1 == TEXT_TIMER * FPS:
            flag_invalid_word = False
            timer_flag_1 = 0
        if timer_flag_2 == TEXT_TIMER * FPS:
            flag_not_enough_letters = False
            timer_flag_2 = 0
        
        #sound
        if audio_on == True:
            text_surface = text.render("Screen reader is on", True, WHITE)
            SCREEN.blit(text_surface, (20, 20))
        else:
            text_surface = text.render("Right click to turn on and off screen reader", True, WHITE)
            SCREEN.blit(text_surface, (20, 20))

        if flag_win:
            text_surface = text.render("Correct! Press 'R' to play again", True, WHITE)
            x_pos = BASE_OFFSET_X - (RECT_WIDTH * (NUM_COLS/5))
            #y_pos = BASE_OFFSET_Y + (DY*7) + (RECT_HEIGHT * NUM_ROWS)
            SCREEN.blit(text_surface, (x_pos, 200))
            if audio_on == True and readWin == False:
                GUESS_RIGHT_SOUND.play()
                PRESS_R_SOUND.play()
                readWin = True

        elif flag_lose:
            text_surface = text.render("Try again! The word was " + guess_word + ". Press 'R' to play again", True, WHITE)
            #x_pos = BASE_OFFSET_X - (RECT_WIDTH * (NUM_COLS/5))
            #y_pos = BASE_OFFSET_Y + (DY*7) + (RECT_HEIGHT * NUM_ROWS)
            SCREEN.blit(text_surface, (250, 200))
            if audio_on == True and readLose == False:
                TRY_AGAIN_SOUND.play()
                PRESS_R_SOUND.play()
                readLose = True

        # Blits each letter of the current word the user is currently typing.
        # Firstly renders each letter, then blits it on the appropriate rectangle according to which letter it is.
        if curr_word:
            for letter_index in range(len(curr_word)):
                word_surface = letter_font.render(curr_word[letter_index], True, WHITE)
                # [0] represents X coord, [1] Y.
                SCREEN.blit(word_surface, (rects[word_count][letter_index][0]+X_PADDING, rects[word_count][letter_index][1]+Y_PADDING))

        # Renders letters and rects of words already inputted by player.
        if used_words:
            for word_index in range(len(used_words)):
                remaining_letters = list(guess_word)
                num_correct = 0
                # Used to make sure that letters that appear more than once don't get counted if that letter appears in guess_word only once.
                # EG: guess_word = "proxy", word = "droop", and 'o' appears more than once. The second 'o' in droop does not get counted.
                same_indeces = [i for i,x in enumerate(zip(guess_word,used_words[word_index].lower())) if all(y==x[0] for y in x)]
                # Same indeces - if guessword is "beast" and usedword[word_index] is "toast", same indeces contains the indeces where same letters in the same positions collide, in this case, "a","s","t" - which have indeces of [2,3,4] respectively.
                if same_indeces:
                    for index in range(len(same_indeces)):
                        num_correct += 1
                        remaining_letters[same_indeces[index]] = ""
                        curr_rect = pygame.Rect((rects[word_index][same_indeces[index]][0], rects[word_index][same_indeces[index]][1]), (RECT_WIDTH, RECT_HEIGHT))
                        pygame.draw.rect(SCREEN,COLOR_CORRECT,curr_rect)
                        past_letter_surface = letter_font.render(used_words[word_index][same_indeces[index]].upper(), True, WHITE)
                        SCREEN.blit(past_letter_surface,(rects[word_index][same_indeces[index]][0]+X_PADDING, rects[word_index][same_indeces[index]][1]+Y_PADDING))

                for letter_index in range(LETTER_LENGTH):
                    if letter_index not in same_indeces:
                        curr_rect = pygame.Rect((rects[word_index][letter_index][0], rects[word_index][letter_index][1]), (RECT_WIDTH, RECT_HEIGHT))
                        cur_past_letter = used_words[word_index][letter_index].lower()
                        past_letter_surface = letter_font.render(cur_past_letter.upper(), True, WHITE)
                        # Incorrect Letters
                        if cur_past_letter not in remaining_letters:
                            pygame.draw.rect(SCREEN,COLOR_INCORRECT,curr_rect)
                            if cur_past_letter not in incorrect_letters:
                                incorrect_letters.append(cur_past_letter)
                        # Letter exists in word, but wrong position.
                        else:
                            pygame.draw.rect(SCREEN,COLOR_MISPLACED,curr_rect)
                            if cur_past_letter not in yellow_letters and cur_past_letter not in green_letters:
                                yellow_letters.append(cur_past_letter)
                            remaining_letters[remaining_letters.index(cur_past_letter)] = ""
                        SCREEN.blit(past_letter_surface,(rects[word_index][letter_index][0]+X_PADDING, rects[word_index][letter_index][1]+Y_PADDING))
                    else:
                        cur_past_letter = used_words[word_index][letter_index].lower()
                        if cur_past_letter not in green_letters:
                                green_letters.append(cur_past_letter)
                                if cur_past_letter in yellow_letters:
                                    yellow_letters.remove(cur_past_letter)
                        
                # Win/lose condition
                if num_correct == 5:
                    flag_win = True
                elif len(used_words) == NUM_ROWS:
                    flag_lose = True 

        #make the keyboard 
        for let in range(len(TOP_ROW)):
            color = DARK_GREY
            if TOP_ROW[let] in incorrect_letters: 
                color = COLOR_INCORRECT
                #column = 50
            if TOP_ROW[let] in green_letters:
                color = COLOR_CORRECT
                #column = 150
            if TOP_ROW[let] in yellow_letters: 
                color = COLOR_MISPLACED
                #column = 100
                # Change font size, also figure out why color is not updating
            letter_surface = letter_font.render(TOP_ROW[let].upper(), True, WHITE)
            curr_rect = pygame.Rect((TOP_ROW_X[let], TOP_ROW_Y), (RECT_WIDTH, RECT_HEIGHT))
            pygame.draw.rect(SCREEN,color,curr_rect)
            SCREEN.blit(letter_surface, (TOP_ROW_X[let] + 8, TOP_ROW_Y + 5))
        for let in range(len(MIDDLE_ROW)):
            color = DARK_GREY
            if MIDDLE_ROW[let] in incorrect_letters: 
                color = COLOR_INCORRECT
                #column = 50
            if MIDDLE_ROW[let] in green_letters:
                color = COLOR_CORRECT
                #column = 150
            if MIDDLE_ROW[let] in yellow_letters: 
                color = COLOR_MISPLACED
                #column = 100
                # Change font size, also figure out why color is not updating
            letter_surface = letter_font.render(MIDDLE_ROW[let].upper(), True, WHITE)
            curr_rect = pygame.Rect((MIDDLE_ROW_X[let], MIDDLE_ROW_Y), (RECT_WIDTH, RECT_HEIGHT))
            pygame.draw.rect(SCREEN,color,curr_rect)
            SCREEN.blit(letter_surface, (MIDDLE_ROW_X[let] + 8, MIDDLE_ROW_Y + 5))
        for let in range(len(BOTTOM_ROW)):
            color = DARK_GREY
            if BOTTOM_ROW[let] in incorrect_letters: 
                color = COLOR_INCORRECT
                #column = 50
            if BOTTOM_ROW[let] in green_letters:
                color = COLOR_CORRECT
                #column = 150
            if BOTTOM_ROW[let] in yellow_letters: 
                color = COLOR_MISPLACED
                #column = 100
                # Change font size, also figure out why color is not updating
            letter_surface = letter_font.render(BOTTOM_ROW[let].upper(), True, WHITE)
            curr_rect = pygame.Rect((BOTTOM_ROW_X[let], BOTTOM_ROW_Y), (RECT_WIDTH, RECT_HEIGHT))
            pygame.draw.rect(SCREEN,color,curr_rect)
            SCREEN.blit(letter_surface, (BOTTOM_ROW_X[let] + 8, BOTTOM_ROW_Y + 5))
        #enter button
        pygame.draw.rect(SCREEN, COLOR_INCORRECT, pygame.Rect((BOTTOM_ROW_X[6] + RECT_WIDTH + 10, BOTTOM_ROW_Y), (90, RECT_HEIGHT)))
        SCREEN.blit(text.render("Enter", True, WHITE), (BOTTOM_ROW_X[6] + RECT_WIDTH + 18, BOTTOM_ROW_Y + 12))
        #backspace button
        pygame.draw.rect(SCREEN, COLOR_INCORRECT, pygame.Rect((BOTTOM_ROW_X[0] - 170, BOTTOM_ROW_Y), (160, RECT_HEIGHT)))
        SCREEN.blit(text.render("Backspace", True, WHITE), (BOTTOM_ROW_X[0] - 162, BOTTOM_ROW_Y + 12))

        pygame.display.update()
        clock.tick(FPS)
        #pygame.time.get_ticks()

def draw_title(font):
    pygame.draw.line(SCREEN, WHITE, (BASE_OFFSET_X-RECT_WIDTH, BASE_OFFSET_Y-RECT_HEIGHT), (BASE_OFFSET_X + (RECT_WIDTH*(NUM_COLS+1)) + (DX*(NUM_COLS-1)), BASE_OFFSET_Y-RECT_HEIGHT), width=1)
    title_surface = font.render("WORDLE", True, WHITE)
    SCREEN.blit(title_surface, (BASE_OFFSET_X+RECT_WIDTH, BASE_OFFSET_Y-(RECT_HEIGHT*2)))

if __name__ == "__main__":
    main()           
