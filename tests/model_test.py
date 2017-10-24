import unittest
from app.model import User, Task


class MyTestCase(unittest.TestCase):
    def test_search(self):
        user = User(username='fxw', password='hahaha', email='21398')
        self.assertTrue(user.verify_password('hahaha'))
        self.assertFalse(user.verify_password('fuckyou'))
#         self.assertTrue(1 + 1 == 2)

    def test_user(self):
        user = User(username='fxw', password='hahaha', email='21398')
        tsk = Task(content='adlkhjj', tag='test', ending='1998.08.09', author=user)
        self.assertTrue(tsk.user_id == user.id)
        print(tsk)


if __name__ == '__main__':
    unittest.main()
    # user = User(username='fxw', password='hahaha', email='21398')
    # print(user.password_hash)
    # s = 'hahaha'
    # print(user.verify_password(s))