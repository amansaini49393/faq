from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FAQ

class FAQListView(APIView):
    def get(self, request):
        lang = request.query_params.get('lang', 'en')
        cache_key = f'faqs_{lang}'
        cached_data = cache.get(cache_key)

        if not cached_data:
            faqs = FAQ.objects.all()
            data = []
            for faq in faqs:
                translation = faq.get_translation(lang)
                data.append({
                    "question": translation["question"],
                    "answer": translation["answer"]
                })
            cache.set(cache_key, data, timeout=60 * 15)  # Cache 15 minutes
            return Response(data)
        return Response(cached_data)