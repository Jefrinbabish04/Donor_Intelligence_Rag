import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from donors.models import Donor
from rag.rag_service import RAGService
from documents.forms import UploadDocumentForm


rag_service = RAGService()


def index_view(request):
    return render(request, 'index.html')


def chat_view(request):
    return render(request, 'chat.html')


def donor_search_view(request):
    query = request.GET.get('q', '')
    donors = []
    if query:
        donors = Donor.objects.filter(name__icontains=query)[:10]
    return render(request, 'donors.html', {'query': query, 'donors': donors})


def dashboard_view(request):
    return render(request, 'dashboard.html', {
        'donor_count': Donor.objects.count(),
        'document_count': 2,
        'chunk_count': 24,
    })


@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    payload = json.loads(request.body)
    question = payload.get('question', '').strip()
    if not question:
        return JsonResponse({'error': 'Question required'}, status=400)

    result = rag_service.ask(question)
    return JsonResponse({'answer': result.get('answer', '')})
