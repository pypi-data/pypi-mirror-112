import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator

from .enums import ActionType, FilterType, LayerType
from .transfer_utils import normalize_data

try:
    from pandas import DataFrame
except ImportError:
    DataFrame = None

# Literal is included in the stdlib as of Python 3.8
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


class CamelCaseBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

        @staticmethod
        def to_camel_case(snake_str: str) -> str:
            """Convert snake_case string to camelCase
            https://stackoverflow.com/a/19053800
            """
            components = snake_str.split('_')
            # We capitalize the first letter of each component except the first one
            # with the 'title' method and join them together.
            return components[0] + ''.join(x.title() for x in components[1:])

        alias_generator = to_camel_case


# TODO: do we expose this class at all?
# class MapOptions(BaseModel):
#     mapUrl: Optional[str]
#     mapUUID: Optional[UUID]
#     appendToId: Optional[str]
#     id: Optional[str]
#     embed: Optional[bool]
#     onLoad: Optional[() => void]
#     onTimelineIntervalChange: Optional[(currentTimeInterval: List[float>) => void]
#     onLayerTimelineTimeChange: Optional[(currentTime: float) => void]
#     appendToDocument: bool
#     width: float
#     height: float

# class MapInstance(BaseModel):
#     iframe: HTMLCanvasElement

FilterValueType = Union[List[float], List[str], bool, Any]


class FilterChangeEvent(CamelCaseBaseModel):
    """Information on filter changes passed to onFilter callbacks

    Kwargs:
        id: Filter ID
        name: Field names the filter applies to
        data_id: Dataset UUID
        prop: Filter property that is changed: 'value', 'name', etc
        type: FilterType
        value: Value of the filter
    """

    id: str
    name: List[str]
    data_id: UUID
    prop: str
    type: FilterType
    value: FilterValueType


class ClickEvent(CamelCaseBaseModel):
    """Information on the object passed to on_click

    Kwargs:
        index: Data row index
        coordinate: Geospatial coordinates [lng, lat]
        x: Mouse position x relative to the viewport
        y: Mouse position y relative to the viewport
        layer_id: The layer id that the picked object belongs to
        data: Picked object in the layer
    """

    index: int
    coordinate: Tuple[float, float]
    x: float
    y: float
    layer_id: Optional[str]
    data: Optional[Dict[str, Any]]


class HoverEvent(CamelCaseBaseModel):
    """Information on the object passed to on_hover

    Kwargs:
        index: Data row index
        coordinate: Geospatial coordinates [lng, lat]
        x: Mouse position x relative to the viewport
        y: Mouse position y relative to the viewport
        layer_id: The layer id that the picked object belongs to
        data: Picked object in the layer
    """

    index: int
    coordinate: Tuple[float, float]
    x: float
    y: float
    layer_id: Optional[str]
    data: Optional[Dict[str, Any]]


OnLoadHandlerType = Optional[Callable[[None], None]]
OnTimelineIntervalChangeHandlerType = Optional[Callable[[List[int]], None]]
OnLayerTimelineTimeChangeHandlerType = Optional[Callable[[int], None]]
OnFilterHandlerType = Optional[Callable[[FilterChangeEvent], None]]
OnHoverHandlerType = Optional[Callable[[HoverEvent], None]]
OnClickHandlerType = Optional[Callable[[ClickEvent], None]]


class MapEventHandlers(CamelCaseBaseModel):
    """Event handlers which can be registered for receiving notifications of certain map events."""

    on_load: OnLoadHandlerType
    on_timeline_interval_change: OnTimelineIntervalChangeHandlerType
    on_layer_timeline_time_change: OnLayerTimelineTimeChangeHandlerType
    on_filter: OnFilterHandlerType
    on_hover: OnHoverHandlerType
    on_click: OnClickHandlerType


class Layer(CamelCaseBaseModel):
    """Layer info returned by `get_layers()`"""

    label: str
    id: str
    is_visible: bool


class ViewState(CamelCaseBaseModel):
    """Map viewport state for use with `set_view_state()`"""

    longitude: float
    latitude: float
    # TODO: From looking at the SDK implementation, this should be Optional?
    zoom: Optional[float] = None


class TimelineInfo(CamelCaseBaseModel):
    """Timeline control state returned by `get_timeline_info()`"""

    data_id: List[UUID]
    domain: List[float]
    is_visible: bool
    enlarged_histogram: List[Any]
    histogram: List[Any]
    value: List[float]
    speed: float
    step: float
    is_animating: bool


