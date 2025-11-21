import io
from .models import Reward, Quiz, Option
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import datetime, timedelta

def create_default_rewards_once():
    """ This function adding demo rewards for once """
    Reward.objects.get_or_create(
        reward_name = "Roblox card",
        reward_value = 500,
        reward_points_required = 5000,
        reward_image = "/static/Quiz/img/redeem/000400000343_v3_262x164.png"
    )
    Reward.objects.get_or_create(
        reward_name = "Amazon Gift card",
        reward_value = 500,
        reward_points_required = 5000,
        reward_image = "/static/Quiz/img/redeem/AmazonPayIN_262x164.png"
    )
    Reward.objects.get_or_create(
        reward_name = "Bookmyshow",
        reward_value = 500,
        reward_points_required = 5000,
        reward_image = "/static/Quiz/img/redeem/BookMyShow_262x164.png"
    )
    Reward.objects.get_or_create(
        reward_name = "Flipkart Gift card",
        reward_value = 500,
        reward_points_required = 5000,
        reward_image = "/static/Quiz/img/redeem/Flipkart_262x164.png"
    )
    Reward.objects.get_or_create(
        reward_name = "Spotify Premium",
        reward_value = 60,
        reward_points_required = 5000,
        reward_image = "/static/Quiz/img/redeem/Spotify_3M_rerun_262x164.png"
    )

def create_default_quizzes_once():
    """ This function adding demo quizzes for once """

    # quiz1 #
    q, _ =  Quiz.objects.get_or_create(
                question_text = "In Python, which method is used to write text to a file?"
            )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "write()",
        is_correct = True
    )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "writing()",
        is_correct = False
    )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "print()",
        is_correct = False
    )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "read()",
        is_correct = False
    )

    # quiz2 #
    q, _ =  Quiz.objects.get_or_create(
                question_text = "In Python, what operator is used to check if two values are equal?"
            )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "==",
        is_correct = True
    )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "===",
        is_correct = False
    )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "!=",
        is_correct = False
    )
    Option.objects.get_or_create(
        quiz = q,
        option_text = "=",
        is_correct = False
    )


def award_badge(user, badge_name):
    from .models import Badge, UserBadge
    badge = Badge.objects.filter(name=badge_name).first()
    if badge and not UserBadge.objects.filter(user=user, badge=badge).exists():
        UserBadge.objects.create(user=user, badge=badge)
        return True
    return False


def generate_weekly_report(user):
    from .models import UserQuizRecord

    one_week_ago = datetime.now() - timedelta(days=7)
    records = UserQuizRecord.objects.filter(user=user, taken_at__gte=one_week_ago)

    data = []
    for r in records:
        data.append({
            'Quiz': r.quiz.question_text[:30],
            'Score': r.score,
            'Correct': 'Yes' if r.correct else 'No',
            'Time Taken (s)': r.time_taken,
            'Date': r.taken_at.strftime('%Y-%m-%d %H:%M')
        })
    df = pd.DataFrame(data)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, height - 40, f"Weekly Quiz Report for {user.username}")

    y = height - 70
    p.setFont("Helvetica", 12)
    for _, row in df.iterrows():
        line = f"{row['Date']} | {row['Quiz']} | Score: {row['Score']} | Correct: {row['Correct']} | Time: {row['Time Taken (s)']}s"
        p.drawString(30, y, line)
        y -= 20
        if y < 40:
            p.showPage()
            y = height - 40

    p.save()
    buffer.seek(0)
    return buffer
