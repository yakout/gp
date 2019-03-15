class Component():

	def get_highlights(chunk):
		pass


class ComponentContainer():

	components_dict = {}

	@staticmethod
	def register_component(component_name, component):
		components_dict[component_name] = component

	@staticmethod
	def get_chunk_highlights(chunk):
		result_dict = {}
		for component_name, component in components_dict.items():
			highlights = component.get_highlights(chunk)
			result_dict[component_name] = highlights
		return result_dict