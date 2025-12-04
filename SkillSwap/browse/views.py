from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Count, Q
from django.core.paginator import Paginator
from accounts.models import UserProfile
from skills.models import Skill, Category 

# Create your views here.

def browse_view(request : HttpRequest):
    
    qs = UserProfile.objects.all().select_related('user')

    #maybe move filter and search to different view (?)
    
    # count each user total skills //optional
    qs = qs.annotate(skills_count=Count('user_skills', distinct=True))

    # # search
    # q = request.GET.get('q', '').strip()
    # if q:
    #     qs = qs.filter(
    #         Q(user__username__icontains=q) |
    #         Q(user__first_name__icontains=q) |
    #         Q(user__last_name__icontains=q)
    #     )

    # filter by skill id
    skill_id = request.GET.get('skill')
    if skill_id:
        qs = qs.filter(user_skills__skill_id=skill_id).distinct()

    # filter by category id
    category_id = request.GET.get('category')
    if category_id:
        qs = qs.filter(user_skills__skill__categories__id=category_id).distinct()

    qs = qs.order_by('user__username')

    # lists for filter controls in template
    categories = Category.objects.filter(parent__isnull=True).order_by('category')  # root categories
    skills = Skill.objects.order_by('skill').all()

    # pagination
    page_num = request.GET.get('page', 1)
    paginator = Paginator(qs, 12)  # 12 cards per page
    profiles_page = paginator.get_page(page_num)

    return render(request, "browse/browse.html", {
        "profiles": profiles_page,
        "paginator": paginator,
        "categories": categories,
        "skills": skills,
        "q": q,
        "selected_skill": skill_id or "",
        "selected_category": category_id or "",
    })
    
    
def search_profiles(request):
    q = request.GET.get("q", "")

    results = UserProfile.objects.filter(
        user__username__icontains=q
    )

    return render(request, "browse/search_results.html", {
        "q": q,
        "results": results
    })
