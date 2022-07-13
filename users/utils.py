

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
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

def paginateProfiles(request,profiles,results):
    #projects,search_query=searchProjects(request)

    # page=2  # on which  page we should be
    # results= 3 # 3 projects  i.e on each page we will 3 results 

    page=request.GET.get('page')
    
    paginator=Paginator(profiles,results)
    try:
        profiles=paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages #num_page will tell no of page 
        # and this will give last page
        profiles=paginator.page(page)
    
    leftIndex=(int(page)-4)
    if leftIndex<1:
        leftIndex=1
    rightIndex=int(page)+5

    if rightIndex> paginator.num_pages:
        rightIndex=paginator.num_pages+1

    custom_range=range(leftIndex,rightIndex)
    return custom_range,profiles