class TimeInterval(CamelCaseBaseModel):
    """Time interval for use with `set_timeline_config()`"""

    start_time: float
    end_time: float


class TimelineConfig(CamelCaseBaseModel):
    """Time configuration for use with `set_timeline_config()`"""

    idx: int
    current_time_interval: Optional[TimeInterval]
    is_visible: Optional[bool]
    is_animating: Optional[bool]
    speed: Optional[float]
    timezone: Optional[str]
    time_format: Optional[str]


class LayerTimelineInfo(CamelCaseBaseModel):
    """Layer timeline state returned by `get_layer_timeline_info()`"""

    current_time: float
    default_time_format: str
    domain: List[float]
    duration: float
    is_visible: bool
    is_animating: bool
    speed: float
    time_format: str
    time_steps: Any
    timezone: str


class LayerTimelineConfig(CamelCaseBaseModel):
    """Layer timeline configuration for use with `set_layer_timeline_config()`"""

    current_time: Optional[float]
    is_visible: Optional[bool]
    is_animating: Optional[bool]
    speed: Optional[float]
    timezone: Optional[str]
    time_format: Optional[str]


TilesetType = Literal['vector-tile', 'raster-tile']


class VectorMeta(CamelCaseBaseModel):
    """Vector tileset metadata"""

    data_url: str
    metadata_url: str


class RasterMeta(CamelCaseBaseModel):
    """Raster tileset metadata"""

    data_url: str
    metadata_url: str


class Tileset(CamelCaseBaseModel):
    """Tileset configuration for use with `add_tileset`"""

    name: str
    type: TilesetType
    meta: Union[VectorMeta, RasterMeta]


class LayerConfig(CamelCaseBaseModel):
    """Layer configuration for use with `add_layer` or `add_dataset`.
    `LayerConfig` is part of `LayerSpec`.
    """

    data_id: UUID
    label: Optional[str]
    columns: Dict[str, Any]
    is_visible: Optional[bool]
    vis_config: Optional[Dict[str, Any]]
    color_field: Optional[Dict[str, Any]]
    color_scale: Optional[str]
    color_ui: Optional[Dict[str, Any]] = Field(alias='colorUI')


class LayerSpec(CamelCaseBaseModel):
    """Layer configuration for use with `add_layer` or `add_dataset`"""

    id: str
    type: LayerType
    config: LayerConfig
    visual_channels: Optional[Dict[str, Any]]


class Dataset(CamelCaseBaseModel):
    """Dataset configuration for use with `add_dataset`.
    Kwargs:
        uuid: Unique identifier of the dataset (will be auto-generated when not provided).
        data: (Optional) CSV, JSON, DataFrame or GeoDataFrame data for the dataset.
    """

    uuid: UUID = Field(default_factory=uuid4)
    label: str = 'Untitled'
    data: Optional[Union[str, DataFrame]]

    @validator('data', pre=True, always=True)
    # pylint: disable=no-self-argument
    def set_data_normalized(
        cls, data: Optional[Union[str, DataFrame]]
    ) -> Optional[str]:
        return normalize_data(data) if data is not None else None

    class Config:
        # to prevent "No validator for DataFrame"
        arbitrary_types_allowed = True
        validate_assignment = True


class FilterInfo(CamelCaseBaseModel):
    """Filter settings for use with `set_filter`"""

    id: str
    data_id: Optional[UUID]
    field: str
    value: FilterValueType


class AddDatasetResponse(BaseModel):
    """Response of `add_dataset`calls"""

    status: Literal['ok', 'fail']
    message: Optional[str]


class RemoveDatasetResponse(BaseModel):
    """Response of `remove_dataset`calls"""

    status: Literal['ok', 'fail']
    message: Optional[str]


class Action(CamelCaseBaseModel):
    """Base Action payload class"""

    type: ActionType
    message_id: UUID = Field(default_factory=uuid4)

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        """Custom dict encoding to put keys within `data` key

        Only top level keys should be type, data, and messageId
        """
        # Export by alias by default, but don't change by_alias=False
        if 'by_alias' not in kwargs.keys():
            kwargs['by_alias'] = True

        # Remove None values by default
        if 'exclude_none' not in kwargs.keys():
            kwargs['exclude_none'] = True

        # Use default superclass dict serialization
        d = super().dict(**kwargs)

        # Make sure the data key doesn't exist yet
        assert d.get('data') == None, 'data key already exists'

        d['data'] = {}

        # Keys that should stay at the top level
        top_level_json_keys = ['type', 'messageId', 'data']

        # Set all keys within the data key, but not recursively
        inner_keys = set(d.keys()).difference(top_level_json_keys)
        for key in inner_keys:
            d['data'][key] = d.pop(key)

        return d

    def json(self, **kwargs: Any) -> str:
        """Custom json encoding to put keys within `data` key

        Only top level keys should be type, data, and messageId
        """
        # Export by alias by default, but don't change by_alias=False
        if 'separators' not in kwargs.keys():
            kwargs['separators'] = (',', ':')

        # Export by alias by default, but don't change by_alias=False
        if 'by_alias' not in kwargs.keys():
            kwargs['by_alias'] = True

        # Remove None values by default
        if 'exclude_none' not in kwargs.keys():
            kwargs['exclude_none'] = True

        return super().json(**kwargs)


