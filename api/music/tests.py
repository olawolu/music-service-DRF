from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer


# Create your tests here.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def setUp(self):
        # add test data
        self.create_song("alright", "kendrick lamar")
        self.create_song("middle child", "j cole")
        self.create_song("all the stars", "kendrick lamar, sza")
        self.create_song("st tropez", "j cole")
        self.create_song("st tropez", "post malone")
        self.create_song("energy", "drake")


class GetAllSongsTest(BaseViewTest):
    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method exist when we make a GET request
        to the songs/ endpoint
        """
        #  hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
