from django.contrib import admin
from .models import FAQ, FAQTranslation
from ckeditor.widgets import CKEditorWidget
from django import forms

class FAQAdminForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'answer': CKEditorWidget(),
        }

class FAQTranslationAdminForm(forms.ModelForm):
    class Meta:
        model = FAQTranslation
        fields = '__all__'
        widgets = {
            'translated_answer': CKEditorWidget(),
        }

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm
    list_display = ('question', 'answer')

@admin.register(FAQTranslation)
class FAQTranslationAdmin(admin.ModelAdmin):
    form = FAQTranslationAdminForm
    list_display = ('faq', 'language', 'translated_question')