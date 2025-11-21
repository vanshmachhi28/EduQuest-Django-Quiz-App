import random


from pyexpat.errors import messages
from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from Account import models
from Account.models import CustomUser
from .models import BrainBoostResult, GamifyBadge, GamifyUserBadge, MapQuestQuestion, MapQuestResult, Reward, Quiz, Option ,Challenge, UserGameProfile, WordWhizResult
from .utils import create_default_rewards_once
from .utils import create_default_quizzes_once
from .utils import generate_weekly_report
from .models import BrainBoostPuzzle, WordWhizQuestion, BrainBoostResult
from .utils import award_badge
from .models import UserQuizRecord, ContactQuery, Quiz, Option
from random import choice as random_choice, random, sample
from random import sample as random_sample
from json import dumps as json_dumps
from django.utils import timezone
from random import choice as random_choice
from random import sample as random_sample
from django.db.models import Avg






# ----------------------- AUTHENTICATION MODULE -----------------------
def login(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request,"Quiz/login.html")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(request,"Quiz/login.html", {"message":"Wrong credentials. please check!"})

def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request,"Quiz/signup.html")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")
        try:
            if  password == re_password:
                CustomUser.objects.create_user(username=username, password=password)
                return redirect("login")
            else:
                return render(request,"Quiz/signup.html", {"message":"Password doesn't mach. please check!"})
        except Exception as e:
                return render(request,"Quiz/signup.html", {"message":"User already exist !"})

@login_required(login_url="login")
def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request)
    return redirect("login")

# ----------------------- HOME MODULE -----------------------
@login_required(login_url="login")
def home(request: HttpRequest) -> HttpResponse:
    context = {
        "admin":request.user.is_superuser
    }
    return render(request,"Quiz/index.html", context)

# ----------------------- REWARD MODULE -----------------------
@login_required(login_url="login")
def redeem(request: HttpRequest) -> HttpResponse:
    create_default_rewards_once()
    context={
        "rewards" : Reward.objects.all()
    }
    return render(request,"Quiz/redeem.html", context)

# ----------------------- MODULE 1: ADAPTIVE QUIZ GENERATOR -----------------------
@login_required(login_url="login")
def quiz(request):
    selected_subject = request.GET.get('subject', 'General')
    selected_difficulty = request.GET.get('difficulty', 'Easy')
    quizzes = Quiz.objects.filter(subject=selected_subject, difficulty=selected_difficulty, approved=True)

    if not quizzes.exists():
        quizzes = Quiz.objects.filter(approved=True)

    if request.method == "POST":
        quiz_id = int(request.POST.get('quiz_id'))
        selected_option = request.POST.get('option')

        try:
            quiz_obj = Quiz.objects.get(id=quiz_id)
            options = Option.objects.filter(quiz=quiz_obj)
            correct_option = options.filter(is_correct=True).first()

            if selected_option == str(correct_option.id):
                messages.success(request, "Correct answer! Well done.")
                return redirect('quiz')  # Redirect for next quiz
            else:
                messages.error(request, "Wrong answer. Try the next question.")
                return redirect('quiz')

        except Quiz.DoesNotExist:
            messages.error(request, "Quiz not found.")
            return redirect('quiz')

    q = random.choice(quizzes)
    options = Option.objects.filter(quiz=q)
    context = {
        'quiz': q,
        'options': options
    }
    return render(request, 'quiz/quiz.html', context)


#Module no . 2 
@login_required(login_url="login")
def brainboost_home(request):
    # BrainBoost category selection screen
    categories = BrainBoostPuzzle.PUZZLE_TYPES
    return render(request, "Quiz/brainboost_home.html", {"categories": categories})

