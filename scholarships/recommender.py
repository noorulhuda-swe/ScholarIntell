from django.db.models import Q
from .models import Scholarship


def recommend_scholarships(profile):
    qs = Scholarship.objects.all()

    # --- Filter by degree level ---
    level_filter = Q()
    for level in ['Bachelor', 'Master', 'PhD']:
        if level.lower() in profile.degree_level.lower():
            level_filter |= Q(level__icontains=level)
    level_filter |= Q(level__icontains='Any')
    qs = qs.filter(level_filter)

    # --- Filter by field of study ---
    field_words = profile.field_of_study.lower().split()
    field_filter = Q(field_of_study__icontains='All Disciplines')
    for word in field_words:
        if len(word) > 3:
            field_filter |= Q(field_of_study__icontains=word)
    qs = qs.filter(field_filter)

    # --- Scoring: rank results ---
    results = []
    for s in qs:
        score = 0

        # Fully funded = big bonus
        if s.fully_funded:
            score += 40

        # Preferred country match
        if profile.preferred_country:
            if profile.preferred_country.lower() in s.host_country.lower():
                score += 30

        # Language score check
        if profile.language_cert and profile.language_score:
            lang_req = s.language_requirements.lower()
            if 'ielts' in lang_req and profile.language_cert == 'IELTS':
                try:
                    # Try to find required score in text
                    import re
                    scores = re.findall(r'\d+\.?\d*', lang_req)
                    req_scores = [float(x) for x in scores if 4 <= float(x) <= 9]
                    if req_scores:
                        min_req = min(req_scores)
                        if profile.language_score >= min_req:
                            score += 20
                except:
                    score += 10
            elif 'toefl' in lang_req and profile.language_cert == 'TOEFL':
                score += 15

        # No strict language requirement = accessible
        if not s.language_requirements or s.language_requirements.strip() == '':
            score += 10

        results.append((score, s))

    # Sort by score descending
    results.sort(key=lambda x: x[0], reverse=True)

    return results
