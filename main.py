import cv2
import time
import threading
import signal
from image_processing import convert_frame_to_pil_image
from caption_generation import generate_caption
from openai_response_generation import generate_response
from input_timeout import input_with_timeout

# create VideoCapture object for camera feed
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # set resolution to 640x280
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 280)

# initialize variable for tracking processing times
last_process_time = time.time()
last_generation_time = time.time()
previous_caption = ""  # initialize variables for tracking previous captions and responses
previous_response = ""
previous_captions = []
previous_responses = []
lock = threading.Lock()  # initialize lock for threading synchronization
question = ""
bool = True

# convert frame to PIL image format and generate caption for a frame
def process_frame(frame):
    global last_generation_time, previous_captions, previous_responses, question
    pil_image = convert_frame_to_pil_image(frame)
    caption = generate_caption(pil_image, question)

    current_time = time.time() # track current time for processing time comparison
    if current_time - last_generation_time >= 3:  # generate response every 2 seconds
        if caption and caption not in previous_captions:
            previous_captions.append(caption) # add caption to previous captions list
            if len(previous_captions) > 20: # limit previous captions list to 10 items
                previous_captions.pop(0)

            response = generate_response(previous_caption + " " + caption, previous_response, question)  # generate response for caption and previous response

            while response in previous_responses: # ensure response is unique
                response = generate_response(previous_caption + " " + caption, previous_response)
            question = ""
            previous_responses.append(response) # add response to previous responses list
            if len(previous_responses) > 20:
                previous_responses.pop(0)
            if bool:
                print(response) # print response to console
        last_generation_time = current_time # update last generation time


def display_frame(frame):
    """
    Function to display a frame on the screen and overlay the previous captions on top of it.
    """
    global previous_captions
    with lock: # synchronize with lock
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.0
        thickness = 1
        color = (0, 0, 0)
        org = (10, 20)
        previous_captions_str = '\n'.join(previous_captions)
        cv2.putText(frame, previous_captions_str, org, font, font_scale, color, thickness, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        flipped_frame = cv2.flip(frame, 1) # Flip the frame horizontally
        cv2.imshow('frame', flipped_frame)

#The LOOOOOOP
def main_loop():
    global last_process_time, question, lock, bool
    while bool:
        ret, frame = cap.read()
        if not ret:
            print("Error capturing frame, exiting.")
            break
        s = input_with_timeout("", 2)
        if s == 's':
            bool = False
            lock.acquire()
            question = input("질문을 입력하세요: ")
            lock.release()
        current_time = time.time()
        if current_time - last_process_time >= 1:
            t = threading.Thread(target=process_frame, args=(frame,))
            t.start()
            last_process_time = current_time

        display_frame(frame)
        if (bool == False):
            bool = True
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main_loop()