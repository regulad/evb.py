from enum import Enum
from typing import Any, Union


class Command:
    """The base class that all commands inherit from."""

    NAME: str = ""
    ARG_TYPE: Any = None

    def __init__(
            self,
            arg_value: ARG_TYPE,
    ):
        self._arg_value = arg_value

    @property
    def arg_value(self):
        return self._arg_value

    def __str__(self):
        if self.__class__.ARG_TYPE is None and self.arg_value is None:
            return self.__class__.NAME
        else:
            return f"{self.__class__.NAME}={self.arg_value}"


class TopText(Command):
    """Top text with Impact font"""

    NAME = "tt"
    ARG_TYPE = str


class BottomText(Command):
    """Bottom text with Impact font"""

    NAME = "bt"
    ARG_TYPE = str


class TopCaption(Command):
    """Motivational poster style top caption"""

    NAME = "tc"
    ARG_TYPE = str


class BottomCaption(Command):
    """Motivational poster style bottom caption"""

    NAME = "bc"
    ARG_TYPE = str


class Caption(Command):
    """Adds a caption in a white box above the video"""

    NAME = "cap"
    ARG_TYPE = str


class Music(Command):
    """Adds the audio from a YouTube/TikTok/SoundCloud (heaps of other sites too) video to your video.
    Use it with the 'mute' command to mute the original audio."""

    NAME = "music"
    ARG_TYPE = str


class MusicSkip(Command):
    """Starts the audio at a given time of the audio in seconds."""

    NAME = "musicskip"
    ARG_TYPE = str


class MusicDelay(Command):
    """Starts the audio at a given time of the audio in seconds."""

    NAME = "musicskip"
    ARG_TYPE = int


class Length(Command):
    """Specifies how long the video should go for when using music= with a still image in seconds.
    Max value is 45 seconds (length=45). If not specified, it defaults to 15."""

    NAME = "length"
    ARG_TYPE = int


class Muffle(Command):
    """Muffles the audio - higher numbers = more muffled."""

    NAME = "muffle"
    ARG_TYPE = int


class StartVideo(Command):
    """The time to start the video from, in seconds."""

    NAME = "start"
    ARG_TYPE = int


class EndVideo(Command):
    """The time to end the video at, in seconds."""

    NAME = "end"
    ARG_TYPE = int


class DeepFry(Command):
    """"Deep fries" the photo or video by increasing it's contrast, saturation and gamma levels."""

    NAME = "df"
    ARG_TYPE = int


class EqRise(Command):
    """Reduces audio bitrate and changes audio stream to logarithmic instead of linear,
    reducing the audio quality and making it louder.
    Basically use this if you hate people who have headphones or have their speakers set to loud."""

    NAME = "er"
    ARG_TYPE = int


class Ricecake(Command):
    """Deletes all i-frames in the video (except for the first few) and randomly duplicates p-frames for a datamosh-like
    effect. rc=0 makes the result completely random. rc=1 - rc=10 slightly changes the probablility of duplicated
    frames, but in the end, it depends on the target video. They're all really powerful."""

    NAME = "rc"
    ARG_TYPE = int


class Shake(Command):
    """Creates a shake effect on the video."""

    NAME = "shake"
    ARG_TYPE = int


class Highpass(Command):
    """Removes lower frequencies in the audio (opposite of muffle, which removes higher frequencies).
    Higher numbers = more frequencies removed."""

    NAME = "highpass"
    ARG_TYPE = int


class Sketch(Command):
    """Makes the video look like it's been sketched on a blank piece of paper.
    Higher number values add more detail, shadows and outlines."""

    NAME = "sketch"
    ARG_TYPE = int


class Spin(Command):
    """Makes the video spin around. Lower numbers mean faster spinning, higher numbers mean slower spinning."""

    NAME = "spin"
    ARG_TYPE = int


class Pixelate(Command):
    """Makes the video spin around. Lower numbers mean faster spinning, higher numbers mean slower spinning."""

    NAME = "spin"
    ARG_TYPE = int


class Glow(Command):
    """Adds a glow effect to the photo/video"""

    NAME = "glow"
    ARG_TYPE = int


class Technicolor(Command):
    """Adds an old-fashioned cartoony technicolor effect."""

    NAME = "technicolor"


class Widen(Command):
    """Makes the video wider.
    A value of 10 preserves the original width, so any value smaller than 10 will make it less wide."""

    NAME = "widen"
    ARG_TYPE = int


class Heighten(Command):
    """Makes the video taller.
    A value of 10 preserves the original height, so any value smaller than 10 will make it less tall."""

    NAME = "heighten"
    ARG_TYPE = int


class Rasp(Command):
    """Makes the audio really weird; distorts it"""

    NAME = "rasp"
    ARG_TYPE = int


class Echo(Command):
    """Makes the audio have an echo"""

    NAME = "echo"
    ARG_TYPE = int


class RandomLag(Command):
    """Randomly shuffles video frames in chunks"""

    NAME = "rlag"
    ARG_TYPE = int


class Rotate(Command):
    """Rotates the media based on the number of degrees given (e.g. rotate=45, would rotate the video by 45Â°)"""

    NAME = "rotate"
    ARG_TYPE = int


class FadeIn(Command):
    """Fades into the video from a black screen.
    The number (in seconds) specifies how long it should take to fully fade in."""

    NAME = "fadein"
    ARG_TYPE = int


class FadeOut(Command):
    """Fades out from the video into a black screen.
    The number (in seconds) specifies how long it should take to fully fade out."""

    NAME = "fadeout"
    ARG_TYPE = int


