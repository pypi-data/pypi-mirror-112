""" Клиент по ручной установке рассылаемых данных в PSD """
from portdatasplitter.tests import test_settings as s
from witapi.main import WITClient
import unittest


class TestClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.client = WITClient('localhost', 1337, login="Login", password="Password")
        self.client.make_connection()

    def test_listen_value(self):
        subscribe_comm = {'subscribe': None}
        self.client.send_data(subscribe_comm)
        print("GET_DATA_RESPONSE", self.client.get_data())
        print("get_weight...", self.client.get_data())
        print("get_weight...", self.client.get_data())
        print("get_weight...", self.client.get_data())
        print("get_weight...", self.client.get_data())
        print("get_weight...", self.client.get_data())

    def test_setting_value(self):
        set_command = {'user_command': {'set_test_value': {'test_value': '0'}}}
        self.client.send_data(set_command)
        response = self.client.get_data()
        self.assertTrue(response['core_method'] == 'set_test_value')


if __name__ == '__main__':
    unittest.main()
