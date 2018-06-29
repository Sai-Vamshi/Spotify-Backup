"""The views for Oauth of yellowant and the AWS credentials"""
import json
import uuid
import urllib.parse
import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from yellowant import YellowAnt
from django.views.decorators.csrf import csrf_exempt
from ..yellowant_command_center.command_center import CommandCenter
from .models import YellowAntRedirectState, UserIntegration, spotify , spotifyRedirectState


def request_yellowant_oauth_code(request):
    """Initiate the creation of a new user integration on YA.
    YA uses oauth2 as its authorization framework. This method requests for an oauth2 code from YA
    to start creating a new user integration for this application on YA.
    """
    # get the user requesting to create a new YA integrationrint
    user = User.objects.get(id=request.user.id)

    # generate a unique ID to identify the user when YA returns an oauth2 code
    state = str(uuid.uuid4())

    # save the relation between user and state
    #  so that we can identify the user when YA returns the oauth2 code
    YellowAntRedirectState.objects.create(user=user.id, state=state)

    # Redirect the application user to the YA authentication page.
    # Note that we are passing state, this app's client id,
    # oauth response type as code, and the url to return the oauth2 code at.
    return HttpResponseRedirect("{}?state={}&client_id={}&response_type=code&redirect_url={}"
                                .format(settings.YA_OAUTH_URL, state, settings.YA_CLIENT_ID,
                                        settings.YA_REDIRECT_URL))


def yellowant_oauth_redirect(request):
    """Receive the oauth2 code from YA to generate a new user integration
    This method calls utilizes the YA Python SDK to create a new user integration on YA.
    This method only provides the code for creating a new user integration on YA.
    Beyond that, you might need to authenticate the user on the actual application
    (whose APIs this application will be calling) and store a relation
    between these user auth details and the YA user integration.
    """
    # oauth2 code from YA, passed as GET params in the url
    code = request.GET.get("code")

    # the unique string to identify the user for which we will create an integration
    state = request.GET.get("state")

    # fetch user with the help of state
    yellowant_redirect_state = YellowAntRedirectState.objects.get(state=state)
    user = yellowant_redirect_state.user

    # initialize the YA SDK client with your application credentials
    ya_client = YellowAnt(app_key=settings.YA_CLIENT_ID, app_secret=settings.YA_CLIENT_SECRET,
                          access_token=None, redirect_uri=settings.YA_REDIRECT_URL)

    # get the access token for a user integration from YA against the code
    access_token_dict = ya_client.get_access_token(code)
    # print(access_token_dict)
    # print(type(access_token_dict))
    access_token = access_token_dict["access_token"]

    # reinitialize the YA SDK client with the user integration access token
    ya_client = YellowAnt(access_token=access_token)

    # get YA user details
    ya_user = ya_client.get_user_profile()

    # create a new user integration for your application
    user_integration = ya_client.create_user_integration()

    # save the YA user integration details in your database
    ut = UserIntegration.objects.create(user=user, yellowant_user_id=ya_user["id"],
                                        yellowant_team_subdomain=ya_user["team"]["domain_name"],
                                        yellowant_integration_id=user_integration["user_application"],
                                        yellowant_integration_invoke_name=user_integration["user_invoke_name"],
                                        yellowant_integration_token=access_token)

    spotify.objects.create(id=ut, access_token="", refresh_token="")
    # A new YA user integration has been created and the details have been successfully
    # saved in your application's database. However, we have only created an integration on YA.
    # As a developer, you need to begin an authentication process for the actual application,
    # whose API this application is connecting to. Once, the authentication process
    # for the actual application is completed with the user, you need to create a db
    # entry which relates the YA user integration, we just created, with the actual application
    # authentication details of the user. This application will then be able to identify
    #  the actual application accounts corresponding to each YA user integration.

    # return HttpResponseRedirect("to the actual application authentication URL")

    # return HttpResponseRedirect(reverse("accounts/"), kwargs={"id":ut})
    state = str(uuid.uuid4())

    spotifyRedirectState.objects.create(id=ut, state = state)
    url = "https://accounts.spotify.com/authorize"  # getDiscoveryDocument.auth_endpoint
    params = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        'response_type': 'code',
        'redirect_uri': settings.SPOTIFY_REDIRECT_URL,
        'state': state,
    }
    url += '?' + urllib.parse.urlencode(params)
    print(url)
    return HttpResponseRedirect(url)


