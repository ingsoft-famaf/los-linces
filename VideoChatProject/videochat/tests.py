from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Video, Profile
from .models import Seen, Chatroom

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from friendship.models import Friend, Follow, FriendshipRequest
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.core.files import File
from django.contrib.staticfiles import finders

class BaseTestCase(TestCase):

    def setUp(self):
        self.user_pw = 'test'
        self.user_turco = self.create_user('turco', 'turco@turco.com', self.user_pw)
        self.user_juampi = self.create_user('juampi', 'juampi@juampi.com', self.user_pw)
        self.user_male = self.create_user('male', 'male@male.com', self.user_pw)
        self.user_mono = self.create_user('mono', 'mono@mono.mono.com', self.user_pw)

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def login(self, user, password):
        return login(self, user, password)

    def create_user(self, username, password, email_address):
        user = User.objects.create_user(username, password, email_address)
        return user

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)


class FriendshipModelTest(BaseTestCase):

    def test_add_friend(self):
        # Turco wants to be friends with Juampi
        friend_request = Friend.objects.add_friend(self.user_turco, self.user_juampi)
        # Let's be sure they don't have any friends
        self.assertEqual(Friend.objects.friends(self.user_turco), [])
        self.assertEqual(Friend.objects.friends(self.user_juampi), [])
        '''
        Ensure they have the sent and received requests:
            Turco sent Juampi a request, so he should have 1 sent request and no received requests.
            Juampi should have Turco's sent request and no sent requests
        '''
        self.assertEqual(len(Friend.objects.requests(self.user_turco)), 0)
        self.assertEqual(len(Friend.objects.requests(self.user_juampi)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(self.user_turco)), 1)
        self.assertEqual(len(Friend.objects.sent_requests(self.user_juampi)), 0)
        self.assertEqual(len(Friend.objects.unread_requests(self.user_juampi)), 1)
        self.assertEqual(Friend.objects.unread_request_count(self.user_juampi), 1)
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_juampi)), 0)
        self.assertEqual(len(Friend.objects.unrejected_requests(self.user_juampi)), 1)
        self.assertEqual(Friend.objects.unrejected_request_count(self.user_juampi), 1)
        # Let's be sure they aren't friends at this point
        self.assertFalse(Friend.objects.are_friends(self.user_turco, self.user_juampi))
        # Accept the request
        friend_request.accept()
        # Ensure neither have pending requests
        self.assertEqual(FriendshipRequest.objects.filter(from_user=self.user_turco).count(), 0)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=self.user_juampi).count(), 0)
        # Ensure both are in each other's friend lists now
        self.assertEqual(Friend.objects.friends(self.user_turco), [self.user_juampi])
        self.assertEqual(Friend.objects.friends(self.user_juampi), [self.user_turco])
        self.assertTrue(Friend.objects.are_friends(self.user_turco, self.user_juampi))

    def test_removeFriend(self):

        # Turco wants to be friends with Juampi
        friend_request = Friend.objects.add_friend(self.user_turco, self.user_juampi)
        # Accept the request
        friend_request.accept()
        # Make sure we can remove friendship
        self.assertTrue(Friend.objects.remove_friend(self.user_turco, self.user_juampi))
        # Ensure there's no friendship between them
        self.assertFalse(Friend.objects.are_friends(self.user_turco, self.user_juampi))
        # Ensure friends can't be removed when there's no friendship
        self.assertFalse(Friend.objects.remove_friend(self.user_turco, self.user_juampi))

    def test_cancel_friend_request(self):

        # Male wants to be friends with Mono, but cancels it
        friend_request = Friend.objects.add_friend(self.user_male, self.user_mono)
        # Ensure they're not friends
        self.assertEqual(Friend.objects.friends(self.user_male), [])
        self.assertEqual(Friend.objects.friends(self.user_mono), [])
        # Cancel the request
        friend_request.cancel()
        # Ensure they are not friends
        self.assertEqual(Friend.objects.requests(self.user_male), [])
        self.assertEqual(Friend.objects.requests(self.user_mono), [])

    def test_rejectfriend_request(self):
        
        # Male wants to be friends with Mono, but Mono rejects it
        friend_request = Friend.objects.add_friend(self.user_male, self.user_mono)
        # Assert neither of them has friends
        self.assertEqual(Friend.objects.friends(self.user_male), [])
        self.assertEqual(Friend.objects.friends(self.user_mono), [])
        # Reject the request
        friend_request.reject()
        # Ensure they are not friends
        self.assertFalse(Friend.objects.are_friends(self.user_male, self.user_mono))
        # Mono now has one rejected request
        self.assertEqual(len(Friend.objects.rejected_requests(self.user_mono)), 1)

    def test_read_friend_request(self):

        # Male wants to be friends with Mono, and Mono reads it
        friend_request = Friend.objects.add_friend(self.user_male, self.user_mono)
        friend_request.mark_viewed()
        # Ensure they are not friends
        self.assertFalse(Friend.objects.are_friends(self.user_male, self.user_mono))
        # Mono now has one read request
        self.assertEqual(len(Friend.objects.read_requests(self.user_mono)), 1)

    def test_yourself_friend_request(self):
        # Ensure we can't be friends with ourselves
        with self.assertRaises(ValidationError):
            Friend.objects.add_friend(self.user_turco, self.user_turco)
        # Ensure we can't do it manually either
        with self.assertRaises(ValidationError):
            Friend.objects.create(to_user=self.user_turco, from_user=self.user_turco)

