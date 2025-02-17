from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import disease_table, key_value_table, testimonial_table, video_table

class HomeView(View):
    def get(self, request):
        try:
            # this will be sent to user
            final_data = {}

            # getting data for topSearchPage
            diseases = disease_table.objects.all()
            diseaseList = list(diseases.values_list('disease', flat=True))
            final_data.update({"topSearchPage": {"diseaseList": diseaseList}})

            # getting data for ourMissionPage
            final_data.update({"ourMissionPage": {
                "youtubeLink": key_value_table.objects.get(key='our_mission_ytlink').value,
                "ourMissionText": key_value_table.objects.get(key='our_mission_data').value,
            }})

            # getting data for testimonialPage
            testimonial_list = []
            for testimonial in testimonial_table.objects.filter(show=True):
                testimonial_list.append({
                    "heading": testimonial.heading,
                    "text": testimonial.text,
                    "name": testimonial.name,
                    "location": testimonial.location
                })
            final_data.update({"testimonialPage": {"testimonialList": testimonial_list}})

            # getting data for videoPage
            video_list = []
            for video in video_table.objects.all():
                video_list.append({
                    "imageLink": video.image.url,
                    "heading": video.heading,
                    "ytPlaylistLink": video.ytplaylist_link
                })
            final_data.update({"videoPage": {
                "text": key_value_table.objects.get(key="video_section_text").value,
                "videoList": video_list 
            }})

            # getting data for bottomSearchPage
            final_data.update({"bottomSearchPage": {"text": key_value_table.objects.get(key="second_search_text").value}})

            # getting data for footer
            final_data.update({"footer": {
                "contactEmail": key_value_table.objects.get(key="contact_email_address").value,
                "contactPhoneNumber": key_value_table.objects.get(key="contact_phone_no").value,
                "contactAddress": key_value_table.objects.get(key="contact_address").value
            }})
            return JsonResponse(data=final_data, status=200)
        except:
            return JsonResponse(data={"message": "error while getting data"}, status=404)
        