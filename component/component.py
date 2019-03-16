from abc import ABC, abstractmethod

class Component():

	@abstractmethod
	def get_highlights(chunk):
		"""
			gets highlights for this video chunk as per this component perspective.
			"""
		pass

class ComponentContainer():

	components_dict = {}

	@staticmethod
	def register_component(component_name, component):
		"""
			registers the given component with the given name in the container.
			"""
		components_dict[component_name] = component

	@staticmethod
	def get_chunk_highlights(chunk):
		"""
			gets chunk highlights from each component and stores in a dict.
			"""
		result_dict = {}
		for component_name, component in components_dict.items():
			highlights = component.get_highlights(chunk)
			result_dict[component_name] = highlights
		return result_dict