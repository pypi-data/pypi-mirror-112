from pathlib import Path

import actionlib
import actionlib_msgs.msg
import rospy
from sound_play.msg import SoundRequest
from sound_play.msg import SoundRequestAction
from sound_play.msg import SoundRequestGoal


_sound_play_clients = {}


def play_sound(sound,
               lang='',
               topic_name='robotsound',
               volume=1.0,
               wait=False):
    """Plays sound using sound_play server

    Parameters
    ----------
    sound : str or int
        if sound is pathname, plays sound file located at given path
        if it is number, server plays builtin sound
        otherwise server plays sound as speech sentence
    topic_name : str
        namespace of sound_play server
    volume : float
        sound volume.
    wait : bool
        wait until sound is played
    """
    msg = SoundRequest(command=SoundRequest.PLAY_ONCE)
    if isinstance(sound, int):
        msg.sound = sound
    elif isinstance(sound, str) and Path(sound).exists():
        msg.sound = SoundRequest.PLAY_FILE
        msg.arg = sound
    elif isinstance(sound, str):
        msg.sound = SoundRequest.SAY
        msg.arg = sound
        msg.arg2 = lang
    else:
        raise ValueError

    if hasattr(msg, 'volume'):
        msg.volume = volume

    if topic_name in _sound_play_clients:
        client = _sound_play_clients[topic_name]
    else:
        client = actionlib.SimpleActionClient(
            topic_name,
            SoundRequestAction)
    client.wait_for_server()

    goal = SoundRequestGoal()
    if client.get_state() == actionlib_msgs.msg.GoalStatus.ACTIVE:
        client.cancel_goal()
        client.wait_for_result(timeout=rospy.Duration(10))
    goal.sound_request = msg
    _sound_play_clients[topic_name] = client
    client.send_goal(goal)

    if wait is True:
        client.wait_for_result(timeout=rospy.Duration(10))
    return client


def speak_en(text,
             topic_name='robotsound',
             volume=1.0,
             wait=False):
    """Speak english sentence

    Parameters
    ----------
    sound : str or int
        if sound is pathname, plays sound file located at given path
        if it is number, server plays builtin sound
        otherwise server plays sound as speech sentence
    topic_name : str
        namespace of sound_play server
    volume : float
        sound volume.
    wait : bool
        wait until sound is played
    """
    return play_sound(text,
                      topic_name=topic_name,
                      volume=volume,
                      wait=wait)


def speak_jp(text,
             topic_name='robotsound_jp',
             volume=1.0,
             wait=False):
    """Speak japanese sentence

    Parameters
    ----------
    sound : str or int
        if sound is pathname, plays sound file located at given path
        if it is number, server plays builtin sound
        otherwise server plays sound as speech sentence
    topic_name : str
        namespace of sound_play server
    volume : float
        sound volume.
    wait : bool
        wait until sound is played
    """
    return play_sound(text,
                      lang='ja',
                      topic_name=topic_name,
                      volume=volume,
                      wait=wait)
