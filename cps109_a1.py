import datetime, random

## Problem Description
# Students often need to review information learned in class to prepare for tests and exams.
# Reviewing notes repeatedly can be time-consuming, and students may find it difficult
# to determine how well they understand the material. A simple quiz program can help
# students practise recalling information, identify areas that need more review, and
# monitor their learning progress.
#
# This program allows users to answer questions stored in 'questions.txt' (one question
# per line, with the question and answer separated by '|') and receive feedback on their
# answers. Empty answers are rejected and re-asked, and capitalization and surrounding
# spaces are ignored. The program keeps track of the number of correct and incorrect
# responses and calculates the user's final score.
#
# At the end of each attempt, the user sees their score, percentage, and the missed
# questions with their correct answers. Each attempt is appended to 'results.txt' with
# a timestamp, so earlier results are kept.
#
# The user can run the quiz again with a fresh score and a shuffled question order.
# A missing or empty questions file, or a badly formatted line, is handled without
# crashing. The program uses basic Python programming concepts to provide a
# straightforward and reusable study tool.

## this function loads and organizes questions from questions.txt
def loads_questions():
  ## handles file not found error
  try:
    ## opens and reads the txt file
    questions_file = open('questions.txt')

  ## catching only FileNotFoundError so other bugs aren't hidden
  # and still show up as normal errors
  except FileNotFoundError:
    print('"questions.txt" not FOUND. Put it in the same FOLDER.')
    ## main() expects a list of questions and answers
    return []

  ## stores the questions and answers as tuples in a list
  quiz_items = []

  ## loops through the txt file for questions and answers
  for line in questions_file:
    ## strips the line so stray spaces or the new line don't end up in the question or answer
    strp_line = line.strip()
    if not strp_line:
      continue
    
    ## splits the line and makes a question and answers pair
    parts = strp_line.split('|')

    ## handles split error on lines that don't exactly split into a question and an answer
    if len(parts) != 2:
      print(f'"{strp_line}" is a BAD line and will be SKIPPED.')
      continue

    ## appends the questions and answers as tuple to the quiz list
    quiz_items.append((parts[0], parts[1]))

  ## closes the file to release it once the user is done reading
  questions_file.close()

  ## returns quiz items
  return quiz_items

## this function asks the user one question and re-asks on empty answer
def ask_question(question, answer):
  ## formats the correct answer
  correct_answer = answer.strip().lower()
  users_answer = ''

  while users_answer == '':
    ## asks the user
    ask_input = input(question + ' ')
    ## formats the users answer
    user_typed = ask_input.strip()
    users_answer = user_typed.lower()

    ## checks if the users answer is still empty
    if users_answer == '':
      print('Enter an ANSWER.')
  
  ## returns if answer was correct and what the user typed
  return (users_answer == correct_answer, user_typed)


## runs one game attempt and returns the score and missed questions
def run_quiz(quiz_items):
  ## scores the user on correct questions
  score = 0
  ## stores the questions the user got wrong
  wrong_answers = []

  ## loops through the quiz items list to get questions and answers
  for question, answer in quiz_items:
    ## calls ask_question() with the questions and answers in quiz items
    was_correct, was_typed = ask_question(question, answer)

    ## acts on correct and wrong answers from the user
    if was_correct:
      score += 1
    else:
      wrong_answers.append((question, answer, was_typed))

  ## returns the score and wrong answers
  return score, wrong_answers

## shows the user their results for the last game run
def results_feedback(score, total, wrong_answers):
  ## calculates the users percentage
  percentage = round(score / total * 100)
  print(f'\nScore: {score}/{total} ({percentage}%)')

  ## score grading
  if percentage >= 90:
    print('\nEXCELLENT!')
  elif percentage >= 70:
    print('\nDecent.')
  else:
    print('\nKeep STUDYING.')

  ## checks if the user got all questions correctly or not
  if wrong_answers:
    for question, answer, typed in wrong_answers:
      print(f'\nQuestion: {question} \nAnswer: {answer} \nUser Typed: {typed}')
  else:
    print('\nCONGRATULATIONS')

  ## returns the users percentage after a run
  return percentage

## saves the users result to results.txt to keep earlier attempts
def save_results(score, total, percentage):
  results = open('results.txt', 'a')
  current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

  results.write(f'Time: {current_time} | Score: {score} | Total: {total} | Percentage: {percentage}\n')

  results.close()

## loads the questions once and runs rounds until the user stops and saves each round
def main():
  ## calls loads_questions() once
  quiz_items = loads_questions()

  ## stops main() from running on an empty list and crashing
  if not quiz_items:
    print('\nThere are NO questions to ASK.')
    return

  ## controls the quiz loop and starts as 'yes' so the first round always runs
  quiz_again = 'yes'

  ## runs one round per pass until the user answers no
  while quiz_again == 'yes':
    random.shuffle(quiz_items)
    score, wrong_answers = run_quiz(quiz_items)
    percentage = results_feedback(score, len(quiz_items), wrong_answers)
    save_results(score, len(quiz_items), percentage)

    ## checks if the user wants to be quizzed again
    quiz_again = input('\nRun quiz again? (yes/no) ').strip().lower()
    
    ## error handles input that isn't yes or no
    while quiz_again != 'yes' and quiz_again != 'no':
      print('Wrong Input.')
      quiz_again = input('\nRun quiz again? (yes/no) ').strip().lower()

  ## lets the user know the quiz has ended
  print('\nQuiz has ended.')


main()