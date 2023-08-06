# flake8: noqa

import pkg_resources


__version__ = pkg_resources.get_distribution("ros-speak").version


from ros_speak.play_sound_lib import play_sound
from ros_speak.play_sound_lib import speak_en
from ros_speak.play_sound_lib import speak_jp