@login_required(login_url="login")
def brainboost_quiz(request, category):
    # Handles sequential quiz flow for 10 questions
    all_puzzles = list(BrainBoostPuzzle.objects.filter(puzzle_type=category))
    if not all_puzzles:
        return render(request, "Quiz/brainboost_quiz.html", {'error': 'No puzzles for this category.'})

    # Figure out where we are in the quiz sequence
    questions_per_quiz = 10
    quiz_session = request.session.setdefault('brainboost_quiz', {})
    quiz_session.setdefault('category', category)
    quiz_session.setdefault('puzzle_ids', [p.pk for p in sample(all_puzzles, min(questions_per_quiz, len(all_puzzles)))])
    quiz_session.setdefault('curr_idx', 0)
    quiz_session.setdefault('score', 0)
    request.session.modified = True

    curr_idx = quiz_session['curr_idx']
    puzzle_ids = quiz_session['puzzle_ids']

    # End of quiz, show results
    if curr_idx >= len(puzzle_ids):
        total_score = quiz_session['score']
        correct_out_of = curr_idx
        request.session.pop('brainboost_quiz', None)
        return render(request, "Quiz/brainboost_result.html", {
            "score": total_score,
            "total": correct_out_of,
            "category": dict(BrainBoostPuzzle.PUZZLE_TYPES)[category]
        })

    puzzle = BrainBoostPuzzle.objects.get(pk=puzzle_ids[curr_idx])
    if request.method == 'GET':
        return render(request, "Quiz/brainboost_quiz.html", {
            "puzzle": puzzle,
            "options": puzzle.get_options(),
            "category": puzzle.get_puzzle_type_display(),
            "time_limit": puzzle.time_limit_seconds,
            "curr": curr_idx+1,
            "total": len(puzzle_ids),
        })

    if request.method == 'POST':
        selected = request.POST.get("selected_answer")
        is_correct = (selected == puzzle.correct_answer)
        # Save result for admin/statistics
        BrainBoostResult.objects.create(
            user=request.user, puzzle=puzzle, selected_option=selected or '', is_correct=is_correct
        )
        if is_correct:
            quiz_session['score'] += 1
        quiz_session['curr_idx'] += 1
        request.session.modified = True
        # Redirect to the same view to show next or final result
        return redirect('brainboost_quiz', category=category)

# Admin/staff result view (optional)
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def brainboost_results_admin(request):
    results = BrainBoostResult.objects.select_related('user', 'puzzle').order_by('-answered_at')
    return render(request, "Quiz/brainboost_results_admin.html", {"results": results})





# --------------- MODULE 3: WORDWHIZ (GRAMMAR & VOCAB GAMES) ---------------
@login_required(login_url="login")
def wordwhiz_home(request):
    categories = WordWhizQuestion.QUESTION_TYPES
    return render(request, 'Quiz/wordwhiz_home.html', {'categories': categories})

@login_required(login_url="login")
def wordwhiz_quiz(request, category):
    questions = WordWhizQuestion.objects.filter(question_type=category)
    if not questions.exists():
        return render(request, 'Quiz/wordwhiz_quiz.html', {'error': 'No questions for this category.'})

    questions_list = list(questions)
    questions_per_quiz = 10

    # control quiz flow via session
    session = request.session.setdefault('wordwhiz_quiz', {})
    if session.get('category') != category:
        session['category'] = category
        session['question_ids'] = [q.pk for q in questions_list[:questions_per_quiz]]
        session['current'] = 0
        session['score'] = 0
        request.session.modified = True

    current = session['current']
    question_ids = session['question_ids']

    # end condition
    if current >= len(question_ids):
        score = session['score']
        total = current
        request.session.pop('wordwhiz_quiz')
        return render(request, 'Quiz/wordwhiz_result.html', {'score': score, 'total': total, 'category': category})

    question = WordWhizQuestion.objects.get(pk=question_ids[current])

    if request.method == 'GET':
        return render(request, 'Quiz/wordwhiz_quiz.html', {
            'question': question,
            'choices': question.choices,
            'category': question.get_question_type_display(),
            'current': current + 1,
            'total': len(question_ids),
            'time_limit': 30,
        })

    if request.method == 'POST':
        selected = request.POST.get('selected_answer')
        is_correct = (selected == question.correct_answer)
        WordWhizResult.objects.create(
            user=request.user,
            question=question,
            selected_option=selected or '',
            is_correct=is_correct
        )
        if is_correct:
            session['score'] += 1
        session['current'] += 1
        request.session.modified = True
        return redirect('wordwhiz_quiz', category=category)
    





