from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1
    raw_id_fields = ('author',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'rating')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('created_at', )
    raw_id_fields = ('author',) 
    inlines = [AnswerInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at', 'is_correct')
    raw_id_fields = ('author', 'question')

admin.site.register(QuestionLike)
admin.site.register(AnswerLike)