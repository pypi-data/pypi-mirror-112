import base64
import oss2, requests, json, os

def get_b64(s):
    json_str = s.encode('utf-8')
    return base64.b64encode(json_str).decode('utf-8')


def test():
    pass


if __name__ == "__main__":
    test()
