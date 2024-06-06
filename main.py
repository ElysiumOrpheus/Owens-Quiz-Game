import json
import random


def load_questions(filename):
  with open(filename, 'r') as file:
    questions = json.load(file)
  return questions

def ask_question(category, difficulty, question_data):
  question = random.choice(question_data[category][difficulty])
  user_answer = input (f"{question['question']} ")
  if user_answer.lower() == question['answer'].lower():
    print ("Correct!")
    return True
  else:
    print(f"Incorrect. The answer was {question['answer']}.")
    return False


def main():
  score = 0
  questions = load_questions('questions.json')
  print("Welcome to Owen's quiz game!")

  while True:
    categories = ', '.join(questions.keys())
    category = input(f"Choose a category ({categories}) or 'quit' to exit: ").title()
    if category == 'Quit':
      break

    if category in questions:
      while True:
          difficulty = input("Choose a difficulty (easy, medium, hard): ").lower()
          if difficulty in questions[category]:
              if ask_question(category, difficulty, questions):
                  score += 1
              else:
                  score -= 1
              print(f"Your current score is: {score}") 
              break
          else:
              print("Invalid difficulty. Please choose again.") 
    else:
      print("Invalid category.")
  print(f"Thanks for playing! Your final score is: {score}")


if __name__ == "__main__":
  main()
  
