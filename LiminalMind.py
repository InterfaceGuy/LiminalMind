import importlib
import pydeation.imports
importlib.reload(pydeation.imports)
from pydeation.imports import *
from HeadWithShoulders.HeadWithShoulders import HeadWithShoulders


class LiminalitySymbol(CustomObject):
    """the trinity symbol consisting of a circle, a rectangle, the tilde and an arrow connection"""

    def __init__(self, relationship=None, diameter=10, **kwargs):
        self.relationship = relationship
        super().__init__(**kwargs)

    def specify_parts(self):
        self.left_semi_circle = Arc(start_angle=PI, end_angle=2*PI, radius=50, color=RED)
        self.left_semi_circle.move(x=-self.left_semi_circle.radius)
        self.left_semi_circle.rotate(h=PI, p=PI/2)
        self.right_semi_circle = Arc(start_angle=0, end_angle=PI, radius=50, color=RED)
        self.right_semi_circle.move(x=self.right_semi_circle.radius)
        self.right_semi_circle.rotate(h=PI, p=PI/2)
        self.tilde = Group(self.left_semi_circle, self.right_semi_circle, h=PI/4, name="Tilde")
        self.circle = Circle(radius=15, x=35, z=35, color=RED, plane="xz", filled=True)
        self.rectangle = Rectangle(width=25, height=25, x=-35, z=-35, color=RED, plane="xz", filled=True)
        self.parts = [self.tilde, self.circle, self.rectangle]
        if self.relationship == "right":
            self.arrow = Arrow(start_point=(-22, 0, -22), stop_point=(20, 0, 20))
            self.parts.append(self.arrow)
        elif self.relationship == "wrong":
            self.arrow = Arrow(stop_point=(-20, 0, -20), start_point=(24, 0, 24))
            self.parts.append(self.arrow)


    def specify_creation(self):
            creation_action = XAction(
                Movement(self.right_semi_circle.creation_parameter, (0, 1), part=self.right_semi_circle),
                Movement(self.left_semi_circle.creation_parameter, (0, 1), part=self.left_semi_circle),
                Movement(self.circle.creation_parameter, (0, 1), part=self.circle),
                Movement(self.rectangle.creation_parameter, (0, 1), part=self.rectangle),
                target=self, completion_parameter=self.creation_parameter, name="Creation")

    def specify_parameters(self):
        self.fold_parameter = UAngle(
            name="FoldParameter", default_value=-PI)
        self.parameters += [self.fold_parameter]

    def specify_relations(self):
        fold_relation = XRelation(part=self.left_semi_circle, whole=self, desc_ids=[ROT_H],
                                  parameters=[self.fold_parameter],
                                  formula=f"{self.fold_parameter.name}")

    def specify_action_parameters(self):
        self.fold_action_parameter = UCompletion(
            name="Fold", default_value=0)
        self.action_parameters += [self.fold_action_parameter]

    def specify_actions(self):
        fold_action = XAction(
            Movement(self.fold_parameter, (0, 1), output=(-PI, 0)),
            target=self, completion_parameter=self.fold_action_parameter, name="Fold")

    def fold(self, completion=1):
        """specifies the fold animation"""
        desc_id = self.fold_action_parameter.desc_id
        animation = ScalarAnimation(
            target=self, descriptor=desc_id, value_fin=completion)
        self.obj[desc_id] = completion
        return animation



class LiminalMind(CustomObject):

    def specify_parts(self):
        self.liminality_symbol = LiminalitySymbol()
        self.head = Human(y=-10, filled=True, fill_color=BLACK)
        self.parts += [self.liminality_symbol, self.head]

    def specify_creation(self):
        creation_action = XAction(
            Movement(self.liminality_symbol.creation_parameter, (1/3, 1), part=self.liminality_symbol),
            Movement(self.head.creation_parameter, (0, 2/3), part=self.head),
            target=self, completion_parameter=self.creation_parameter, name="Creation")


class LiminalMind3D(CustomObject):

    def specify_parts(self):
        self.liminality_symbol = LiminalitySymbol()
        self.head = HeadWithShoulders(scale=2.8, y=-70, z=7)
        self.parts += [self.liminality_symbol, self.head]

    def specify_creation(self):
        creation_action = XAction(
            Movement(self.liminality_symbol.creation_parameter, (0, 1), part=self.liminality_symbol),
            Movement(self.head.creation_parameter, (0, 1), part=self.head),
            target=self, completion_parameter=self.creation_parameter, name="Creation")


if __name__ == "__main__":
    liminal_mind = LiminalMind3D(creation=True)