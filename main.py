import requests
import json
import random
import html

correct = 0
wrong = 0

# Text coloring.
colors = {
    "RESET": "\033[0m",
    "YELLOW": "\033[1;33;40m",
    "BLUE": "\033[1;34;40m",
    "WHITE": "\033[1;37;40m",
    "GREEN": "\033[1;32;40m",
    "GREEN_BG_BLACK_FG": "\033[0;37;42m",
    "RED_BG_BLACK_FG": "\033[0;37;41m",
}


def get_questions(amount: int) -> list:
    response = requests.get(
        f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    )
    if response.status_code == 200:
        data = json.loads(response.text)
        return data["results"]
    print(
        colors["RED_BG_BLACK_FG"]
        + f"Error while fetching data: Error {response.status_code}"
        + colors["RESET"]
    )


def serve_questions(questions: list):
    global correct, wrong
    for question in questions:
        category = question["category"]
        difficulty = question["difficulty"].capitalize()  # Capitalized the string.
        question_text = question["question"]

        answers = [
            html.unescape(q)
            for q in question["incorrect_answers"] + [question["correct_answer"]]
        ]
        correct_answer = question["correct_answer"]
        answers_insensitive = [i.lower() for i in answers]
        correct_answer_insensitive = correct_answer.lower()

        random.shuffle(answers)

        print(colors["YELLOW"] + f"Category: {category}" + colors["RESET"])
        print(colors["YELLOW"] + f"Difficulty: {difficulty}\n" + colors["RESET"])
        print(colors["GREEN"] + f"{html.unescape(question_text)}" + colors["RESET"])
        print(
            colors["BLUE"] + f"Answer choices: {', '.join(answers)}\n" + colors["RESET"]
        )

        while True:
            try:
                user_input = int(
                    input(colors["WHITE"] + "Answer index: " + colors["RESET"])
                )
                user_answer = answers_insensitive[user_input]
            except ValueError:
                print("Please enter an integer!")
                continue
            except IndexError:
                print("Please enter a valid python index (starts at 0)!")
                continue

            if user_answer == correct_answer_insensitive:
                print(colors["GREEN_BG_BLACK_FG"] + "\nCorrect!\n" + colors["RESET"])
                correct += 1
                break
            else:
                print(
                    colors["RED_BG_BLACK_FG"]
                    + f"\nIncorrect! The correct answer is {correct_answer}\n"
                    + colors["RESET"]
                )
                wrong += 1
                break


while True:
    try:
        questions_amount = int(
            input(colors["WHITE"] + "Enter the amount of questions: " + colors["RESET"])
        )
    except ValueError:
        print(colors["RED_BG_BLACK_FG"] + "Enter a valid integer!" + colors["RESET"])
        continue

    serve_questions(get_questions(questions_amount))

    print(
        colors["BLUE"]
        + f"Game finished!\nYou have solved {questions_amount} question(s) with {correct} correct answer(s) and {wrong} wrong answer(s)."
        + colors["RESET"]
    )

    if input(colors["WHITE"] + "Play again? (y/n): " + colors["RESET"]) == "n":
        print("Exiting the program...")
        break