class FadeInAudio(Command):
    """Fades into the video from silence. The number (in seconds) specifies how long it should take to fully fade in."""

    NAME = "fadeinaudio"
    ARG_TYPE = int


class FadeOutAudio(Command):
    """Fades out from the video into silence.
    The number (in seconds) specifies how long it should take to fully fade out."""

    NAME = "fadeoutaudio"
    ARG_TYPE = int


class Greyscale(Command):
    """Makes the photo/video black and white"""

    NAME = "greyscale"


class InvertColours(Command):
    """Inverts the colours in the media."""

    NAME = "invert"


class Distort(Command):
    """Distorts the video with a wobble like effect"""

    NAME = "distort"
    ARG_TYPE = int


class Zoom(Command):
    """Zooms in the video. A value of zoom=2 would zoom it in 2x and so on."""

    NAME = "zoom"
    ARG_TYPE = int


class Blur(Command):
    """Blurs out the whole video"""

    NAME = "blur"
    ARG_TYPE = int


class Morph(Command):
    """Creates a motion blur effect on the video (not to be confused with blur= which just blurs the whole frame)"""

    NAME = "morph"
    ARG_TYPE = int


class Vignette(Command):
    """Puts a vignette effect on the video. Higher numbers make the vignette more visible."""

    NAME = "vignette"
    ARG_TYPE = int


class Volume(Command):
    """Adjusts the volume of the audio. Negative values or decibels decrease the volume, positive value increase it."""

    NAME = "volume"
    ARG_TYPE = Union[int, str]


# class Noise(Command):
#     """"Adds visual noise to the video (similar to the original VideoEditBot's 'acid' function)"""
#
#     NAME = "noise"
#     ARG_TYPE = int
#
#
class SeizureMode(Command):
    """Makes the video rapidly flash on and off."""

    NAME = "seizure"


class Disco(Command):
    """Creates a sort of weird flashing rainbow effect on the video"""

    NAME = "disco"
    ARG_TYPE = int


class RGBSplit(Command):
    """Separates the video into its red, green and blue parts. Higher numbers result in them being split even more."""

    NAME = "rgbsplit"
    ARG_TYPE = int


class HorizontalFlip(Command):
    """Flips the media horizontally."""

    NAME = "hflip"


class VerticalFlip(Command):
    """Flips the media vertically."""

    NAME = "vflip"


class DownloadVideo(Command):
    """Just put this in a reply to someone if you just want to download their video, not edit it or anything else.
    Does not work with any other commands. For videos only."""

    NAME = "downloadvid"


class Reverse(Command):
    """Reverses both the video and audio.
    Trying to use this with vreverse or areverse will return an error, or not process the video as you want."""

    NAME = "reverse"


class VideoReverse(Command):
    """Reverses the video only.
    Trying to use this with reverse or areverse will return an error, or not process the video as you want."""

    NAME = "vreverse"


class AudioReverse(Command):
    """Reverses the audio only.
    Trying to use this with reverse or vreverse will return an error, or not process the video as you want."""

    NAME = "areverse"


class Speed(Command):
    """Speeds up both the video and audio"""

    NAME = "speed"
    ARG_TYPE = float


class VideoSpeed(Command):
    """Speeds up the video only. Audio stays the same."""

    NAME = "vspeed"
    ARG_TYPE = float


class AudioSpeed(Command):
    """Speeds up the audio only. Video stays the same."""

    NAME = "aspeed"
    ARG_TYPE = float


class Bandicam(Command):
    """Adds a bandicam watermark to the top middle of your video
    (not sure why this is even a function but people seem to like it)."""

    NAME = "bndc"


class Commands(Enum):
    TOP_TEXT = TopText
    BOTTOM_TEXT = BottomText
    TOP_CAPTION = TopCaption
    BOTTOM_CAPTION = BottomCaption
    CAPTION = Caption
    MUSIC = Music
    MUSIC_SKIP = MusicSkip
    MUSIC_DELAY = MusicDelay
    LENGTH = Length
    MUFFLE = Muffle
    START_VIDEO = StartVideo
    END_VIDEO = EndVideo
    DEEP_FRY = DeepFry
    EQ_RISE = EqRise
    RICECAKE = Ricecake
    SHAKE = Shake
    HIGHPASS = Highpass
    SKETCH = Sketch
    SPIN = Spin
    PIXELATE = Pixelate
    GLOW = Glow
    TECHNICOLOR = Technicolor
    WIDEN = Widen
    HEIGHTEN = Heighten
    RASP = Rasp
    ECHO = Echo
    RANDOM_LAG = RandomLag
    ROTATE = Rotate
    FADE_IN = FadeIn
    FADE_OUT = FadeOut
    FADE_IN_AUDIO = FadeInAudio
    FADE_OUT_AUDIO = FadeOutAudio
    GREYSCALE = Greyscale
    INVERT_COLOURS = InvertColours
    DISTORT = Distort
    ZOOM = Zoom
    BLUR = Blur
    VIGNETTE = Vignette
    VOLUME = Volume
    SEIZURE_MODE = SeizureMode
    DISCO = Disco
    RGB_SPLIT = RGBSplit
    HORIZONTAL_FLIP = HorizontalFlip
    VERTICAL_FLIP = VerticalFlip
    DOWNLOAD_VIDEO = DownloadVideo
    REVERSE = Reverse
    VIDEO_REVERSE = VideoReverse
    AUDIO_REVERSE = AudioReverse
    SPEED = Speed
    VIDEO_SPEED = VideoSpeed
    AUDIO_SPEED = AudioSpeed
    BANDICAM = Bandicam


__all__ = ["Commands", "Command"]
