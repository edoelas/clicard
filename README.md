Clicards is a really simple script to review flashcards from the terminal. It has been programmed with python.  Its main advantages over other options like anki are:

- **Easy and fast flashcard creation**: A set of flashcards is just a csv file. Each column is one side of the flashcard (more than two can exist). The first row of the csv file must be the name of the information stored and from there, each row is a flashcard.

  This is an example for learning chines characters:

  ```
  Hanzi,	Pinyin,	Meaning
  你,		nǐ,		You
  好,		hǎo,	Good
  你好,		nǐ hǎo,	Hi
  我,		wǒ,		I
  是,		shì,	To be
  ```

  

- **Easy and fast question creation**: Each type of question is configured in a different json file. The json file consist in a dictionary which keys are a the information to be asked about and the values how it will be asked. As many questions as you want can be made in the order you want.

  This is an example that shows the hanzi and asks for its meaning in a multiple choice question:

  ```json
  {
      "Hanzi": "show",
      "Meaning": "choose"
  }
  ```



- **Easy to modify**: All the code consist in less than 150 lines, including comments. The code is really simple to understand. To add new ways to ask questions you just need to program a function that gets a correct answer and a list of possible answers and returns true or false. After that you just need to add a line in a dict that binds each option in the json configuration file with the function.

  This is the code for the multiple choice question and the dictionary that binds the configuration with the functions:

  ```python
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
      
  question_type = {
      "show": show_question,
      "write": write_answer,
      "choose": choose_answer,
      "bool": bool_answer
  }
  ```

  the function `input2` is a wrapper of `input` that when the input is "exit" exits the main loop.



Other features are:

- The script also takes care of writing in the same csv file the amount of right and wrong answers for a certain flashcards with a certain configuration. 
- The script asks more frequently for the flashcards that have been answered wrong or have not been asked as much as the others. 
- At the end of each execution tells you the amount of wrong and right answers.



The way I was thinking to use this script when I made it was to have multiple sets of flashcards (for example, a set for different levels or themes) and multiple ways to make questions (for example, one gives you the English word and you have to write the Chinese word, another gives you the Chinese word and you have to write the pronunciation etc.), all of this without investing too much time to develop the flashcards or the questions.

There are some features that I have decided to exclude to keep it simple: a ncurses or graphical interface, audio or image support or the possibility of define the different options of the multiple choice questions.

To run the script just exec `clicard.py flashcards_file.csv config_file.json`