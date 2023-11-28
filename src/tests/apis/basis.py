# from django.test import TestCase
from django.core.cache import cache
from django.http import HttpResponse
from django.test import TestCase


class BasisTestCase(TestCase):
    # def setUp(self) -> None:
    #     return super().setUp()
    method = 'get'
    path = '/'

    def tearDown(self):
        cache.clear()

        return super().tearDown()

    def mock_request(self, data: dict = None, headers: dict = None, err_msg: str = None, err_code: str = None) -> dict:
        request_func = getattr(self.client, self.method)
        self.client.get()
        resp: HttpResponse = request_func(self.path, data=data, headers=headers)

        res = resp.json()
        if err_msg or err_code:
            self.assertEqual(res['error'], err_msg)
            self.assertEqual(res['code'], err_code)

        else:
            self.assertEqual(resp.status_code, 200)

        return res
