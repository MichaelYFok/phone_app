# -*- coding:utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class VerifyCodeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == "/login/" and request.method == "POST":
            code = request.POST.get("verifycode")
            verifycode = request.session.get("verifycode")
            if code  != verifycode:
                #验证失败
                return redirect("/login/")


