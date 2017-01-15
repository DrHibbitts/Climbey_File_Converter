from collections import OrderedDict

STATIC_BLOCKS = ['Icy', 'Spikes', 'Metal', 'Glass', 'Lava', 'Grabbable', 'Spikes', 'Jumpy', 'GravityField', '[CameraRig]', 'Finishline']
GAME_MODES = [0]

class Block:
    # public class Block {
    # 	public string Type;
    # 	public Vector3 Size;
    # 	public Vector3 Position;
    # 	public Quaternion Rotation;
    # 	public bool LockX,LockY,LockZ;
    # }
    OVERRIDES = {
        '[CameraRig]' : {
            "Size" : [1.0, 1.0, 1.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0]
        },
        'Finishline' : {
            "Size" : [0.5, 1.0, 0.5],
            "Rotation" : [0.0, 0.0, 0.0, 1.0]
        }
    }
    def __init__(self, Type, Size, Position, Rotation, LockX, LockY, LockZ):
        self.Type = Type
        self.Size = Size
        self.Position = Position
        self.Rotation = Rotation
        self.LockX = bool(LockX)
        self.LockY = bool(LockY)
        self.LockZ = bool(LockZ)

    def toJSON(self):
        a = OrderedDict([
            ("Type", self.Type),
            ("Size", self.Size),
            ("Position", self.Position),
            ("Rotation", self.Rotation),
            ("LockX", self.LockX),
            ("LockY", self.LockY),
            ("LockZ", self.LockZ)
        ])

        # Some blocks are special and have set values
        if self.Type in self.OVERRIDES:
            for key, value in self.OVERRIDES[self.Type].iteritems():
                a[key] = value

        # Vectors are stored as a dict with keys x y and z
        for k in ["Size", "Position"]:
            a[k] = {axis: value for axis, value in zip(['x','y','z'], a[k])}

        # Quaternions are stored as a dict with keys x y z and w
        # Written in a loop in case of future Quaternions and to keep a consistent style
        for k in ["Rotation"]:
            a[k] = {axis: value for axis, value in zip(['x','y','z','w'], a[k])}

        return a

class SignBlock:
    # [System.Serializable]
    # public class SignBlock : Block{
    # 	public string text;
    # }
    def __init__(self, block, text):
        assert isinstance(block, Block)
        self.block = block
        self.text = str(text)

    def toJSON(self):
        a = self.block.toJSON()
        a["text"] = self.text
        return a

class ZiplineBlock:
    # [System.Serializable]
    # public class ZiplineBlock : Block{
    # 	public Block[] PoleBlocks;
    # }
    def __init__(self, block, PoleBlocks):
        assert isinstance(block, Block)
        self.block = block
        assert isinstance(PoleBlocks, list) and isinstance(PoleBlocks[0], Block)
        self.PoleBlocks = PoleBlocks

    def toJSON(self):
        a = self.block.toJSON()
        a["PoleBlocks"] = [block.toJSON() for block in self.PoleBlocks]
        return a

class MovingBlock:
    # [System.Serializable]
    # public class MovingBlock : Block {
    # 	public List<Block> Waypoints = new List<Block>();
    # 	public float ArrivalTime;
    # 	public float Speed;
    # 	public bool PingPong;
    # 	public bool WaitForPlayer;
    # }
    def __init__(self, block, Waypoints, ArrivalTime, Speed, PingPong, WaitForPlayer):
        assert isinstance(block, Block)
        self.block = block
        assert isinstance(Waypoints, list) and isinstance(Waypoints[0], Block)
        self.Waypoints = Waypoints
        self.ArrivalTime = float(ArrivalTime)
        self.Speed = float(Speed)
        self.PingPong = bool(PingPong)
        self.WaitForPlayer = bool(WaitForPlayer)

    def toJSON(self):
        a = self.block.toJSON()
        a["Waypoints"] = [point.toJSON() for point in self.Waypoints]
        a["ArrivalTime"] = self.ArrivalTime
        a["Speed"] = self.Speed
        a["PingPing"] = self.PingPong
        a["WaitForPlayer"] = self.WaitForPlayer
        return a

class SettingsBlock:
    # [System.Serializable]
    # public class SettingsBlock : Block {
    # 	public int Checkpoints = 3;
    # 	public GamemodeTypes Gamemode;
    # }
    def __init__(self, block, Checkpoints = 3, Gamemode = GAME_MODES[0]):
        self.block = block
        self.Checkpoints = int(Checkpoints)
        assert Gamemode in GAME_MODES
        self.Gamemode = Gamemode

    def toJSON(self):
        a = self.block.toJSON()
        a["Checkpoints"] = self.Checkpoints
        a["Gamemode"] = self.Gamemode
        return a