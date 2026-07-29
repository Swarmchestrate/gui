from enum import StrEnum


class PostGisTableNames(StrEnum):
    SPATIAL_REF_SYS = "spatial_ref_sys"
    GEOGRAPHY_COLUMNS = "geography_columns"
    GEOMETRY_COLUMNS = "geometry_columns"


class TableNames(StrEnum):
    APPLICATION = "application"
    APPLICATION_COLOCATE = "application_colocate"
    APPLICATION_ENVIRONMENT_VAR = "application_environment_var"
    APPLICATION_MICROSERVICE = "application_microservice"
    APPLICATION_NEW = "application_new"
    APPLICATION_NODE_FILTER = "application_node_filter"
    APPLICATION_PROPERTY = "application_property"
    APPLICATION_SECURITY_RULE = "application_security_rule"
    CAPACITY = "capacity"
    CAPACITY_INSTANCE_TYPE = "capacity_instance_type"
    CAPACITY_NEW = "capacity_new"
    CAPACITY_PORT_RULE = "capacity_port_rule"
    CAPACITY_RESOURCE_QUOTA = "capacity_resource_quota"
    COLUMN_METADATA = "column_metadata"
    LOCALITY = "locality"