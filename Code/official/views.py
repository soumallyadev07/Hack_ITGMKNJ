from django.shortcuts import render
from .models import Personality
from django.shortcuts import redirect
import csv, io, os, time

def csv_to_dbsql(request):
    file = os.path.join(os.path.dirname(os.path.dirname(__file__)),"scrapping_scripts/ScrappedData/PoliticalLeaders.csv")
    with open(file,encoding='utf-8', errors='ignore') as csv_file:
        for row in csv.reader(csv_file):
            print(row)
            _, created = Personality.objects.update_or_create(
                country     = row[0],
                full_name   = row[1],
                first_name  = row[2],
                middle_name = row[3],
                last_name   = row[4],
                gender      = row[5],
                title       = row[6],
                designation = row[7],
                contact     = row[8],
                images      = row[9],
                last_updated= row[10],
            )
            time.sleep(1)
    
    return redirect('personalities')


