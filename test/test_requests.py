import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        from app.util.utils import Requests
        self.r = Requests()

    def test_something(self):
        res = self.r.get("http://www.baidu.com")
        self.assertEquals(res.ok, 1)
        future = self.r.async_get("http://www.baidu.com")
        ret = future.result()
        self.assertEquals(ret.ok, 1)


if __name__ == '__main__':
    unittest.main()
