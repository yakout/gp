from video_model.video_model import Highlight

class Merger():

	def get_points(highlights_dict, component_confidence):
		points = []
		for component, highlights in highlights_dict.items():
			component_score = component_confidence[component]
			for highlight in highlights:
				# Add start point with type 1
				points.append((highlight.start_index, 1, component_score * highlight.score))
				# Add end point with type 0
				points.append((highlight.end_index, 0, component_score * highlight.score))
		points.sort()
		return points

	@staticmethod
	def merge(highlights_dict : "dict[component_name]=list of highlights", component_confidence : "dict[component_name]=confidence(0 -1)"):
		"""
		merges the list of highlights generated by each component into one list of highlights.
		return list of highlights
		"""
		ret = []

		points = get_points(highlights_dict, component_confidence)

		current_score = 0
		previous_index = -1
		for point in points:
			index, type, score = point[0], point[1], point[2]

			if previous_index != -1 and index != previous_index:
				highlight = Highlight(previous_index, index, current_score)
				ret.append(highlight)

			previous_index = index if current_score > 0 else -1
			current_score += score if type == 1 else -score

		return ret


class Summarizer():

	@staticmethod
	def summarize(chunk_highlights_dict : "dict[chunk]=list of highlights", duration_limit : "max frames count"):
		"""
		summarizes the the list of highlights for all chunks to the given length
		"""
		highlights = []
		for chunk, chunk_highlights in chunk_highlights_dict.items():
			for highlight in chunk_highlights:
				highlights.append(highlight)

		highlights = sorted(highlights, key=lambda highlight: highlight.score, reverse=True)   # sort by score
		summarized_highlights = []
		for highlight in highlights:
			l, r = highlight.get_highlight_endpoints()
			if(duration_limit >= r-l+1):
				summarized_highlights.append(highlight)
				duration_limit -= r-l+1

		summarized_highlights = sorted(summarized_highlights, key=lambda highlight: highlight.start_index)   # sort by start
		return summarized_highlights