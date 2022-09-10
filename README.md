# Clone of Wordle Clone With Extra Features
Summary: We used the wordle clone originally made by lohchness and made some edits. Wordle is a word guessing game that traditionally relies on colors. By adding a keyboard and a "screen reader", we tried to make this game more accessible and make it more playable without having to distinguish between colors.

## Original Wordle Game
Link: https://www.nytimes.com/games/wordle/index.html 
Players are given six tries to guess a five letter word. After submitting a guess, letters in the word can be highlighted green, yellow, or gray. Green letters are in the correct position. Yellow letters are in the word to be guessed, but the wrong position. Gray letters are not in the word.

## Original Wordle Clone
Link: https://github.com/lohchness/wordleclone
This was a fully functioning wordle game and letters were highlighted correctly. Players could play multiple games in a row. However, there was no keyboard to serve as a catalog of which letters had been guessed correctly, misplaced, or incorrectly. 

## Wordle With Keyboard
The first step was making a keyboard that could show the player which letters had been guessed correctly/misplaced/incorrectly. The same colors used for highlighting letters in the actual guess were used. Unused letters are not highlighted. There is also an enter and backspace button. 

## Audio Description/Screen Reader
A player can activate audio description/screen reader mode by right clicking in the game window. Right clicking again deactivates this mode. Afterwards, clicking on elements should read out a description - reading the title, the screen reader activation mode, etc. When typing, the letters typed are read aloud. However, when using the in game keyboard to input a word (by clicking the actual letter on the keyboard), the status of the letter is also read out loud - whether it's correctly placed, misplaced, incorrectly placed, or unused (the most "correct" status of the letter is read - if it was placed correctly once, then the audio description will describe it as correct). 
Furthermore, after submission of a guess, if the guess is invalid (the guess is not a word in the word list or it's too short) the screen reader will also announce this. 

## Challenges
The NYT Wordle and Pygame aren't exactly screen reader friendly. On the NYT wordle (as of 9/10/22) buttons on the keyboard don't give indications of the status of the letter (correct, incorrect, etc). Python actually has some screen reader libraries but I didn't have time to learn them within the time period of this project, so I manually put in the audio descriptions using google translate. Definitely want to look into that in the future, as this game is kind of birttle given all the manual work I did.

## Credits
https://github.com/lohchness/wordleclone for the original wordle clone
https://www.nytimes.com/games/wordle/index.html 
https://evolution.voxeo.com/library/audio/prompts/alphabet/index.jsp for reading out the letters
Google translate for reading the various descriptions in the game
ShellHacks 2022 - why we thought of this project :)
