


from users.views import profile,skill
from django.db.models import Q
#for searching i.e we need to search for short_intro as well as name


def searchProfiles(request): 
    search_query=''
    if request.GET.get('text'):
        search_query=request.GET.get('text')
        print(search_query)
    
    skills=skill.objects.filter(name__icontains=search_query)

    profiles=profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query)|
        Q(skill__in=skills)
        )
    return profiles,search_query
