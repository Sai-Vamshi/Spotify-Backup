"""This file contains the logic to understand a user message request
 from YA and return a response in the format of
 a YA message object accordingly

"""
import spotipy
import sys
import pprint
from yellowant.messageformat import MessageClass, MessageAttachmentsClass, AttachmentFieldsClass
from ..yellowant_api.models import spotify, UserIntegration



class CommandCenter(object):
    """Handles user commands
    Args:
        yellowant_integration_id (int): The integration id of a YA user
        self.commands (str): Invoke name of the command the user is calling
        args (dict): Any arguments required for the command to run
    """

    def __init__(self, yellowant_user_id, yellowant_integration_id, function_name,
                 args, application_invoke_name):
        self.yellowant_user_id = yellowant_user_id
        self.application_invoke_name = application_invoke_name
        self.yellowant_integration_id = yellowant_integration_id
        self.account_id = UserIntegration.objects.get(yellowant_integration_invoke_name=
                                                      self.application_invoke_name)
        self.access_token = spotify.objects.get(id=self.account_id).access_token
        # self.cret_token = awss3.objects.get(id=self.account_id).AWS_APISecretAccess
        self.function_name = function_name
        self.args = args

    def parse(self):
        """The connection between yellowant commands and functions in django"""
        self.commands = {
            'search': self.search,
            'saved-tracks': self.saved_tracks,
            'new-releases': self.new_releases,
        }
        return self.commands[self.function_name](self.args)

    # def show_tracks(results):
    #     for i, item in enumerate(results['items']):
    #         track = item['track']
    #         print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name'])

    def search(self,args):
        input =  args['input']
        sp = spotipy.Spotify(auth=self.access_token)
        # artist_name = 'Ed Sheeran'.join(sys.argv[1:])
        results = sp.search(q=input, limit=20)
        message = MessageClass()
        for i, t in enumerate(results['tracks']['items']):
            print(' ', i, t['name'])
            attachment = MessageAttachmentsClass()
            attachment.title = t['name']
            message.attach(attachment)
        message.message_text = "The Search Results are"
        return message.to_json()

    def saved_tracks(self,args):
        input =  args['input']
        sp = spotipy.Spotify(auth=self.access_token)
        # artist_name = 'Ed Sheeran'.join(sys.argv[1:])
        results = sp.search(q=input, limit=20)
        message = MessageClass()

        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])
            attachment = MessageAttachmentsClass()
            field = AttachmentFieldsClass()
            field.title = track['name']
            field.value = track['artists'][0]['name']
            message.attach(attachment)
        message.message_text = "The Saved Tracks are:"
        return message.to_json()

    def new_releases(self,args):
        # input =  args['input']
        sp = spotipy.Spotify(auth=self.access_token)
        # artist_name = 'Ed Sheeran'.join(sys.argv[1:])
        results = sp.search(q=input, limit=20)
        message = MessageClass()
        response = sp.new_releases()


        albums = response['albums']
        for i, item in enumerate(albums['items']):
            print(albums['offset'] + i, item['name'])
            attachment = MessageAttachmentsClass()
            attachment.title = item['name']
        # if albums['next']:
        #     response = sp.next(albums)
            message.attach(attachment)
        message.message_text = "The New Releases are:"
        return message.to_json()

    # def user_playlists_contents(self,args):
    #     username =  args['Username']
    #     sp = spotipy.Spotify(auth=self.access_token)
    #     # artist_name = 'Ed Sheeran'.join(sys.argv[1:])
    #     results = sp.search(q=input, limit=20)
    #     message = MessageClass()
    #     playlists = sp.user_playlists(username)
    #     for playlist in playlists['items']:
    #         if playlist['owner']['id'] == username:
    #             print()
    #             print(playlist['name'])
    #             print('  total tracks', playlist['tracks']['total'])
    #             results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
    #             tracks = results['tracks']
    #             show_tracks(tracks)
    #             while tracks['next']:
    #                 tracks = sp.next(tracks)
    #                 show_tracks(tracks)
    #         attachment = MessageAttachmentsClass()
    #         attachment.title = t['name']
    #         message.attach(attachment)
    #     message.message_text = "The Search Results are"
    #     return message.to_json()

