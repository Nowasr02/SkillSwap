from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from skills.models import (
    Skill, Category, OfferedSkill, NeededSkill, 
    SkillExchange, ExchangeChain, ChainLink, BrokerProposal
)
from django.db.models import Sum

# Create your views here.

def home_view(request):
    """Home page - shows featured skills and exchanges"""
    context = {
        'featured_skills': Skill.objects.all()[:8],
        'recent_exchanges': SkillExchange.objects.filter(
            status='completed'
        ).order_by('-completed_at')[:4],
        'total_users': User.objects.count(),
        'total_exchanges': SkillExchange.objects.filter(status='completed').count(),
        'total_hours_traded': SkillExchange.objects.filter(
            status='completed'
        ).aggregate(total=Sum('initiator_hours_required'))['total'] or 0,
    }
    return render(request, 'skills/home.html', context)
