import tempfile
import os
import shutil

from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.materials.models import Material


class MaterialViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )

        self.dummy_file = SimpleUploadedFile(
            "test_file.txt", b"file_content", content_type="text/plain"
        )

        self.material_public = Material.objects.create(
            name="Public Material", is_public=True, file=self.dummy_file
        )
        self.material_private = Material.objects.create(
            name="Private Material", is_public=False, file=self.dummy_file
        )

        self.material_with_file = Material.objects.create(
            name="Material with File", is_public=True, file=self.dummy_file
        )

        self.materials_url = reverse("materials:main")
        self.delete_material_url = lambda pk: reverse("materials:delete", args=[pk])

    def test_materials_view_authenticated_user(self):
        self.client.login(username="user", password="password")
        response = self.client.get(self.materials_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.material_public.name)
        self.assertNotContains(response, self.material_private.name)
        self.assertContains(response, self.material_with_file.name)

    def test_materials_view_staff_user(self):
        self.client.login(username="staff", password="password")
        response = self.client.get(self.materials_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.material_public.name)
        self.assertContains(response, self.material_private.name)
        self.assertContains(response, self.material_with_file.name)

    def test_materials_view_unauthenticated(self):
        response = self.client.get(self.materials_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.material_public.name)
        self.assertNotContains(response, self.material_private.name)

    def test_materials_view_forbidden_for_non_staff(self):
        self.client.login(username="user", password="password")
        response = self.client.get(self.materials_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.material_public.name)
        self.assertNotContains(response, self.material_private.name)


class DeleteMaterialViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )

        self.dummy_file = SimpleUploadedFile(
            "test_file.txt", b"file_content", content_type="text/plain"
        )

        self.material = Material.objects.create(
            name="Material to Delete", is_public=True, file=self.dummy_file
        )

        self.delete_material_url = reverse("materials:delete", args=[self.material.pk])

    def test_delete_material_view_staff_user(self):
        self.client.login(username="staff", password="password")
        response = self.client.post(self.delete_material_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("materials:main"))
        self.assertFalse(Material.objects.filter(pk=self.material.pk).exists())

    def test_delete_material_view_non_staff_user(self):
        self.client.login(username="user", password="password")
        response = self.client.post(self.delete_material_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("materials:main"))
        self.assertTrue(Material.objects.filter(pk=self.material.pk).exists())

    def test_delete_material_view_unauthenticated_user(self):
        response = self.client.post(self.delete_material_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Material.objects.filter(pk=self.material.pk).exists())


class MaterialModelTestCase(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_material_creation_with_file(self):
        dummy_file = SimpleUploadedFile(
            "test_file.txt",
            b"file_content",
            content_type="text/plain",
        )
        material = Material.objects.create(
            name="Material with File", file=dummy_file, is_public=True
        )

        self.assertTrue(Material.objects.filter(name="Material with File").exists())
        self.assertIsNotNone(material.file)
        self.assertEqual(material.file.name, "materials/test_file.txt")
