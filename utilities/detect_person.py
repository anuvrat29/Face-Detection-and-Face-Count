"""
    This file will detect person.
"""
import os
import glob
import cv2
import datetime
from mtcnn.mtcnn import MTCNN

from .config import PREDICTED_IMAGE

DETECTOR = MTCNN()

class Person:
    """
        This class contains method to detect person in a snapped image.
    """

    @classmethod
    def detect_person(cls, filepath):
        """
            This will generate output_image.
        """
        image = cv2.imread(filepath)
        frame1 = cv2.resize(image, (image.shape[1], image.shape[0]))
        frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        result = DETECTOR.detect_faces(frame2)

        if result != []:
            for person in result:
                bounding_box = person['box']
                keypoints = person['keypoints']
        
                cv2.rectangle(frame1, (bounding_box[0], bounding_box[1]), (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]), (0,155,255), 2)
                cv2.circle(frame1, (keypoints['left_eye']), 2, (0,155,255), 2)
                cv2.circle(frame1, (keypoints['right_eye']), 2, (0,155,255), 2)
                cv2.circle(frame1, (keypoints['nose']), 2, (0,155,255), 2)
                cv2.circle(frame1, (keypoints['mouth_left']), 2, (0,155,255), 2)
                cv2.circle(frame1, (keypoints['mouth_right']), 2, (0,155,255), 2)

        if not os.path.isdir(PREDICTED_IMAGE):
            os.mkdir(PREDICTED_IMAGE)
        else:
            for image in glob.glob(os.path.join(PREDICTED_IMAGE, "*.*")):
                try:
                    os.remove(image)
                except:
                    pass
        output = f"{str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))}-{os.path.basename(filepath)}"
        cv2.imwrite(os.path.join(PREDICTED_IMAGE, output), frame1)
        return {"imagename": output, "total_persons": len(result)}
