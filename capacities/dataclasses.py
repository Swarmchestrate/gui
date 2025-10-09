from dataclasses import dataclass


@dataclass
class GpsLocation:
    latitude: float | None
    longitude: float | None
