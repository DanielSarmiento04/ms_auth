import os

__config__        = os.environ
__url_client__    = __config__.get("MONGO_CLIENT")
__name_database__ = __config__.get("CLIENT_DATABASE")

SECRET_KEY        = __config__.get('SECRET_KEY')

RESEND_API_KEY    = __config__.get('RESEND_API_KEY')