@csrf_exempt
def yellowant_api(request):
    """Receive user commands from YA"""
    # print("reached")
    data = json.loads(request.POST.get("data"))
    # print(data)
    if data["verification_token"] == settings.YA_VERIFICATION_TOKEN:
        command = CommandCenter(data["user"], data['application'], data['function_name'],
                                data['args'], data['application_invoke_name'])

        account_id = UserIntegration.objects.get(yellowant_integration_invoke_name=
                                                      data['application_invoke_name'])
        aby = spotify.objects.get(id=account_id)

        url = "https://accounts.spotify.com/api/token"  # getDiscoveryDocument.auth_endpoint
        params = {
            'grant_type': 'refresh_token',
            'refresh_token':aby.refresh_token ,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URL,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
        payload = urllib.parse.urlencode(params)
        url = "https://accounts.spotify.com/api/token"

        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            # 'postman-token': "e40b9e80-a8f0-7461-f66e-61213d180733"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        #print(response.text)
        response = response.json()
        print(response)
        access_token = response['access_token']
        enter_credentials = spotify.objects.get(id_id=aby.id)
        enter_credentials.access_token = access_token
        enter_credentials.save()

        reply = command.parse()
        # print (reply)
        # Return to command centre for processing the functin call
        return HttpResponse(reply)

    else:
        # If an error occurs to processthen show 403 response
        return HttpResponse(status=403)

def spotify_redirect(request):
    code = request.GET.get("code", True)
    state = request.GET.get("state")
    # print(code)
    print("\n")
    print(state)
    print("\n")
    # print("In spotifyRedirecturl")
    url = "https://accounts.spotify.com/api/token"  # getDiscoveryDocument.auth_endpoint
    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URL,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    payload = urllib.parse.urlencode(params)
    url = "https://accounts.spotify.com/api/token"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        # 'postman-token': "e40b9e80-a8f0-7461-f66e-61213d180733"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    response = response.json()
    access_token=response['access_token']
    refresh_token= response['refresh_token']
    aby = spotifyRedirectState.objects.get(state=state)
    print(aby.id)
    enter_credentials = spotify.objects.get(id_id=aby.id_id)
    enter_credentials.access_token = access_token
    enter_credentials.refresh_token = refresh_token
    enter_credentials.save()

    return HttpResponseRedirect("/")

# def get_spotify_access(request):
#     code = request.GET.get("access_token", False)
#     print(code)
#     data = json.loads(request.POST.get("data"))
#     print(data)
#     return HttpResponse("ok",status=200)

#
# def api_key(request):
#     """ This function is used for taking the AWS Credentials from user and store it in the database"""
#     data = json.loads(request.body)
#
#     # The data is received from screens-account-Settings page and is redirected
#     # here which is now assigned as follows:
#     api_token = data['AWS_APIAccessKey']
#     api_secret = data['AWS_APISecretAccess']
#
#     # This try catch is used to verify the Credentials,
#     # if they are right then we save it in the database
#     # else we show the message Invalid Credentials.
#     try:
#         sss = boto3.client(service_name='s3', region_name="us-east-2", api_version=None,
#                            use_ssl=True, verify=None, endpoint_url=None,
#                            aws_access_key_id=api_token, aws_secret_access_key=api_secret,
#                            aws_session_token=None, config=None)
#         response = sss.list_buckets()
#         print(response)
#         # for instance in instances:
#         #     a = instance.id
#     except:
#         return HttpResponse("Invalid credentials. Please try again")
#
#     # For storing the data in our database and updating that it is stored.
#     aby = awss3.objects.get(id=int(data["integration_id"]))
#     aby.AWS_APIAccessKey = data["AWS_APIAccessKey"]
#     aby.AWS_APISecretAccess = data["AWS_APISecretAccess"]
#     aby.AWS_update_login_flag = True
#     aby.save()
#
#     return HttpResponse("Success", status=200)
