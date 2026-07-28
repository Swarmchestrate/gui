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
    CAPACITY_ENERGY_CONSUMPTION = "capacity_energy_consumption"
    CAPACITY_INSTANCE_TYPE = "capacity_instance_type"
    CAPACITY_NEW = "capacity_new"
    CAPACITY_OPERATING_SYSTEM = "capacity_operating_system"
    CAPACITY_PORT_RULE = "capacity_port_rule"
    CAPACITY_PRICE = "capacity_price"
    CAPACITY_RESOURCE_QUOTA = "capacity_resource_quota"
    COLUMN_METADATA = "column_metadata"
    LOCALITY = "locality"