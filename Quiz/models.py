from django.db import models
from django.conf import settings
from django.utils import timezone

# ------------------ MODULE 1: Adaptive Quiz Generator -------------------

class Quiz(models.Model):
    question_text = models.CharField(max_length=255)
    subject = models.CharField(max_length=100, default='General')
    topic = models.CharField(max_length=100, default='General')

    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='Easy')
    category = models.CharField(max_length=100, default='General')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.topic} - {self.difficulty} - {self.question_text[:30]}"


class Option(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_text} ({'Correct' if self.is_correct else 'Wrong'})"


class Reward(models.Model):
    reward_name = models.CharField(max_length=100)
    reward_value = models.IntegerField(default=0)

    def __str__(self):
        return self.reward_name
    

    
# ------------------ MODULE 2: BrainBoost Puzzles (Math & Logic) -------------------
class BrainBoostPuzzle(models.Model):
    PUZZLE_TYPES = [
        ('sequence', 'Number Sequence'),
        ('calculation', 'Calculation'),
        ('pattern', 'Pattern Recognition'),
    ]
    puzzle_type = models.CharField(max_length=20, choices=PUZZLE_TYPES)
    question_text = models.CharField(max_length=300)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    time_limit_seconds = models.PositiveIntegerField(default=30)  # seconds allowed

    def get_options(self):
        return [self.option1, self.option2, self.option3, self.option4]

    def __str__(self):
        return f"{self.get_puzzle_type_display()} - {self.question_text[:30]}"


class BrainBoostResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    puzzle = models.ForeignKey('BrainBoostPuzzle', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

# ------------------ MODULE 3: WordWhiz Questions (Language Games) -------------------
class WordWhizQuestion(models.Model):
    QUESTION_TYPES = [
        ('synonym', 'Synonym'),
        ('antonym', 'Antonym'),
        ('sentence_correction', 'Sentence Correction'),
        ('flash_word', 'Flash Word Race'),
    ]
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES)
    question_text = models.TextField()
    choices = models.JSONField(default=list)  # List of answer choices
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_question_type_display()} - {self.question_text[:40]}"


class WordWhizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey('WordWhizQuestion', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)




# ------------------ MODULE 4: MapQuest Questions (Geography Games) -------------------
# ------------------ MapQuest Models ------------------
class MapQuestQuestion(models.Model):
    QUESTION_TYPES = [
        ('capital', 'Click Capital'),
        ('state_location', 'Locate State/Country'),
        ('flag_match', 'Match Flag'),
        ('drag_drop', 'Drag & Drop'),
    ]

    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES)
    question_text = models.TextField()
    image = models.ImageField(upload_to='mapquest/', blank=True, null=True)
    choices = models.JSONField(default=list)  # List of choices, e.g. ['Delhi', 'Mumbai', 'Bengaluru']
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_question_type_display()} - {self.question_text[:40]}"


class MapQuestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(MapQuestQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)


# ------------------ MODULE 5: User Quiz Records (Performance Tracking) -------------------
class UserQuizRecord(models.Model):
    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    time_taken = models.FloatField(default=0)  # seconds
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.quiz} | Score: {self.score}"

# Admin registration for analytics!
from django.contrib import admin

@admin.register(UserQuizRecord)
class UserQuizRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'correct', 'time_taken', 'taken_at')
    list_filter = ('correct', 'taken_at')
    search_fields = ('user__username', 'quiz__question_text')
    ordering = ('-taken_at',)







# ------------------ MODULE 6: Challenge Mode -------------------
class Challenge(models.Model):
    challenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='challenges_sent',
        on_delete=models.CASCADE
    )
    opponent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='challenges_received',
        on_delete=models.CASCADE
    )
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    challenger_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Challenge: {self.challenger} vs {self.opponent} on {self.quiz}"
    




# ------------------ MODULE 8: Gamification + Badges -------------------
class UserGameProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    trophies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} GameProfile"

    def gain_xp(self, amount):
        self.xp += amount
        level_up = False
        while self.xp >= self.next_level_xp():
            self.xp -= self.next_level_xp()
            self.level += 1
            level_up = True
        self.save()
        return level_up

    def next_level_xp(self):
        return 100 + (self.level - 1) * 30

class GamifyBadge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    criteria = models.TextField(help_text="Earning requirement")

    def __str__(self):
        return self.name

class GamifyUserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ForeignKey(GamifyBadge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


# ------------------ MODULE 11: Contact Us Queries -------------------
class ContactQuery(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"