# --------------- MODULE 4: MAPQUEST (GEOGRAPHY GAMES) ---------------
@login_required(login_url='login')
def mapquest_home(request):
    categories = MapQuestQuestion.QUESTION_TYPES
    return render(request, 'Quiz/mapquest_home.html', {'categories': categories})


@login_required(login_url='login')
def mapquest_quiz(request, category):
    questions = MapQuestQuestion.objects.filter(question_type=category)
    if not questions.exists():
        return render(request, 'Quiz/mapquest_quiz.html', {'error': 'No questions available for this category.'})

    questions = list(questions)
    question_ids = request.session.get('mapquest_question_ids')
    if not question_ids or request.session.get('mapquest_category') != category:
        question_ids = [q.pk for q in questions[:10]]
        request.session['mapquest_question_ids'] = question_ids
        request.session['mapquest_category'] = category
        request.session['mapquest_current'] = 0
        request.session['mapquest_score'] = 0

    current = request.session.get('mapquest_current', 0)
    score = request.session.get('mapquest_score', 0)

    if current >= len(question_ids):
        # Quiz finished
        total = len(question_ids)
        request.session.pop('mapquest_question_ids')
        request.session.pop('mapquest_category')
        request.session.pop('mapquest_current')
        request.session.pop('mapquest_score')
        return render(request, 'Quiz/mapquest_result.html', {'score': score, 'total': total, 'category': dict(MapQuestQuestion.QUESTION_TYPES)[category]})

    question = MapQuestQuestion.objects.get(pk=question_ids[current])

    if request.method == 'GET':
        return render(request, 'Quiz/mapquest_quiz.html', {
            'question': question,
            'choices': question.choices,
            'current': current + 1,
            'total': len(question_ids),
            'category': question.get_question_type_display(),
            'image': question.image.url if question.image else None,
            'time_limit': 30,
        })

    if request.method == 'POST':
        selected_option = request.POST.get('selected_option')
        is_correct = (selected_option == question.correct_answer)

        MapQuestResult.objects.create(
            user=request.user,
            question=question,
            selected_option=selected_option or '',
            is_correct=is_correct,
        )

        if is_correct:
            request.session['mapquest_score'] = score + 1
        request.session['mapquest_current'] = current + 1
        request.session.modified = True

        return redirect('mapquest_quiz', category=category)


@staff_member_required
def mapquest_results_admin(request):
    results = MapQuestResult.objects.select_related('user', 'question').order_by('-answered_at')
    return render(request, 'Quiz/mapquest_results_admin.html', {'results': results})



# ----------------- MODULE 5: PERFORMANCE TRACKER & ANALYTICS -----------------
@login_required(login_url="login")
def performance_tracker(request):
    records = UserQuizRecord.objects.filter(user=request.user)
    total_attempts = records.count()
    correct_count = records.filter(correct=True).count()
    avg_time = records.aggregate(avg=Avg('time_taken'))['avg'] or 0
    accuracy = int((correct_count / total_attempts) * 100) if total_attempts else 0

    topic_counts = {}
    for rec in records:
        topic = getattr(rec.quiz, 'topic', 'Unknown')
        topic_counts[topic] = topic_counts.get(topic, 0) + 1

    topic_sorted = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

    context = {
        'accuracy': accuracy,
        'avg_time': round(avg_time, 2),
        'records': records,
        'topic_counts': topic_sorted,
    }
    return render(request, 'Quiz/performance_tracker.html', context)





