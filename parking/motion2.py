import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE


class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self, video, coordinates):
        self.video = video
        self.coordinates_data = coordinates
        self.contours = []
        self.bounds = []
        self.mask = []

    def detect_motion(self):
        capture = open_cv.VideoCapture(self.video)
        capture.set(open_cv.CAP_PROP_POS_FRAMES, 0)  # Start video from frame 0

        # Process coordinates
        for p in self.coordinates_data:
            coordinates = self._coordinates(p)
            rect = open_cv.boundingRect(coordinates)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8
            )
            self.mask.append(mask == 255)

        # Initialize statuses and times
        statuses = [False] * len(self.coordinates_data)
        times = [None] * len(self.coordinates_data)

        # Variables to track total and available slots
        total_slots = len(self.coordinates_data)
        available_slots = 0

        while capture.isOpened():
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            new_frame = frame.copy()

            position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0

            # Update statuses for each slot
            available_slots = 0
            for index, p in enumerate(self.coordinates_data):
                status = self.__apply(grayed, index, p)
                if times[index] is None and self.status_changed(statuses, index, status):
                    times[index] = position_in_seconds

                if status:
                    available_slots += 1

                statuses[index] = status

            # Draw contours for each slot
            for index, p in enumerate(self.coordinates_data):
                coordinates = self._coordinates(p)
                color = COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)

            # Display total and available slots on the frame
            cv2.putText(new_frame, f"Total Slots: {total_slots}", (10, 20), open_cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1)
            cv2.putText(new_frame, f"Available Slots: {available_slots}", (10, 40), open_cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1)

            open_cv.imshow(str(self.video), new_frame)
            if open_cv.waitKey(1) == ord("q"):
                break
        capture.release()
        open_cv.destroyAllWindows()

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        rect = self.bounds[index]
        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        return np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
