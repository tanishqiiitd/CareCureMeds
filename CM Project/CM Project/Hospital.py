import pandas as pd
import numpy as np
from collections import Counter
import requests
import urllib.parse
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import urllib
import gmaps
import plotly.express as px
from pathlib import Path
import plotly.graph_objects as go
from geopy.distance import geodesic

geolocator = Nominatim(user_agent = 'myapplication')

features = ["Facility Name","Address","Phone Number","Hospital Type","Hospital overall rating","Emergency Services","Distance"]

def getFromAddress(address):
    try:
        add = geolocator.geocode(address)
        return (add.raw['lat'],add.raw['lon'])
    except:
        return (None,None)

def thirdTry(address):
    finalurl = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    try:
        response = requests.get(finalurl).json()
        return (response[0]["lat"],response[0]["lon"])
    except:
        return (None,None)

def tryAgain(address):
    url = "http://api.positionstack.com/v1/forward?access_key=2733691e1a178352d5f8c5857902c83f"
    raw_address = urllib.parse.quote(address)
    final_url = url+"&query="+raw_address
    try:
        add = requests.get(final_url).json()
        return (add["data"][0]["latitude"],add["data"][0]["longitude"])
    except:
        return thirdTry(address)


def getLatLong(address):
    data = getFromAddress(address)
    if(data[0]==None):
        return tryAgain(address)
    else:
        return (data[0],data[1])

def getDistance(lat1,lon1,lat2,lon2):
    comb1 = (lat1,lon1)
    comb2 = (lat2,lon2)
    dist = geodesic(comb1,comb2).km
    return dist


def getHospitalData(lat1,lon1,radius):
    HospitalData = pd.read_csv("Datasets/Hospital_data.csv")
    HospitalData = HospitalData[HospitalData["Hospital overall rating"]!= "Not Available"]
    Dist = []
    for x in range(len(HospitalData)):
        tempData = HospitalData.iloc[x,:]
        tempLat = tempData["Latitude"]
        tempLon = tempData["Longitude"]
        tempDist = getDistance(lat1,lon1,tempLat,tempLon)
        Dist.append(tempDist)
    HospitalData["Distance"] = Dist
    HospitalData = HospitalData[HospitalData["Distance"] <= radius]
    return HospitalData

def createGraph(address,radius,count):
    latLon = getLatLong(address)
    data = getHospitalData(latLon[0],latLon[1],float(radius)) 
    data = pd.DataFrame(data)
    color_discrete = {"1":'red','2':'orange','3':"yellow",'4':'chartreuse','5':'green'}
    color_scale = [(0,'red'),(1,'green')]
    fig = px.scatter_mapbox(data,lat = "Latitude",
                            lon = "Longitude",hover_name = 'Facility Name',
                        hover_data = ["Address","City","State","ZIP Code","Latitude","Longitude","Phone Number","Hospital overall rating","Emergency Services","Hospital Type","Hospital Ownership","Distance"],
                        color = "Hospital overall rating",color_discrete_map = color_discrete,
                            zoom = 8,
                            height = 400,
                            width = 600
                        )
    fig.add_trace(go.Scattermapbox(
        lat=[float(latLon[0])],
        lon=[float(latLon[1])],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text = ["Your Location "+address]
    ))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    with Path("static/map/map.html").open("w") as f:
        f.write(fig.to_html())
    
    data = data.sort_values(by = ["Hospital overall rating","Distance"],ascending=[False,True])
    data = data[(data["Hospital Type"]=="Acute Care Hospitals") | (data["Hospital Type"]=="Critical Access Hospitals")]
    data = data.reset_index()
    data = data[features]
    return data