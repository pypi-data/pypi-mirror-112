# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = metadata_change_event_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class AspectType(Enum):
    DASHBOARD_INFO = "DASHBOARD_INFO"
    DASHBOARD_UPSTREAM = "DASHBOARD_UPSTREAM"
    DATASET_COMMENT = "DATASET_COMMENT"
    DATASET_DOCUMENTATION = "DATASET_DOCUMENTATION"
    DATASET_DOWNSTREAM = "DATASET_DOWNSTREAM"
    DATASET_SCHEMA = "DATASET_SCHEMA"
    DATASET_STATISTICS = "DATASET_STATISTICS"
    DATASET_UPSTREAM = "DATASET_UPSTREAM"
    GROUP_INFO = "GROUP_INFO"
    KNOWLEDGE_CARD_INFO = "KNOWLEDGE_CARD_INFO"
    OWNERSHIP = "OWNERSHIP"
    PERSON_EDITABLE_INFO = "PERSON_EDITABLE_INFO"
    PERSON_ORGANIZATION = "PERSON_ORGANIZATION"
    PERSON_PROPERTIES = "PERSON_PROPERTIES"
    PERSON_SLACK_PROFILE = "PERSON_SLACK_PROFILE"
    PROPERTIES = "PROPERTIES"
    SUPPORT_INFO = "SUPPORT_INFO"


class ChartType(Enum):
    AREA = "AREA"
    BAR = "BAR"
    BOX_PLOT = "BOX_PLOT"
    COLUMN = "COLUMN"
    DONUT = "DONUT"
    FUNNEL = "FUNNEL"
    LINE = "LINE"
    MAP = "MAP"
    OTHER = "OTHER"
    PIE = "PIE"
    SCATTER = "SCATTER"
    TABLE = "TABLE"
    TEXT = "TEXT"
    TIMELINE = "TIMELINE"
    UNKNOWN = "UNKNOWN"
    WATERFALL = "WATERFALL"


