import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_folders')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)

    def file_exists(self):
        """
        파일이 실제로 존재하는지 확인하는 메서드
        """
        return os.path.isfile(self.upload.path)

# 파일이 존재하지 않으면 데이터베이스에서 Document 인스턴스를 삭제하는 시그널
@receiver(models.signals.pre_save, sender=Document)
def delete_if_file_not_exists(sender, instance, **kwargs):
    """
    Document를 저장하기 전에 파일이 존재하지 않으면 삭제하는 로직
    """
    if instance.pk:  # 업데이트 시에만 체크
        try:
            old_file = Document.objects.get(pk=instance.pk).upload
            if not os.path.isfile(old_file.path):
                # 파일이 존재하지 않으면 데이터베이스 레코드 삭제
                instance.delete()
        except Document.DoesNotExist:
            pass

# 기존 파일 삭제 시 기존 파일 제거
@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Document 모델 인스턴스가 삭제될 때 해당 파일도 삭제합니다.
    """
    if instance.upload:
        if os.path.isfile(instance.upload.path):
            os.remove(instance.upload.path)

# 파일 변경 시 기존 파일 삭제
@receiver(models.signals.pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Document 파일이 변경될 때 기존 파일을 삭제합니다.
    """
    if not instance.pk:
        return False

    try:
        old_file = Document.objects.get(pk=instance.pk).upload
    except Document.DoesNotExist:
        return False

    new_file = instance.upload
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# 파일이 없으면 예외를 처리하고, 사용자에게 메시지를 보여줍니다.
def get_file_size_or_zero(document):
    try:
        if os.path.exists(document.upload.path):
            return os.path.getsize(document.upload.path)
        else:
            return 0  # 파일이 없으면 크기를 0으로 반환
    except FileNotFoundError:
        return 0
