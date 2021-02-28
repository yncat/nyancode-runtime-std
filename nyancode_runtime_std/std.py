# -*- coding: utf-8 -*-
# Nyancode runtime module

import os
import random
import time
import wx
from .pybass import pybass


last_one_shot_hstream = None  # 最後に再生したワンショットのストリームハンドル。「最後に再生した音を止める」のためにとっておく。


class Options:
    # データディレクトリのルートを指定する。
    data_directory = ""


options = Options()


def configure(data_directory):
    """モジュールの初期設定を受け取って保存する。"""
    options.data_directory = data_directory


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


def playOneShot(path):
    hstream = pybass.BASS_StreamCreateFile(False, getRealPath(
        path), 0, 0, pybass.BASS_UNICODE | pybass.BASS_STREAM_AUTOFREE)
    pybass.BASS_ChannelPlay(hstream, True)


# initialization
if pybass.BASS_Init(-1, 44100, 0, 0, 0) is False:
    raise ImportError("could not initialize audio")


def getRealPath(path):
    return os.path.join(options.data_directory, path)
