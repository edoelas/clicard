#!/usr/bin/env python

import pandas as pd
import json
import random
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def input2():
    global keep_asking
    user_answer = input()
    if user_answer == "exit":
        keep_asking = False
        return user_answer
    return user_answer


def write_answer(right_answer, options):
    print("Writte answer: ")
    user_answer = input2()
    return user_answer == right_answer


def choose_answer(right_answer, options):
    choices = random.choices(options,k=3) + [right_answer]
    random.shuffle(choices)
    for index,choice in enumerate(choices):
        print(str(index) + ". " + choice)
    print("Choose answer: ")
    user_answer = input2()
    if user_answer not in ["0","1","2","3"]:
        return False
    return choices[int(user_answer)] == right_answer


def bool_answer(right_answer, options):
    option = random.choices([random.choices(options),right_answer])
    print(option)
    print("True or False: ")
    user_answer = input2()
    return (user_answer == "t") != (right_answer == option)


def show_question(right_answer, options):
   print(right_answer)
   return True

def main():
    flashcards_path = sys.argv[1]
    config_path = sys.argv[2]
    # Read flashcards headers
    flashcards = pd.read_csv(flashcards_path,index_col=None)
    # Read config
    config = {}
    with open(config_path) as json_file:
        config = json.load(json_file)
    # Check adequate config
    config_keys = list(config.keys())
    flashcards_headers = list(flashcards)

    if all(x in flashcards_headers for x in config_keys):
        # If prob column exist load it, else create it
        right_answers_column_name = "right_" + config_path
        wrong_answers_column_name = "wrong_" + config_path
        right_answers = []
        wrong_answers = []
        if right_answers_column_name in flashcards and wrong_answers_column_name in flashcards:
            right_answers = flashcards[right_answers_column_name].tolist()
            wrong_answers = flashcards[wrong_answers_column_name].tolist()
        else:
            rows = len(flashcards.index)
            right_answers = [0] * rows
            wrong_answers = [0] * rows

        # While not exit
        while keep_asking:
            # Choose random row and create dict
            rows = len(flashcards.index)
            probs = [max(w*2 - r+10,1)  for r,w in zip(right_answers,wrong_answers)]
            row_index = random.choices(range(0,rows), weights=probs)[0]
            row_dict = flashcards.iloc[row_index].to_dict()
            # Read config dictionary
            right = True
            for key in config:
                # Apply functions in order (return true or false)
                answer = row_dict[key]
                options = flashcards[key].tolist()
                question = question_type[config[key]]
                user_output = question(answer,options)
                if not keep_asking:
                    break
                print("----")
                right = right and user_output
                
            if keep_asking:
                if right:
                    right_answers[row_index] += 1
                    print(f"{bcolors.OKGREEN}CORRECT{bcolors.ENDC}")
                else:
                    wrong_answers[row_index] += 1
                    print(f"{bcolors.FAIL}WRONG!!{bcolors.ENDC}")

            print("")
            print("")
            


        # Print sumary
        if sum(wrong_answers) == 0:
            print("Ratio: INF" )
        else:
            print("Num right answers: " + str( sum(right_answers) - sum(flashcards[right_answers_column_name].tolist()) ) )
            print("Num wrong answers: " + str( sum(wrong_answers) - sum(flashcards[wrong_answers_column_name].tolist()) ) )
            

        # save statistics 
        flashcards[right_answers_column_name] = right_answers 
        flashcards[wrong_answers_column_name] = wrong_answers 
        flashcards.to_csv(flashcards_path,index=False)

    else:
        print("configuration and flashcard do not match")


question_type = {
    "show": show_question,
    "write": write_answer,
    "choose": choose_answer,
    "bool": bool_answer
}
keep_asking = True

if __name__ == "__main__":
    main()

