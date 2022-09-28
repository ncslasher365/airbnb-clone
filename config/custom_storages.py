from storages.backends.s3boto3 import S3Boto3Storage


class StatisStorage(S3Boto3Storage):
    location = "static/"
    file_overwrite = False


class UploadStorage(S3Boto3Storage):
    location = "uploads/"
    file_overwrite = False
