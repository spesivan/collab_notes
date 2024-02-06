import cv2
import os

def convert_video_to_frames(video_path, output_folder):
    video_capture = cv2.VideoCapture(video_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame_number in range(frame_count):
        # Read the frame
        ret, frame = video_capture.read()

        frame_name = f"frame_{frame_number:04d}.jpg"
        frame_path = os.path.join(output_folder, frame_name)
        cv2.imwrite(frame_path, frame)

    video_capture.release()

if __name__ == "__main__":
    video_path = "video_name"

    output_folder = "./frames"

    convert_video_to_frames(video_path, output_folder)
