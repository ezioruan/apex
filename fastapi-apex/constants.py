from enum import Enum, IntEnum, StrEnum

ACCESS_TOKEN_HEADER_KEY = "Authorization"
TOKEN_HEADER_VALUE_PREFIX = "Bearer"
INTERNAL_AUTHORIZATION_HEADER_KEY = "InternalAuthorization"
INTERNAL_TOKEN_EXPIRE_MINUTES = 10

SWAGGER_LOGIN_URL = "/swagger/login"
PRESIGNED_URL = "/api/v1/s3/presigned_url"

FULL_ACCESS_PERMISSION = "FullAccess"


class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50


class HTTPMessage(Enum):
    SUCCESS = "SUCCESS"


class BusinessCode(IntEnum):
    NO_ERROR = 0

    NOT_FOUND_S3_KEY = 90001


class S3ACL(StrEnum):
    PRIVATE = "private"
    PUBLIC_READ = "public-read"
    PUBLIC_READ_WRITE = "public-read-write"
    AWS_EXEC_READ = "aws-exec-read"
    AUTHENTICATED_READ = "authenticated-read"
    BUCKET_OWNER_READ = "bucket-owner-read"
    BUCKET_OWNER_FULL_CONTROL = "bucket-owner-full-control"
    LOG_DELIVERY_WRITE = "log-delivery-write"
