from enum import StrEnum


class PostGisTableNames(StrEnum):
    SPATIAL_REF_SYS = "spatial_ref_sys"
    GEOGRAPHY_COLUMNS = "geography_columns"
    GEOMETRY_COLUMNS = "geometry_columns"


class TableNames(StrEnum):
    APPLICATION = "application"
    APPLICATION_MICROSERVICE = "application_microservice"
    APPLICATION_NEW = "application_new"
    CAPACITY = "capacity"
    CAPACITY_NEW = "capacity_new"
    COLUMN_METADATA = "column_metadata"