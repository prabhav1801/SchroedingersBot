import os
import atexit
from ursina import *
import cv2

from vision import VideoStream, process_vision
from bot import TransformerBot

cap_stream = VideoStream(0)
atexit.register(cap_stream.release)

app = Ursina()
window.title = "Schrödinger's Bot"
window.color = color.rgb(10, 10, 15)
window.fps_counter.enabled = True

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

ground = Entity(model='plane', scale=(40, 1, 40), color=color.rgb(15, 15, 20))
grid_overlay = Entity(model='grid', scale=(40, 40, 40), color=color.cyan, y=0.01, alpha=0.3)
DirectionalLight(y=40, z=-30, color=color.white, shadows=True)
AmbientLight(color=color.rgb(40, 40, 70))

hud_status = Text(text="STATUS: PATROL", position=(-0.85, 0.40), scale=0.8, color=color.lime)
hud_metrics = Text(text="YAW: 0.0 | PITCH: 0.0 | FACE_W: 0", position=(-0.85, 0.35), scale=0.8, color=color.light_gray)

bot = TransformerBot(position=(0, 0, 0))

is_disguised = False
debounce = 0

def update():
    global is_disguised, debounce
    found, yaw, pitch, fw = False, None, None, 0
    
    success, frame = cap_stream.read()
    if success:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, int(640 * frame.shape[0] / frame.shape[1])))
        found, yaw, pitch, fw = process_vision(frame, face_cascade)

    target_state = found
    if target_state != is_disguised:
        debounce += 1
        if debounce > 2:
            is_disguised = target_state
            debounce = 0
    else:
        debounce = 0

    target_factor = 0.0 if is_disguised else 1.0
    bot.morph_factor = lerp(bot.morph_factor, target_factor, 8 * time.dt)
    bot.morph(bot.morph_factor)
    bot.navigate(is_disguised)

    if is_disguised:
        hud_status.text = "STATUS: DISGUISED (LOCKED)"
        hud_status.color = color.orange
    else:
        hud_status.text = "STATUS: PATROL (ROAMING)"
        hud_status.color = color.lime

    y_str = f"{yaw:.1f}" if yaw is not None else "N/A"
    p_str = f"{pitch:.1f}" if pitch is not None else "N/A"
    hud_metrics.text = f"YAW: {y_str} | PITCH: {p_str} | FACE_W: {fw}"

app.run()