class SetViewState(Action):
    """Action payload sent with `set_view_state`calls"""

    type: ActionType = ActionType.SET_VIEW_STATE
    view_state: ViewState


class GetLayers(Action):
    """Action payload sent with `get_layers`calls"""

    type: ActionType = ActionType.GET_LAYERS


class SetLayerVisibility(Action):
    """Action payload sent with `set_layer_visibility`calls"""

    type: ActionType = ActionType.SET_LAYER_VISIBILITY
    layer_id: str
    is_visible: bool


class SetTheme(Action):
    """Action payload sent with `set_theme`calls"""

    type: ActionType = ActionType.SET_THEME
    theme: Literal['light', 'dark']


class GetTimelineInfo(Action):
    """Action payload sent with `get_timeline_info`calls"""

    type: ActionType = ActionType.GET_TIMELINE_INFO
    idx: int


class ToggleTimelineAnimation(Action):
    """Action payload sent with `toggle_timeline_animation`calls"""

    type: ActionType = ActionType.TOGGLE_TIMELINE_ANIMATION
    idx: int


class ToggleTimelineVisibility(Action):
    """Action payload sent with `toggle_timeline_visibility`calls"""

    type: ActionType = ActionType.TOGGLE_TIMELINE_VISIBILITY
    idx: int


class SetTimelineInterval(Action):
    """Action payload sent with `set_timeline_interval`calls"""

    type: ActionType = ActionType.SET_TIMELINE_INTERVAL
    idx: int
    start_time: float
    end_time: float


class SetTimelineAnimationSpeed(Action):
    """Action payload sent with `set_timeline_animation_speed`calls"""

    type: ActionType = ActionType.SET_TIMELINE_SPEED
    idx: int
    speed: float


class SetTimelineConfig(Action):
    """Action payload sent with `set_timeline_config` calls"""

    type: ActionType = ActionType.SET_TIMELINE_CONFIG
    config: TimelineConfig


class RefreshMapData(Action):
    """Action payload sent with `refresh_map_data` calls"""

    type: ActionType = ActionType.REFRESH_MAP_DATA


class GetLayerTimelineInfo(Action):
    """Action payload sent with `get_layer_timeline_info` calls"""

    type: ActionType = ActionType.GET_LAYER_TIMELINE_INFO


class SetLayerTimelineConfig(Action):
    """Action payload sent with `set_layer_timeline_config` calls"""

    type: ActionType = ActionType.SET_LAYER_TIMELINE_CONFIG
    config: LayerTimelineConfig


class AddTileset(Action):
    """Action payload sent with `add_tileset` calls"""

    type: ActionType = ActionType.ADD_TILESET_TO_MAP
    tileset: Tileset


class AddDataset(Action):
    """Action payload sent with `add_dataset` calls"""

    type: ActionType = ActionType.ADD_DATASET_TO_MAP
    dataset: Dataset
    auto_create_layers: bool


class RemoveDataset(Action):
    """Action payload sent with `remove_dataset` calls"""

    type: ActionType = ActionType.REMOVE_DATASET_FROM_MAP
    uuid: UUID


class AddLayer(Action):
    """Action payload sent with `add_layer` calls"""

    type: ActionType = ActionType.ADD_LAYER
    layer: LayerSpec


class RemoveLayer(Action):
    """Action payload sent with `remove_layer` calls"""

    type: ActionType = ActionType.REMOVE_LAYER
    id: str


class RemoveFilter(Action):
    """Action payload sent with `remove_filter` calls"""

    type: ActionType = ActionType.REMOVE_FILTER
    id: str


class SetFilter(Action):
    """Action payload sent with `set_filter` calls"""

    type: ActionType = ActionType.SET_FILTER
    info: FilterInfo
