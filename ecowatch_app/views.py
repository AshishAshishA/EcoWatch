from django.shortcuts import render, redirect
from .models import WasteSite, Video
# from .forms import UploadForm, TagForm

def waste_site_list(request):
    waste_sites=WasteSite.objects.all()
    return render(request,'waste_site_list.html',{"waste_sites":waste_sites})

def upload_and_tag(request):
    if request.method == 'POST':
        # Get data from the POST request
        video_file = request.FILES.get('video_file')

        city_name = request.POST.get('city_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        description = request.POST.get('description')
        
        # Create Video object
        video = Video.objects.create(video_file=video_file)
        
        # Create WasteSite object
        WasteSite.objects.create(city_name=city_name, latitude=latitude, longitude=longitude, description=description, video=video)
        
        return redirect('waste_site_list')  # Update with correct URL name
    else:
        return render(request, 'upload_and_tag.html')

def tag_waste_site_map(request):
    waste_sites = WasteSite.objects.all()
    return render(request, 'tag_waste_site_map.html', {'waste_sites': waste_sites})

def map_view(request):
    return render(request, 'map.html')

