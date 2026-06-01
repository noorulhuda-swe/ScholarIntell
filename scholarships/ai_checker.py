from groq import Groq
from django.conf import settings


def check_eligibility(profile, scholarship):
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are a scholarship eligibility advisor. Analyze if this student qualifies for the scholarship.

STUDENT PROFILE:
- Name: {profile.user.get_full_name() or profile.user.username}
- Degree Level: {profile.degree_level}
- Field of Study: {profile.field_of_study}
- CGPA: {profile.cgpa} / 4.0
- Country of Origin: {profile.country_of_origin}
- Language Certificate: {profile.language_cert or 'None'}
- Language Score: {profile.language_score or 'Not provided'}
- Preferred Country: {profile.preferred_country or 'Any'}

SCHOLARSHIP DETAILS:
- Name: {scholarship.name}
- Host Country: {scholarship.host_country}
- Level Required: {scholarship.level}
- Field of Study: {scholarship.field_of_study}
- Fully Funded: {'Yes' if scholarship.fully_funded else 'No'}
- What It Covers: {scholarship.what_it_covers}
- Special Requirements: {scholarship.special_requirements or 'None mentioned'}
- Language Requirements: {scholarship.language_requirements or 'None mentioned'}
- Deadline: {scholarship.deadline or 'Check website'}

INSTRUCTIONS:
Give a clear eligibility analysis in this exact format:

VERDICT: [STRONG MATCH / PARTIAL MATCH / NOT ELIGIBLE]

REASONS YOU QUALIFY:
- List each matching point clearly

CONCERNS OR GAPS:
- List anything the student may be missing or needs to check

RECOMMENDATION:
Write 2-3 sentences of honest advice for this student about whether to apply.

Keep the tone helpful, encouraging, and honest. Be specific using the actual numbers and values.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.7,
    )

    return response.choices[0].message.content
