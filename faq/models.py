from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from google.cloud import translate_v2 as translate
from django.conf import settings
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS

class FAQ(models.Model):
    question = models.TextField(_("Question (English)"))
    answer = RichTextField(_("Answer (English)"))

    def get_translation(self, lang):
        translation = FAQTranslation.objects.filter(faq=self, language=lang).first()
        if translation:
            return {
                "question": translation.translated_question,
                "answer": translation.translated_answer
            }
        return {
            "question": self.question,
            "answer": self.answer
        }

    def __str__(self):
        return self.question

class FAQTranslation(models.Model):
    LANGUAGES = [
        ('hi', 'Hindi'),
        ('bn', 'Bengali'),
        # Add more languages here
    ]

    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE)
    language = models.CharField(max_length=5, choices=LANGUAGES)
    translated_question = models.TextField()
    translated_answer = RichTextField()

    def save(self, *args, **kwargs):
        if not self.translated_question or not self.translated_answer:
            client = translate.Client()
            try:
                if not self.translated_question:
                    result = client.translate(self.faq.question, target_language=self.language)
                    self.translated_question = result['translatedText']
                if not self.translated_answer:
                    result = client.translate(self.faq.answer, target_language=self.language)
                    self.translated_answer = result['translatedText']
            except Exception:
                # Fallback to English
                self.translated_question = self.faq.question
                self.translated_answer = self.faq.answer
        super().save(*args, **kwargs)