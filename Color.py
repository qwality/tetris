from dataclasses import dataclass, astuple

@dataclass
class Color:
    black       :tuple = ( 10,  0,  0)
    soft_grey   :tuple = ( 60, 62, 65)
    dark_grey   :tuple = ( 35, 32, 30)
    white       :tuple = (255,255,255)
    red         :tuple = (220, 40, 30)
    green       :tuple = ( 30,200, 40)
    blue        :tuple = ( 30, 40,200)
    yellow      :tuple = (255,220,  0)

    __instance = None

    @classmethod
    def lighter(cls, color, factor):
        return tuple(max(0, i - factor) for i in color)
    
    @classmethod
    def darker(cls, color, factor):
        return tuple(min(255, i + factor) for i in color)


    @classmethod
    @property
    def colors(cls):
        if cls.__instance is None: cls.__instance = Color()
        return astuple(cls.__instance)
