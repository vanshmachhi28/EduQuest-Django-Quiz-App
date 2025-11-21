from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import (
    BrainBoostPuzzle, BrainBoostResult, ContactQuery, GamifyBadge, GamifyUserBadge, UserGameProfile,
    MapQuestQuestion, MapQuestResult, Quiz, Reward, WordWhizQuestion, WordWhizResult,
    UserQuizRecord, Option, Challenge
)

# ---------------- MODULE 2: BrainBoost Puzzles -------------------
@admin.register(BrainBoostPuzzle)
class BrainBoostPuzzleAdmin(admin.ModelAdmin):
    list_display = ['puzzle_type', 'question_text', 'time_limit_seconds']
    search_fields = ['question_text']

@admin.register(BrainBoostResult)
class BrainBoostResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'puzzle', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']

# ---------------- MODULE 11: Contact Queries --------------------
@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_at', 'is_resolved']
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['name', 'subject']

# ---------------- MODULE 8: Gamification + Badges ---------------
@admin.register(UserGameProfile)
class UserGameProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'xp', 'level', 'trophies']

@admin.register(GamifyBadge)
class GamifyBadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(GamifyUserBadge)
class GamifyUserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']

# ---------------- MODULE 4: MapQuest Questions ------------------
@admin.register(MapQuestQuestion)
class MapQuestQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_type', 'question_text']
    search_fields = ['question_text']

@admin.register(MapQuestResult)
class MapQuestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_correct', 'answered_at']

# ---------------- MODULE 1 & 7: Quiz, Option, Reward -------------
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['subject', 'topic', 'difficulty', 'approved']
    list_filter = ['subject', 'difficulty', 'approved']

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'option_text', 'is_correct']

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['reward_name', 'reward_value']

# ---------------- MODULE 3: WordWhiz Questions & Results ---------
@admin.register(WordWhizQuestion)
class WordWhizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_type', 'question_text']

@admin.register(WordWhizResult)
class WordWhizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_correct', 'answered_at']

# ---------------- MODULE 5: User Quiz Records (Safe Duplicate Handling) ------------
try:
    @admin.register(UserQuizRecord)
    class UserQuizRecordAdmin(admin.ModelAdmin):
        list_display = ['user', 'quiz', 'score', 'correct', 'time_taken', 'taken_at']
        list_filter = ['correct', 'taken_at']
        search_fields = ['user__username', 'quiz__question_text']
except AlreadyRegistered:
    pass

# ---------------- MODULE 6: Challenge Mode ----------------------
@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['challenger', 'opponent', 'quiz', 'challenger_score', 'opponent_score', 'completed', 'created_at']
    list_filter = ['completed', 'created_at']