@dataclass
class Chart:
    chart_type: Optional[ChartType] = None
    title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Chart':
        assert isinstance(obj, dict)
        chart_type = from_union([ChartType, from_none], obj.get("chartType"))
        title = from_union([from_str, from_none], obj.get("title"))
        return Chart(chart_type, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["chartType"] = from_union([lambda x: to_enum(ChartType, x), from_none], self.chart_type)
        result["title"] = from_union([from_str, from_none], self.title)
        return result


@dataclass
class ObjectID:
    """A class representation of the BSON ObjectId type."""
    """The generation time of this ObjectId instance"""
    generation_time: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ObjectID':
        assert isinstance(obj, dict)
        generation_time = from_union([from_float, from_none], obj.get("generationTime"))
        return ObjectID(generation_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["generationTime"] = from_union([to_float, from_none], self.generation_time)
        return result


@dataclass
class DashboardInfo:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    charts: Optional[List[Chart]] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    dashboard_info_id: Optional[str] = None
    latest: Optional[bool] = None
    title: Optional[str] = None
    url: Optional[str] = None
    view_count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DashboardInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        charts = from_union([lambda x: from_list(Chart.from_dict, x), from_none], obj.get("charts"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dashboard_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        title = from_union([from_str, from_none], obj.get("title"))
        url = from_union([from_str, from_none], obj.get("url"))
        view_count = from_union([from_float, from_none], obj.get("viewCount"))
        return DashboardInfo(id, aspect_type, charts, created_at, description, entity_id, dashboard_info_id, latest, title, url, view_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["charts"] = from_union([lambda x: from_list(lambda x: to_class(Chart, x), x), from_none], self.charts)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dashboard_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["title"] = from_union([from_str, from_none], self.title)
        result["url"] = from_union([from_str, from_none], self.url)
        result["viewCount"] = from_union([to_float, from_none], self.view_count)
        return result


class EntityType(Enum):
    DASHBOARD = "DASHBOARD"
    DATASET = "DATASET"
    GROUP = "GROUP"
    KNOWLEDGE_CARD = "KNOWLEDGE_CARD"
    PERSON = "PERSON"
    PROJECT = "PROJECT"


class DashboardPlatform(Enum):
    LOOKER = "LOOKER"
    UNKNOWN = "UNKNOWN"


@dataclass
class DashboardLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    dashboard_id: Optional[str] = None
    platform: Optional[DashboardPlatform] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DashboardLogicalID':
        assert isinstance(obj, dict)
        dashboard_id = from_union([from_str, from_none], obj.get("dashboardId"))
        platform = from_union([DashboardPlatform, from_none], obj.get("platform"))
        return DashboardLogicalID(dashboard_id, platform)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dashboardId"] = from_union([from_str, from_none], self.dashboard_id)
        result["platform"] = from_union([lambda x: to_enum(DashboardPlatform, x), from_none], self.platform)
        return result


class DataPlatform(Enum):
    DOCUMENTDB = "DOCUMENTDB"
    DYNAMODB = "DYNAMODB"
    ELASTICSEARCH = "ELASTICSEARCH"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    RDS = "RDS"
    REDIS = "REDIS"
    REDSHIFT = "REDSHIFT"
    S3 = "S3"
    SNOWFLAKE = "SNOWFLAKE"
    UNKNOWN = "UNKNOWN"


@dataclass
class DatasetLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    name: Optional[str] = None
    platform: Optional[DataPlatform] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetLogicalID':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        platform = from_union([DataPlatform, from_none], obj.get("platform"))
        return DatasetLogicalID(name, platform)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["platform"] = from_union([lambda x: to_enum(DataPlatform, x), from_none], self.platform)
        return result


@dataclass
class DashboardUpstream:
    """DashboardUpstream captures upstream lineages from data sources to this dashboard"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    dashboard_upstream_id: Optional[str] = None
    latest: Optional[bool] = None
    source_datasets: Optional[List[str]] = None
    sources: Optional[List[DatasetLogicalID]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DashboardUpstream':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dashboard_upstream_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        sources = from_union([lambda x: from_list(DatasetLogicalID.from_dict, x), from_none], obj.get("sources"))
        return DashboardUpstream(id, aspect_type, created_at, entity_id, dashboard_upstream_id, latest, source_datasets, sources)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dashboard_upstream_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["sources"] = from_union([lambda x: from_list(lambda x: to_class(DatasetLogicalID, x), x), from_none], self.sources)
        return result


@dataclass
class Dashboard:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    dashboard_created_at: Optional[datetime] = None
    dashboard_info: Optional[DashboardInfo] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    dashboard_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[DashboardLogicalID] = None
    """DashboardUpstream captures upstream lineages from data sources to this dashboard"""
    upstream: Optional[DashboardUpstream] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dashboard':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        dashboard_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dashboard_info = from_union([DashboardInfo.from_dict, from_none], obj.get("dashboardInfo"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        dashboard_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([DashboardLogicalID.from_dict, from_none], obj.get("logicalId"))
        upstream = from_union([DashboardUpstream.from_dict, from_none], obj.get("upstream"))
        return Dashboard(created_at, id, dashboard_created_at, dashboard_info, deleted_at, entity_type, dashboard_id, last_modified_at, logical_id, upstream)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.dashboard_created_at)
        result["dashboardInfo"] = from_union([lambda x: to_class(DashboardInfo, x), from_none], self.dashboard_info)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.dashboard_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(DashboardLogicalID, x), from_none], self.logical_id)
        result["upstream"] = from_union([lambda x: to_class(DashboardUpstream, x), from_none], self.upstream)
        return result


@dataclass
class AuditStamp:
    actor: Optional[str] = None
    time: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditStamp':
        assert isinstance(obj, dict)
        actor = from_union([from_str, from_none], obj.get("actor"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        return AuditStamp(actor, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["actor"] = from_union([from_str, from_none], self.actor)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        return result


@dataclass
class DatasetComment:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    content: Optional[str] = None
    created: Optional[AuditStamp] = None
    created_at: Optional[datetime] = None
    deleted: Optional[AuditStamp] = None
    entity_id: Optional[str] = None
    field: Optional[str] = None
    dataset_comment_id: Optional[str] = None
    latest: Optional[bool] = None
    parent: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetComment':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        content = from_union([from_str, from_none], obj.get("content"))
        created = from_union([AuditStamp.from_dict, from_none], obj.get("created"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted = from_union([AuditStamp.from_dict, from_none], obj.get("deleted"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field = from_union([from_str, from_none], obj.get("field"))
        dataset_comment_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        parent = from_union([from_str, from_none], obj.get("parent"))
        return DatasetComment(id, aspect_type, content, created, created_at, deleted, entity_id, field, dataset_comment_id, latest, parent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["content"] = from_union([from_str, from_none], self.content)
        result["created"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.created)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deleted"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.deleted)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["field"] = from_union([from_str, from_none], self.field)
        result["id"] = from_union([from_str, from_none], self.dataset_comment_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["parent"] = from_union([from_str, from_none], self.parent)
        return result


@dataclass
class FieldDocumentation:
    documentation: Optional[str] = None
    field_path: Optional[str] = None
    tests: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldDocumentation':
        assert isinstance(obj, dict)
        documentation = from_union([from_str, from_none], obj.get("documentation"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        tests = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tests"))
        return FieldDocumentation(documentation, field_path, tests)

    def to_dict(self) -> dict:
        result: dict = {}
        result["documentation"] = from_union([from_str, from_none], self.documentation)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["tests"] = from_union([lambda x: from_list(from_str, x), from_none], self.tests)
        return result


@dataclass
class DatasetDocumentation:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    dataset_documentations: Optional[List[str]] = None
    entity_id: Optional[str] = None
    field_documentations: Optional[List[FieldDocumentation]] = None
    dataset_documentation_id: Optional[str] = None
    latest: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetDocumentation':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dataset_documentations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("datasetDocumentations"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field_documentations = from_union([lambda x: from_list(FieldDocumentation.from_dict, x), from_none], obj.get("fieldDocumentations"))
        dataset_documentation_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        return DatasetDocumentation(id, aspect_type, created_at, dataset_documentations, entity_id, field_documentations, dataset_documentation_id, latest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["datasetDocumentations"] = from_union([lambda x: from_list(from_str, x), from_none], self.dataset_documentations)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fieldDocumentations"] = from_union([lambda x: from_list(lambda x: to_class(FieldDocumentation, x), x), from_none], self.field_documentations)
        result["id"] = from_union([from_str, from_none], self.dataset_documentation_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        return result


@dataclass
class DatasetDownstream:
    """DatasetDownstream captures downstream lineages from this dataset"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    dashboards: Optional[List[DashboardLogicalID]] = None
    dependent_dashboards: Optional[List[str]] = None
    dependent_datasets: Optional[List[str]] = None
    destinations: Optional[List[DatasetLogicalID]] = None
    entity_id: Optional[str] = None
    dataset_downstream_id: Optional[str] = None
    latest: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetDownstream':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dashboards = from_union([lambda x: from_list(DashboardLogicalID.from_dict, x), from_none], obj.get("dashboards"))
        dependent_dashboards = from_union([lambda x: from_list(from_str, x), from_none], obj.get("dependentDashboards"))
        dependent_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("dependentDatasets"))
        destinations = from_union([lambda x: from_list(DatasetLogicalID.from_dict, x), from_none], obj.get("destinations"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dataset_downstream_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        return DatasetDownstream(id, aspect_type, created_at, dashboards, dependent_dashboards, dependent_datasets, destinations, entity_id, dataset_downstream_id, latest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["dashboards"] = from_union([lambda x: from_list(lambda x: to_class(DashboardLogicalID, x), x), from_none], self.dashboards)
        result["dependentDashboards"] = from_union([lambda x: from_list(from_str, x), from_none], self.dependent_dashboards)
        result["dependentDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.dependent_datasets)
        result["destinations"] = from_union([lambda x: from_list(lambda x: to_class(DatasetLogicalID, x), x), from_none], self.destinations)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dataset_downstream_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        return result


@dataclass
class GroupID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    group_name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GroupID':
        assert isinstance(obj, dict)
        group_name = from_union([from_str, from_none], obj.get("groupName"))
        return GroupID(group_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["groupName"] = from_union([from_str, from_none], self.group_name)
        return result


@dataclass
class GroupOwner:
    group: Optional[GroupID] = None
    role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GroupOwner':
        assert isinstance(obj, dict)
        group = from_union([GroupID.from_dict, from_none], obj.get("group"))
        role = from_union([from_str, from_none], obj.get("role"))
        return GroupOwner(group, role)

    def to_dict(self) -> dict:
        result: dict = {}
        result["group"] = from_union([lambda x: to_class(GroupID, x), from_none], self.group)
        result["role"] = from_union([from_str, from_none], self.role)
        return result


@dataclass
class PersonLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    email: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonLogicalID':
        assert isinstance(obj, dict)
        email = from_union([from_str, from_none], obj.get("email"))
        return PersonLogicalID(email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_union([from_str, from_none], self.email)
        return result


@dataclass
class PersonOwner:
    person: Optional[PersonLogicalID] = None
    role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonOwner':
        assert isinstance(obj, dict)
        person = from_union([PersonLogicalID.from_dict, from_none], obj.get("person"))
        role = from_union([from_str, from_none], obj.get("role"))
        return PersonOwner(person, role)

    def to_dict(self) -> dict:
        result: dict = {}
        result["person"] = from_union([lambda x: to_class(PersonLogicalID, x), from_none], self.person)
        result["role"] = from_union([from_str, from_none], self.role)
        return result


@dataclass
class Ownership:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    groups: Optional[List[GroupOwner]] = None
    ownership_id: Optional[str] = None
    latest: Optional[bool] = None
    people: Optional[List[PersonOwner]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Ownership':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        groups = from_union([lambda x: from_list(GroupOwner.from_dict, x), from_none], obj.get("groups"))
        ownership_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        people = from_union([lambda x: from_list(PersonOwner.from_dict, x), from_none], obj.get("people"))
        return Ownership(id, aspect_type, created_at, entity_id, groups, ownership_id, latest, people)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["groups"] = from_union([lambda x: from_list(lambda x: to_class(GroupOwner, x), x), from_none], self.groups)
        result["id"] = from_union([from_str, from_none], self.ownership_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["people"] = from_union([lambda x: from_list(lambda x: to_class(PersonOwner, x), x), from_none], self.people)
        return result


@dataclass
class Deprecation:
    deprecated_by: Optional[AuditStamp] = None
    reason: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Deprecation':
        assert isinstance(obj, dict)
        deprecated_by = from_union([AuditStamp.from_dict, from_none], obj.get("deprecatedBy"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return Deprecation(deprecated_by, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["deprecatedBy"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.deprecated_by)
        result["reason"] = from_union([from_str, from_none], self.reason)
        return result


@dataclass
class Properties:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    deprecated: Optional[Deprecation] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    properties_id: Optional[str] = None
    latest: Optional[bool] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Properties':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deprecated = from_union([Deprecation.from_dict, from_none], obj.get("deprecated"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        properties_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Properties(id, aspect_type, created_at, deprecated, description, entity_id, properties_id, latest, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deprecated"] = from_union([lambda x: to_class(Deprecation, x), from_none], self.deprecated)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.properties_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


@dataclass
class SchemaField:
    description: Optional[str] = None
    field_path: Optional[str] = None
    native_type: Optional[str] = None
    nullable: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SchemaField':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        native_type = from_union([from_str, from_none], obj.get("nativeType"))
        nullable = from_union([from_bool, from_none], obj.get("nullable"))
        return SchemaField(description, field_path, native_type, nullable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["nativeType"] = from_union([from_str, from_none], self.native_type)
        result["nullable"] = from_union([from_bool, from_none], self.nullable)
        return result


class SchemaType(Enum):
    AVRO = "AVRO"
    DYNAMODB = "DYNAMODB"
    JSON = "JSON"
    ORC = "ORC"
    PARQUET = "PARQUET"
    PROTOBUF = "PROTOBUF"
    SCHEMALESS = "SCHEMALESS"
    SQL = "SQL"


@dataclass
class ForeignKey:
    field_path: Optional[str] = None
    parent: Optional[DatasetLogicalID] = None
    parent_field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ForeignKey':
        assert isinstance(obj, dict)
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        parent = from_union([DatasetLogicalID.from_dict, from_none], obj.get("parent"))
        parent_field = from_union([from_str, from_none], obj.get("parentField"))
        return ForeignKey(field_path, parent, parent_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["parent"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.parent)
        result["parentField"] = from_union([from_str, from_none], self.parent_field)
        return result


class MaterializationType(Enum):
    TABLE = "TABLE"
    VIEW = "VIEW"


@dataclass
class SQLSchema:
    foreign_key: Optional[List[ForeignKey]] = None
    materialization: Optional[MaterializationType] = None
    primary_key: Optional[List[str]] = None
    table_schema: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SQLSchema':
        assert isinstance(obj, dict)
        foreign_key = from_union([lambda x: from_list(ForeignKey.from_dict, x), from_none], obj.get("foreignKey"))
        materialization = from_union([MaterializationType, from_none], obj.get("materialization"))
        primary_key = from_union([lambda x: from_list(from_str, x), from_none], obj.get("primaryKey"))
        table_schema = from_union([from_str, from_none], obj.get("tableSchema"))
        return SQLSchema(foreign_key, materialization, primary_key, table_schema)

    def to_dict(self) -> dict:
        result: dict = {}
        result["foreignKey"] = from_union([lambda x: from_list(lambda x: to_class(ForeignKey, x), x), from_none], self.foreign_key)
        result["materialization"] = from_union([lambda x: to_enum(MaterializationType, x), from_none], self.materialization)
        result["primaryKey"] = from_union([lambda x: from_list(from_str, x), from_none], self.primary_key)
        result["tableSchema"] = from_union([from_str, from_none], self.table_schema)
        return result


@dataclass
class DatasetSchema:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    fields: Optional[List[SchemaField]] = None
    dataset_schema_id: Optional[str] = None
    last_modified: Optional[AuditStamp] = None
    latest: Optional[bool] = None
    schema_type: Optional[SchemaType] = None
    sql_schema: Optional[SQLSchema] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetSchema':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        fields = from_union([lambda x: from_list(SchemaField.from_dict, x), from_none], obj.get("fields"))
        dataset_schema_id = from_union([from_str, from_none], obj.get("id"))
        last_modified = from_union([AuditStamp.from_dict, from_none], obj.get("lastModified"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        schema_type = from_union([SchemaType, from_none], obj.get("schemaType"))
        sql_schema = from_union([SQLSchema.from_dict, from_none], obj.get("sqlSchema"))
        return DatasetSchema(id, aspect_type, created_at, description, entity_id, fields, dataset_schema_id, last_modified, latest, schema_type, sql_schema)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fields"] = from_union([lambda x: from_list(lambda x: to_class(SchemaField, x), x), from_none], self.fields)
        result["id"] = from_union([from_str, from_none], self.dataset_schema_id)
        result["lastModified"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.last_modified)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["schemaType"] = from_union([lambda x: to_enum(SchemaType, x), from_none], self.schema_type)
        result["sqlSchema"] = from_union([lambda x: to_class(SQLSchema, x), from_none], self.sql_schema)
        return result


@dataclass
class DatasetStatistics:
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    data_size: Optional[float] = None
    entity_id: Optional[str] = None
    dataset_statistics_id: Optional[str] = None
    last_updated: Optional[datetime] = None
    latest: Optional[bool] = None
    record_count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetStatistics':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        data_size = from_union([from_float, from_none], obj.get("dataSize"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dataset_statistics_id = from_union([from_str, from_none], obj.get("id"))
        last_updated = from_union([from_datetime, from_none], obj.get("lastUpdated"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        record_count = from_union([from_float, from_none], obj.get("recordCount"))
        return DatasetStatistics(id, aspect_type, created_at, data_size, entity_id, dataset_statistics_id, last_updated, latest, record_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["dataSize"] = from_union([to_float, from_none], self.data_size)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dataset_statistics_id)
        result["lastUpdated"] = from_union([lambda x: x.isoformat(), from_none], self.last_updated)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["recordCount"] = from_union([to_float, from_none], self.record_count)
        return result


@dataclass
class ChannelSlackInfo:
    channel_id: Optional[str] = None
    is_archived: Optional[bool] = None
    name: Optional[str] = None
    purpose: Optional[str] = None
    team_id: Optional[str] = None
    topic: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ChannelSlackInfo':
        assert isinstance(obj, dict)
        channel_id = from_union([from_str, from_none], obj.get("channelId"))
        is_archived = from_union([from_bool, from_none], obj.get("isArchived"))
        name = from_union([from_str, from_none], obj.get("name"))
        purpose = from_union([from_str, from_none], obj.get("purpose"))
        team_id = from_union([from_str, from_none], obj.get("teamId"))
        topic = from_union([from_str, from_none], obj.get("topic"))
        return ChannelSlackInfo(channel_id, is_archived, name, purpose, team_id, topic)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channelId"] = from_union([from_str, from_none], self.channel_id)
        result["isArchived"] = from_union([from_bool, from_none], self.is_archived)
        result["name"] = from_union([from_str, from_none], self.name)
        result["purpose"] = from_union([from_str, from_none], self.purpose)
        result["teamId"] = from_union([from_str, from_none], self.team_id)
        result["topic"] = from_union([from_str, from_none], self.topic)
        return result


@dataclass
class SupportInfo:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    email: Optional[str] = None
    entity_id: Optional[str] = None
    support_info_id: Optional[str] = None
    latest: Optional[bool] = None
    slack_info: Optional[ChannelSlackInfo] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SupportInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        email = from_union([from_str, from_none], obj.get("email"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        support_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        slack_info = from_union([ChannelSlackInfo.from_dict, from_none], obj.get("slackInfo"))
        return SupportInfo(id, aspect_type, created_at, email, entity_id, support_info_id, latest, slack_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["email"] = from_union([from_str, from_none], self.email)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.support_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["slackInfo"] = from_union([lambda x: to_class(ChannelSlackInfo, x), from_none], self.slack_info)
        return result


@dataclass
class DatasetField:
    dataset: Optional[DatasetLogicalID] = None
    field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetField':
        assert isinstance(obj, dict)
        dataset = from_union([DatasetLogicalID.from_dict, from_none], obj.get("dataset"))
        field = from_union([from_str, from_none], obj.get("field"))
        return DatasetField(dataset, field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dataset"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.dataset)
        result["field"] = from_union([from_str, from_none], self.field)
        return result


@dataclass
class FieldMapping:
    destination: Optional[str] = None
    sources: Optional[List[DatasetField]] = None
    transformation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldMapping':
        assert isinstance(obj, dict)
        destination = from_union([from_str, from_none], obj.get("destination"))
        sources = from_union([lambda x: from_list(DatasetField.from_dict, x), from_none], obj.get("sources"))
        transformation = from_union([from_str, from_none], obj.get("transformation"))
        return FieldMapping(destination, sources, transformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["destination"] = from_union([from_str, from_none], self.destination)
        result["sources"] = from_union([lambda x: from_list(lambda x: to_class(DatasetField, x), x), from_none], self.sources)
        result["transformation"] = from_union([from_str, from_none], self.transformation)
        return result


@dataclass
class DatasetUpstream:
    """DatasetUpstream captures upstream lineages from data sources to this dataset"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    executor_url: Optional[str] = None
    field_mappings: Optional[List[FieldMapping]] = None
    dataset_upstream_id: Optional[str] = None
    latest: Optional[bool] = None
    source_code_url: Optional[str] = None
    source_datasets: Optional[List[str]] = None
    sources: Optional[List[DatasetLogicalID]] = None
    transformation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetUpstream':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        executor_url = from_union([from_str, from_none], obj.get("executorUrl"))
        field_mappings = from_union([lambda x: from_list(FieldMapping.from_dict, x), from_none], obj.get("fieldMappings"))
        dataset_upstream_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        source_code_url = from_union([from_str, from_none], obj.get("sourceCodeUrl"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        sources = from_union([lambda x: from_list(DatasetLogicalID.from_dict, x), from_none], obj.get("sources"))
        transformation = from_union([from_str, from_none], obj.get("transformation"))
        return DatasetUpstream(id, aspect_type, created_at, entity_id, executor_url, field_mappings, dataset_upstream_id, latest, source_code_url, source_datasets, sources, transformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["executorUrl"] = from_union([from_str, from_none], self.executor_url)
        result["fieldMappings"] = from_union([lambda x: from_list(lambda x: to_class(FieldMapping, x), x), from_none], self.field_mappings)
        result["id"] = from_union([from_str, from_none], self.dataset_upstream_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["sourceCodeUrl"] = from_union([from_str, from_none], self.source_code_url)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["sources"] = from_union([lambda x: from_list(lambda x: to_class(DatasetLogicalID, x), x), from_none], self.sources)
        result["transformation"] = from_union([from_str, from_none], self.transformation)
        return result


@dataclass
class Dataset:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    comments: Optional[List[DatasetComment]] = None
    dataset_created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    documentation: Optional[DatasetDocumentation] = None
    """DatasetDownstream captures downstream lineages from this dataset"""
    downstream: Optional[DatasetDownstream] = None
    entity_type: Optional[EntityType] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    dataset_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[DatasetLogicalID] = None
    ownership: Optional[Ownership] = None
    properties: Optional[Properties] = None
    schema: Optional[DatasetSchema] = None
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    statistics: Optional[DatasetStatistics] = None
    support_info: Optional[SupportInfo] = None
    """DatasetUpstream captures upstream lineages from data sources to this dataset"""
    upstream: Optional[DatasetUpstream] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        comments = from_union([lambda x: from_list(DatasetComment.from_dict, x), from_none], obj.get("comments"))
        dataset_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        documentation = from_union([DatasetDocumentation.from_dict, from_none], obj.get("documentation"))
        downstream = from_union([DatasetDownstream.from_dict, from_none], obj.get("downstream"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        dataset_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([DatasetLogicalID.from_dict, from_none], obj.get("logicalId"))
        ownership = from_union([Ownership.from_dict, from_none], obj.get("ownership"))
        properties = from_union([Properties.from_dict, from_none], obj.get("properties"))
        schema = from_union([DatasetSchema.from_dict, from_none], obj.get("schema"))
        statistics = from_union([DatasetStatistics.from_dict, from_none], obj.get("statistics"))
        support_info = from_union([SupportInfo.from_dict, from_none], obj.get("supportInfo"))
        upstream = from_union([DatasetUpstream.from_dict, from_none], obj.get("upstream"))
        return Dataset(created_at, id, comments, dataset_created_at, deleted_at, documentation, downstream, entity_type, dataset_id, last_modified_at, logical_id, ownership, properties, schema, statistics, support_info, upstream)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["comments"] = from_union([lambda x: from_list(lambda x: to_class(DatasetComment, x), x), from_none], self.comments)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.dataset_created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["documentation"] = from_union([lambda x: to_class(DatasetDocumentation, x), from_none], self.documentation)
        result["downstream"] = from_union([lambda x: to_class(DatasetDownstream, x), from_none], self.downstream)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.dataset_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.logical_id)
        result["ownership"] = from_union([lambda x: to_class(Ownership, x), from_none], self.ownership)
        result["properties"] = from_union([lambda x: to_class(Properties, x), from_none], self.properties)
        result["schema"] = from_union([lambda x: to_class(DatasetSchema, x), from_none], self.schema)
        result["statistics"] = from_union([lambda x: to_class(DatasetStatistics, x), from_none], self.statistics)
        result["supportInfo"] = from_union([lambda x: to_class(SupportInfo, x), from_none], self.support_info)
        result["upstream"] = from_union([lambda x: to_class(DatasetUpstream, x), from_none], self.upstream)
        return result


@dataclass
class EventHeader:
    app_name: Optional[str] = None
    server: Optional[str] = None
    time: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EventHeader':
        assert isinstance(obj, dict)
        app_name = from_union([from_str, from_none], obj.get("appName"))
        server = from_union([from_str, from_none], obj.get("server"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        return EventHeader(app_name, server, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["appName"] = from_union([from_str, from_none], self.app_name)
        result["server"] = from_union([from_str, from_none], self.server)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        return result


@dataclass
class GroupInfo:
    id: Optional[ObjectID] = None
    admins: Optional[List[PersonLogicalID]] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    email: Optional[str] = None
    entity_id: Optional[str] = None
    group_info_id: Optional[str] = None
    latest: Optional[bool] = None
    members: Optional[List[PersonLogicalID]] = None
    subgroups: Optional[List[GroupID]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GroupInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        admins = from_union([lambda x: from_list(PersonLogicalID.from_dict, x), from_none], obj.get("admins"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        email = from_union([from_str, from_none], obj.get("email"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        group_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        members = from_union([lambda x: from_list(PersonLogicalID.from_dict, x), from_none], obj.get("members"))
        subgroups = from_union([lambda x: from_list(GroupID.from_dict, x), from_none], obj.get("subgroups"))
        return GroupInfo(id, admins, aspect_type, created_at, email, entity_id, group_info_id, latest, members, subgroups)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["admins"] = from_union([lambda x: from_list(lambda x: to_class(PersonLogicalID, x), x), from_none], self.admins)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["email"] = from_union([from_str, from_none], self.email)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.group_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["members"] = from_union([lambda x: from_list(lambda x: to_class(PersonLogicalID, x), x), from_none], self.members)
        result["subgroups"] = from_union([lambda x: from_list(lambda x: to_class(GroupID, x), x), from_none], self.subgroups)
        return result


@dataclass
class Group:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    group_created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    group_info: Optional[GroupInfo] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    group_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[GroupID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Group':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        group_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        group_info = from_union([GroupInfo.from_dict, from_none], obj.get("groupInfo"))
        group_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([GroupID.from_dict, from_none], obj.get("logicalId"))
        return Group(created_at, id, group_created_at, deleted_at, entity_type, group_info, group_id, last_modified_at, logical_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.group_created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["groupInfo"] = from_union([lambda x: to_class(GroupInfo, x), from_none], self.group_info)
        result["id"] = from_union([from_str, from_none], self.group_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(GroupID, x), from_none], self.logical_id)
        return result


@dataclass
class Input:
    created: Optional[datetime] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Input':
        assert isinstance(obj, dict)
        created = from_union([from_datetime, from_none], obj.get("created"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Input(created, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created"] = from_union([lambda x: x.isoformat(), from_none], self.created)
        result["name"] = from_union([from_str, from_none], self.name)
        return result


@dataclass
class PersonEditableInfo:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    person_editable_info_id: Optional[str] = None
    latest: Optional[bool] = None
    skills: Optional[List[Input]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonEditableInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        person_editable_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        skills = from_union([lambda x: from_list(Input.from_dict, x), from_none], obj.get("skills"))
        return PersonEditableInfo(id, aspect_type, created_at, entity_id, person_editable_info_id, latest, skills)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.person_editable_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["skills"] = from_union([lambda x: from_list(lambda x: to_class(Input, x), x), from_none], self.skills)
        return result


@dataclass
class PersonOrganization:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    department: Optional[str] = None
    division: Optional[str] = None
    employee_number: Optional[str] = None
    entity_id: Optional[str] = None
    groups: Optional[List[GroupID]] = None
    person_organization_id: Optional[str] = None
    latest: Optional[bool] = None
    manager: Optional[PersonLogicalID] = None
    manager_id: Optional[str] = None
    manager_name: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonOrganization':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        department = from_union([from_str, from_none], obj.get("department"))
        division = from_union([from_str, from_none], obj.get("division"))
        employee_number = from_union([from_str, from_none], obj.get("employeeNumber"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        groups = from_union([lambda x: from_list(GroupID.from_dict, x), from_none], obj.get("groups"))
        person_organization_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        manager = from_union([PersonLogicalID.from_dict, from_none], obj.get("manager"))
        manager_id = from_union([from_str, from_none], obj.get("managerId"))
        manager_name = from_union([from_str, from_none], obj.get("managerName"))
        name = from_union([from_str, from_none], obj.get("name"))
        title = from_union([from_str, from_none], obj.get("title"))
        return PersonOrganization(id, aspect_type, created_at, department, division, employee_number, entity_id, groups, person_organization_id, latest, manager, manager_id, manager_name, name, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["department"] = from_union([from_str, from_none], self.department)
        result["division"] = from_union([from_str, from_none], self.division)
        result["employeeNumber"] = from_union([from_str, from_none], self.employee_number)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["groups"] = from_union([lambda x: from_list(lambda x: to_class(GroupID, x), x), from_none], self.groups)
        result["id"] = from_union([from_str, from_none], self.person_organization_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["manager"] = from_union([lambda x: to_class(PersonLogicalID, x), from_none], self.manager)
        result["managerId"] = from_union([from_str, from_none], self.manager_id)
        result["managerName"] = from_union([from_str, from_none], self.manager_name)
        result["name"] = from_union([from_str, from_none], self.name)
        result["title"] = from_union([from_str, from_none], self.title)
        return result


@dataclass
class PersonProperties:
    """Object / output type for PersonProperties aspect contains the full aspect fields
    
    Input type for PersonProperties aspect, contains just the common fields across input and
    output
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    display_name: Optional[str] = None
    entity_id: Optional[str] = None
    first_name: Optional[str] = None
    full_name: Optional[str] = None
    person_properties_id: Optional[str] = None
    issuer: Optional[str] = None
    last_login: Optional[str] = None
    last_name: Optional[str] = None
    latest: Optional[bool] = None
    mobile_phone: Optional[str] = None
    occupation: Optional[str] = None
    primary_phone: Optional[str] = None
    provider_name: Optional[str] = None
    status: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonProperties':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        avatar_url = from_union([from_str, from_none], obj.get("avatarUrl"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        first_name = from_union([from_str, from_none], obj.get("firstName"))
        full_name = from_union([from_str, from_none], obj.get("fullName"))
        person_properties_id = from_union([from_str, from_none], obj.get("id"))
        issuer = from_union([from_str, from_none], obj.get("issuer"))
        last_login = from_union([from_str, from_none], obj.get("lastLogin"))
        last_name = from_union([from_str, from_none], obj.get("lastName"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        mobile_phone = from_union([from_str, from_none], obj.get("mobilePhone"))
        occupation = from_union([from_str, from_none], obj.get("occupation"))
        primary_phone = from_union([from_str, from_none], obj.get("primaryPhone"))
        provider_name = from_union([from_str, from_none], obj.get("providerName"))
        status = from_union([from_str, from_none], obj.get("status"))
        return PersonProperties(id, aspect_type, avatar_url, created_at, display_name, entity_id, first_name, full_name, person_properties_id, issuer, last_login, last_name, latest, mobile_phone, occupation, primary_phone, provider_name, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["avatarUrl"] = from_union([from_str, from_none], self.avatar_url)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["displayName"] = from_union([from_str, from_none], self.display_name)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["firstName"] = from_union([from_str, from_none], self.first_name)
        result["fullName"] = from_union([from_str, from_none], self.full_name)
        result["id"] = from_union([from_str, from_none], self.person_properties_id)
        result["issuer"] = from_union([from_str, from_none], self.issuer)
        result["lastLogin"] = from_union([from_str, from_none], self.last_login)
        result["lastName"] = from_union([from_str, from_none], self.last_name)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["mobilePhone"] = from_union([from_str, from_none], self.mobile_phone)
        result["occupation"] = from_union([from_str, from_none], self.occupation)
        result["primaryPhone"] = from_union([from_str, from_none], self.primary_phone)
        result["providerName"] = from_union([from_str, from_none], self.provider_name)
        result["status"] = from_union([from_str, from_none], self.status)
        return result


@dataclass
class PersonSlackProfile:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    deleted: Optional[bool] = None
    entity_id: Optional[str] = None
    person_slack_profile_id: Optional[str] = None
    latest: Optional[bool] = None
    slack_id: Optional[str] = None
    team_id: Optional[str] = None
    username: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonSlackProfile':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted = from_union([from_bool, from_none], obj.get("deleted"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        person_slack_profile_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        slack_id = from_union([from_str, from_none], obj.get("slackId"))
        team_id = from_union([from_str, from_none], obj.get("teamId"))
        username = from_union([from_str, from_none], obj.get("username"))
        return PersonSlackProfile(id, aspect_type, created_at, deleted, entity_id, person_slack_profile_id, latest, slack_id, team_id, username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deleted"] = from_union([from_bool, from_none], self.deleted)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.person_slack_profile_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["slackId"] = from_union([from_str, from_none], self.slack_id)
        result["teamId"] = from_union([from_str, from_none], self.team_id)
        result["username"] = from_union([from_str, from_none], self.username)
        return result


@dataclass
class Person:
    """A person entity represents any individual who is a member of the organization (or beyond)
    and can
    potentially have some relation to the other entities in our application
    """
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    avatar_url: Optional[str] = None
    person_created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    editable_info: Optional[PersonEditableInfo] = None
    entity_type: Optional[EntityType] = None
    first_name: Optional[str] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    person_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    last_name: Optional[str] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[PersonLogicalID] = None
    organization: Optional[PersonOrganization] = None
    password: Optional[str] = None
    properties: Optional[PersonProperties] = None
    slack_profile: Optional[PersonSlackProfile] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Person':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        avatar_url = from_union([from_str, from_none], obj.get("avatarUrl"))
        person_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        editable_info = from_union([PersonEditableInfo.from_dict, from_none], obj.get("editableInfo"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        first_name = from_union([from_str, from_none], obj.get("firstName"))
        person_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        last_name = from_union([from_str, from_none], obj.get("lastName"))
        logical_id = from_union([PersonLogicalID.from_dict, from_none], obj.get("logicalId"))
        organization = from_union([PersonOrganization.from_dict, from_none], obj.get("organization"))
        password = from_union([from_str, from_none], obj.get("password"))
        properties = from_union([PersonProperties.from_dict, from_none], obj.get("properties"))
        slack_profile = from_union([PersonSlackProfile.from_dict, from_none], obj.get("slackProfile"))
        return Person(created_at, id, avatar_url, person_created_at, deleted_at, editable_info, entity_type, first_name, person_id, last_modified_at, last_name, logical_id, organization, password, properties, slack_profile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["avatarUrl"] = from_union([from_str, from_none], self.avatar_url)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.person_created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["editableInfo"] = from_union([lambda x: to_class(PersonEditableInfo, x), from_none], self.editable_info)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["firstName"] = from_union([from_str, from_none], self.first_name)
        result["id"] = from_union([from_str, from_none], self.person_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["lastName"] = from_union([from_str, from_none], self.last_name)
        result["logicalId"] = from_union([lambda x: to_class(PersonLogicalID, x), from_none], self.logical_id)
        result["organization"] = from_union([lambda x: to_class(PersonOrganization, x), from_none], self.organization)
        result["password"] = from_union([from_str, from_none], self.password)
        result["properties"] = from_union([lambda x: to_class(PersonProperties, x), from_none], self.properties)
        result["slackProfile"] = from_union([lambda x: to_class(PersonSlackProfile, x), from_none], self.slack_profile)
        return result


@dataclass
class MetadataChangeEvent:
    dashboard: Optional[Dashboard] = None
    dataset: Optional[Dataset] = None
    event_header: Optional[EventHeader] = None
    group: Optional[Group] = None
    """A person entity represents any individual who is a member of the organization (or beyond)
    and can
    potentially have some relation to the other entities in our application
    """
    person: Optional[Person] = None
    tenant: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MetadataChangeEvent':
        assert isinstance(obj, dict)
        dashboard = from_union([Dashboard.from_dict, from_none], obj.get("dashboard"))
        dataset = from_union([Dataset.from_dict, from_none], obj.get("dataset"))
        event_header = from_union([EventHeader.from_dict, from_none], obj.get("eventHeader"))
        group = from_union([Group.from_dict, from_none], obj.get("group"))
        person = from_union([Person.from_dict, from_none], obj.get("person"))
        tenant = from_union([from_str, from_none], obj.get("tenant"))
        return MetadataChangeEvent(dashboard, dataset, event_header, group, person, tenant)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dashboard"] = from_union([lambda x: to_class(Dashboard, x), from_none], self.dashboard)
        result["dataset"] = from_union([lambda x: to_class(Dataset, x), from_none], self.dataset)
        result["eventHeader"] = from_union([lambda x: to_class(EventHeader, x), from_none], self.event_header)
        result["group"] = from_union([lambda x: to_class(Group, x), from_none], self.group)
        result["person"] = from_union([lambda x: to_class(Person, x), from_none], self.person)
        result["tenant"] = from_union([from_str, from_none], self.tenant)
        return result


def metadata_change_event_from_dict(s: Any) -> MetadataChangeEvent:
    return MetadataChangeEvent.from_dict(s)


def metadata_change_event_to_dict(x: MetadataChangeEvent) -> Any:
    return to_class(MetadataChangeEvent, x)
