import cv2
import numpy as np
from tqdm import tqdm

def convertRGBtoLuminosity(frame):
  frame = np.array(frame) / 255

  # NOTE: This is the correct way to convert RGB to luminosity, but it's too slow
  # linear_space = np.where(frame <= 0.04045, frame / 12.92, ((frame + 0.055) / 1.055) ** 2.4)

  return np.mean(np.sum(frame * np.array([0.0722, 0.7152, 0.2126]), axis=2))


def process_video(input_path: str, output_path: str, luminosity_threshold):
  vidcap = cv2.VideoCapture(input_path)
  video_format = cv2.VideoWriter_fourcc(*'mp4v') # type: ignore
  fps = int(vidcap.get(cv2.CAP_PROP_FPS))
  frame_width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
  frame_height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

  writer = cv2.VideoWriter(output_path, video_format, fps, (frame_width, frame_height))

  prev_output_frame = None
  for _ in tqdm(range(num_frames)):
    success, current_frame = vidcap.read()
    current_frame = np.array(current_frame)

    if success and len(current_frame.shape) < 3:
      continue

    if prev_output_frame is None:
      prev_output_frame = current_frame

    curr_frame_luminosity = convertRGBtoLuminosity(current_frame)

    if curr_frame_luminosity > luminosity_threshold:
      out_frame = np.max(np.array([prev_output_frame, current_frame], dtype=np.uint8), axis=0)
      prev_output_frame = out_frame

      writer.write(out_frame)

  writer.release()


if __name__ == "__main__":
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument("input_path", type=str, help="Path to input video")
  parser.add_argument("--output-path", type=str, help="Path to output video", required=False, default="output.mp4")
  parser.add_argument("--luminosity-threshold", type=float, help="Luminosity threshold", required=False, default=0.0)
  args = parser.parse_args()

  process_video(args.input_path, args.output_path, args.luminosity_threshold)