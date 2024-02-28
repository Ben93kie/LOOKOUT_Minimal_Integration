import asyncio
import websockets
import cv2
import json
import time

def encode_frame_to_jpeg(frame):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encoded_image = cv2.imencode('.jpg', frame, encode_param)
    if result:
        return encoded_image.tobytes()
    else:
        return None

def load_bounding_boxes(file_path):
    bounding_boxes = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            frame_number, category, obj_id, x, y, width, height = parts[:7]
            distance, distance_confidence, speed, speed_confidence, bearing, bearing_confidence, category_confidence = parts[7:]
            if frame_number not in bounding_boxes:
                bounding_boxes[frame_number] = []
            bounding_boxes[frame_number].append({
                "category": category,
                "category_confidence": float(category_confidence),
                "obj_id": obj_id,
                "x": int(x),
                "y": int(y),
                "width": int(width),
                "height": int(height),
                "distance": float(distance),
                "distance_confidence": float(distance_confidence),
                "speed": float(speed),
                "speed_confidence": float(speed_confidence),
                "bearing": float(bearing),
                "bearing_confidence": float(bearing_confidence)
            })
    return bounding_boxes


def scale_bounding_boxes(bboxes, orig_width, orig_height, target_width, target_height):
    width_scale = target_width / orig_width
    height_scale = target_height / orig_height
    scaled_bboxes = []
    for bbox in bboxes:
        scaled_bbox = {
            "category": bbox["category"],
            "category_confidence": bbox["category_confidence"],
            "obj_id": bbox["obj_id"],
            "x": int(bbox["x"] * width_scale),
            "y": int(bbox["y"] * height_scale),
            "width": int(bbox["width"] * width_scale),
            "height": int(bbox["height"] * height_scale),
            "distance": bbox["distance"],
            "distance_confidence": bbox["distance_confidence"],
            "speed": bbox["speed"],
            "speed_confidence": bbox["speed_confidence"],
            "bearing": bbox["bearing"],
            "bearing_confidence": bbox["bearing_confidence"]
        }
        scaled_bboxes.append(scaled_bbox)
    return scaled_bboxes

async def video_and_metadata_stream(websocket, path):
    await stream_handler(websocket, include_video=True)

async def metadata_stream(websocket, path):
    await stream_handler(websocket, include_video=False)

async def stream_handler(websocket, include_video):
    TARGET_FRAME_TIME = 1.0 / 30.0  # Approximately 30 FPS
    cap = cv2.VideoCapture(r"Sample.mkv")
    bounding_boxes = load_bounding_boxes(r"Sample_det.txt")
    frame_count = 0
    orig_width, orig_height = 1920, 1080
    target_width, target_height = 1920, 1080
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (target_width, target_height))

        str_frame_count = str(frame_count + 1)
        bboxes_info = {}
        if str_frame_count in bounding_boxes:
            scaled_bboxes = scale_bounding_boxes(bounding_boxes[str_frame_count], orig_width, orig_height, target_width, target_height)
            bboxes_info = {"frame_number": frame_count, "bboxes": scaled_bboxes}
        encoded_frame = encode_frame_to_jpeg(frame) if include_video else None
        bboxes_json = json.dumps(bboxes_info).encode('utf-8')

        if include_video and encoded_frame:
            # Video + Metadata Stream
            final_message = len(bboxes_json).to_bytes(4, byteorder='big') + bboxes_json + encoded_frame
            await websocket.send(final_message)
        else:
            # Only Metadata Stream
            await websocket.send(bboxes_json)

        processing_time = time.time() - start_time
        sleep_time = max(0.0, TARGET_FRAME_TIME - processing_time)
        await asyncio.sleep(sleep_time)
        frame_count += 1

    cap.release()

# Start the WebSocket servers on different ports
start_video_and_metadata_server = websockets.serve(video_and_metadata_stream, "0.0.0.0", 5678)
start_metadata_server = websockets.serve(metadata_stream, "0.0.0.0", 5679)

asyncio.get_event_loop().run_until_complete(start_video_and_metadata_server)
asyncio.get_event_loop().run_until_complete(start_metadata_server)
asyncio.get_event_loop().run_forever()
