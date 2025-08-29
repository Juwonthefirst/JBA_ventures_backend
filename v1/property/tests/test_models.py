from rest_framework.test import APITestCase
from v1.property.models import Property as PropertyModel
from django.core.files import File
from django.core.exceptions import ValidationError


class TestPropertyModel(APITestCase):
	def setUp(self):
		self.property1 = PropertyModel(
			address="4 cheese street",
			state="cheesington",
			lga="cheese square",
			description="cheese hall is overrun with cats",
			type="shop",
		)
		with open("/media/tmp/test.jpg", "rb") as testImage:
			self.property1.main_image.save("test.jpg", File(testImage), save=True)
		self.property1.save()

	"""def test_deleting_row_deletes_file(self):
		self.property1.address = ""
		with self.assertRaises(ValidationError):
			self.property1.full_clean()
			"""
