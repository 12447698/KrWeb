from django.db.utils import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.projects.models import Project


class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            code="TEST001",
            html_content="<p>Test content</p>"
        )

    def test_project_creation(self):
        project = self.project
        self.assertTrue(Project.objects.filter(name="Test Project").exists())
        self.assertEqual(project.code, "TEST001")
        self.assertEqual(project.html_content, "<p>Test content</p>")

    def test_project_string_representation(self):
        project = self.project
        self.assertEqual(str(project), "Test Project")

    def test_unique_code(self):
        project = Project.objects.create(
            name="Another Project",
            code="TEST002",
            html_content="<p>Another test content</p>"
        )
        self.assertEqual(project.code, "TEST002")

        with self.assertRaises(IntegrityError):
            Project.objects.create(
                name="Duplicate Code Project",
                code="TEST001",  # Повторение кода
                html_content="<p>Test content</p>"
            )

    def test_project_code_max_length(self):
        long_code = "T" * 51
        project = Project(
            name="Project with long code",
            code=long_code,
            html_content="<p>Content</p>"
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_html_content_field(self):
        project = Project.objects.create(
            name="Project with HTML content",
            code="TEST003",
            html_content="<h1>HTML Heading</h1><p>Some content</p>"
        )
        self.assertEqual(project.html_content, "<h1>HTML Heading</h1><p>Some content</p>")

