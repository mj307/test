# import pandas as pd
# import re
# import nltk
# from nltk.tokenize import word_tokenize
# from geopy.geocoders import Nominatim
# import folium
# from folium.plugins import HeatMap
# import plotly.express as px

# # Load the dataset from Task 2
# df = pd.read_csv("classified_mental_health_posts.csv")

# # Initialize geolocator
# geolocator = Nominatim(user_agent="crisis_geolocation")

# # Function to extract location (based on simple NLP for place names in the text)
# def extract_location(text):
#     # List of common city names or phrases that might indicate a location
#     location_keywords = [
#         "new york", "los angeles", "chicago", "houston", "phoenix", "philadelphia", "san antonio",
#         "san diego", "dallas", "austin", "seattle", "boston", "miami", "denver", "portland", "atlanta",
#         "london", "paris", "sydney", "melbourne", "toronto", "vancouver", "australia", "california"
#     ]
    
#     # Check if any location keyword appears in the content
#     for loc in location_keywords:
#         if loc.lower() in text.lower():
#             return loc
#     return None

# # Apply location extraction to the content
# df['Location'] = df['Content'].apply(extract_location)

# # Geocode the location and get latitude/longitude
# def geocode_location(location):
#     if location is not None:
#         try:
#             # Use geopy to convert the location into lat/lon
#             location_obj = geolocator.geocode(location)
#             if location_obj:
#                 return location_obj.latitude, location_obj.longitude
#         except Exception as e:
#             print(f"Error geocoding {location}: {e}")
#     return None, None

# # Apply geocoding function to the Location column
# df['Latitude'], df['Longitude'] = zip(*df['Location'].apply(geocode_location))

# # Drop rows without valid latitude/longitude
# df = df.dropna(subset=['Latitude', 'Longitude'])

# # Create a map using Folium
# def create_heatmap(dataframe):
#     # Create a folium map centered around the USA
#     m = folium.Map(location=[37.0902, -95.7129], zoom_start=5)
    
#     # Prepare the data for the heatmap (latitude, longitude)
#     heat_data = [[row['Latitude'], row['Longitude']] for index, row in dataframe.iterrows()]
    
#     # Add the heatmap layer
#     HeatMap(heat_data).add_to(m)
    
#     # Save the map to an HTML file
#     m.save("crisis_heatmap.html")

# # Create and display heatmap
# create_heatmap(df)

# # Plotting the top 5 locations with the most crisis discussions
# top_locations = df['Location'].value_counts().head(5)

# # Plot with Plotly
# fig = px.bar(top_locations, x=top_locations.index, y=top_locations.values, labels={'x': 'Location', 'y': 'Frequency'},
#              title="Top 5 Locations with the Highest Crisis Discussions")
# fig.show()

#### SECOND PARTT


# import pandas as pd
# import folium
# from folium.plugins import HeatMap
# from geopy.geocoders import Nominatim
# import plotly.express as px

# # Load the dataset from Task 2
# df = pd.read_csv("classified_mental_health_posts.csv")

# # Initialize geolocator
# geolocator = Nominatim(user_agent="crisis_geolocation")

# # Function to geocode the location (i.e., cities from the random 'City' column)
# def geocode_location(location):
#     if location is not None:
#         try:
#             # Use geopy to convert the location into lat/lon
#             location_obj = geolocator.geocode(location)
#             if location_obj:
#                 return location_obj.latitude, location_obj.longitude
#         except Exception as e:
#             print(f"Error geocoding {location}: {e}")
#     return None, None

# # Apply geocoding function to the 'City' column
# df['Latitude'], df['Longitude'] = zip(*df['City'].apply(geocode_location))

# # Drop rows without valid latitude/longitude
# df = df.dropna(subset=['Latitude', 'Longitude'])

# # Create a heatmap using Folium
# def create_heatmap(dataframe):
#     # Create a folium map centered around the USA
#     m = folium.Map(location=[37.0902, -95.7129], zoom_start=5)
    
#     # Prepare the data for the heatmap (latitude, longitude)
#     heat_data = [[row['Latitude'], row['Longitude']] for index, row in dataframe.iterrows()]
    
#     # Add the heatmap layer
#     HeatMap(heat_data).add_to(m)
    
#     # Save the map to an HTML file
#     m.save("crisis_heatmap.html")

# # Create and display the heatmap
# create_heatmap(df)

# # Plotting the top 5 locations with the most crisis discussions
# top_locations = df['City'].value_counts().head(5)

# # Plot with Plotly
# fig = px.bar(top_locations, x=top_locations.index, y=top_locations.values, labels={'x': 'City', 'y': 'Frequency'},
#              title="Top 5 Cities with the Highest Crisis Discussions")
# fig.show()
import pandas as pd
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import plotly.express as px
import time
import webbrowser
import os

# Load the dataset
df = pd.read_csv("classified_mental_health_posts.csv")

# Initialize geolocator with longer timeout
geolocator = Nominatim(user_agent="crisis_geolocation", timeout=10)

# Cache for already geocoded cities
geo_cache = {}

# Function to geocode with delay and caching
def geocode_location(location):
    if pd.isna(location):
        return None, None
    if location in geo_cache:
        return geo_cache[location]
    try:
        location_obj = geolocator.geocode(location)
        if location_obj:
            lat_lon = (location_obj.latitude, location_obj.longitude)
            geo_cache[location] = lat_lon
            time.sleep(1)  # Respect rate limits
            return lat_lon
    except GeocoderTimedOut:
        print(f"Timeout geocoding {location}, retrying...")
        return geocode_location(location)  # Retry once
    except Exception as e:
        print(f"Error geocoding {location}: {e}")
    return None, None

# Apply geocoding
df['Latitude'], df['Longitude'] = zip(*df['City'].apply(geocode_location))

# Drop rows with missing geodata
df = df.dropna(subset=['Latitude', 'Longitude'])

# Create Heatmap
def create_heatmap(dataframe):
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=5)
    heat_data = [[row['Latitude'], row['Longitude']] for _, row in dataframe.iterrows()]
    HeatMap(heat_data).add_to(m)
    m.save("crisis_heatmap.html")
    webbrowser.open("file://" + os.path.realpath("crisis_heatmap.html"))

create_heatmap(df)

# Top 5 cities
top_locations = df['City'].value_counts().head(5)
fig = px.bar(top_locations, x=top_locations.index, y=top_locations.values,
             labels={'x': 'City', 'y': 'Frequency'},
             title="Top 5 Cities with the Highest Crisis Discussions")
fig.show()
