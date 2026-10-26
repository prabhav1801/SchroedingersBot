from ursina import *
import cv2
import math
from vision import ObserverVision
from bot import TransformerStateMachine

app = Ursina()

window.title = "Schrodinger's Bot - Final Fixed Edition"
window.color = color.black
window.size = (800, 600)

# --- UNIFIED COMPACT BOT RIG (Using unlit=True to force exact RGB colors) ---
bot = Entity(position=(0, 0, 0), scale=0.5)

# 1. Torso (Optimus Red)
torso = Entity(model='cube', color=color.rgb(215, 25, 33), unlit=True, scale=(1.4, 2.0, 0.8), parent=bot, position=(0, 0, 0))

# 2. Head (Blue) - Flush on top of torso
head = Entity(model='cube', color=color.rgb(15, 45, 140), unlit=True, scale=(0.6, 0.6, 0.6), parent=torso, position=(0, 1.3, 0))

# 3. Arms (Silver) - Flush against torso sides
left_arm = Entity(model='cube', color=color.rgb(200, 200, 200), unlit=True, scale=(0.35, 1.8, 0.35), parent=torso, position=(-0.9, 0, 0))
right_arm = Entity(model='cube', color=color.rgb(200, 200, 200), unlit=True, scale=(0.35, 1.8, 0.35), parent=torso, position=(0.9, 0, 0))

# 4. Legs (Blue) - Flush beneath torso
left_leg = Entity(model='cube', color=color.rgb(15, 45, 140), unlit=True, scale=(0.4, 1.8, 0.4), parent=torso, position=(-0.35, -1.9, 0))
right_leg = Entity(model='cube', color=color.rgb(15, 45, 140), unlit=True, scale=(0.4, 1.8, 0.4), parent=torso, position=(0.35, -1.9, 0))

# Fixed Camera framing
camera.position = (0, 0, -8)
camera.rotation = (0, 0, 0)

status_text = Text(text='STATUS: ROBOT PATROL', position=(-0.7, 0.4), scale=1.5, color=color.cyan)

vision = ObserverVision()
bot_sm = TransformerStateMachine()
cap = cv2.VideoCapture(0)

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
        # Smooth roaming patrol across screen
        bot.x = math.sin(roam_timer * 1.5) * 2.5
        bot.y = math.cos(roam_timer * 2.0) * 0.8
        bot.rotation_y = math.sin(roam_timer * 0.8) * 20
        
        # Solid Robot Form
        torso.scale = lerp(torso.scale, Vec3(1.4, 2.0, 0.8), 0.1)
        torso.color = color.rgb(215, 25, 33) # Red
        head.enabled = True
        left_arm.enabled = True
        right_arm.enabled = True
        left_leg.enabled = True
        right_leg.enabled = True
        
        status_text.text = "STATUS: ROBOT PATROL (Roaming)"
        status_text.color = color.cyan
    else:
        # Transforms into a sleek vehicle disguise when observed!
        bot.x = lerp(bot.x, 0, 0.1)
        bot.y = lerp(bot.y, -0.2, 0.1)
        bot.rotation_y = lerp(bot.rotation_y, 0, 0.1)
        
        # Vehicle Form (Retract limbs, flatten into a sleek car body)
        torso.scale = lerp(torso.scale, Vec3(3.2, 0.7, 1.8), 0.1)
        torso.color = color.rgb(220, 20, 20) # Bright car red
        head.enabled = False
        left_arm.enabled = False
        right_arm.enabled = False
        left_leg.enabled = False
        right_leg.enabled = False
        
        status_text.text = "STATUS: VEHICLE DISGUISE (OBSERVED!)"
        status_text.color = color.red

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Webcam (Press 'q' to quit)", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        bot_sm.save_telemetry("telemetry_log.json")
        application.quit()

app.run()
