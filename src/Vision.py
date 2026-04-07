import math


class Vision:
    def __init__(self, vision_sensor):
        self.vision_sensor = vision_sensor

    def get_adjustment_amount(self) -> float:
        """

        Returns: -1 to 1 for how hard to turn

        """
        ai_vision_3__LongGoal = Colordesc(1, 129, 66, 35, 12, 0.2)
        ai_objects = self.vision_sensor.take_snapshot(ai_vision_3__LongGoal)
        return math.copysign(math.exp2((160 - ai_objects[0].centerX) / 160), 160-ai_objects[0].centerX)

