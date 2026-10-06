import random
from ursina import *

class TransformerBot(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rig = Entity(parent=self, position=(0,0,0))
        
        self.r_torso = Entity(parent=self.rig, model='cube', color=color.red, scale=(1.1, 1.2, 0.6), position=(0, 1.2, 0))
        self.r_head = Entity(parent=self.rig, model='cube', color=color.blue, scale=(0.5, 0.5, 0.5), position=(0, 2.05, 0))
        self.r_arms = [
            Entity(parent=self.rig, model='cube', color=color.blue, scale=(0.3, 1.1, 0.3), position=(-0.75, 1.2, 0)),
            Entity(parent=self.rig, model='cube', color=color.blue, scale=(0.3, 1.1, 0.3), position=(0.75, 1.2, 0))
        ]
        self.r_legs = [
            Entity(parent=self.rig, model='cube', color=color.blue, scale=(0.4, 1.0, 0.4), position=(-0.3, 0.5, 0)),
            Entity(parent=self.rig, model='cube', color=color.blue, scale=(0.4, 1.0, 0.4), position=(0.3, 0.5, 0))
        ]

        self.v_body = Entity(parent=self.rig, model='cube', color=color.red, scale=(1.6, 0.9, 2.2), position=(0, 0.5, -0.2))
        self.v_cabin = Entity(parent=self.rig, model='cube', color=color.cyan, scale=(1.4, 0.4, 0.8), position=(0, 0.7, 0.4))
        self.v_grille = Entity(parent=self.rig, model='cube', color=color.light_gray, scale=(1.5, 0.5, 0.5), position=(0, 0.3, 1.1))

        self.morph_factor = 1.0
        self.target_x = 0.0
        self.target_z = 0.0
        self.speed = 2.0
        self.wander_interval = random.uniform(3, 6)
        self.move_timer = 0.0

    def morph(self, factor):
        self.r_torso.scale = Vec3(1.1, 1.2, 0.6) * factor
        self.r_head.scale = Vec3(0.5, 0.5, 0.5) * factor
        for arm in self.r_arms: arm.scale = Vec3(0.3, 1.1, 0.3) * factor
        for leg in self.r_legs: leg.scale = Vec3(0.4, 1.0, 0.4) * factor

        inv = 1.0 - factor
        self.v_body.scale = Vec3(1.6, 0.9, 2.2) * inv
        self.v_cabin.scale = Vec3(1.4, 0.4, 0.8) * inv
        self.v_grille.scale = Vec3(1.5, 0.5, 0.5) * inv

    def navigate(self, disguised):
        if not disguised:
            self.move_timer += time.dt
            curr = Vec3(self.x, 0, self.z)
            target = Vec3(self.target_x, 0, self.target_z)
            
            if self.move_timer > self.wander_interval or distance(curr, target) < 0.5:
                self.target_x = random.uniform(-10, 10)
                self.target_z = random.uniform(-10, 10)
                self.speed = random.uniform(1.5, 3.0)
                self.wander_interval = random.uniform(3, 6)
                self.move_timer = 0.0
                
            dir_vec = target - curr
            if dir_vec.length() > 0.05:
                dir_vec = dir_vec.normalized()
                self.position += dir_vec * self.speed * time.dt
                self.look_at(self.position + dir_vec)