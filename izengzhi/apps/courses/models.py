# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from izengzhi.apps.organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'所属的课程机构')
    name = models.CharField(max_length=50, verbose_name=u'课程名字')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(max_length=2, verbose_name=u'课程难度',
                              choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), default='cj')
    learn_duration = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    student_num = models.IntegerField(default=0, verbose_name=u'学生人数')
    favorites_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(max_length=200, upload_to='courses/%Y/%m', verbose_name=u'封面图')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default=u'web开发/后端开发')
    tag = models.CharField(max_length=20, verbose_name=u'课程标签', default='')
    teacher = models.ForeignKey(Teacher, verbose_name=u'课程的教师', null=True, blank=True)
    need_know = models.CharField(max_length=100, verbose_name=u'课程须知', default='')
    can_learn = models.CharField(max_length=100, verbose_name=u'课程能学到什么', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_course_lessons(self):
        return self.lesson_set.all()

    def get_learn_users(self):
        return self.usercourse_set.all()[:6]


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'所属课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'所属章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    url = models.CharField(max_length=300, verbose_name=u'视频链接', default='')
    video_duration = models.IntegerField(default=0, verbose_name=u'视频时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'所属课程')
    name = models.CharField(max_length=100, verbose_name=u'课程资源名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name=u'课程资源文件')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
