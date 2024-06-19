import os
import time

from FlightRadar24 import FlightRadar24API
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import Collector
from dotenv import load_dotenv

load_dotenv()

# Seatac Airport (SEA) default location
LAT = float(os.getenv('LAT', 47.4484)) 
LON = float(os.getenv('LON', -122.3086))
BOUNDS = int(os.getenv('BOUNDS', 5000)) # distance in meters
PORT = int(os.getenv('FLIGHT_PORT', 11019))

fr_api = FlightRadar24API()
bounds = fr_api.get_bounds_by_point(LAT, LON, BOUNDS)

class FlightCollector(Collector):
    def collect(self):
        flight_info = InfoMetricFamily('flight', 'Flight Info')

        ground_speed_gauge = GaugeMetricFamily('flight_ground_speed',
                                        'Flight Ground Speed',
                                        labels=['flight_id', 'callsign'])

        vertical_speed_gauge = GaugeMetricFamily('flight_vertical_speed',
                                        'Flight Ground Speed',
                                        labels=['flight_id', 'callsign'])

        altitude_gauge = GaugeMetricFamily('flight_altitude',
                                           'Flight Altitude',
                                        labels=['flight_id', 'callsign'])

        latitude_gauge = GaugeMetricFamily('flight_latitude',
                                           'Flight Latitude',
                                        labels=['flight_id', 'callsign'])

        longitude_gauge = GaugeMetricFamily('flight_longitude',
                                            'Flight Longitude',
                                        labels=['flight_id', 'callsign'])

        heading_gauge = GaugeMetricFamily('flight_heading',
                                          'Flight Heading (degrees)',
                                        labels=['flight_id', 'callsign'])
      
        aircraft_overhead = GaugeMetricFamily('aircraft_overhead',
                                          'Number of aircraft in sky overhead')

        flights = fr_api.get_flights(bounds=bounds)

        aircraft_overhead.add_metric([], len(flights))

        for flight in flights:
            flight_details = fr_api.get_flight_details(flight)
            flight.set_flight_details(flight_details)

            flight_info.add_metric(
                labels=flight.id,
                value={
                    "airline_name": flight.airline_name,
                    "callsign": flight.callsign,
                    "flight_number": flight.number,
                    "flight_id": flight.id,
                    "registration": flight.registration,
                    "aircraft_model": flight.aircraft_model,
                    "aircraft_code": flight.aircraft_code,
                    "origin_airport_name": flight.origin_airport_name,
                    "destination_airport_name": flight.destination_airport_name,
                    "status_text": flight.status_text,
                    "latitude": str(flight.latitude),
                    "longitude": str(flight.longitude)
                },
            )

            ground_speed_gauge.add_metric([flight.id, flight.callsign], flight.ground_speed)
            vertical_speed_gauge.add_metric([flight.id, flight.callsign], flight.vertical_speed)
            altitude_gauge.add_metric([flight.id, flight.callsign], flight.altitude)
            latitude_gauge.add_metric([flight.id, flight.callsign], flight.latitude)
            longitude_gauge.add_metric([flight.id, flight.callsign], flight.longitude)
            heading_gauge.add_metric([flight.id, flight.callsign], flight.heading)

        yield aircraft_overhead
        yield flight_info
        yield ground_speed_gauge
        yield vertical_speed_gauge
        yield altitude_gauge
        yield latitude_gauge
        yield longitude_gauge
        yield heading_gauge


if __name__ == '__main__':
    print(f"Scanning for flights at {LAT}, {LON} with {BOUNDS} meter radius. /metrics on :{PORT}")
    start_http_server(PORT)
    REGISTRY.register(FlightCollector())
    while True:
        time.sleep(1)
