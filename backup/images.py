import cv2
import io

from PIL import Image

class VideoParser:
    target_w = 512
    target_h = 512

    vidcap = None
    frames = 0

    count = 0
    done = False

    reverse = False

    def __init__(self, video: str, reverse = False):
        self.vidcap = cv2.VideoCapture(video)
        self.frames = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.reverse = reverse
        if self.reverse:
            self.count = self.frames

    def next(self):
        if self.reverse:
            self.count -= 1
            self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, self.count)
        else:
            self.count += 1

        success, frame = self.vidcap.read()

        self.done = not success

        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            img.thumbnail((self.target_w, self.target_h))

            w, h = img.size

            img = img.crop((((w - self.target_w) / 2), ((h - self.target_h) / 2), ((w + self.target_w) / 2), ((h + self.target_h) / 2)))

            return img
        else:
            return None
    
    def skip(self, n: int):
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, self.count + n if not self.reverse else self.count - n)
        self.count = self.count + n if not self.reverse else self.count - n

    def skip_to(self, i: int):
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
        self.count = i

    def get_all(self):
        frames = []

        ret = True
        while ret:
            ret, frame = self.vidcap.read()
            self.count += 1

            if not ret:
                break

            img = Image.fromarray(frame)
            img.thumbnail((self.target_w, self.target_h))

            w, h = img.size

            img = img.crop((((w - self.target_w) / 2), ((h - self.target_h) / 2), ((w + self.target_w) / 2), ((h + self.target_h) / 2)))
            i = io.BytesIO()

            img.save(i, format="PNG")
    
            frames.append(i)

            print(f"Read {self.count} / {self.frames} ...")

        return frames