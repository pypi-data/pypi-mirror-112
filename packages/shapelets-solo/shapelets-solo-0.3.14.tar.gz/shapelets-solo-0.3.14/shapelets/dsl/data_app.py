# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from enum import Enum
import json
from json import JSONEncoder
import time
from typing import List, overload, TypeVar

from shapelets.dsl.data_app_events import Event
from shapelets.dsl.data_app_widgets import (
    BarChart,
    Button,
    DonutChart,
    Label,
    LineChart,
    Markdown,
    MetadataField,
    MultiSequenceSelector,
    Number,
    PieChart,
    PolarArea,
    RadarArea,
    SequenceSelector,
    Selector,
    Slider,
    Widget,
    WidgetNode,
)
from shapelets.dsl.data_app_context import (
    FilteringContext,
    TemporalContext
)
from shapelets.dsl.graph import Node
from shapelets.model import Collection, Sequence, MetadataType, NDArray, View
from shapelets.dsl.data_app_panel import VerticalFlowPanel, HorizontalFlowPanel, GridPanel, Panel


class AttributeNames(Enum):
    CREATION_DATE = "creationDate"
    CUSTOM_GRAPH = "customGraphs"
    DESCRIPTION = "description"
    FILTERING_CONTEXTS = "filteringContexts"
    MAIN_PANEL = "mainPanel"
    NAME = "name"
    ID = "id"
    TEMPORAL_CONTEXTS = "temporalContexts"
    TITLE = "title"
    UPDATE_DATE = "updateDate"


