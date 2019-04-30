# from __future__ import print_function
# import os
#
# # Standard PySceneDetect imports:
# from scenedetect.video_manager import VideoManager
# from scenedetect.scene_manager import SceneManager
# # For caching detection metrics and saving/loading to a stats file
# from scenedetect.stats_manager import StatsManager
#
# # For content-aware scene detection:
# from scenedetect.detectors.content_detector import ContentDetector
#
#
# def find_scenes(video_path, threshold=30, min_scene_length=15):
#     # type: (str) -> List[Tuple[FrameTimecode, FrameTimecode]]
#     video_manager = VideoManager([video_path])
#     stats_manager = StatsManager()
#     # Construct our SceneManager and pass it our StatsManager.
#     scene_manager = SceneManager(stats_manager)
#
#     # Add ContentDetector algorithm (each detector's constructor
#     # takes detector options, e.g. threshold).
#     scene_manager.add_detector(ContentDetector(threshold, min_scene_length))
#     base_timecode = video_manager.get_base_timecode()
#
#     # We save our stats file to {VIDEO_PATH}.stats.csv.
#     stats_file_path = '%s.stats.csv' % video_path
#
#     scene_list = []
#
#     try:
#         # If stats file exists, load it.
#         if os.path.exists(stats_file_path):
#             # Read stats from CSV file opened in read mode:
#             with open(stats_file_path, 'r') as stats_file:
#                 stats_manager.load_from_csv(stats_file, base_timecode)
#
#         # Set downscale factor to improve processing speed.
#         video_manager.set_downscale_factor()
#
#         # Start video_manager.
#         video_manager.start()
#
#         # Perform scene detection on video_manager.
#         scene_manager.detect_scenes(frame_source=video_manager)
#
#         # Obtain list of detected scenes.
#         scene_list = scene_manager.get_scene_list(base_timecode)
#         # Each scene is a tuple of (start, end) FrameTimecodes.
#
#         print('List of scenes obtained:')
#         for i, scene in enumerate(scene_list):
#             print(
#                 'Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
#                 i+1,
#                 scene[0].get_timecode(), scene[0].get_frames(),
#                 scene[1].get_timecode(), scene[1].get_frames(),))
#
#         # We only write to the stats file if a save is required:
#         if stats_manager.is_save_required():
#             with open(stats_file_path, 'w') as stats_file:
#                 stats_manager.save_to_csv(stats_file, base_timecode)
#
#     finally:
#         video_manager.release()
#
#     return scene_list


from __future__ import division

import subprocess

def find_scenes(src_video, threshold=0):
    """
    uses ffprobe to produce a list of shot
    boundaries (in seconds)

    Args:
        src_video (string): the path to the source
            video
        threshold (float): the minimum value used
            by ffprobe to classify a shot boundary

    Returns:
        List[(float, float)]: a list of tuples of floats
        representing predicted shot boundaries (in seconds) and
        their associated scores
    """
    scene_ps = subprocess.Popen(("ffprobe",
                                "-show_frames",
                                "-of",
                                "compact=p=0",
                                "-f",
                                "lavfi",
                                "movie=" + src_video + ",select=gt(scene\," + str(threshold) + ")"),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    output = scene_ps.stdout.read()
    print(type(output))
    print(output.decode("utf-8"))
    outpu = output.decode("utf-8")
    boundaries = extract_boundaries_from_ffprobe_output(output)
    print("\n\n\n", len(boundaries))

    sd_results = get_shot_predictions(boundaries)

    print("\n\n\n", sd_results)
    print("\n\n\n", len(sd_results))

    # print("\n\n\n", boundaries.shape)
    return sd_results

def extract_boundaries_from_ffprobe_output(output):
    """
    extracts the shot boundaries from the string output
    producted by ffprobe

    Args:
        output (string): the full output of the ffprobe
            shot detector as a single string

    Returns:
        List[(float, float)]: a list of tuples of floats
        representing predicted shot boundaries (in seconds) and
        their associated scores
    """
    boundaries = []
    print(len(output.split("\n".encode())))
    for line in output.split("\n".encode())[15:-1]:
        print(len(line.split('|'.encode())))
        if(len(line.split('|'.encode())) < 5):
            continue
        boundary = float(line.split('|'.encode())[4].split('='.encode())[-1])
        score = float(line.split('|'.encode())[-1].split('='.encode())[-1])
        boundaries.append((boundary, score))
        # print('boundaries ', boundaries)
    return boundaries


import csv

def get_shot_predictions(boundaries, threshold=0.1):
    """

    """
    results = []
    boundaries = sorted(boundaries, key=lambda x: x[1], reverse=True)

    for bound, score in boundaries:
        if(score >= threshold):
            results.append(bound)


    return sorted(results)
