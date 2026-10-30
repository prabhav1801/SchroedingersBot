import atexit
from ursina import *
import cv2
import math
from vision import ObserverVision
from bot import TransformerStateMachine

app = Ursina()

window.title = "Schrodinger's Bot"
window.color = color.black
window.size = (800, 600)

# Bot built from cubes; unlit=True keeps the exact RGB colors
bot = Entity(position=(0, 0, 0), scale=0.5)

# torso
torso = Entity(model='cube', color=color.rgb(215, 25, 33), unlit=True, scale=(1.4, 2.0, 0.8), parent=bot, position=(0, 0, 0))

# head
head = Entity(model='cube', color=color.rgb(15, 45, 140), unlit=True, scale=(0.6, 0.6, 0.6), parent=torso, position=(0, 1.3, 0))

# arms
left_arm = Entity(model='cube', color=color.rgb(200, 200, 200), unlit=True, scale=(0.35, 1.8, 0.35), parent=torso, position=(-0.9, 0, 0))
right_arm = Entity(model='cube', color=color.rgb(200, 200, 200), unlit=True, scale=(0.35, 1.8, 0.35), parent=torso, position=(0.9, 0, 0))

# legs
left_leg = Entity(model='cube', color=color.rgb(15, 45, 140), unlit=True, scale=(0.4, 1.8, 0.4), parent=torso, position=(-0.35, -1.9, 0))
right_leg = Entity(model='cube', color=color.rgb(15, 45, 140), unlit=True, scale=(0.4, 1.8, 0.4), parent=torso, position=(0.35, -1.9, 0))

# fixed camera
camera.position = (0, 0, -8)
camera.rotation = (0, 0, 0)

status_text = Text(text='STATUS: ROBOT PATROL', position=(-0.7, 0.4), scale=1.5, color=color.cyan)

vision = ObserverVision()
bot_sm = TransformerStateMachine()
cap = cv2.VideoCapture(0)
atexit.register(lambda: (cap.release(), bot_sm.save_telemetry("telemetry_log.json")))

roam_timer = 0

def update():
    global roam_timer
    ret, frame = cap.read()
    if not ret:
        return

    is_observed, faces = vision.check_observer(frame)
    state, progress = bot_sm.update(is_observed)
    
    roam_timer += 1 * time.dt
    
    if state == "ROBOT_PATROL":
        # patrol: roam along a sine/cosine path
        bot.x = math.sin(roam_timer * 1.5) * 2.5
        bot.y = math.cos(roam_timer * 2.0) * 0.8
        bot.rotation_y = math.sin(roam_timer * 0.8) * 20

        # robot form
        torso.scale = lerp(torso.scale, Vec3(1.4, 2.0, 0.8), 0.1)
        torso.color = color.rgb(215, 25, 33) 
        head.enabled = True
        left_arm.enabled = True
        right_arm.enabled = True
        left_leg.enabled = True
        right_leg.enabled = True

        status_text.text = "STATUS: ROBOT PATROL"
        status_text.color = color.cyan
    else:
        # observed: move to center and flatten into the vehicle form
        bot.x = lerp(bot.x, 0, 0.1)
        bot.y = lerp(bot.y, -0.2, 0.1)
        bot.rotation_y = lerp(bot.rotation_y, 0, 0.1)

        torso.scale = lerp(torso.scale, Vec3(3.2, 0.7, 1.8), 0.1)
        torso.color = color.rgb(220, 20, 20) 
        head.enabled = False
        left_arm.enabled = False
        right_arm.enabled = False
        left_leg.enabled = False
        right_leg.enabled = False

        status_text.text = "STATUS: VEHICLE DISGUISE (face detected)"
        status_text.color = color.red

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Webcam (Press 'q' to quit)", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        application.quit()

app.run()
