from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pandas as pd
import geocoder # type: ignore
import folium # type: ignore

from django.db.models import Q
from django.contrib import messages
from .models import CancerHospitals
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt

from geopy.location import Location # type: ignore
import geopy.distance as gd # type: ignore
from geopy.geocoders import Nominatim # type: ignore
from geopy.extra.rate_limiter import RateLimiter # type: ignore
from geopy.exc import GeocoderTimedOut, GeocoderServiceError # type: ignore



# python manage.py runserver <ipconfig--v4_address>:8000

def Index(request):
    latitude = longitude = 0.0
    state = country = 'none'
    ip = get_ip(request, defalult=True)  # Get the IP address of the user tiles="cartodb positron"
    m = folium.Map(location=[latitude, longitude], zoom_start=2, min_zoom=2, tiles="openstreetmap", 
                   max_zoom=20, max_bounds=True, max_bounds_style=None, scrollWheelZoom=True)
    
    # doctors_obj = Doctors.objects.all()

    if request.method == 'POST':
        
        # Get the latitude and longitude from the form submission
        try:
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
        except (ValueError, TypeError):
            messages.error(request, "Disabled to get location.")
            return redirect('home')
        
        cancer_type = request.POST.get('cancerType')
        location_choosed = request.POST.get('location')
        state, country = get_state_(latitude, longitude)

        rows_contain_cancer_type = CancerHospitals.objects.filter(
                Q(tags__icontains=cancer_type) | Q(region__icontains=state) & Q(country__icontains=country)
            )
        
        df = filtered_objDF(request, rows_contain_cancer_type)

        google_link = '#'
        if (location_choosed != '') and (cancer_type != ''):

            print("Location:", location_choosed, " | Cancer Type:", cancer_type)
            location_choosed = get_coordinates(location_choosed)
            try:
                latitude = location_choosed['latitude']
                longitude = location_choosed['longitude']
                print("coordinates:", latitude,", ", longitude)
                
                state, country = get_state_(latitude, longitude)
                rows_contain_cancer_type = CancerHospitals.objects.filter(
                        Q(tags__icontains=cancer_type) & Q(region__icontains=state) & Q(country__icontains=country)
                )
                
                try:
                    near, dist_km, all_set = get_nearest_hospital(filtered_objDF(request, rows_contain_cancer_type), (latitude, longitude)) # calculate distance between choosed location and hospital 
                    coord = near.iloc[0, 10].replace(' ', '').split(",")
                except:
                    messages.error(request, f"We are currently unable to find any hospitals in {location_choosed}.")
                    return redirect('home')

                folium.Marker(location=[latitude, longitude], icon=folium.Icon(color='blue', icon='person', prefix='fa'), tooltip=f"Your Entered Location</br>{latitude},{longitude}").add_to(m)
                folium.Marker(location=[coord[0], coord[1]], icon=folium.Icon(color='green', icon='hospital', prefix='fa'), tooltip=f"Coordinate: {near.iloc[0, 10]}").add_to(m)
                m.fit_bounds([[latitude, longitude]])

                google_link = track_on_google([latitude, longitude], coord, near.iloc[0, 14])
            except TypeError:
                messages.error(request, f"Unable to get location by this address. Try with another format or check spelling.")
                return redirect('home')
            
        #################################################    
            try:
                note = location_choosed['note']
                messages.error(request, note)
            except KeyError:
                note = None
        #################################################        

        elif cancer_type != '':
            near, dist_km, all_set = get_nearest_hospital(df, (latitude, longitude)) # calculate distance between your current location and hospital
            coord = near.iloc[0, 10].replace(' ', '').split(",")
            
            folium.Marker(location=[latitude, longitude], icon=folium.Icon(color='red', icon='crosshairs', prefix='fa'), tooltip=f"Your Location</br>{latitude},{longitude}").add_to(m)
            folium.Circle(location=[latitude, longitude], radius=1000, color='#21eb57', fill=True, fill_color='#78f098', fill_opacity=0.2).add_to(m)
            folium.Marker(location=[coord[0], coord[1]], icon=folium.Icon(color='green', icon='hospital', prefix='fa'), tooltip=f"Coordinate: {near.iloc[0, 10]}").add_to(m)
            
            m.fit_bounds([[latitude, longitude]])

            google_link = track_on_google([latitude, longitude], coord, near.iloc[0, 14])
            print("Latitude:", latitude)
            print("Longitude:", longitude, "Type:", cancer_type)
        
        # m.save(os.path.join(settings.BASE_DIR, 'templates', 'map.html'))

        return render(request, 'cancer-center/Index.html' , {
                'latitude': latitude,
                'longitude': longitude,
                'map': m._repr_html_(),
                'cdata': rows_contain_cancer_type,
                'g_link': google_link,
                'n_hospital': near.iloc[0, 1], 'n_center': near.iloc[0, 2], 'n_city': near.iloc[0, 3], 'n_region': near.iloc[0, 4], 'n_country': near.iloc[0, 5], 'n_phone': near.iloc[0, 6],
                'n_website': near.iloc[0, 7], 'n_bloodb': near.iloc[0, 8], 'n_path': near.iloc[0, 9], 'n_hp': near.iloc[0, 11], 'n_pc': near.iloc[0, 12], 'n_dc': near.iloc[0, 13],
                'distance': f"We are founded a hospital where average of {round(dist_km, 2)} Km from your location.",
            })

    else: pass
    
    # return HttpResponse(f"Hello, world. You're at the Cancer Care GPS Locator index.</br> {latitude}, {longitude}")
    return render(request, 'cancer-center/Index.html', {
        'latitude': latitude,
        'longitude': longitude, 'map': m._repr_html_(),
        })





