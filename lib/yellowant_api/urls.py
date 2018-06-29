"""For creating the integration with yellowant and storing the credentials in databse"""
from django.urls import path

from .views import request_yellowant_oauth_code, yellowant_oauth_redirect, yellowant_api, spotify_redirect

urlpatterns = [
    path("create-new-integration/", request_yellowant_oauth_code, name="request-yellowant-oauth"),
    path("yellowant-oauth-redirect/", yellowant_oauth_redirect, name="yellowant-oauth-redirect"),

    # Commands are passed using yellowant-api
    path("yellowantredirecturl/", spotify_redirect, name="yellowantredirecturl"),

    #path("spotifyredirecturl/",get_spotify_access,"spotify-access"),

    path("yellowant-api/", yellowant_api, name="yellowant-api"),

    # To collect the user Credentials
    # path("apikey/", api_key, name="yellowant-api"),
]
