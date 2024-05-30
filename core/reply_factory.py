from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def start_quiz_session(session):
    '''
    Initializes a new quiz session by setting the current_question_id to 0 and score to 0.
    '''
    session['current_question_id'] = 0  # Set to the index of the first question
    session['score'] = 0
    session.save()

def update_current_question(session):
    '''
    Updates the current_question_id to the index of the next question.
    '''
    current_question_id = session.get('current_question_id')
    if current_question_id is not None:
        # Increment to the index of the next question
        session['current_question_id'] = current_question_id + 1
        session.save()

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        session["current_question_id"] = 0
        session.save()
        return bot_responses

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is None:
        return False, "No question is active."

    question = PYTHON_QUESTION_LIST[current_question_id]
    correct_answer = question['answer']

    if answer == correct_answer:
        session['score'] = session.get('score', 0) + 1
        session.save()
        return True, ""
    else:
        return False, "Incorrect answer. Try again."

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0]['question_text'], 0
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[0]['question_text'], next_question_id
    else:
        return None, -1

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    final_score = session.get('score', 0)
    total_que = len(PYTHON_QUESTION_LIST)
    percentage = (final_score / total_que) * 100
    final_response = f"Quiz completed!\nYour score: {final_score}/{total_que} ({percentage:.2f}%)."

    return final_response