def filtered_objDF(request, queryset_object):
    try:
        datalist = [['host_code', 'hospital', 'center', 'city', 'region', 'country', 'phone_tel', 'website', 'blood_bank', 'pathology', 'coords', 'hospital_policy', 'palliative_care', 'diagnosis_center', 'geo_location']]
        for row in queryset_object:
            datalist.append([row.host_code, row.hospital, row.center, row.city, row.region, row.country, row.phone_tel, row.website, row.blood_bank, row.pathology, row.coords, row.hospital_policy, row.palliative_care, row.diagnosis_center, row.geo_location])
        df = pd.DataFrame(datalist[1:], columns=datalist[0])
        return df
    except Exception as e:
        messages.error(request, f"No any Nearby hospitals found. Try with another location or cancer type. </br>Error: {str(e)}")
        return redirect('home')
    

def get_nearest_hospital(df, myloc):

    (dist_km, host_code) = ([], [])
    for code, coord in zip(list(df.host_code), list(df.coords)):
        desigs_coord_ = tuple(coord.replace(' ', '').split(","))
        dist_km.append(gd.geodesic(myloc, desigs_coord_).kilometers)
        host_code.append(code)
    df['distance'] = dist_km
    nearest__hot_code = host_code[dist_km.index(min(dist_km))]  # location of nearest hospital
        # return the nearest hospital and sorted dataframe by distance
    return df.loc[df.host_code.isin([nearest__hot_code])], min(dist_km), df.sort_values(by='distance', ascending=True)  # return the nearest hospital and sorted dataframe by distance
    


@xframe_options_exempt
def map(request):
    return render(request, 'map.html')




# get country and state by coordinate
def get_state_(latitude, longitude):
    geolocator = Nominatim(user_agent="geocoding_app")
    coordinates = f"{latitude}, {longitude}"
    location: Location = geolocator.reverse(coordinates, exactly_one=True)
    
    if location:
        address = location.raw['address']
        country = address.get('country')
        state = address.get('state') or address.get('region')
        
        return state, country
    else:
        return None, None

