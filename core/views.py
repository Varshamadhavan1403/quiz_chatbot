from django.shortcuts import render
from django.http import JsonResponse
from .reply_factory import generate_bot_responses, start_quiz_session

def chat(request):
    if not request.session.session_key:
        request.session.create()

    request.session['message_history'] = []

    start_quiz_session(request.session)
    bot_responses = generate_bot_responses('', request.session)
    for response in bot_responses:
        request.session['message_history'].append({'is_user': False, 'text': response})
    request.session.save()

    return render(request, 'chat.html')

def start_quiz(request):
    return JsonResponse({'status': 'success'})

def reset_quiz(request):
    start_quiz_session(request.session)
    return JsonResponse({'status': 'success'})