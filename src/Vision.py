import math

from Constants import DrivetrainProperties


class Vision:
    def __init__(self, vision_sensor):
        self.vision_sensor = vision_sensor
        self.TARGET_ASPECT_RATIO = 140/62

    def get_adjustment_amount(self) -> float:
        """
        Returns: -1 to 1 for how hard to turn
        """

        ai_objects = self.vision_sensor.take_snapshot(DrivetrainProperties.LONG_GOAL_COLOR_DESC)
        if not ai_objects:
            return 0

        best_aspect_ratio = None

        for ai_object in ai_objects:
            aspect_ratio = (ai_object.height / ai_object.width)
            if not best_aspect_ratio:
                best_aspect_ratio = ai_object
                continue
            if abs(aspect_ratio - self.TARGET_ASPECT_RATIO) < abs(aspect_ratio - (best_aspect_ratio.height / best_aspect_ratio.width)):
                best_aspect_ratio = ai_object

        return math.copysign(((160 - best_aspect_ratio.centerX) / 160) ** 2, 160 - best_aspect_ratio.centerX)
