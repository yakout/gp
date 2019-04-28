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
        pass

    def evaluate(self, highlights_list):
        """
        Evaluates the quality of the given highlights list.
        It counts the percentage of highlights frames based on the ground
        truth provided.

        Parameters:
            highlights_list : final list of Highlight produced by the system.

        Return:
            - accurracy
            - precision
            - recall
        """
        pass
