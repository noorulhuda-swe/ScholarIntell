from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Scholarship
from .recommender import recommend_scholarships
from .ai_checker import check_eligibility


def home(request):
    total     = Scholarship.objects.count()
    funded    = Scholarship.objects.filter(fully_funded=True).count()
    countries = Scholarship.objects.values('host_country').distinct().count()
    return render(request, 'home.html', {
        'total': total, 'funded': funded, 'countries': countries,
    })


@login_required
def dashboard(request):
    try:
        profile = request.user.studentprofile
        if not profile.profile_complete:
            messages.info(request, 'Please complete your profile first.')
            return redirect('profile_setup')
    except:
        messages.info(request, 'Please complete your profile first.')
        return redirect('profile_setup')

    ranked         = recommend_scholarships(profile)
    filter_funded  = request.GET.get('funded', '')
    filter_country = request.GET.get('country', '')
    filter_level   = request.GET.get('level', '')

    filtered = []
    for score, s in ranked:
        if filter_funded == 'yes' and not s.fully_funded:
            continue
        if filter_country and filter_country.lower() not in s.host_country.lower():
            continue
        if filter_level and filter_level.lower() not in s.level.lower():
            continue
        filtered.append((score, s))

    paginator   = Paginator(filtered, 12)
    page_obj    = paginator.get_page(request.GET.get('page'))
    all_countries = sorted(set(s.host_country for _, s in ranked if s.host_country))

    return render(request, 'scholarships/dashboard.html', {
        'ranked': page_obj,
        'page_obj': page_obj,
        'total_found': len(filtered),
        'profile': profile,
        'all_countries': all_countries,
        'all_levels': ['Bachelor', 'Master', 'PhD'],
        'filter_funded': filter_funded,
        'filter_country': filter_country,
        'filter_level': filter_level,
    })


@login_required
def scholarship_detail(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    related = Scholarship.objects.filter(
        Q(host_country=scholarship.host_country) |
        Q(level__icontains=scholarship.level.split(',')[0].strip())
    ).exclude(pk=pk)[:3]
    return render(request, 'scholarships/detail.html', {
        'scholarship': scholarship,
        'related': related,
    })


@login_required
def eligibility_check(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    try:
        profile = request.user.studentprofile
    except:
        messages.error(request, 'Please complete your profile first.')
        return redirect('profile_setup')

    ai_result = None
    error     = None

    if request.method == 'POST':
        try:
            ai_result = check_eligibility(profile, scholarship)
        except Exception as e:
            error = f"AI service error: {str(e)}"

    return render(request, 'scholarships/eligibility.html', {
        'scholarship': scholarship,
        'profile': profile,
        'ai_result': ai_result,
        'error': error,
    })


@login_required
def search_view(request):
    query          = request.GET.get('q', '').strip()
    filter_funded  = request.GET.get('funded', '')
    filter_country = request.GET.get('country', '')
    filter_level   = request.GET.get('level', '')

    results = Scholarship.objects.all()

    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(host_country__icontains=query) |
            Q(host_institution__icontains=query) |
            Q(field_of_study__icontains=query) |
            Q(what_it_covers__icontains=query)
        )

    if filter_funded == 'yes':
        results = results.filter(fully_funded=True)
    if filter_country:
        results = results.filter(host_country__icontains=filter_country)
    if filter_level:
        results = results.filter(level__icontains=filter_level)

    total_found = results.count()
    paginator   = Paginator(results, 12)
    page_obj    = paginator.get_page(request.GET.get('page'))
    all_countries = sorted(
        Scholarship.objects.values_list('host_country', flat=True).distinct()
    )

    return render(request, 'scholarships/search.html', {
        'results': page_obj,
        'page_obj': page_obj,
        'query': query,
        'total_found': total_found,
        'all_countries': all_countries,
        'all_levels': ['Bachelor', 'Master', 'PhD'],
        'filter_funded': filter_funded,
        'filter_country': filter_country,
        'filter_level': filter_level,
    })


def custom_404(request, exception):
    return render(request, '404.html', status=404)
