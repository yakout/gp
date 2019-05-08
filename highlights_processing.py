from video_model import Highlight


class Merger():
    @staticmethod
    def get_points(highlights_dict, component_confidence):
        points = []
        for component, highlights in highlights_dict.items():
            if not highlights:
                continue

            component_score = component_confidence[component]
            for highlight in highlights:
                # Add start point with type 1
                points.append((highlight.start_index, 1,
                               component_score * highlight.score))
                # Add end point with type 0
                points.append(
                    (highlight.end_index, 0, component_score * highlight.score))
        points.sort()
        return points

    @staticmethod
    def merge(highlights_dict, component_confidence):
        """
        merges the list of highlights generated by each component into one list of highlights.
        return list of highlights

        highlights_dict : dict[component_name]=list of highlights
        component_confidence : dict[component_name]=confidence(0 -1)
        """
        ret = []
        SCORE_THRESHOLD = 0.5

        points = Merger.get_points(highlights_dict, component_confidence)
        # print("#merge points : {}".format(points))

        current_score = 0
        previous_index = -1
        for point in points:
            # the point contains three info:
            # 1. index: start index
            # 2. type:
            #       1 for start of highlight
            #       0 for end of highlight
            # 3. score: highlight score (component confidence * highlight score)
            index, type, score = point[0], point[1], point[2]
            # print("index {}, type {}, score {}".format(index, type, score))

            if previous_index != -1 and index != previous_index and current_score > SCORE_THRESHOLD:
                # print("#merge previous_index {}, current_score {}, index {}".format(previous_index, current_score, index))
                highlight = Highlight(previous_index, index, current_score)
                ret.append(highlight)

            current_score += score if type == 1 else -score
            previous_index = index if current_score > 0 else -1

        print("Merge: highlights length returned: {}".format(len(ret)))
        return ret


class Summarizer():

    @staticmethod
    def summarize(chunk_highlights_dict, duration_limit, fps):
        """
        summarizes the list of highlights for all chunks to the given length
        chunk_highlights_dict : "dict[chunk_position]=list of highlights"
        duration_limit : "max video length output in minutes"
        """
        duration_limit = duration_limit * 60 * fps
        highlights = []
        chunkOfHighlight = {}
        for chunk_position, chunk_highlights in chunk_highlights_dict.items():
            for highlight in chunk_highlights:
                highlights.append(highlight)
                chunkOfHighlight[highlight] = chunk_position

        summarized_highlights = {}
        highlights = sorted(
            highlights, key=lambda highlight: highlight.score, reverse=True)   # sort by score
        for highlight in highlights:
            start, end = highlight.get_highlight_endpoints()
            if(duration_limit >= end-start+1):
                chunk_position = chunkOfHighlight[highlight]
                if chunk_position not in summarized_highlights:
                    summarized_highlights[chunk_position] = []
                summarized_highlights[chunk_position].append(highlight)
                duration_limit -= end-start+1

        for chunk_position, highlights in summarized_highlights.items():
            summarized_highlights[chunk_position] = sorted(
                highlights, key=lambda highlight: highlight.start_index)   # sort by start
            print("Summarizer: sorted highlights for chunk in position = {} has length = {}".format(
                chunk_position, len(highlights)))
        return summarized_highlights
