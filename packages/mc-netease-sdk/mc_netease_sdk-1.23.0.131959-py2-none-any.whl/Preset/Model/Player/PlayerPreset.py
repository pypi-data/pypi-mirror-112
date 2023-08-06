# -*- coding: utf-8 -*-

from Preset.Model.Entity.EntityPreset import EntityPreset

class PlayerPreset(EntityPreset):
    def __init__(self):
        # type: () -> None
        """
        PlayerPreset（玩家预设）是一类特殊的实体预设，玩家预设与玩家实体进行绑定。每个AddOn（编辑器作品）只允许创建一个玩家预设。如果玩家同时启用了多个使用了玩家预设的AddOn，只会加载第一个玩家预设。
        """
        self.entityId = None

    def GetPlayerId(self):
        # type: () -> str
        """
        获取玩家预设的玩家ID
        """
        pass

