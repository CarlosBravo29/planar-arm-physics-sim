
class ArmAnimation:
    def __init__(self, root, robot, frame_ms=16):
        self.root = root
        self.robot = robot
        self.frame_ms = frame_ms
        self.frames = []
        self.current_frame = 0
        self.running = False
        self.on_frame = None
        self.on_finish = None

    def play(self, frames, on_frame=None, on_finish=None):
        if not frames:
            return
        self.frames = frames
        self.current_frame = 0
        self.running = True
        self.on_frame = on_frame
        self.on_finish = on_finish
        self._play_next_frame()

    def _play_next_frame(self):
        if not self.running:
            return
        if self.current_frame >= len(self.frames):
            self.running = False
            if self.on_finish:
                self.on_finish()
            return

        angles, points = self.frames[self.current_frame]
        self.robot.set_position(points, angles)

        if self.on_frame:
            self.on_frame(angles, points)

        self.current_frame += 1
        self.root.after(self.frame_ms, self._play_next_frame)

    def stop(self):
        self.running = False