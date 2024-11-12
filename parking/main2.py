import argparse
import yaml
from motion2 import MotionDetector
import logging


def main():
    logging.basicConfig(level=logging.INFO)

    args = parse_args()
    data_file = args.data_file

    with open(data_file, "r") as data:
        points = yaml.load(data, Loader=yaml.SafeLoader)
        detector = MotionDetector(args.video_file, points)
        detector.detect_motion()


def parse_args():
    parser = argparse.ArgumentParser(description='Detect motion based on predefined coordinates')

    parser.add_argument("--video",
                        dest="video_file",
                        required=True,
                        help="Video file to detect motion on")

    parser.add_argument("--data",
                        dest="data_file",
                        required=True,
                        help="Data file with coordinates")

    return parser.parse_args()


if __name__ == '__main__':
    main()
