import pytest
from rest_framework.test import APIClient
from v1.property.models import Property as PropertyModel, PropertyMedia
from v1.property.serializers import ListCreatePropertySerializer, PropertySerializer
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from PIL import Image
from io import BytesIO

User = get_user_model()


def create_test_image(name="test.jpg"):
    imageIO = BytesIO()
    img = Image.new("RGB", (100, 100), color="red")
    img.save(imageIO, "JPEG")
    imageIO.seek(0)

    return SimpleUploadedFile(name, imageIO.getvalue(), content_type="image/jpeg")


class TestListOrCreatePropertyView(TestCase):
    def test_get_method(self):
        client = APIClient()
        property1 = PropertyModel(
            address="4 cheese street",
            state="lagos",
            lga="ikorodu",
            description="cheese hall is overrun with cats",
            benefits=["hello", "goodbye"],
            type="Shop",
            offer="House",
            price=3000,
        )
        with open("media/tmp/test.jpg", "rb") as testImage:
            property1.main_image.save("test.jpg", File(testImage), save=True)

        property1.save()

        property2 = PropertyModel(
            address="4 cheese street",
            state="lagos",
            lga="ikorodu",
            description="cheese hall is overrun with cats",
            benefits=["hello", "goodbye"],
            type="Shop",
            offer="House",
            price=3000,
        )
        with open("media/tmp/test.jpg", "rb") as testImage:
            property2.main_image.save("test.jpg", File(testImage), save=True)

        property2.save()

        response = client.get("/api/v1/property/")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data["results"]), 2)

    def test_post_method(self):
        client = APIClient()
        user = User.objects.create_superuser(username="john", password="pass12345")
        main_image = create_test_image("main_image.jpg")
        extra_image_1 = create_test_image("extra_image_1.jpg")

        payload = {
            "main_image": main_image,
            "extra_media": [extra_image_1],
            "address": "6 cheese street",
            "state": "cheesington",
            "lga": "cheese square",
            "description": "there's a wacko next to my house",
            "type": "Shop",
            "benefits": ["hello", "goodbye"],
            "offer": "House",
            "price": 3000,
        }
        response = client.post(
            "/api/v1/property/",
            payload,
            format="multipart",
        )

        self.assertEqual(response.status_code, 401)
        main_image.seek(0)
        extra_image_1.seek(0)

        client.force_authenticate(user=user)
        response = client.post("/api/v1/property/", payload, format="multipart")
        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            PropertyModel.objects.filter(address="6 cheese street").exists()
        )
        self.assertTrue(PropertyMedia.objects.filter(id=1).exists())


class TestRetrieveOrUpdatePropertyView(TestCase):
    def test_methods(self):
        client = APIClient()
        user = User.objects.create_superuser(username="james", password="pass12345")
        property1 = PropertyModel(
            address="4 cheese street",
            state="lagos",
            lga="ikorodu",
            description="cheese hall is overrun with cats",
            benefits=["hello", "goodbye"],
            type="Shop",
            offer="House",
            price=3000,
        )
        with open("media/tmp/test.jpg", "rb") as testImage:
            property1.main_image.save("test.jpg", File(testImage), save=True)

        property1.save()
        with open("media/tmp/test.jpg", "rb") as testImage:
            property1_extra_media=PropertyMedia.objects.create(
                property=property1, media=create_test_image("extra_image_1")
            )
        property1_extra_media.save()

        response = client.get(f"/api/v1/property/{property1.id}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["address"], "4 cheese street")

        patch_payload = {"address": "17 cheese street"}
        response = client.patch(
            f"/api/v1/property/{property1.id}/",
            patch_payload,
            format="json",
        )
        self.assertEqual(response.status_code, 401)

        client.force_authenticate(user=user)
        response = client.patch(
            f"/api/v1/property/{property1.id}/",
            patch_payload,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        updated_property1 = PropertyModel.objects.filter(id=property1.id).first()
        self.assertEqual(updated_property1.address, patch_payload["address"])
        self.assertEqual(updated_property1.state, property1.state)

        response = client.delete(f"/api/v1/property/{property1.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(PropertyModel.objects.filter(id=property1.id).exists())
