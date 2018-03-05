# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView,CourseCommentView,AddCourseCommentView,CourseVideoView

__author__ = 'dongfangyao'
__date__ = '2017/11/6 下午2:50'
__product__ = 'PyCharm'
__filename__ = 'urls'

urlpatterns = [
    # 课程机构列表页面
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 某个课程的详情页面 必须知道哪个课程的id
    url(r'^detail/(?P<course_id>[0-9]+)/$', CourseDetailView.as_view(), name='course_detail'),

    # 某个课程的章节视频页面 课程评论页面
    url(r'^info/(?P<course_id>[0-9]+)/$', CourseInfoView.as_view(), name='course_info'),

    url(r'^comment/(?P<course_id>[0-9]+)$', CourseCommentView.as_view(), name='course_comment'),

    url(r'^add_comment/$', AddCourseCommentView.as_view(), name='course_add_comment'),

    # 视频播放页面
    url(r'^video/(?P<video_id>[0-9]+)/$', CourseVideoView.as_view(), name='course_video'),

]
