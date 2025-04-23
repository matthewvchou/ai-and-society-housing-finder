import re
import json
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from streeteasy_helper.query_streeteasy import create_possible_areas

def create_zip_to_neighborhood():
    raw_entries = [
        [["kingsbridge,riverdale"],  (10463, 10471)],
        [["baychester,williamsbridge"], (10466, 10469, 10470, 10475)],
        [['fordham,bronx-park'], (10458, 10467, 10468)],
        [['pelham-bay,throgs-neck'], (10461, 10462, 10464, 10465, 10472, 10473)],
        [['crotona-park-east,east-tremont'], (10453, 10457, 10460)],
        [['highbridge,morrisania'], (10451, 10452, 10456)],
        [['hunts-point,mott-haven'], (10454, 10455, 10459, 10474)],
        [['greenpoint'], (11211, 11222)],
        [['downtown-brooklyn,brooklyn-heights,park-slope'], (11201, 11205, 11215, 11217, 11231)],
        [['bedford-stuyvesant,crown-heights'], (11213, 11212, 11216, 11233, 11238)],
        [['east-new-york'], (11207, 11208)],
        [['sunset-park'], (11220, 11232)],
        [['borough-park'], (11204, 11218, 11219, 11230)],
        [['east-flatbush,flatbush'], (11203, 11210, 11225, 11226)],
        [['canarsie,flatlands'], (11234, 11236, 11239)],
        [['bensonhurst,bay-ridge'], (11209, 11214, 11228)],
        [['coney-island,sheepshead-bay'], (11223, 11224, 11229, 11235)],
        [['williamsburg,bushwick'], (11206, 11221, 11237)],
        [['washington-heights,inwood'], (10031, 10032, 10033, 10034, 10040)],
        [['central-harlem,morningside-heights'], (10026, 10027, 10030, 10037, 10039)],
        [['east-harlem'], (10029, 10035)],
        [['upper-west-side'], (10023, 10024, 10025)],
        [['upper-east-side'], (10021, 10028, 10044, 10128)],
        [['chelsea,clinton-hill'], (10001, 10011, 10018, 10019, 10020, 10036)],
        [['gramercy-park,murray-hill'], (10010, 10016, 10017, 10022)],
        [['greenwich-village,soho'], (10012, 10013, 10014)],
        [['lower-east-side'], (10002, 10003, 10009)],
        [['financial-district,tribeca,civic-center'], (10004, 10005, 10006, 10007, 10038, 10280)],
        [['long-island-city,astoria'], (11101, 11102, 11103, 11104, 11105, 11106)],
        [['elmhurst,corona,jackson-heights,woodside'], (11368, 11369, 11370, 11372, 11373, 11377, 11378)],
        [['flushing,clearview'], (11354, 11355, 11356, 11357, 11358, 11359, 11360)],
        [['bayside,little-neck'], (11361, 11362, 11363, 11364)],
        [['ridgewood,forest-hills'], (11374, 11375, 11379, 11385)],
        [['fresh-meadows'], (11365, 11366, 11367)],
        [['ozone-park,woodhaven,howard-beach'], (11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421)],
        [['jamaica'], (11412, 11423, 11432, 11433, 11434, 11435, 11436)],
        [['glen-oaks,floral-park,cambria-heights'], (11004, 11005, 11411, 11413, 11422, 11426, 11427, 11428, 11429)],
        [['rockaway-all'], (11691, 11692, 11693, 11694, 11695, 11697)],
        [['port-richmond'], (10302, 10303, 10310)],
        [['stapleton,saint-george'], (10301, 10304, 10305)],
        [['willowbrook'], (10314,)],
        [['south-beach,tottenville'], (10306, 10307, 10308, 10309, 10312)],
    ]

    zip_to_neighborhood_mapping = {}
    for neighborhoods, zipcodes in raw_entries:
        for zipcode in zipcodes:
            zip_to_neighborhood_mapping[zipcode] = neighborhoods

    return zip_to_neighborhood_mapping

def get_all_neighborhoods_from_listings(listings, zip_to_neighborhood_mapping):
    geolocator = geopy.Nominatim(user_agent="zipcode-mapping")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=3)

    zipcode_url_mapping = {}
    # map zipcode to url w/ geolocator
    for entry in listings:
        location = geolocator.reverse((entry['latitude'], entry['longitude']))
        if 'address' in location.raw.keys():
            if 'postcode' in location.raw['address'].keys():
                zipcode_url_mapping[(int(location.raw['address']['postcode']))] = entry['url']


    neighborhood_url_mapping = {}
    for zipcode, url in zipcode_url_mapping.items():
        possible_neighborhoods = zip_to_neighborhood_mapping.get(zipcode, [])[0].split(',')
        for neighborhood in possible_neighborhoods:
            neighborhood_url_mapping[neighborhood] = url

    return neighborhood_url_mapping
                
