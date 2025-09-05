import pytest
from rest_framework.test import APIClient
from v1.property.models import Property as PropertyModel
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestListOrCreatePropertyView(TestCase):
    def test_get_method(self):
        client = APIClient()
        property1 = PropertyModel(
            address="4 cheese street",
            state="cheesington",
            lga="cheese square",
            description="cheese hall is overrun with cats",
            type="shop",
        )
        with open("media/tmp/test.jpg", "rb") as testImage:
            property1.main_image.save("test.jpg", File(testImage), save=True)

        property1.save()

        property2 = PropertyModel(
            address="5 cheese street",
            state="cheesington",
            lga="cheese square",
            description="there's a wacko next to my house",
            type="shop",
        )
        with open("media/tmp/test.jpg", "rb") as testImage:
            property2.main_image.save("test.jpg", File(testImage), save=True)

        property2.save()

        response = client.get("api/v1/property/")
        self.assertEqual(response.code, 200)
        data = response.json()
        self.assertEqual(len(data.results), 2)

    def test_post_method(self):
        client = APIClient()
        user = User.objects.create_user(username="james", password="pass12345")
        image = SimpleUploadedFile(
            "image.jpg", b"who are we why are we here", content_type="image/jpeg"
        )
        payload = {
            "main_image": image,
            "address": "6 cheese street",
            "state": "cheesington",
            "lga": "cheese square",
            "description": "there's a wacko next to my house",
            "type": "shop",
        }
        response = client.post("api/v1/property/", payload, format="multipart")
        self.assertEqual(response.code, 401)

        client.force_authenticate(user=user)
        response = client.post("api/v1/property/", payload, format="multipart")
        self.assertEqual(response.code, 201)
        self.assertTrue(
            PropertyModel.objects.filter(address="6 cheese street").exists()
        )


class TestRetrieveOrUpdatePropertyView(TestCase):
    def test_methods(self):
        client = APIClient()
        user = User.objects.create_user(username="james", password="pass12345")
        property1 = PropertyModel(
            address="7 cheese street",
            state="cheesington",
            lga="cheese square",
            description="cheese hall is overrun with cats",
            type="shop",
        )
        with open("media/tmp/test.jpg", "rb") as testImage:
            property1.main_image.save("test.jpg", File(testImage), save=True)

        property1.save()

        response = client.get("api/v1/property/1")
        self.assertEqual(response.code, 200)
        data = response.json()
        self.assertEqual(data.address, "7 cheese street")

        payload = {"address": "17 cheese street"}
        response = client.patch("api/v1/property/1/", payload, format="json")
        self.assertEqual(response.code, 401)

        client.force_authenticate(user=user)
        response = client.patch("api/v1/property/1/", payload, format="json")
        self.assertEqual(response.code, 200)
        data = response.json()
        self.assertTrue(
            PropertyModel.objects.filter(address="17 cheese street").exists()
        )

        response = client.delete("api/v1/property/1")
        self.assertEqual(response.code, 204)
        self.assertFalse(
            PropertyModel.objects.filter(address="17 cheese street").exists()
        )
