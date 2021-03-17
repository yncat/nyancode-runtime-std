# -*- coding: utf-8 -*-
# Nyancode runtime module

import os
import random
import time
import wx
from .pybass import pybass


class InternalVars:
    last_one_shot_hstream = None  # 最後に再生したワンショットのストリームハンドル。「最後に再生した音を止める」のためにとっておく。
    last_environment_hstream = None  # 最後に再生した環境音のストリームハンドル。現在再生中でも、名前は last。上と合わせている。


class Options:
    # データディレクトリのルートを指定する。
    data_directory = ""
    # 親ウィンドウを指定する。
    parent_window = None


def configure(data_directory, parent_window):
    """モジュールの初期設定を受け取って保存する。"""
    options.data_directory = data_directory
    options.parent_window = parent_window


def onStart():
    pass


def onExit():
    if internalVars.last_environment_hstream:
        pybass.BASS_ChannelSlideAttribute(
            internalVars.last_environment_hstream, pybass.BASS_ATTRIB_VOL, 0, 500)
        time.sleep(0.6)
        pybass.BASS_ChannelStop(internalVars.last_environment_hstream)


def message(title, message):
    """メッセージを表示"""
    dlg = wx.MessageDialog(options.parent_window, message, title, wx.OK)
    dlg.ShowModal()


def question(title, message):
    """質問ダイアログを表示"""
    dlg = wx.MessageDialog(options.parent_window, message, title, wx.YES_NO)
    return dlg.ShowModal() == wx.ID_YES


def wait(t):
    """一定時間待つ"""
    time.sleep(t)


def randomPattern(max):
    """1から max までの整数を生成"""
    return random.randint(1, max)


def playOneShot(path, wait=False):
    hstream = pybass.BASS_StreamCreateFile(False, getRealPath(
        path), 0, 0, pybass.BASS_UNICODE | pybass.BASS_STREAM_AUTOFREE)
    pybass.BASS_ChannelPlay(hstream, True)
    if wait:
        _waitOneShot(hstream)


def playEnvironment(path):
    hstream = pybass.BASS_StreamCreateFile(
        False,
        getRealPath(path),
        0,
        0,
        pybass.BASS_UNICODE | pybass.BASS_STREAM_AUTOFREE | pybass.BASS_SAMPLE_LOOP)
    pybass.BASS_ChannelSetAttribute(hstream, pybass.BASS_ATTRIB_VOL, 0)
    pybass.BASS_ChannelPlay(hstream, True)
    pybass.BASS_ChannelSlideAttribute(
        hstream, pybass.BASS_ATTRIB_VOL, 0.5, 500)
    internalVars.last_environment_hstream = hstream


def _waitOneShot(hstream):
    while pybass.BASS_ChannelIsActive(hstream) == pybass.BASS_ACTIVE_PLAYING:
        time.sleep(0.02)


# initialization
internalVars = InternalVars()
options = Options()
if pybass.BASS_Init(-1, 44100, 0, 0, 0) is False:
    raise ImportError("could not initialize audio")


def getRealPath(path):
    return os.path.join(options.data_directory, path)
