from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser


class ModelTests(TestCase):
    
    #dont know if the authentication related things are important but still keeping them
    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'medo@testemail.com'
        password = 'thispasswordisbad'
        username ='us'
        club_name ="hjh"
        student_id = "j"
        user_type = 1

        user = get_user_model().objects.create_user(
            username = username,
            email=email,
            password=password,
            club_name = club_name,
            student_id = student_id,
            user_type = user_type,

        )
        self.assertEqual(user.email, email) 
    """
    def test_new_user_email_normalized(self):
        
        username = 'bdb'
        email = 'medo@TESTUSER.COM'
        password='test123',
        club_name = "jshdj",
        student_id = "df",
        user_type = 2,
        user = get_user_model().objects.create_user(
            username= username,
            email=email,
            password= password,
            club_name= club_name,
            student_id= student_id, 
            user_type= user_type,
             )

        self.assertNotEqual(user.email, email.lower())
    """
    def test_new_user_invalid_email(self):
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    """
    def test_create_new_superuser(self):
        
        user = get_user_model().objects.create_superuser(
            'testsuperuser@adminemail.com',
            'testadmin123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    """
    def test_model_str(self):
        abc = get_user_model()
        new_user= abc.objects.create(first_name = "john", last_name = "Doe", student_id = "1234", club_name = "MDU", user_type = 1)
        self.assertEqual(str(new_user), "john Doe 1234 MDU 1")
    
    def test_create_user_with_invalid_id(self):
        studentId = '5234'

        email = 'medo@testemail.com'
        password = 'thispasswordisbad'
        username ='us'
        club_name ="hjh"
        user_type = 1
        user = get_user_model().objects.create_user(
            username = username,
            email=email,
            password=password,
            club_name = club_name,
            student_id = "9234",
            user_type = user_type,
        ) 
        self.assertNotEqual(user.student_id, studentId, msg="Unauthorized request")
    
    def test_create_user_with_invalid_username(self):
        uName = 'asdsfdsf'

        email = 'medo@testemail.com'
        password = 'thispasswordisbad'
        club_name ="hjh"
        user_type = 1
        user = get_user_model().objects.create_user(
           username = "shgdhsg",
           email=email,
           password=password,
           club_name = club_name,
           student_id = "9234",
           user_type = user_type,

        )  
        self.assertNotEqual(user.username, uName, msg="Unauthorized request")

    def test_create_user_with_missing_information(self):
        firstName = None
        username = 'us'
        email = 'medo@testemail.com'
        password = 'thispasswordisbad'
        club_name ="hjh"
        user_type = 1

        user = get_user_model().objects.create_user(
            username =username,
            email=email,
            password=password,
            club_name = club_name,
            student_id = "9234",
            user_type = user_type,
            first_name = "john"
           
        )  
        self.assertNotEqual(user.first_name, firstName, msg="Incomplete information")
        
    def test_creation_of_different_users(self):
        treasurer = get_user_model().objects.create_user(
            username ="aabb",
            email="some@mail.com",
            password="somepassword",
            club_name = "mrt",
            student_id = "9234",
            user_type = 1,
            first_name = "jane"
           
        ) 
        president = get_user_model().objects.create_user(
            username ="ccdd",
            email="dgf",
            password="dhd",
            club_name = "mdu",
            student_id = "9234",
            user_type = 2,
            first_name = "john"
           
        )
        Different_users ={
            "Treasurer" : 1,
            "President" : 2
        }
        
        self.assertEqual(treasurer.user_type, Different_users.get('Treasurer'))
        self.assertEqual(president.user_type, Different_users.get('President'))
    
    def test_for_duplicates(self):
        users_created ={
            "Ann" : "123",
            "Lane" : "234",
            "Dan" : "345"
        }
        firstName = 'Ann'
        username = 'us'
        email = 'medo@testemail.com'
        password = 'thispassword'
        club_name ="hjh"
        user_type = 1

        user = get_user_model().objects.create_user(
            username =username,
            email=email,
            password=password,
            club_name = club_name,
            student_id = "123",
            user_type = user_type,
            first_name = firstName

        )

        self.assertEqual(user.student_id, users_created.get('Ann'), msg="Already registered")

    def test_for_non_smu_members(self):
        ssmu_members = {
            "Harris" : "324",
            "Warren" : "567", 
            "Cortez" : "121",
            "Nooyi"  : "234"
        }
          
        user = get_user_model().objects.create_user(
            username = 'jhj',
            email = 'e@mail.com',
            password = 'goodpassword',
            club_name = 'mrt',
            student_id = "567",
            user_type = 1,
            first_name = 'Warren'
        )
        user1 = get_user_model().objects.create_user(
           username = 'jij',
           email = 't@mail.com',
           password = 'badpassword',
           club_name = 'mrt',
           student_id = "345",
           user_type = 1,
           first_name = 'Trump'
        )

        status = user.student_id in ssmu_members.values()
        self.assertTrue(status)
        self.assertFalse(user1.student_id in ssmu_members.values(), msg= "Not a SSMU member")