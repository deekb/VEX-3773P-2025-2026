from CompetitionRobot import Robot as CompetitionRobot

class Robot(CompetitionRobot):
    def __init__(self, brain):
        super().__init__(brain)
        self.brain.screen.print("Testing Robot Initialized")
