import unittest
import os
from app import db, create_app
from app.models.course import Course
from app.utils.initializers import initialize_roles

class TestCourseBP(unittest.TestCase):
    
    def setUp(self):
        os.environ["FLASK_CONTEXT"] = "testing"
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        initialize_roles()
        
    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_course(self):
        data = {
            "name": "test"
        }
        
        response = self.client.post("/courses", json = data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["message"], "Course registered successfully")
        
        created_course_id = response.json["id"]
        created_course = Course.query.filter_by(id = created_course_id).first()
        
        self.assertIsNotNone(created_course)
        self.assertEqual(created_course.name, "test")
        self.assertEqual(created_course.id, created_course_id)
        
    def test_get_all_courses(self):
        course1 = Course(name = "course1")
        course2 = Course(name = "course2")
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()
        
        response = self.client.get("/courses")
        
        self.assertEqual(response.status_code, 200)
        courses = response.json["courses"]
        
        self.assertIsNotNone(courses)
        
        courses_names = [course["name"] for course in courses]
        self.assertIn("course1", courses_names)
        self.assertIn("course2", courses_names)
    
    def test_update_course(self):
        course = Course(name = "test")
        db.session.add(course)
        db.session.commit()
        
        data = {
            "name": "updated"
        }
        course_id = course.id
        response = self.client.put(f"/courses/{course_id}", json = data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Course updated successfully"), 200
        
        course_updated = Course.query.filter_by(id = course_id).first()
        self.assertIsNotNone(course_updated)
        self.assertEqual(course_updated.name, "updated")