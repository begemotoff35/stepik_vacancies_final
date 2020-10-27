# Чистим storage
from django.core.files.storage import get_storage_class

storage = get_storage_class()
print(storage)
