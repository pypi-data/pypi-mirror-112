# These are all the empty lists we will need.
question_answer_list = {}

# This is for the command: jare_run_list
def jare_run_list(input_character_list, question_list_from_user_jare, answer_list_from_user_jare):
    # This converts the two lists in to one dictionary
    for question_ in question_list_from_user_jare : 
        for answer_ in answer_list_from_user_jare: 
            question_answer_list[question_] = answer_ 
            answer_list_from_user_jare.remove(answer_) 
            break
        # This ask's the user for input and then print's out the response
        while True:
            list_input_from_user = input(input_character_list)
            print(question_answer_list[list_input_from_user])


# This is for the command: jare_run_dictionary
def jare_run_dictionary(input_character_dictionary, dictionary_dictionary_from_user_jare):
    # This ask's the user for input and then print's out the response
    while True:
            dictionary_input_from_user = input(input_character_dictionary)
            print(dictionary_dictionary_from_user_jare[dictionary_input_from_user])