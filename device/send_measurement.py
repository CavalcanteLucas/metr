import requests

endpoint = 'http://localhost:8000/api/measurements/'

data = {
   "data":[
      {
         "value":"2020-06-26T06:49:00.000000",
         "tariff":0,
         "subunit":0,
         "dimension":"Time Point (time & date)",
         "storagenr":0
      },
      {
         "value":29690,
         "tariff":0,
         "subunit":0,
         "dimension":"Energy (kWh)",
         "storagenr":0
      },
      {
         "value":"2019-09-30T00:00:00.000000",
         "tariff":0,
         "subunit":0,
         "dimension":"Time Point (date)",
         "storagenr":1
      },
      {
         "value":16274,
         "tariff":0,
         "subunit":0,
         "dimension":"Energy (kWh)",
         "storagenr":1
      }
   ],
   "device":{
      "type":4,
      "status":0,
      "identnr":83251076,
      "version":0,
      "accessnr":156,
      "manufacturer":5317
   }
}

get_response = requests.post(
    endpoint,
    json=data,
)

print(get_response.text)