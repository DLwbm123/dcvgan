import numpy as np
from PIL import Image
import skvideo.io

def read_img(path):
    return np.asarray(Image.open(str(path)))

def write_img(img, path):
    Image.fromarray(img).save(str(path))

def save_video_as_images(video_tensor, path):
    """
    Save video frames into the directory

    Parameters
    ----------
    video_tensor: numpy.array
        video tensor in the shape of (frame, height, width, channel)
        
    path : pathlib.Path
        path to the video
    """
    path.mkdir(parents=True, exist_ok=True)
    
    placeholder = str(path / "{:03d}.jpg")
    for i, frame in enumerate(video_tensor):
        write_img(frame, placeholder.format(i))

def read_video(path):
    """
    read a video

    Parameters
    ----------
    path : string or pathlib.Path
        path to the video
        
    Returns
    -------
    video_tensor : numpy.array
        video tensor in the shape of (frame, height, width, channel)
    """
    videogen = skvideo.io.vreader(str(path))
    video_tensor = np.stack([frame for frame in videogen])

    return video_tensor

def write_video(video_tensor, path):
    """
    save a video

    Parameters
    ----------
    video_tensor: numpy.array
        video tensor in the shape of (frame, height, width, channel)
        
    path : string or pathlib.Path
        path to the video
    """
    writer = skvideo.io.FFmpegWriter(str(path))
    for frame in video:
        writer.writeFrame(frame)
    writer.close()

class SerializableFileObject(object):
    def __init__(self, f):
        self.file = f
        self.filename = f.name
        self.mode = f.mode
    
    def exec(self, func_name, *args):
        eval("self.file." + func_name)(*args)
        
    def __getstate__(self):
        self.f.close()
        state = self.__dict__.copy()
        del state['file']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.file = open(self.filename, mode=self.mode)