class DataApp:
    """
    Entry point for data app registration.
    """

    @staticmethod
    def now() -> int:
        return int(time.mktime(time.gmtime()) * 1e3)

    def __init__(self,
                 name: str,  # acts as app_id, must be unique
                 description: str,
                 creation_date: int = None,
                 update_date: int = None,
                 main_panel: Panel = None):
        self.name = name
        self.description = description
        self.creation_date = creation_date
        self.update_date = update_date
        self.main_panel = main_panel if main_panel else VerticalFlowPanel(panel_id=name)
        self.title = name
        self.temporal_contexts = []
        self.filtering_contexts = []
        self._custom_graphs: List[Event] = []

    def set_title(self, title: str):
        """
        Sets the DataApp's title.
        :param title: The title for the app
        :return: None
        """
        self.title = title

    def temporal_context(self, name: str = None,
                         widgets: List[WidgetNode] = None,
                         context_id: str = None):
        """
        Define a temporal context for your dataApp.
        :param name: String with the temporal context name.
        :param widgets: List of Widgets inside the temporal context.
        :param context_id: String with the temporal context ID.
        :return: new temporal context.
        """
        widget_ids = []
        if widgets:
            for widget in widgets:
                if hasattr(widget, 'temporal_context'):
                    widget_ids.append(widget.widget_id)
                else:
                    raise Exception(f"Component {widget.widget_type} does not allow temporal context")
        temporal_context = TemporalContext(name, widget_ids, context_id)
        self.temporal_contexts.append(temporal_context)
        return temporal_context

    def filtering_context(self, name: str = None,
                          input_filter: List[MetadataField] = None,
                          context_id: str = None):
        input_filters_ids = []
        collection_id = None
        if input_filter:
            collection_ids = [mfield.collection.collection_id for mfield in input_filter]
            collection_ids_set = set(collection_ids)
            if len(set(collection_ids)) == 1:
                collection_id = collection_ids_set.pop()
                for widget in input_filter:
                    # if hasattr(widget, 'filtering_context'):
                    input_filters_ids.append(widget.widget_id)
                    # else:
                    #     raise Exception(f"Component {widget.widget_type} does not allow filtering context")
            else:
                raise Exception("Collection missmatch: All MetadataFields need to come from the same Collection.")
        filtering_context = FilteringContext(name, collection_id, input_filters_ids, context_id)
        self.filtering_contexts.append(filtering_context)
        return filtering_context

    @staticmethod
    def set_filtering_context(input_filter: WidgetNode, output_filter: List[WidgetNode]):
        for widget in output_filter:
            if hasattr(widget, 'filtering_context'):
                widget.filtering_context = input_filter.widget_id
            else:
                raise AttributeError(f"Output widget {widget.widget_type} does not allow filtering context")

    def add_custom_graph(self, event: Event):
        self._custom_graphs.append(event)

    def number(self,
               from_node: Node = None,
               name: str = None,
               default_value: float = 0,
               value_type: type = float,
               **additional) -> Number:
        number = Number(name=name,
                        default_value=default_value,
                        value_type=value_type,
                        parent_data_app=self,
                        **additional)
        if from_node:
            Event.add_output_mapping(self._custom_graphs, from_node, number.widget_id)
        return number

    def slider(self,
               min_value,
               max_value,
               step=None,
               default_value=None,
               in_range: bool = False,
               title: str = None,
               value_type: type = int,
               formatter: str = "number",
               **additional) -> Slider:
        return Slider(
            min_value,
            max_value,
            step,
            default_value=default_value,
            value_type=value_type,
            in_range=in_range,
            title=title,
            formatter=formatter,
            parent_data_app=self,
            **additional)

    def button(self, name: str = None, text: str = "", **additional) -> Button:
        return Button(name, text, parent_data_app=self, **additional)

    def vertical_flow_panel(self,
                            title: str = None,
                            panel_id: str = None,
                            **additional) -> VerticalFlowPanel:
        return VerticalFlowPanel(panel_title=title, panel_id=panel_id, **additional)

    def horizontal_flow_panel(self,
                              title: str = None,
                              panel_id: str = None,
                              **additional) -> HorizontalFlowPanel:
        return HorizontalFlowPanel(panel_title=title, panel_id=panel_id, **additional)

    def grid_panel(self,
                   num_rows: int,
                   num_cols: int,
                   title: str = None,
                   panel_id: str = None,
                   **additional):
        return GridPanel(num_rows, num_cols, panel_title=title, panel_id=panel_id, **additional)

    @overload
    def line_chart(self, sequence: TypeVar('T', Sequence, SequenceSelector, Node), views: TypeVar('T', List[View], Node) = None,
                   title: str = None,
                   temporal_context: TemporalContext = None,
                   filtering_context: FilteringContext = None, **additional):
        ...

    @overload
    def line_chart(self, y_axis: TypeVar('T', NDArray, Node), x_axis: TypeVar('T', NDArray, Node) = None, title=None):
        ...

    def line_chart(self,
                   title: str = None,
                   sequence: TypeVar('T', Sequence, SequenceSelector, Node) = None,
                   x_axis: TypeVar('T', NDArray, Node) = None,
                   y_axis: TypeVar('T', NDArray, Node) = None,
                   views: TypeVar('T', List[View], Node) = None,
                   temporal_context: TemporalContext = None,
                   filtering_context: FilteringContext = None, **additional):
        return LineChart(
            title,
            sequence,
            x_axis,
            y_axis,
            views,
            temporal_context,
            filtering_context,
            parent_data_app=self,
            **additional)

    def metadata_field(self,
                       field_name: str,
                       field_type: MetadataType,
                       collection: Collection,
                       name: str = None,
                       **additional):
        return MetadataField(field_name, field_type, collection, name, parent_data_app=self, **additional)

    def sequence_selector(self,
                          collection: Collection = None,
                          sequences: List[Sequence] = None,
                          default_sequence: Sequence = None,
                          name: str = None,
                          title: str = None,
                          **additional):
        return SequenceSelector(collection,
                                sequences,
                                default_sequence,
                                name,
                                title,
                                parent_data_app=self,
                                **additional)

    def multi_sequence_selector(self,
                                collection: Collection = None,
                                sequences: List[Sequence] = None,
                                default_sequence: List[Sequence] = None,
                                name: str = None,
                                title: str = None,
                                **additional):
        return MultiSequenceSelector(collection,
                                     sequences,
                                     default_sequence,
                                     name,
                                     title,
                                     parent_data_app=self,
                                     **additional)

    @overload
    def selector(self, options: List[str], title: str = None, value: str = None):
        ...

    @overload
    def selector(self, options: List[int], title: str = None, value: int = None):
        ...

    @overload
    def selector(self, options: List[float], title: str = None, value: float = None):
        ...

    @overload
    def selector(self, options: List[dict], index_by: str, label_by: str, value_by: str,
                 value: any = None, title: str = None):
        ...

    def selector(self, options: List, title: str = None, index_by: str = None, label_by: str = None,
                 value_by: str = None,
                 value: any = None, **additional):
        return Selector(options, title, index_by, label_by, value_by, value, parent_data_app=self, **additional)

    def bar_chart(self,
                  data: NDArray,
                  categories: NDArray = None,
                  name: str = None,
                  title: str = None,
                  **additional):
        return BarChart(data, categories, name, title, **additional)

    def pie_chart(self,
                  data: NDArray,
                  categories: NDArray = None,
                  name: str = None,
                  title: str = None,
                  **additional):
        return PieChart(data, categories, name, title, **additional)

    def donut_chart(self,
                    data: NDArray,
                    categories: NDArray = None,
                    name: str = None,
                    title: str = None,
                    **additional):
        return DonutChart(data, categories, name, title, **additional)

    def polar_area_chart(self,
                         categories: NDArray,
                         data: NDArray,
                         name: str = None,
                         title: str = None,
                         **additional):
        return PolarArea(categories, data, name, title, **additional)

    def radar_area_chart(self,
                         categories: NDArray,
                         data: NDArray,
                         groups: NDArray,
                         name: str = None,
                         title: str = None,
                         **additional):
        return RadarArea(categories, data, groups, name, title, **additional)

    def markdown(self, text: TypeVar('T', str, int, float, Node), **additional):
        return Markdown(text, **additional)

    def label(self, text: TypeVar('T', str, int, float, Node), **additional):
        return Label(text, **additional)

    def place(self, widget: Widget, *args, **kwargs):
        self.main_panel.place(widget, *args, **kwargs)

    def to_dict_widget(self):
        self_dict = {
            AttributeNames.ID.value: self.name,
            AttributeNames.NAME.value: self.name,
            AttributeNames.DESCRIPTION.value: self.description,
            AttributeNames.CREATION_DATE.value: self.creation_date,
            AttributeNames.UPDATE_DATE.value: self.update_date,
            AttributeNames.TEMPORAL_CONTEXTS.value: self.temporal_contexts,
            AttributeNames.FILTERING_CONTEXTS.value: self.filtering_contexts
        }
        if hasattr(self, AttributeNames.TITLE.value):
            self_dict.update({
                AttributeNames.TITLE.value: self.title
            })
        self_dict[AttributeNames.MAIN_PANEL.value] = self.main_panel.to_dict_widget()
        temporal_context = []
        for temporal in self.temporal_contexts:
            temporal_context.append(temporal.to_dict())
        self_dict[AttributeNames.TEMPORAL_CONTEXTS.value] = temporal_context

        filtering_context = []
        for filter_context in self.filtering_contexts:
            filtering_context.append(filter_context.to_dict())
        self_dict[AttributeNames.FILTERING_CONTEXTS.value] = filtering_context

        for event in self._custom_graphs:
            if event.custom_graph_dict:
                custom_graphs = self_dict.get(AttributeNames.CUSTOM_GRAPH.value)
                if not custom_graphs:
                    custom_graphs = {}
                    self_dict[AttributeNames.CUSTOM_GRAPH.value] = custom_graphs
                custom_graphs.update({event.custom_graph_name: event.custom_graph_dict})

        return self_dict

    class DataAppEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, (DataApp, Widget)):
                return o.to_dict_widget()
            try:
                return o.__dict__
            except AttributeError as attr_error:
                print(f"ERROR: {attr_error}")
                return {}

    def to_json(self):
        return json.dumps(self, cls=DataApp.DataAppEncoder, indent=2)

    def __repr__(self):
        s_repr = f"{AttributeNames.NAME.value}={self.name}, "
        s_repr += f"{AttributeNames.DESCRIPTION.value}={self.description}, "
        s_repr += f"{AttributeNames.CREATION_DATE.value}={self.creation_date}, "
        s_repr += f"{AttributeNames.UPDATE_DATE.value}={self.update_date}"
        return s_repr
