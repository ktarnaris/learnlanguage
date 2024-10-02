from os import walk
from re import template
from django.http import HttpResponse
from django.template import context, loader
from django.shortcuts import render
import random

# from . import main.main
from quiz.functions import main


def welcome_page(request):
    count = main.count_words()
    template = loader.get_template("welcome.html")
    context = {
        "count": count,
    }
    return HttpResponse(template.render(context, request))


def list_words(request):
    list = main.return_all_values(main.filter(""))
    template = loader.get_template("list.html")
    context = {
        "list": list,
    }
    return HttpResponse(template.render(context, request))


def quiz(request):
    # Check if there is already a word and answers in the session (for consistency across requests)

    # Set difficulty level - default if it is unset
    request.session["set_difficulty"] = (
        3
        if "set_difficulty" not in request.session
        else request.session["set_difficulty"]
    )

    # Set date - fallback to "" if it is unset
    request.session["set_date"] = (
        "" if "set_date" not in request.session else request.session["set_date"]
    )

    # Check if words is saved in the session - if not then populated with words
    if "the_word" not in request.session or "possible_answers" not in request.session:
        the_word, possible_answers = main.quiz(
            request.session["set_difficulty"], main.filter(request.session["set_date"])
        )
        request.session["the_word"] = the_word  # Store in session
        request.session["possible_answers"] = possible_answers  # Store in session
    else:
        the_word = request.session["the_word"]
        possible_answers = request.session["possible_answers"]

    template = loader.get_template("quiz.html")
    context = {
        "the_word": the_word["el"],
        "possible_answers": possible_answers,
    }

    if request.method == "POST":
        # Capture input from form
        user_input = request.POST.get("input_data", "")

        # Check if the user's answer is correct
        if main.find_the_correct(the_word, user_input):
            user_input = "🗸 Correct Answer! Go to next question."
            # Clear specific session keys after processing the POST request
            if "the_word" in request.session:
                del request.session["the_word"]
            if "possible_answers" in request.session:
                del request.session["possible_answers"]
        else:
            user_input = "✗ Wrong Answer! Try Again."

        # Update the context with the result
        context["results"] = user_input

    return HttpResponse(template.render(context, request))


def prepare_quiz(request):
    request.session["set_date"] = (
        "" if "set_date" not in request.session else request.session["set_date"]
    )

    if "words_pool" not in request.session not in request.session:
        words_pool = main.return_all_values(main.filter(request.session["set_date"]))
    else:
        words_pool = request.session["words_pool"]

    template = loader.get_template("prepare.html")

    # Check for end of available words
    remaining = len(words_pool)
    status = remaining != 0

    to_show = words_pool.pop(random.randint(0, len(words_pool) - 1))
    context = {
        "question": to_show["el"],
        "answer": to_show["de"],
        "remaining": remaining,
        "status": status,
    }

    # Update session words after .pop
    request.session["words_pool"] = words_pool

    return HttpResponse(template.render(context, request))


def settings(request):
    template = loader.get_template("settings.html")
    context = {}

    if request.method == "POST":
        # Capture input from form
        request.session.clear()
        request.session["set_difficulty"] = int(request.POST.get("set_difficulty"))

        request.session["set_date"] = request.POST.get("set_date")

    return HttpResponse(template.render(context, request))
