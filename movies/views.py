from django.shortcuts import render, get_object_or_404
from .models import Movie
import requests
import json
from django.db.models import Q
from itertools import chain

def home(request):
    query = request.GET.get('query', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies, 'query': query})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Convert YouTube URL to embed format if possible
    if movie.trailer_url and "watch?v=" in movie.trailer_url:
        movie.trailer_embed_url = movie.trailer_url.replace("watch?v=", "embed/")
    else:
        movie.trailer_embed_url = movie.trailer_url

    return render(request, 'movie_detail.html', {'movie': movie})


def get_unique_split_values(queryset):
    values = chain.from_iterable(
        value.split(',') for value in queryset if value
    )
    return sorted(set(v.strip() for v in values if v.strip()))

def recommend(request):
    recommended_movies = []
    user_input_text = ""
    selected = {}

    # Prepare dropdown options from DB
    raw_genres = Movie.objects.exclude(genres__isnull=True).exclude(genres__exact='').values_list('genres', flat=True)
    raw_moods = Movie.objects.exclude(mood__isnull=True).exclude(mood__exact='').values_list('mood', flat=True)
    raw_languages = Movie.objects.exclude(language__isnull=True).exclude(language__exact='').values_list('language', flat=True)
    raw_platforms = Movie.objects.exclude(available_on__isnull=True).exclude(available_on__exact='').values_list('available_on', flat=True)

    genres = get_unique_split_values(raw_genres)
    moods = get_unique_split_values(raw_moods)
    languages = get_unique_split_values(raw_languages)
    platforms = get_unique_split_values(raw_platforms)

    if request.method == 'POST':
        selected = {
            'genre': request.POST.get('genre', ''),
            'mood': request.POST.get('mood', ''),
            'language': request.POST.get('language', ''),
            'platform': request.POST.get('platform', '')
        }
        user_input_text = request.POST.get('preferences', '')

        # Combine user inputs
        parts = []
        if selected['genre']:
            parts.append(f"Genre: {selected['genre']}")
        if selected['mood']:
            parts.append(f"Mood: {selected['mood']}")
        if selected['language']:
            parts.append(f"Language: {selected['language']}")
        if selected['platform']:
            parts.append(f"Platform: {selected['platform']}")
        if user_input_text:
            parts.append(f"Other preferences: {user_input_text}")

        combined_input = "\n".join(parts)

        # Fetch matching titles from DB to pass as context
        filtered_movies = Movie.objects.all()
        if selected['genre']:
            filtered_movies = filtered_movies.filter(genres__icontains=selected['genre'])
        if selected['mood']:
            filtered_movies = filtered_movies.filter(mood__icontains=selected['mood'])
        if selected['language']:
            filtered_movies = filtered_movies.filter(language__icontains=selected['language'])
        if selected['platform']:
            filtered_movies = filtered_movies.filter(available_on__icontains=selected['platform'])

        sample_titles = list(filtered_movies.values_list('title', flat=True)[:50])
        available_titles_str = ", ".join(f'"{title}"' for title in sample_titles)

        movie_list_context = f"""
Here are some example movies you can choose from:
[{available_titles_str}]
"""

        # Final prompt
        prompt = f"""
You are an intelligent Bollywood movie recommendation engine.
Based on the user's preferences, suggest 5 movies they are likely to enjoy.

User Preferences:
{combined_input}

{movie_list_context}

Avoid recommending the same movies all the time. Pick diverse, unique titles when possible.

Respond ONLY with a JSON array like this:
["Movie Title 1", "Movie Title 2", "Movie Title 3", "Movie Title 4", "Movie Title 5"]
"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                headers={"Content-Type": "application/json"},
                data=json.dumps({
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.8,
                    "top_p": 0.9
                }),
                timeout=20
            )

            result_text = response.json().get("response", "").strip()
            print("LLaMA2 Response:", result_text)

            list_start = result_text.find('[')
            list_end = result_text.find(']', list_start) + 1
            recommendations = json.loads(result_text[list_start:list_end])

            query = Q()
            for title in recommendations:
                query |= Q(title__icontains=title.strip())

            recommended_movies = Movie.objects.filter(query)

            # Fallback: If some movies aren't found, replace them with random ones from the same filters
            if recommended_movies.count() < 5:
                missing_titles = [title for title in recommendations if not Movie.objects.filter(title__icontains=title.strip()).exists()]
                print(f"Missing movies: {missing_titles}")

                # Replace missing titles with random available ones
                for title in missing_titles:
                    fallback_movie = Movie.objects.filter(genres__icontains=selected['genre']).exclude(title__icontains=title).first()
                    if fallback_movie:
                        recommended_movies = recommended_movies | Movie.objects.filter(id=fallback_movie.id)

        except Exception as e:
            print("Error in recommendation:", str(e))

    return render(request, 'recommend.html', {
        'recommended_movies': recommended_movies,
        'genres': genres,
        'moods': moods,
        'languages': languages,
        'platforms': platforms,
        'selected': selected,
        'user_input': user_input_text
    })