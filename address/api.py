from collections import defaultdict
from django.utils.encoding import smart_text
from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error
from address.models import City, District


class JsonRpcError(Error):

    def __init__(self, message):
        self.message = message

    @property
    def json_rpc_format(self):
        return {'code': -32000, 'message': smart_text(self.message)}


@jsonrpc_method('get_cities')
def get_cities(request, key):
    cities = City.objects.filter(scope_uuid=key)
    districts = District.objects.filter(city__scope_uuid=key)
    districts_dict = defaultdict(list)
    for district in districts:
        districts_dict[district.city_id].append({
            'district_id': district.id,
            'name': district.name,
            'population': district.population})
    return [{'city_id': city.id,
             'city_name': city.name,
             'lat': city.lat,
             'lon': city.lon,
             'districts': districts_dict.get(city.id, [])} for city in cities]


@jsonrpc_method('create_city')
def create_city(request, key, name, lat, lon):
    try:
        float(lat)
        float(lon)
        coord_error = False
    except:
        coord_error = True
    if not (key or name or coord_error):
        raise JsonRpcError(message='Incorrect data')
    return City.objects.create(scope_uuid=key, name=name, lat=lat, lon=lon).id


@jsonrpc_method('set_city')
def set_city(request, key, city_id, name, lat, lon):
    try:
        float(lat)
        float(lon)
        coord_error = False
    except:
        coord_error = True
    if not (key or name or coord_error):
        raise JsonRpcError(message='Incorrect data')
    city = City.objects.filter(scope_uuid=key, id=city_id).first()
    if not city:
        raise JsonRpcError(message='City not found')
    city.name = name
    city.lat = lat
    city.lon = lon
    city.save()
    return city_id


@jsonrpc_method('delete_city')
def delete_city(request, key, city_id):
    city = City.objects.filter(scope_uuid=key, id=city_id).first()
    if not city:
        raise JsonRpcError(message='City not found')
    city.delete()
    return city_id


@jsonrpc_method('create_district')
def create_district(request, key, city_id, name, population):
    try:
        int(population)
        population_error = False
    except:
        population_error = True
    if not (key or city_id or name or population_error):
        raise JsonRpcError(message='Incorrect data')
    city = City.objects.filter(scope_uuid=key, id=city_id).first()
    if not city:
        raise JsonRpcError(message='City not found')
    return District.objects.create(
        city=city, name=name, population=population).id


@jsonrpc_method('set_district')
def set_district(request, key, district_id, name, population):
    try:
        int(population)
        population_error = False
    except:
        population_error = True
    if not (key or name or population_error):
        raise JsonRpcError(message='Incorrect data')
    district = District.objects.filter(
        city__scope_uuid=key, id=district_id).first()
    if not district:
        raise JsonRpcError(message='District not found')
    district.name = name
    district.population = population
    district.save()
    return district_id


@jsonrpc_method('delete_district')
def delete_district(request, key, district_id):
    district = District.objects.filter(
        city__scope_uuid=key, id=district_id).first()
    if not district:
        raise JsonRpcError(message='District not found')
    district.delete()
    return district_id
