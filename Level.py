from collections import OrderedDict

class Level:
    # [System.Serializable]
    # public class Level {
    # 	public Block[] LevelArray;
    # 	public MovingBlock[] MovingArray;
    # 	public SettingsBlock LevelSettings;
    # 	public SignBlock[] SignsArray;
    # 	public ZiplineBlock[] ZiplinesArray;
    # }
    def __init__(self, LevelArray, MovingArray, LevelSettings, SignsArray, ZiplinesArray):
        self.LevelArray = LevelArray
        self.MovingArray = MovingArray
        self.LevelSettings = LevelSettings
        self.SignsArray = SignsArray
        self.ZiplinesArray = ZiplinesArray

    def toJSON(self):
        return OrderedDict(
            [
                ("LevelArray", [block.toJSON() for block in self.LevelArray]),
                ("MovingArray", [moving_block.toJSON() for moving_block in self.MovingArray]),
                ("LevelSettings", self.LevelSettings.toJSON()),
                ("SignsArray", [sign.toJSON() for sign in self.SignsArray]),
                ("ZiplinesArray", [zipline.toJSON() for zipline in self.ZiplinesArray])
            ]
        )