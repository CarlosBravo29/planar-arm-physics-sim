
class ProgramExecutor:
    def __init__(self, move_callback, set_callback, finish_callback=None):
        self.move_callback = move_callback
        self.set_callback = set_callback
        self.finish_callback = finish_callback

        self.instructions = []
        self.current_instruction = 0
        self.running = False

    def run(self, ast):
        if not ast:
            return
        self.instructions = ast
        self.current_instruction = 0
        self.running = True

        self._execute_next()

    def _execute_next(self):
        if not self.running:
            return
        if self.current_instruction >= len(self.instructions):
            self.running = False
            if self.finish_callback:
                self.finish_callback()
            return
        instruction = self.instructions[self.current_instruction]
        action = instruction["action"]
        if action == "MoveL":
            self.move_callback(instruction, self._instruction_finished)
        elif action == "SET":
            self.set_callback(instruction)
            self._instruction_finished()
        else:
            raise ValueError(f"Unknown instruction: {action}")

    def _instruction_finished(self):
        self.current_instruction += 1
        self._execute_next()

    def stop(self):
        self.running = False