# Owen's Quiz Game

This is Owen's Quiz Game, a trivia game where you can see if you know as much music as you think you do. This project was created using my knowledge of Python and some bug testing ran by my friends.

## How to Play

1. **Run the Program**: Click on the "Run" button to start the game.
2. **Choose Mode**: Select between single-player (1) or multiplayer mode (2).
3. **Select Category**: Choose a category from the available options by typing out the name. (Ex: "jazz")
4. **Answer Questions**: Answer the trivia questions within the given time limit of twenty seconds.
5. **Score Tracking**: Your score will be updated based on correct or incorrect answers.
6. **High Scores**: If you're on single player mode, after completing the game, high scores are displayed and saved.

## Features

- Multiple different music genres with questions that have differing values from 200 to 1000.
- Single-player and multiplayer modes.
- High score tracking to keep a record of top scores.

## File Structure

- `main.py`: The main program file containing the game logic.
- `questions.json`: A JSON file with all the trivia questions.
- `highscores.json`: A JSON file to store and retrieve high scores.

## Example Questions

- **Rock (200 points)**: "Who is known as the 'King of Rock and Roll'?" - Answer: Elvis Presley
- **Metal (400 points)**: "Who is the lead singer of Iron Maiden?" - Answer: Bruce Dickinson
- **Pop (600 points)**: "Which artist released the album 'Future Nostalgia'?" - Answer: Dua Lipa

## How to Add More Questions

1. Open the `questions.json` file.
2. To add a new category use the following template and put it in the middle, to place it at the end or the start of the `questions.json` you will need to adjust the beginning and end like it is writtin in the file
```
},
"category_name": {
  "200": [
    {"question": "Put your question here", "answer": "Put your answer here"}
  ],
  "400": [
    {"question": "Put your question here", "answer": "Put your answer here"}
  ],
  "600": [
    {"question": "Put your question here", "answer": "Put your answer here"}
  ],
  "800": [
    {"question": "Put your question here", "answer": "Put your answer here"}
  ],
  "1000": [
    {"question": "Put your question here", "answer": "Put your answer here"}
  ]
},
```
3. To add new questions use this format and adjust the snippet based upon if its a single question in a category or multiple. You can check the `questions.json` for an example
```
{"question": "Put your question here", "answer": "Put your answer here"}
```

## Contact

If you have any questions feel free to send me a message on one of these places:
1. Replit: https://replit.com/@owenofarrell202
2. Email: owen.o_farrell@my.ucdsb.ca
3. Github: https://github.com/OwenOfarrell/Owens-Quiz-Game/
