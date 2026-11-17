# Flight-Exporter

Flight-Exporter is a Prometheus exporter for the FlightRadar24 API. Given GPS coordinates and a distance radius for a location, it tracks stats for aircraft that fly overhead.

## Features

- Tracks aircraft within a specified radius of given GPS coordinates.
- Collects data such as flight numbers, aircraft types, altitudes, speeds, departure, and destination airports.
- Exposes metrics in Prometheus format for easy integration with monitoring and alerting systems.
- Provides pre-built Grafana dashboards for visualizing flight data.

## Grafana Visualizations

Pre-built Grafana dashboards include:
- **Flights by Altitude/Speed**: Visualizes the altitude and speed of flights.
- **Heat Map of Flight Paths**: Shows the density and paths of flights over a given area.
- **Active Flights Overhead**: Track the number of active flights overhead by time.
- **Top Destination Airports**: Lists the most frequent destination airports from the tracked flights.

## Deployment

Pre-built Docker containers are available on DockerHub and GitHub Registry:
- DockerHub: [mitchtech/flight-exporter](https://hub.docker.com/r/mitchtech/flight-exporter)
- GitHub Registry: [ghcr.io/mitchtech/flight-exporter](https://ghcr.io/mitchtech/flight-exporter)

### Docker

Run directly with Docker (example using explicit environment variables):
```
docker run -p "10019:10019" --rm \
	--env LAT=47.4484 \
	--env LON=-122.308 \
	--env BOUNDS=15000 \
	--env FLIGHT_PORT=10019 \
	mitchtech/flight-exporter
```
### Docker Compose

Or run using compose (example using environment variable file):
```
  flight-exporter:
    image: mitchtech/flight-exporter
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - 10019:10019
```

### Prometheus Config

Example Prometheus scrape config:
```
scrape_configs:
- job_name: flight-exporter
  scrape_interval: 60s
  scrape_timeout: 60s
  metrics_path: /metrics
  static_configs:
    - targets:
      - localhost:10019
``` 

### Flight Exporter + Prometheus + Grafana

A complete Docker Compose example with all services is also proved in the /example directory. Edit the environment variables, rename the sample to `.env` and start everything with compose.
```
mv .env.example .env
docker compose up
```

## Implementation

- Flight-Exporter is based on the unofficial FlightRadar24 API: [FlightRadarAPI · PyPI](https://pypi.org/project/FlightRadarAPI/).
- Uses the official Python client for Prometheus: [Prometheus Python Client](https://prometheus.io/).
- Implements a 'probe-style' custom collector: [Custom Collectors in Prometheus Python Client](https://prometheus.github.io/client_python/collector/custom/).
	- The exporter does not actively collect flight data; the FlightRadar24 API is queried only when the `/metrics` endpoint is scraped.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to the GitHub repository.

## License

This project is licensed under the Apache 2 License. See the [LICENSE](https://github.com/mitchtech/flight-exporter/blob/main/LICENSE) file for details.