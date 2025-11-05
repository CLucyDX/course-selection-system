import unittest  
from user import user
import json

class TestUser(unittest.TestCase):  
    def setUp(self):  
        self.user = user
        user.config['TESTING'] = True
        self.client = user.test_client()
  
    # Test case: empty email_address
    def test_register_empty_email(self):
        response = self.client.post("/register", data={})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1001)
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Register_email_address")

    def test_login_empty_email(self):
        response = self.client.post("/login", data={})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1003)
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Login_email_address")
    
    # Test case: empty email_address but non-empty password
    def test_register_empty_email_non_empty_password(self):
        response = self.client.post("/register", data={"password":"123456"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1001)
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Register_email_address")

    def test_login_empty_email_non_empty_password(self):
        response = self.client.post("/login", data={"password":"123456"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1003)
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Login_email_address")
    
    # email_address不合法的情况
    def test_register_invalid_name(self):  
        counter = 0
        illegal_char = '()[]{}' 
        email_address = "admin@uic.com"
        
        # 非法字符检验
        while counter < 5:  
            # 处理user 
            email_address += illegal_char[counter]  
            response = self.client.post("/register", data={"email_address":email_address,"password":"123456"})

            # 重置：
            code = 1000
            msg = ""

            # 测试
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn("code", resp_dict)
            code = resp_dict.get("code")
            self.assertEqual(code, 1001) 
            msg = resp_dict.get('message')
            self.assertEqual(msg, "WRONG_Register_email_address")

            # counter自增  
            counter += 1  
        
        # 非法格式检验1
        email_address = "adminuic.com"
        response = self.client.post("/register", data={"email_address":email_address,"password":"123456"})
         # 重置：
        code = 1000
        msg = ""
        # 测试
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1001) 
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Register_email_address")
        # 非法格式检验2
        email_address = "admin@uiccom"
        response = self.client.post("/register", data={"email_address":email_address,"password":"123456"})
         # 重置：
        code = 1000
        msg = ""
        # 测试
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1001) 
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Register_email_address")
    
    def test_login_invalid_name(self):  
        counter = 0
        illegal_char = '()[]{}' 
        email_address = "admin@uic.com"
        
        # 非法字符检验
        while counter < 5:  
            # 处理user 
            email_address += illegal_char[counter]  
            response = self.client.post("/login", data={"email_address":email_address,"password":"123456"})

            # 重置：
            code = 1000
            msg = ""

            # 测试
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn("code", resp_dict)
            code = resp_dict.get("code")
            self.assertEqual(code, 1003) 
            msg = resp_dict.get('message')
            self.assertEqual(msg, "WRONG_Login_email_address")

            # counter自增  
            counter += 1 
        
        # 非法格式检验1
        email_address = "adminuic.com"
        response = self.client.post("/register", data={"email_address":email_address,"password":"123456"})
         # 重置：
        code = 1000
        msg = ""
        # 测试
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1001) 
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Register_email_address")
        # 非法格式检验2
        email_address = "admin@uiccom"
        response = self.client.post("/register", data={"email_address":email_address,"password":"123456"})
         # 重置：
        code = 1000
        msg = ""
        # 测试
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, 1001) 
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Register_email_address")
        
    # email_address正常但password为空
    def test_register_valid_name_and_empty_password(self):  
        response = self.client.post("/register", data={"email_address": "admin@uic.com"})
        # response data
        resp_json = response.data
        # convert to json
        resp_dict = json.loads(resp_json)
        # use assert to verify
        self.assertIn("code", resp_dict)
        # compare the code value
        code = resp_dict.get("code")
        self.assertEqual(code, 1002)
        # return message
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Register_Password")
    
    def test_login_valid_name_and_empty_password(self):  
        response = self.client.post("/login", data={"email_address": "admin@uic.com"})
        # response data
        resp_json = response.data
        # convert to json
        resp_dict = json.loads(resp_json)
        # use assert to verify
        self.assertIn("code", resp_dict)
        # compare the code value
        code = resp_dict.get("code")
        self.assertEqual(code, 1004)
        # return message
        msg = resp_dict.get('message')
        self.assertEqual(msg, "WRONG_Login_Password")
    
    # email_address正常但password不合法的情况
    def test_register_valid_name_and_invalid_password(self):  
        counter = 0
        illegal_char = '()[]""{}' 
        password = "123456"
        
        while counter < 5:  
            # 处理password
            password += illegal_char[counter]  
            response = self.client.post("/register", data={"email_address":"admin@uic.com","password":password})

            # 重置：
            code = 1000
            msg = ""
            
            # 测试
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn("code", resp_dict)
            code = resp_dict.get("code")
            self.assertEqual(code, 1002) 
            msg = resp_dict.get('message')
            self.assertEqual(msg, "WRONG_Register_Password")

            # counter自增  
            counter += 1 
    
    def test_login_valid_name_and_invalid_password(self):  
        counter = 0
        illegal_char = '()[]""{}' 
        password = "123456"
        
        while counter < 5:  
            # 处理password
            password += illegal_char[counter]  
            response = self.client.post("/login", data={"email_address":"admin@uic.com","password":password})

            # 重置：
            code = 1000
            msg = ""
            
            # 测试
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn("code", resp_dict)
            code = resp_dict.get("code")
            self.assertEqual(code, 1004) 
            msg = resp_dict.get('message')
            self.assertEqual(msg, "WRONG_Login_Password")

            # counter自增  
            counter += 1 
        
    # email_address和password均正常的情况
    def test_register_valid_name_and_valid_password(self):
        response = self.client.post("/register", data={"email_address": "admin@uic.com", "password":"Ybx61120"})
        # response data
        resp_json = response.data
        # convert to json
        resp_dict = json.loads(resp_json)
        # use assert to verify
        self.assertIn("code", resp_dict)
        # compare the code value 1002 (since your application logic expects 1002 for successful registration)
        code = resp_dict.get("code")
        self.assertEqual(code, 0)
        # return message
        msg = resp_dict.get('message')
        self.assertEqual(msg, "OK")

    def test_login_valid_name_and_valid_password(self):
        response = self.client.post("/login", data={"email_address": "admin@uic.com", "password":"123456"})
        # response data
        resp_json = response.data
        # convert to json
        resp_dict = json.loads(resp_json)
        # use assert to verify
        self.assertIn("code", resp_dict)
        # compare the code value 1001
        code = resp_dict.get("code")
        self.assertEqual(code, 0)
        # return message
        msg = resp_dict.get('message')
        self.assertEqual(msg, "OK")
    
    # 测试密码复杂度不足的情况
    def test_register_weak_passwords(self):
        # 密码太短
        response = self.client.post("/register", data={"email_address": "admin@example.com", "password": "Short1!"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertEqual(resp_dict.get("code"), 1002)
        self.assertIn("Password must be at least 8 characters long", resp_dict.get('message'))

        # 缺少大写字母
        response = self.client.post("/register", data={"email_address": "admin@example.com", "password": "lowercase1!"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertEqual(resp_dict.get("code"), 1002)
        self.assertIn("Password must contain at least one uppercase letter", resp_dict.get('message'))

        # 缺少小写字母
        response = self.client.post("/register", data={"email_address": "admin@example.com", "password": "UPPERCASE1!"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertEqual(resp_dict.get("code"), 1002)
        self.assertIn("Password must contain at least one lowercase letter", resp_dict.get('message'))

        # 缺少数字
        response = self.client.post("/register", data={"email_address": "admin@example.com", "password": "LowerUpper!"})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertEqual(resp_dict.get("code"), 1002)
        self.assertIn("Password must contain at least one digit", resp_dict.get('message'))

        

  
# 运行测试  
if __name__ == '__main__':  
    unittest.main()