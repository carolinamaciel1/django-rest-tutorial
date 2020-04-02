from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_songs(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def SetUp(self):
        self.create_songs("Don't start now", "Dua Lipa"),
        self.create_songs("Say something", "Justin Timberlake"),
        self.create_songs("New York", "Alicia Keys")


class GetAllSongsTest(BaseViewTest):
    def test_get_all_songs(self):
        response = self.client.get(reverse("songs-all", kwargs={"version": "v1"}))
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEquals(response.data, serialized.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
