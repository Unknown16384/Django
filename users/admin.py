from django.contrib import admin

from .models import UserProfile, Skills, SkillList

class SkillInLine(admin.StackedInline):
    model = Skills
    extra = 0

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'all_skills')
    inlines = (SkillInLine,)

    def full_name(self, obj):
        return f'{obj.family} {obj.name} {obj.surname}'
    full_name.short_description = 'ФИО'
    def all_skills(self, obj):
        return list(Skills.objects.filter(user_id=obj.id))
    all_skills.short_description = 'Навыки'

admin.site.register(SkillList)