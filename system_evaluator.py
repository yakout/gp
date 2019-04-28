import os
class SystemEvaluator:
    """
    This class servers to evaluate the quality of the produced
    highlights given the list of highlights produced by the system and
    a manualy labeled file specifying whether each scene, as per scenedetector,
    is considered highlight or not.

    Attributes :
        scene_labels : list of binary labels for this video
            label for each scene whether it is considered highlight or not.

    Methods:
        evaluate(highlights_list)
            computes the accurracy obtained on this video given the
            highlights_list
    """

    def __init__(self, video_path):
        # read labeled ground truth file
        self.scene_labels = None
        self.read_labels_file(video_path)

    def read_labels_file(self, video_path):
        labels_file_path = (os.path.splitext(video_path)[0]) + ".ht"
        video_labels = []
        with open(labels_file_path) as f:
            for line in f: # read rest of lines
                video_labels.append(int(line))
            self.scene_labels = video_labels

    def evaluate(self, highlights_dict, chunks_info_dict):
        """
        Evaluates the quality of the given highlights list.
        It counts the percentage of highlights frames based on the ground
        truth provided.

        # NOTE: it is assumed that highlghts_dict carry entry, even if empty,
        for every chunk

        Parameters:
            highlights_dict : final dict of Highlight produced by the system.
            chunks_info_dict : dict containing info for each chunk like chunk length.

        Return:
            - accurracy
            - precision
            - recall
        """
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        true_negatives = 0

        labels_index = 0
        for chunk_position, highlights in highlights_dict.items():
            chunk_label = self.scene_labels[labels_index]
            chunk_positives = 0
            for highlight in highlights:
                # For each highlight get starting/ending frames of video
                start_frame, end_frame = highlight.get_highlight_endpoints()
                # positives because they are included in highlights
                chunk_positives += (end_frame - start_frame + 1)

            if (chunk_label == 1):
                # this chunk is highilight,
                # considerd frames are TP, ignored are FN
                false_negatives += (chunks_length_dict[chunk_position]
                                        - chunk_positives)
                true_positives += chunk_positives
            else:
                # this chunk is NOT highilight,
                # considerd frames are FP, ignored are TN
                true_negatives += (chunks_length_dict[chunk_position]
                                        - chunk_positives)
                false_positives += chunk_positives
            labels_index += 1

        # Computing precision, recall, and accurracy
        precision = (true_positives) / (true_positives + false_positives)

        recall = (true_positives) / (true_positives + false_negatives)

        total = true_negatives + true_positives + false_negatives + false_positives
        accurracy = (true_positives + true_negatives) / (total)
        return precision, recall, accurracy
