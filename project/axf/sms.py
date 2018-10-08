#-*- coding:utf-8 -*-
import http.client
import urllib

host  = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

account  = "C66204495"
password = "f4bcaf08bcd2d18b8325763abf61935c"

def send_sms(text, mobile):
    params = urllib.parse.urlencode({'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' })
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str 

if __name__ == '__main__':

    mobile = "13691511443"
    text = "您的验证码是：121254。请不要把验证码泄露给其他人。"

    print(send_sms(text, mobile))