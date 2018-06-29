"""Views of application front end"""
import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from yellowant import YellowAnt
from ..yellowant_api.models import UserIntegration, spotify
# Create your views here.


def index(request, path):
    """Basic home page request"""
    context = {
        "base_href": settings.BASE_HREF,
        "application_id": settings.YA_APP_ID,
        "user_integrations": []
    }
    # Appends each integrations to the user integrations
    if request.user.is_authenticated:
        user_integrations = UserIntegration.objects.filter(user=request.user.id)
        for user_integration in user_integrations:
            context["user_integrations"].append(user_integration)

    # For loading the home page
    return render(request, "home.html", context)


def userdetails(request):

    """ Function which returns all the user integrations to be displayed on Home page"""
    user_integrations_list = []
    if request.user.is_authenticated:
        user_integrations = UserIntegration.objects.filter(user=request.user.id)
        for user_integration in user_integrations:

            # Checks if that particular integration is integrated with AWS or not
            try:
                smut = spotify.objects.get(id_id=user_integration.id)
                user_integrations_list.append({"user_invoke_name": user_integration.yellowant_integration_invoke_name,
                                               "id": user_integration.id, "app_authenticated": True,
                                               "is_valid": smut.update_login_flag})
            except UserIntegration.DoesNotExist:
                user_integrations_list.append({"user_invoke_name": user_integration.yellowant_integration_invoke_name,
                                               "id": user_integration.id,
                                               "app_authenticated": False})

    return HttpResponse(json.dumps(user_integrations_list), content_type="application/json")


def delete_integration(request, id=None):
    # Function for deleting an integration by taking the id as input.
    print(id)
    access_token_dict = UserIntegration.objects.get(id=id)
    user_id = access_token_dict.user
    if user_id == request.user.id:

        access_token = access_token_dict.yellowant_integration_token
        user_integration_id = access_token_dict.yellowant_integration_id
        url = "https://api.yellowant.com/api/user/integration/%s" % (user_integration_id)
        yellowant_user = YellowAnt(access_token=access_token)
        profile = yellowant_user.delete_user_integration(id=user_integration_id)
        response_json = UserIntegration.objects.get(yellowant_integration_token=access_token).delete()
        return HttpResponse("successResponse", status=204)
    else:
        return HttpResponse("Not Authenticated", status=403)


def view_integration(request, account_id=None):

    """For displaying the paricular integration in account-Settings screen."""
    smut = spotify.objects.get(id_id=account_id)

    # Returns if particular integration is integrated with AWS or not
    return HttpResponse(json.dumps({

        "is_valid": smut.AWS_update_login_flag

    }))
