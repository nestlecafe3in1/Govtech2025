class Q1Constants:
    restaurant_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    country_code_file = "Country-Code.xlsx"
    output_file_path = "output/restaurants.csv"
    normalize_record_path = "restaurants"
    left_join_key = 'restaurant.location.country_id'
    right_join_key = 'Country Code'
    columns_to_rename = {
        'restaurant.R.res_id': 'Restaurant Id',
        'restaurant.name': 'Restaurant Name',
        'restaurant.location.city': 'City',
        'restaurant.user_rating.votes': 'User Rating Votes',
        'restaurant.user_rating.aggregate_rating': 'User Aggregate Rating',
        'restaurant.cuisines': 'Cuisines'
        }
    column_convert = "restaurant.user_rating.aggregate_rating"
    column_selection = [
        'Restaurant Id', 
        'Restaurant Name', 
        'Country', 
        'City', 
        'User Rating Votes', 
        'User Aggregate Rating', 
        'Cuisines'
        ]
    
class Q2Constants:
    output_file_path = "output/restaurant_events.csv"
    event_column_to_unpack = 'restaurant.zomato_events'
    column_start_date = 'event.start_date'
    column_end_date = 'event.end_date'
    specified_month = 4
    specified_year = 2019
    photos_column_to_unpack = "event.photos"
    column_selection = [
        "event.event_id", "Restaurant Id", 
        "Restaurant Name", "restaurant.photos_url",
        "event.title", "event.start_date", 
        "event.end_date"
        ]
    columns_to_rename = {
        "event.event_id": "Event Id", 
        "restaurant.photos_url": "Photo URL",
        "event.title": "Event Title", 
        "event.start_date": "Event Start Date",
        "event.end_date": "Event End Date"
        }   

class Q3Constants:  
    pass