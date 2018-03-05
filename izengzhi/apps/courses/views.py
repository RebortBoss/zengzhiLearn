# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse
from .models import Course, CourseResource, Video

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from izengzhi.apps.operation.models import UserFavorite, CourseComment, UserCourse
from izengzhi.apps.utils.mixin_utils import LoginRequireMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_num')[:3]

        # 对学习人数 课程数的排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-student_num')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_num')

        # 课程列表页面的分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 获取某个课程的所有章节数
        # lesson_nums = course.lesson_set.all().count()
        # 点击课程详情的时候 需要将课程的click数加1
        course.click_num += 1
        course.save()

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=3):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org

        })


# 自动验证登录
class CourseInfoView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # all_course_resource = course.courseresource_set.all()
        all_course_resource = CourseResource.objects.filter(course_id=int(course_id))

        # if not request.user.is_authenticated():
        #     return render(request,'login.html')

        # 对课程和用户进行关联
        user_course_exists = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course_exists:
            user_course_object = UserCourse(user=request.user, course=course)
            user_course_object.save()
            # 课程的学生人数需要增加
        course.student_num += 1
        course.save()

        #  相关课程推荐， 学过该课程的用户还学过什么课程
        user_courses = course.usercourse_set.all()
        # 学过该课程所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据用户ID 查询用户学习课程id
        # __in 表示 只要 user_id 在 user_ids里面都会返回
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 课程ids
        course_ids = [all_user_course.id for all_user_course in all_user_courses]
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]

        return render(request, 'course-video.html', {
            'course': course,
            'all_course_resource': all_course_resource,
            'relate_course': relate_course
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # all_course_resource = course.courseresource_set.all()
        all_course_resource = CourseResource.objects.filter(course_id=int(course_id))

        all_comments = course.coursecomment_set.all().order_by('-add_time')

        #  相关课程推荐， 学过该课程的用户还学过什么课程
        user_courses = course.usercourse_set.all()
        # 学过该课程所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据用户ID 查询用户学习课程id
        # __in 表示 只要 user_id 在 user_ids里面都会返回
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 课程ids
        course_ids = [all_user_course.id for all_user_course in all_user_courses]
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]

        return render(request, 'course-comment.html', {
            'course': course,
            'all_course_resource': all_course_resource,
            'all_comments': all_comments,
            'relate_course': relate_course
        })


class CourseVideoView(View):
    def get(self, request, video_id):

        video = Video.objects.get(id=int(video_id))

        course = video.lesson.course
        all_course_resource = CourseResource.objects.filter(course=course)

        # 对课程和用户进行关联
        user_course_exists = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course_exists:
            user_course_object = UserCourse(user=request.user, course=course)
            user_course_object.save()
            # 课程的学生人数需要增加
        course.student_num += 1
        course.save()

        #  相关课程推荐， 学过该课程的用户还学过什么课程
        user_courses = course.usercourse_set.all()
        # 学过该课程所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 根据用户ID 查询用户学习课程id
        # __in 表示 只要 user_id 在 user_ids里面都会返回
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 课程ids
        course_ids = [all_user_course.id for all_user_course in all_user_courses]
        relate_course = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]

        return render(request, 'course-play.html', {
            'course': course,
            'all_course_resource': all_course_resource,
            'relate_course': relate_course,
            'video':video
        })


class AddCourseCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', '0')
        comment_content = request.POST.get('comment_content', '')
        if int(course_id) > 0 and comment_content:
            course_comment = CourseComment()
            course_comment.user = request.user
            course_comment.comments = comment_content
            course_comment.course = Course.objects.get(id=int(course_id))
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论出错"}', content_type='application/json')
