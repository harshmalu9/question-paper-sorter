import cv2


class ImagePreprocessor:

    @staticmethod
    def generate_rotations(image_path: str):

        image = cv2.imread(image_path)

        return {
            0: image,
            90: cv2.rotate(
                image,
                cv2.ROTATE_90_CLOCKWISE
            ),
            180: cv2.rotate(
                image,
                cv2.ROTATE_180
            ),
            270: cv2.rotate(
                image,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )
        }