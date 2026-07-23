from django.shortcuts import render

from documents.forms import UploadDocumentForm


def upload_view(request):
    message = ''
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            message = f'Uploaded {uploaded_file.name}'
    else:
        form = UploadDocumentForm()

    return render(request, 'upload.html', {'form': form, 'message': message})
