question_answer = {}


def jare_run(input_character, questions_user, answers_user):
    for question_ in questions_user : 
        for answer_ in answers_user: 
            question_answer[question_] = answer_ 
            answers_user.remove(answer_) 
            break
        while True:
            qs = input(input_character)
            print(question_answer[qs])