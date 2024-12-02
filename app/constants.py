from dotenv import dotenv_values

__config__        = dotenv_values(".env")
__url_client__    = __config__.get("MONGO_CLIENT")
__name_database__ = __config__.get("CLIENT_DATABASE")

SECRET_KEY        = __config__.get('SECRET_KEY')

RESEND_API_KEY    = __config__.get('RESEND_API_KEY')
