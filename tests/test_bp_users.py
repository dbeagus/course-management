import unittest
import os
from flask import Flask
from app import db, create_app
from app.models.user import User
from app.models.profile import Profile
from app.models.role import Role
from app.utils.initializers import initialize_roles

class TestUserBP(unittest.TestCase):
    
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
    
    def test_create_user(self):
        data = {
            "email" : "test@test.com",
            "password" : "test",
            "role" : "ADMINISTRADOR"
        }
        
        response = self.client.post("/users", json = data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["message"], "User registered successfully")
        
        created_user_id = response.json["id"]
        created_user = User.query.filter_by(id = created_user_id).first()
        role = Role.query.filter_by(name = "ADMINISTRADOR").first()
        created_profile = Profile.query.filter_by(user_id = created_user_id).first()
        
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, "test@test.com")
        self.assertTrue(created_user.check_password("test"))
        
        self.assertIsNotNone(created_profile)
        self.assertEqual(created_profile.role_id, role.id)
        self.assertEqual(created_profile.user_id, created_user_id)
        
if __name__ == "__main__":
    unittest.main()