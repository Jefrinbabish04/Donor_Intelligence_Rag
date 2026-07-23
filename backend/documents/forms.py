from django import forms


class UploadDocumentForm(forms.Form):
    file = forms.FileField(required=True)