# worked for development only
def get_ip(request_, defalult = False):
    if defalult: ip = 'me'
    else: ip = request_.META.get('HTTP_X_FORWARDED_FOR') or request_.META.get('REMOTE_ADDR')
    g = geocoder.ip(ip)
    print("IP Address:", g.ip)
    if g.ok:
        return g.ip
    else:
        return "Unknown" 

# get location by coordinate
def location_by_coordinate(coord):
    geocoder = Nominatim(user_agent="CancerCare")
    geocode = RateLimiter(geocoder.geocode, min_delay_seconds = 1, return_value_on_exception = None) 
    location = geocoder.reverse(coord)
    return location.address.replace(" ", "")


# generate google map link for my location to another location
def track_on_google(from_coord, to_coord, to_full_addr):    
    to_full_addr = to_full_addr.replace(" ", "+")
    return f"https://www.google.com/maps/dir/{from_coord[0]},{from_coord[1]}/{to_full_addr}/@{to_coord[0]},{to_coord[1]}"


# TODO: create a hospital search page by hospital name
def search_hospitals(request):

    latitude = longitude = 0.0
    m = folium.Map(location=[latitude, longitude], zoom_start=2, tiles="openstreetmap", max_zoom=20, min_zoom=2, max_bounds=True, max_bounds_style=None, scrollWheelZoom=True)
    
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        print("lat, long: ", latitude, longitude)
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(color='pink', icon='crosshairs', prefix='fa'), tooltip=f"You'r Currently Here</br>{latitude}, {longitude}").add_to(m)

    elif request.method == 'GET':
        hospital = request.GET.get('hospital')
        data_row = None
        try:
            data_row = CancerHospitals.objects.filter(hospital__icontains=hospital)
            
            # TODO: create multiple data row of wiki btn
            
            print("Hospital Name: ", data_row[0].hospital)
            return render(request, 'searchHosp.html', {
                'hospital': data_row, 'map': m._repr_html_()
            })
        except ValueError:
            pass
    
    
    return render(request, 'searchHosp.html', {
        'map': m._repr_html_()
    })


def get_coord_to_ip(ip):
    g = geocoder.ip(ip)
    if g.ok:
        latitude = g.latlng[0]
        longitude = g.latlng[1]
    else:
        latitude = longitude = 0.0
    return latitude, longitude

# def home(request):
#     g = geocoder.ip('me')
#     if g.ok:
#         city = g.city
#         region = g.state
#         country = g.country
#         try:
#             latitude = g.latlng[0]
#             longitude = g.latlng[1]
#         except IndexError:
#             latitude = longitude = "Unknown"
#     else:
#         city = region = country = latitude = longitude = "Unknown"
    
#     return render(request, 'Index.html', {
#             'city': city,
#             'region': region,
#             'country': country,
#             'latitude': latitude,
#             'longitude': longitude
#     })

def get_coordinates(address):
    try:
        # Initialize Nominatim geocoder with a unique user_agent
        geolocator = Nominatim(user_agent="CancerCare_geocoder")
        
        # Try geocoding the address
        location = geolocator.geocode(address, timeout=10)
        
        if location:
            return {
                "address": location.address,
                "latitude": location.latitude,
                "longitude": location.longitude
            }
        else:
            print("Exact address not found, trying a broader search...")
            # Fallback: Try a less specific address (e.g., remove street-level details)
            parts = address.split(", ")
            if len(parts) > 2:
                broader_address = ", ".join(parts[1:])  # Skip street, try city onwards
                # print(f"Trying broader address: {broader_address}")
                location = geolocator.geocode(broader_address, timeout=10)
                if location:
                    return {
                        "address": location.address,
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "note": "Exact address not found, showing coordinates for broader area."
                    }
            return "Address not found. Try a different format or check spelling."

    except GeocoderTimedOut:
        return "Error: Request timed out. Try again later."
    except GeocoderServiceError as e:
        return f"Error: Nominatim service issue - {str(e)}. Try again later."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
