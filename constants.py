class Q1Constants:
    RESTAURANT_URL = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    COUNTRY_CODEFILE = "Country-Code.xlsx"
    OUTPUT_FILE_PATH = "output/restaurants.csv"
    NORMALIZE_RECORD_PATH = "restaurants"
    LEFT_JOIN_KEY = 'restaurant.location.country_id'
    RIGHT_JOIN_KEY = 'Country Code'
    COLUMNS_TO_RENAME = {
        'restaurant.R.res_id': 'Restaurant Id',
        'restaurant.name': 'Restaurant Name',
        'restaurant.location.city': 'City',
        'restaurant.user_rating.votes': 'User Rating Votes',
        'restaurant.user_rating.aggregate_rating': 'User Aggregate Rating',
        'restaurant.cuisines': 'Cuisines'
        }
    COLUMN_CONVERT = "restaurant.user_rating.aggregate_rating"
    COLUMN_SELECTION = [
        'Restaurant Id', 
        'Restaurant Name', 
        'Country', 
        'City', 
        'User Rating Votes', 
        'User Aggregate Rating', 
        'Cuisines'
        ]
    
class Q2Constants:
    OUTPUT_FILE_PATH = "output/restaurant_events.csv"
    EVENT_COLUMN_TO_UNPACK = 'restaurant.zomato_events'
    COLUMN_START_DATE = 'event.start_date'
    COLUMN_END_DATE = 'event.end_date'
    SPECIFIED_MONTH = 4
    SPECIFIED_YEAR = 2019
    PHOTOS_COLUMN_TO_UNPACK = "event.photos"
    COLUMN_SELECTION = [
        "event.event_id", "Restaurant Id", 
        "Restaurant Name", "restaurant.photos_url",
        "event.title", "event.start_date", 
        "event.end_date"
        ]
    COLUMNS_TO_RENAME = {
        "event.event_id": "Event Id", 
        "restaurant.photos_url": "Photo URL",
        "event.title": "Event Title", 
        "event.start_date": "Event Start Date",
        "event.end_date": "Event End Date"
        }   

class Q3Constants: 
    RATINGS_TO_FILTER = [
        'Excellent', 'Very Good', 'Good', 'Average', 'Poor'
        ]
    COLUMN_TO_RENAME = {"restaurant.user_rating.rating_text":"Rating Text"}
    AGGREGATE_RATING_COLUMN = 'User Aggregate Rating'
    RATING_TEXT_COLUMN = "Rating Text"
    AGGREGATES_LIST = ['min', 'max']
    SORT_VARIABLE = 'min'