# -------------------- MODULE 6: CHALLENGE MODE ----------------------
@login_required(login_url="login")
def challenge_mode(request):
    # Show list of users and quizzes to create a challenge
    if request.method == 'GET':
        users = CustomUser.objects.exclude(pk=request.user.pk)
        quizzes = Quiz.objects.all()
        
        # Also, fetch challenges sent to current user that are not completed
        pending_challenges = Challenge.objects.filter(opponent=request.user, completed=False)
        
        context = {
            'users': users,
            'quizzes': quizzes,
            'pending_challenges': pending_challenges,
        }
        return render(request, 'Quiz/challenge_mode.html', context)

    if request.method == 'POST':
        opponent_id = request.POST.get('opponent')
        quiz_id = request.POST.get('quiz')
        opponent = get_object_or_404(CustomUser, pk=opponent_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        challenge = Challenge.objects.create(
            challenger=request.user,
            opponent=opponent,
            quiz=quiz
        )
        return JsonResponse({'success': True, 'challenge_id': challenge.id})
    



# ----------------- MODULE 7: QUESTION MANAGEMENT & SUBMISSION ---------------
@login_required(login_url="login")
def submit_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        subject = request.POST.get('subject')
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        category = request.POST.get('category', 'General')
        Quiz.objects.create(
            question_text=question_text,
            subject=subject,
            topic=topic,
            difficulty=difficulty,
            category=category,
            approved=False # Needs admin approval
        )
        return render(request, 'Quiz/submit_question.html', {'success': True})
    return render(request, 'Quiz/submit_question.html')

# ------------ MODULE 8: PROFILE, BADGES, GAMIFICATION ---------------
@login_required
def leaderboard_view(request):
    leaderboard = UserGameProfile.objects.select_related('user').order_by('-level', '-xp')[:10]
    return render(request, 'Quiz/leaderboard.html', {'leaderboard': leaderboard})

@login_required
def badge_showcase_view(request):
    user_badges = GamifyUserBadge.objects.filter(user=request.user).select_related('badge')
    return render(request, 'Quiz/badges.html', {'badges': user_badges})

# Example badge award function
def award_badge(user, badge_name):
    badge, _ = GamifyBadge.objects.get_or_create(name=badge_name)
    if not GamifyUserBadge.objects.filter(user=user, badge=badge).exists():
        GamifyUserBadge.objects.create(user=user, badge=badge)

# Example: Call this logic after a quiz completion
@login_required
def quiz_complete_view(request):
    profile, _ = UserGameProfile.objects.get_or_create(user=request.user)
    xp_earned = 50  # Example
    level_up = profile.gain_xp(xp_earned)
    if level_up:
        award_badge(request.user, "Level Up Star")
    # Check for more badges and do the rest
    return redirect('leaderboard')

# ------------ MODULE 9: PDF EMAIL WEEKLY REPORTS/ADMIN/TEACHER DASH -------------
@login_required(login_url="login")
def download_weekly_report(request):
    pdf_buffer = generate_weekly_report(request.user)
    return FileResponse(pdf_buffer, as_attachment=True, filename='weekly_report.pdf')

# ------------ MODULE 10: ABOUT US PAGE ---------------
def about_us(request):
    return render(request, 'Quiz/about_us.html')

# ------------ MODULE 11: CONTACT US PAGE ---------------
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and subject and message:
            ContactQuery.objects.create(name=name, subject=subject, message=message)
            return render(request, 'Quiz/contact_us.html', {'success': True})

    return render(request, 'Quiz/contact_us.html')


def home(request):
    incomplete_challenges = 0
    if request.user.is_authenticated:
        incomplete_challenges = request.user.challenges_received.filter(completed=False).count()
    # add any existing context you have here...
    return render(request, 'Quiz/index.html', {
        # ...other context...
        'incomplete_challenges': incomplete_challenges,
    })




