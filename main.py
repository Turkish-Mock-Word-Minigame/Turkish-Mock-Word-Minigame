from Game import generate_question, check_answer

print("Welcome to our Mock Word Minigame! \n")

while True:
    input("Press enter to play")

    question = generate_question()

    print(question['sentence'])
    for option in question['options']:
        print(option)

    answer = input("Your answer: ")
    is_correct, correct_answer, sentence = check_answer(answer)

    if is_correct:
        print("\n Correct! \n")
    else:
        print("\n Correct answer was: " + correct_answer + "\n")

    print("The sentence was: " + sentence + "\n")
