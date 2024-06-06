import json
import random
import time


def load_questions(filename):
  with open(filename, 'r') as file:
    questions = json.load(file)
  return questions

def load_high_scores(filename):
  try:
    with open(filename, 'r') as file:
      high_scores = json.load(file)
  except FileNotFoundError:
    high_scores = {"highscores": []}
  return high_scores

def save_high_scores(filename, high_scores):
  with open(filename, 'w') as file:
    json.dump(high_scores, file, indent=4)

def ask_question(category, value, question_data):
  question = random.choice(question_data[category][str(value)])
  print(f"Question: {question['question']}")
  start_time = time.time()
  user_answer = input("Your answer: ")
  end_time = time.time()
  if end_time - start_time > 10:
    print("Time's up!")
    return False
  if user_answer.lower() == question['answer'].lower():
    print("Correct!")
    return True
  else:
    print(f"Incorrect. The answer was {question['answer']}")
    return False
  


def main():
  score = 0
  questions = load_questions('questions.json')
  print("Welcome to Owen's quiz game!")

  player_mode = input("Choose a mode: (1) Single player or (2) Multiplayer: ")
  while player_mode not in ['1', '2']:
    player_mode = input("Invalid. Choose again, (1) Single player or (2) Multiplayer: ")

  if player_mode == '1':
    player_name = input("Enter your name: ")
    score = 0
    available_questions = {category: [200, 400, 600, 800, 1000] for category in questions.keys()}
    while any(values for values in available_questions.values()):
      print(f"Your current score is {score}")
      categories = ', '.join(map(str, available_questions.keys()))  
      value = int(input(f"Choose a value ({values}): "))
      if value in available_questions[category]:
        if ask_question(category, value, questions):
          score += value
        else:
          score -= value
        available_questions[category].remove(value)
      else:
        print("Invalid value.")
    else:
      print("Invalid category.")
  high_scores = load_high_scores('highscores.json')
  high_scores["highscores"].append({"name": player_name, "score": score})
  high_scores["highscores"] = sorted(high_scores["highscores"], key=lambda x: x["score"], reverse=True)[:3]
  save_high_scores('highscores.json', high_scores)
  print(f"Thanks for playing, {player_name}! Your final score is {score}.")
  print("Top 3 High Scores: ")
  for entry in high_scores["highscores"]:
    print(f"{entry['name']}: {entry['score']}")

elif player_mode == '2':
  scores = [0, 0]
  current_player = random.randint(0, 1)
  available_questions = {category: [200, 400, 600, 800, 1000] for category in questions.keys()}
  while any(values for values in available_questions.values()):
    print(f"Player {current_player + 1}'s turn")
    print (f"Player 1 score: {scores[0]}, Player 2 score: {scores[1]}")
    categories = ', '.join(available_questions.keys())
    category = input(f"Choose a category ({categories}): ")
    if category in available_questions and available_questions[category]:
      values = ', '.join(map(str, available_questions[category]))
      value = int(input(f"Choose a value ({values}): "))
      if value in available_questions[category]:
        if ask_question(category, value, questions):
          scores[current_player] += value
        else:
          scores[current_player] -+ value 
          current_player = 1 - current_player
        available_questions[category].remove(value)
      else:
        print("Invalid value.")
    else: 
      print("Invalid category.")
  print("Game over!")
  print(f"Player 1 final score: {scores[0]}")
  print(f"Player 2 final score: {scores[1]}")
  if scores[0] > scores[1]:
    print("Player 1 wins!")
  elif scores[1] > scores[0]
    print("Player 2 wins!")
  else:
    print("It's a tie!")
  
if __name__ == "__main__":
  main()
