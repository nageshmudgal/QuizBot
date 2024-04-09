
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question and next_question_id==0:
        bot_responses.append(next_question)
    elif next_question and next_question_id!=0:
        bot_responses.clear()
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id!=None and current_question_id!=-1:
        print(current_question_id)
        if PYTHON_QUESTION_LIST[current_question_id]['answer']==answer:
            score = session.get("score")
            session["score"] = score+1
            session.save()
    
    return True, ""


def get_next_question(current_question_id):

    if current_question_id==None:
        temp = PYTHON_QUESTION_LIST[0]['question_text']+"\n options are: \n"
        for i in PYTHON_QUESTION_LIST[0]['options']:
            temp=temp+i+",\n"
        return temp,0

    elif current_question_id==9:
        return None,-1

    else:
        current_question_id +=1 
        temp = PYTHON_QUESTION_LIST[current_question_id]['question_text']+"\n options are: \n"
        for i in PYTHON_QUESTION_LIST[current_question_id]['options']:
            temp=temp+i+",\n"
        return temp,current_question_id



def generate_final_response(session):

    return "Your result is "+str(session["score"])+" out of 10"
