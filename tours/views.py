from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from django.views import View
from stepik_tours import data
import random


class MainView(View):
    def get(self, request):
        departures = data.departures.items()
        tours = random.sample(data.tours.items(), 6)  # 6 рандомных туров
        context = {'title': data.title,
                   'subtitle': data.subtitle,
                   'description': data.description,
                   'tours': tours,
                   'departures': departures}
        return render(request, 'tours/index.html', context=context)


class DepatureView(View):
    def get(self, request, departure):
        if departure not in data.departures.keys():
            raise Http404

        departure_data = []  # список туров по отбору города выезда
        departures = data.departures.items()
        tours = data.tours.items()
        for departure_id, departure_name in tours:
            if departure == departure_name['departure']:
                departure_data.append(departure_name)
        count_tours = len(departure_data)
        price_tour = [prices['price'] for prices in departure_data]
        nights_tour = [night['nights'] for night in departure_data]
        context = {'departures': departures,
                   'departure': departure,
                   'tours': tours,
                   'count_tours': count_tours,
                   'min_price_tour': min(price_tour),
                   'max_price_tour': max(price_tour),
                   'min_nights_tour': min(nights_tour),
                   'max_nights_tour': max(nights_tour)}

        return render(request, 'tours/departure.html', context=context)


class TourView(View):
    def get(self, request, tour_id):
        if tour_id not in data.tours.keys():
            raise Http404

        tour_info = data.tours.get(tour_id)
        departure_info = data.departures[tour_info['departure']]
        departures = data.departures.items()
        context = {'tour_info': tour_info,
                   'departure_info': departure_info,
                   'departures': departures}

        return render(request, 'tours/tour.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    return HttpResponseServerError('Ой, что то сломалось... '
                                   'Простите извините!')
