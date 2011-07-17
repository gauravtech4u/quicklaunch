#!/usr/bin/env python
from django.core.management.base import BaseCommand, CommandError
from core.models import RandomLinks
from institute.models import Institute
from video.models import Video
from internship.models import Internship
from djangovoice.models import Feedback
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        random_list =   RandomLinks.objects.all()
        for obj in random_list:
            obj.delete()
        institute_list=Institute.objects.all()
        video_list=Video.objects.all()
        intern_list=Internship.objects.all()
        feedback_list=Feedback.objects.all()
        inst_obj=institute_list[int(random.random()*len(institute_list))+1]
        RandomLinks(slug=inst_obj.slug,description=inst_obj.description[:200],object_id=inst_obj.id).save()
        video_obj=video_list[int(random.random()*len(institute_list))+1]
        RandomLinks(slug=video_obj.slug,description=video_obj.title,object_id=video_obj.id).save()
        #intern_obj=video_list[int(random.random()*len(institute_list)+1)]
        #RandomLinks(slug=intern_obj.slug,description=intern_obj.description,object_id=intern_obj.id).save()
        feedback_obj=feedback_list[int(random.random()*len(feedback_list))+1]
        RandomLinks(slug=feedback_obj.title,description=feedback_obj.description[:100],object_id=feedback_obj.id).save()
                    