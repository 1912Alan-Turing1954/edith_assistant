import cv2
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import requests

# Load the DETR model and processor
processor = DetrImageProcessor.from_pretrained(
    "facebook/detr-resnet-101", revision="no_timm"
)
model = DetrForObjectDetection.from_pretrained(
    "facebook/detr-resnet-101", revision="no_timm"
)

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide the path to a video file

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the OpenCV frame (BGR) to PIL format (RGB) for processing with DETR
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Preprocess the image using the DETR processor
    inputs = processor(images=image, return_tensors="pt")

    # Perform inference
    outputs = model(**inputs)

    # Convert outputs (bounding boxes and class logits) to COCO API format
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes, threshold=0.9
    )[0]

    for score, label, box in zip(
        results["scores"], results["labels"], results["boxes"]
    ):
        box = [round(i, 2) for i in box.tolist()]
        label_str = model.config.id2label[label.item()]
        confidence = round(score.item(), 3)

        # Display bounding box and label on the frame
        cv2.rectangle(
            frame,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            (255, 0, 0),
            2,
        )
        cv2.putText(
            frame,
            f"{label_str} {confidence}",
            (int(box[0]), int(box[1]) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2,
        )

    # Display the frame with detected objects
    cv2.imshow("Object Detection using DETR", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
