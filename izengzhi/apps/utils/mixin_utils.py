# -*- coding: utf-8 -*-
__author__ = 'pengxin'
__date__ = '2018/2/28 16:04'
__product__ = 'PyCharm'
__filename__ = 'mixin_utils.py'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequireMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequireMixin, self).dispatch(request, *args, **kwargs)
