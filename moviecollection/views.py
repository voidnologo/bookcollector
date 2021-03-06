import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render

from .forms import SearchForm
from .models import Series, Genre, Movie, Tag, FORMAT_CHOICES


@login_required
def index(request):
    context = {
        'movies': sorted(Movie.objects.all(), key=lambda b: b.alphabetical_title),
        'movie_count': Movie.objects.count(),
        'genreData': json.dumps({g.name: g.movie_count for g in Genre.objects.all()}),
        'formatData': json.dumps({f[1]: Movie.objects.filter(disc_format=f[0]).count() for f in FORMAT_CHOICES}),
    }
    return render(request, 'moviecollection/index.html', context=context)


@login_required
def movie_covers(request):
    context = {
        'movies': sorted(Movie.objects.all(), key=lambda b: b.alphabetical_title)
    }
    return render(request, 'moviecollection/movie_covers.html', context=context)


@login_required
def movies(request):
    movies = Movie.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            movies = movies.filter(title__icontains=search_text)
    movies = sorted(movies, key=lambda b: b.alphabetical_title)
    paginator = Paginator(movies, 50)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_movies = paginator.page(page)
    except PageNotAnInteger:
        all_movies = paginator.page(1)
    except EmptyPage:
        all_movies = paginator.page(paginator.num_pages)
    return render(request, 'moviecollection/movies.html', {'all_movies': all_movies, 'search_form': search_form})


@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'moviecollection/movie_detail.html', {'movie': movie})


@login_required
def genres(request):
    all_genres = Genre.objects.all()
    return render(request, 'moviecollection/genres.html', {'all_genres': all_genres})


@login_required
def series(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            series = Series.objects.filter(name__icontains=search_text)
    else:
        series = Series.objects.all()
    paginator = Paginator(series, 50)
    page = request.GET.get('page')
    search_form = SearchForm()
    try:
        all_series = paginator.page(page)
    except PageNotAnInteger:
        all_series = paginator.page(1)
    except EmptyPage:
        all_series = paginator.page(paginator.num_pages)
    return render(request, 'moviecollection/series.html', {'all_series': all_series, 'search_form': search_form})


@login_required
def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genre=genre).order_by('title')
    series = [s for s in Series.objects.all() if s.genre == genre]
    context = {
        'genre': genre,
        'movie_count': len(movies),
        'movies': movies,
        'series': series,
        'series_count': len(series),
        'genreData': json.dumps({s.name: Movie.objects.filter(subgenre=s).count() for s in genre.subgenre_set.all()})
    }
    return render(request, 'moviecollection/genre_detail.html', context=context)


@login_required
def series_detail(request, series_id):
    series = get_object_or_404(Series, pk=series_id)
    series_movies = series.movie_set.all().order_by('series_number')
    return render(request, 'moviecollection/series_detail.html', {'series': series, 'series_movies': series_movies})


@login_required
def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genre=genre).order_by('title')
    paginator = Paginator(movies, 50)
    page = request.GET.get('page')
    try:
        all_movies = paginator.page(page)
    except PageNotAnInteger:
        all_movies = paginator.page(1)
    except EmptyPage:
        all_movies = paginator.page(paginator.num_pages)
    return render(request, 'moviecollection/movies.html', {'all_movies': all_movies})


@login_required
def genre_series(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    series = [s for s in Series.objects.all() if s.genre == genre]
    paginator = Paginator(series, 50)
    page = request.GET.get('page')
    try:
        all_series = paginator.page(page)
    except PageNotAnInteger:
        all_series = paginator.page(1)
    except EmptyPage:
        all_series = paginator.page(paginator.num_pages)
    return render(request, 'moviecollection/series.html', {'all_series': all_series})


@login_required
def tags(request):
    tags = Tag.objects.all()
    return render(request, 'moviecollection/tags.html', {'tags': tags})


@login_required
def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    tag_movies = sorted(tag.movie_set.all(), key=lambda b: b.alphabetical_title)
    return render(request, 'moviecollection/tag_detail.html', {'tag': tag, 'tag_movies': tag_movies})
