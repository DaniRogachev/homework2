from dateutil import parser
from django.shortcuts import render
from .models import Car
from typing import Union
import requests


PI = 3.14


def home(request):
    return render(request, 'home.html')



def cars(request):
    all_cars = Car.objects.all()
    return render(request, 'cars.html', {'cars': all_cars})


def commuters(request):
    result = requests.get("https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort"
                          "=departure_time&include=schedule%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place"
                          "-north")

    class Schedule:
        def __init__(self, m_time, m_destination, m_train, m_status):
            self.m_time = m_time
            self.m_destination = m_destination
            self.m_train = m_train
            self.m_status = m_status

    info = []
    for i in range(0, 10):
        try:
            time = str(
                parser.parse(result.json()["included"][i + 10]["attributes"]["departure_time"]).strftime("%H:%M %p"))
        except:
            time = "none"
        try:
            destination = str(result.json()["included"][i]["attributes"]["headsign"])
        except:
            destination = "none"
        try:
            train = str(result.json()["included"][i]["attributes"]["name"])
        except:
            train = "none"
        try:
            status = str(result.json()["data"][i]["attributes"]["status"])
        except:
            status = "none"
        schedule = Schedule(time, destination, train, status)
        info.append(schedule)

    return render(request, 'commuters.html', {'info': info})
