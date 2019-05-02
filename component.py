from abc import ABC, abstractmethod
from typing import List, Mapping
from video_model import Highlight, Chunk

class Component:
    """
    This is an abstract class that any new highlight generator component should extend.
    """
    @abstractmethod
    def get_highlights(self, chunk: Chunk) -> 'List[Highlight]':
        """
        Gets highlights for this video chunk as per this component's perspective.
        :param chunk: the current video chunk being processed
        :return: list of highlights from given chunk
        """
        pass


class ComponentContainer:
    """
    This class is a container for all highlight generator components registered in the system.
    """

    components_dict = {}
    errors_count = 0 # keep track of number of errors for the sake of improving performance

    @staticmethod
    def register_component(component_name: str, component: Component):
        """
        Registers the given component with the given name in the container.
                :param component_name: string representing the component name (must be unique for each component)
                :param component: Component object to be registered
        """
        ComponentContainer.components_dict[component_name] = component

    @staticmethod
    def get_chunk_highlights(chunk: Chunk) -> 'Mapping[str, List[Highlight]]':
        """
        Gets chunk highlights from each component and
        """
        result_dict = {}  # result_dict is a dict of component_name -> list of highlights
        for component_name, component in ComponentContainer.components_dict.items():
            highlights = component.get_highlights(chunk)
            result_dict[component_name] = highlights
        return result_dict
