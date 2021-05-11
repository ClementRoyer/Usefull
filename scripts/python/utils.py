# Author     : clement.royer@epitech.eu
# Descrption : Utils methods

##
# Ask user a question and expect an answer
##
# @private
# @param {string} question
# @return {string} answer
##
def ask(question):
    answer = input(question)
    if (answer == None or len(answer) == 0):
        print("❌ Can't be empty.")
        return ask(question)
    return answer
