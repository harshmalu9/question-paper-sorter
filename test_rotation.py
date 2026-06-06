import cv2
import easyocr
import tempfile
import os

IMAGE_PATH = "data/temp/page_009.jpg"

reader = easyocr.Reader(
    ['en'],
    gpu=True
)

image = cv2.imread(IMAGE_PATH)

rotations = {
    0: image,
    90: cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE),
    180: cv2.rotate(image, cv2.ROTATE_180),
    270: cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
}

results = {}

for angle, rotated_image in rotations.items():

    with tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    ) as temp_file:

        temp_path = temp_file.name

    cv2.imwrite(
        temp_path,
        rotated_image
    )

    text = "\n".join(
        reader.readtext(
            temp_path,
            detail=0
        )
    )

    os.remove(temp_path)

    results[angle] = text

    print("\n" + "=" * 50)
    print(f"ROTATION {angle}")
    print("=" * 50)

    print(text[:500])

best_angle = max(
    results,
    key=lambda angle: len(results[angle])
)

print("\n")
print("=" * 50)
print(f"BEST ROTATION: {best_angle}")
print("=" * 50)