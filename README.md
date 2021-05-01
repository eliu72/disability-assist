# Disability-Assistance Airport API ✈️

## Accessing the API
Visit https://disability-assist.herokuapp.com/ to access the API.
Currently, the API only supports the map for the Hartsfield-Jackson Atlanta Intl Airport (ATL) Concourse C.

## Path-finding API Requests 🗺️
https://disability-assist.herokuapp.com/api/path?lat=33.64307&lon=-84.43250&airport=ATL&map=C&destID=C33

### API Endpoint
/api/path

### Query Parameters (Input):
- **lat:** user's current latitude
- **lon:** user's current longitude
- **airport:** airport code [hard-coded at the moment]
- **map:** map id [hard-coded at the moment]
- **destID:** id of the destination within map [hard-coded at the moment]

### Output:
The API returns a JSON of the directions from the user's current location to the destination. The JSON is formatted as a list of "legs". Each "leg" of the route gives the distance and direction the user needs to travel.

## Map Places API Requests 📍
https://disability-assist.herokuapp.com/api/places?airport=ATL&map=C

### API Endpoint
/api/places

### Query Parameters (Input):
- **airport:** airport code [hard-coded at the moment]
- **map:** map id [hard-coded at the moment]

### Output:
The API returns a JSON of the list of places on the selected map with its corresponding integer label.