class VideoTest(BaseTestCase):
    
    def test_login(self):
        client = Client()
        # Log into a user's account
        response = client.post('/login/', {'username':'turco', 'password':self.user_pw})
        # Check if redirection happens
        self.assertResponse302(response)

    def test_video_upload(self):
        client = Client()
        # Log into a user's account
        response = client.post('/login/', {'username':'turco', 'password':self.user_pw})
        # Check if redirection happens
        self.assertResponse302(response)
        # Load testvideo from /static
        video = finders.find('static/testvideo.mp4')
        response = client.post('/upload/', {'title':'hola2', 'description':'caca', 'video_file':video})
        # Check if video was uploaded correctly
        self.assertResponse200(response)

    def test_play_unexisting_video(self):
        client = Client()
        video = Video(title= "Primer video", description= "probando", path="/static/testvideo.mp4")
        video.save()
        videopk = video.pk
        # Log into a user's account
        response = client.post('/login/', {'username':'turco', 'password':self.user_pw})
        # Check if redirection happens
        self.assertResponse302(response)
        videopk += 1
        url = reverse('videochat:v', args=[video.pk])
        response = client.post(url)
        self.assertResponse404(response)

class ChatroomTest(TestCase):
	
	def setUp(self):
		self.user_pw = 'test'
        # Create three users
		self.user_turco = User.objects.create_user('turco', 'turco@turco.com', self.user_pw)
		self.user_mono = User.objects.create_user('mono', 'mono@mono.mono.com', self.user_pw)
		self.user_male = User.objects.create_user('male', 'male@male.com', self.user_pw)
        # Create three clients
		self.client1 = Client()
		self.client2 = Client()
        self.client3 = Client()
        # Login with the three users
		self.client1.login(username='turco', password=self.user_pw)
		self.client2.login(username='mono', password=self.user_pw)
        self.client3.login(username='male', password=self.user_pw)
		# Create a friendship between users turco and mono
        friend_request = Friend.objects.add_friend(self.user_turco, self.user_mono)
		friend_request.accept()
        # Create a sample video
		self.video1 = Video(title= "Primer video", description= "probando", path="/static/testvideo.mp4")
		self.video1.save()
		self.chatroom_pk= 1

	def test_create_chatroom(self):
		# Log into a user's account
		url = reverse('videochat:v', args=[self.video1.pk])
		response = self.client1.post(url)
		# Check if redirection happens
		self.assertEqual(response.status_code, 302)
		url = reverse('videochat:v', args=[self.video1.pk, self.chatroom_pk])
		self.assertRedirects(response, url)

	def test_enter_unexisting_chatroom(self):
        # Create unexisting chatroom's primary key
		unexisting_chatroom_pk = self.chatroom_pk + 1
		url = reverse('videochat:v', args=[self.video1.pk, unexisting_chatroom_pk])
		response = self.client.post(url)
        # Ensure user gets error when connecting to unexisting chatroom
		self.assertEqual(response.status_code, 404)

	def test_enter_friend_chatroom(self):
        # Creates two sessions for two users which are friends
		url1 = reverse('videochat:v', args=[self.video1.pk])
		response1 = self.client1.post(url1)
		url2 = reverse('videochat:v', args=[self.video1.pk, self.chatroom_pk])
		response2 = self.client2.post(url2)
        # Checks if user1 can access correctly to user2's chatroom
		self.assertEqual(response2.status_code, 200)

    def test_enter_not_friend_chatroom(self):
        # Creates two sessions for two users which are not friends
        url1 = reverse('videochat:v', args=[self.video1.pk])
        response1 = self.client1.post(url1)
        url2 = reverse('videochat:v', args=[self.video1.pk, self.chatroom_pk])
        response2 = self.client3.post(url2)
        ''' 
        Checks if the user2 (Who is not friends with user 1) gets an error 
        while trying to get into user1's chatroom
        '''
        self.assertEqual(response2.status_code, 404) #TODO: define the status_code
        
        

    
