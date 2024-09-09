from django.core.management.base import BaseCommand
from cloudapp.models import Document
import os

class Command(BaseCommand):
    help = '서버에 없는 파일을 참조하는 Document 레코드를 정리합니다.'

    def handle(self, *args, **kwargs):
        documents = Document.objects.all()

        for document in documents:
            if document.upload and not os.path.exists(document.upload.path):
                self.stdout.write(f"Deleting {document.upload.name} as file does not exist.")
                document.delete()
