from django import forms
from .models import Document,Folder

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload', )

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name', )