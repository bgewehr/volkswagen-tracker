import datetime

from influxdb import InfluxDBClient

from environment import get_database_host, get_database_port, get_database_user, get_database_pass


def add_entry(json_info, emanager_info_json):
    time = datetime.datetime.now()
    # Create the json containing the relevant data
    json_body = [
        {
            "measurement": "mileage",
            "time": time,
            "fields": {
                "mileage_value": json_info['vehicleDetails']['distanceCovered']
            }
        },
        {
            "measurement": "range",
            "time": time,
            "fields": {
                "current_range": json_info['vehicleDetails']['range']
            }
        },
                {
            "measurement": "charging",
            "time": time,
            "fields": {
                "chargingState": '1' if emanager_info_json['EManager']['rbc']['status']['chargingState'] == 'ON' else '0',
                "batteryPercentage": emanager_info_json['EManager']['rbc']['status']['batteryPercentage'],
            }
        }
    ]
    
    # Connect to the database
    client = InfluxDBClient(get_database_host(),
                            get_database_port(),
                            get_database_user(),
                            get_database_pass(),
                            'volkswagen')

    client.create_database('volkswagen')

    # Write the data to the database
    client.write_points(json_body)
