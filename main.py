from ursina import *
import math
import random

app = Ursina()

sky = Sky()

ground = Entity(
    model='plane', 
    scale=(20000, 1, 20000), 
    color=color.green.tint(-0.3), 
    texture='white_cube', 
    texture_scale=(10000, 10000),
    collider='box',
    name='ground'
)

runway = Entity(
    model='plane',
    scale=(12, 1, 400),
    color=color.dark_gray,
    position=(0, 0.01, 150),
    name='runway'
)

for z_pos in range(0, 360, 30):
    Entity(model='plane', scale=(0.4, 1, 10), color=color.white, position=(0, 0.02, z_pos))

building_entities = []
building_data = [
    {'pos': (-40, 15, 120), 'scale': (15, 30, 15)},
    {'pos': (-65, 25, 200), 'scale': (20, 50, 20)},
    {'pos': (-45, 20, 280), 'scale': (18, 40, 18)},
    {'pos': (-80, 35, 350), 'scale': (25, 70, 25)},
    {'pos': (-50, 10, 420), 'scale': (15, 20, 15)},
    {'pos': (40, 20, 150), 'scale': (16, 40, 16)},
    {'pos': (70, 15, 230), 'scale': (22, 30, 22)},
    {'pos': (45, 30, 310), 'scale': (15, 60, 15)},
    {'pos': (85, 40, 390), 'scale': (30, 80, 30)},
    {'pos': (55, 25, 460), 'scale': (20, 50, 20)},
    {'pos': (-110, 30, 180), 'scale': (22, 60, 22)},
    {'pos': (-95, 20, 260), 'scale': (18, 40, 18)},
    {'pos': (-120, 45, 400), 'scale': (26, 90, 26)},
    {'pos': (-75, 15, 490), 'scale': (15, 30, 15)},
    {'pos': (110, 25, 190), 'scale': (20, 50, 20)},
    {'pos': (100, 35, 280), 'scale': (24, 70, 24)},
    {'pos': (130, 50, 360), 'scale': (30, 100, 30)},
    {'pos': (90, 15, 440), 'scale': (16, 30, 16)},
    {'pos': (-30, 20, 530), 'scale': (20, 40, 20)},
    {'pos': (30, 25, 550), 'scale': (18, 50, 18)}
]

for data in building_data:
    bx, by, bz = data['pos']
    bld_y = data['scale'][1] / 2
    
    bld = Entity(
        model='cube',  
        color=color.light_gray,
        position=(bx, bld_y, bz),
        scale=data['scale'],
        name='building' 
    )
    building_entities.append(bld)

    b_width, b_height, b_depth = data['scale']
    floors = int(b_height / 4)
    windows_x = int(b_width / 3)
    windows_z = int(b_depth / 3)
    
    for floor in range(floors):
        y_pos = (floor / floors) - 0.5 + (0.5 / floors)
        for win in range(windows_x):
            x_pos = (win / windows_x) - 0.5 + (0.5 / windows_x)
            Entity(parent=bld, model='quad', color=color.azure, scale=(0.4/b_width, 1.5/b_height), position=(x_pos, y_pos, 0.51))
            Entity(parent=bld, model='quad', color=color.azure, scale=(0.4/b_width, 1.5/b_height), position=(x_pos, y_pos, -0.51))
        for win in range(windows_z):
            z_pos = (win / windows_z) - 0.5 + (0.5 / windows_z)
            Entity(parent=bld, model='quad', color=color.azure, scale=(0.4/b_depth, 1.5/b_height), position=(-0.51, y_pos, z_pos), rotation_y=90)
            Entity(parent=bld, model='quad', color=color.azure, scale=(0.4/b_depth, 1.5/b_height), position=(0.51, y_pos, z_pos), rotation_y=90)

hills_entities = [] 
hills_data = [
    {'pos': (-210, 0, 320), 'scale': (80, 45, 80), 'sub_count': 4},   
    {'pos': (220, 0, 220), 'scale': (90, 50, 90), 'sub_count': 4},    
    {'pos': (0, -15, 750), 'scale': (160, 110, 160), 'sub_count': 6}, 
    {'pos': (-350, -5, 850), 'scale': (110, 65, 110), 'sub_count': 4},
    {'pos': (360, -5, 950), 'scale': (120, 70, 120), 'sub_count': 5},
    {'pos': (-260, 0, 150), 'scale': (70, 35, 70), 'sub_count': 3},   
    {'pos': (270, 0, 400), 'scale': (85, 55, 85), 'sub_count': 4},    
    {'pos': (-180, -5, 600), 'scale': (100, 60, 100), 'sub_count': 5},
    {'pos': (190, -5, 650), 'scale': (95, 55, 95), 'sub_count': 4},   
    {'pos': (-500, -10, 450), 'scale': (150, 80, 150), 'sub_count': 5}
]

random.seed(42)

for h_data in hills_data:
    cx, cy, cz = h_data['pos']
    base_w, base_h, base_d = h_data['scale']
    
    hill_anchor = Entity(position=(cx, cy, cz), name='hill_group')
    
    for i in range(h_data['sub_count']):
        offset_x = random.uniform(-base_w * 0.25, base_w * 0.25) if i > 0 else 0
        offset_z = random.uniform(-base_d * 0.25, base_d * 0.25) if i > 0 else 0
        offset_y = random.uniform(-base_h * 0.15, 0) if i > 0 else 0
        
        sub_w = base_w * random.uniform(0.7, 1.1)
        sub_h = base_h * random.uniform(0.6, 1.0)
        sub_d = base_d * random.uniform(0.7, 1.1)
        sub_rot_y = random.uniform(0, 360)
        
        sub_hill = Entity(
            parent=hill_anchor,
            model='sphere',
            color=color.gray.tint(random.uniform(-0.08, 0.08)), 
            texture='white_cube',
            texture_scale=(6, 6),
            position=(offset_x, offset_y, offset_z),
            scale=(sub_w, sub_h, sub_d),
            rotation_y=sub_rot_y,
            name='sub_hill'
        )
        hills_entities.append(sub_hill)

drone_specs = {
    'plane': {
        'name_display': 'Тип 1 (Самолет)',
        'mass': 4.5,           
        'max_thrust': 52.0,    
        'drag_coef': 0.08,     
        'side_drag': 0.6,      
        'lift_factor': 0.95,   
        'min_height': 0.55
    },
    'scout_wing': {
        'name_display': 'Тип 2 (Крыло)',
        'mass': 1.8,           
        'max_thrust': 130.0,   
        'drag_coef': 0.05,     
        'side_drag': 0.25,     
        'lift_factor': 0.99,
        'min_height': 0.4
    }
}

drone_types = ['plane', 'scout_spec'] 
drone_keys = ['plane', 'scout_wing']   
current_drone_index = 0
current_spec = drone_specs['plane']

velocity = Vec3(0, 0, 0)      
target_throttle = 0.0         
current_throttle = 0.0        
GRAVITY = 9.81                
target_takeoff_height = 15.0  

wind_enabled = False
wind_force = 0.0
wind_angle = 90.0

drone = Entity(model='cube', color=color.gray, scale=(0.5, 0.4, 3.0), position=(0, 0.55, 0))

wings = Entity(parent=drone, model='cube', color=color.orange, scale=(6.0, 0.05, 0.8), position=(0, 0, 0.2))
tail_horizontal = Entity(parent=drone, model='cube', color=color.dark_gray, scale=(1.8, 0.04, 0.4), position=(0, 0, -1.3))
tail_vertical = Entity(parent=drone, model='cube', color=color.orange, scale=(0.04, 0.8, 0.4), position=(0, 0.4, -1.3))
propeller = Entity(parent=drone, model='cube', color=color.white, scale=(1.2, 0.05, 0.05), position=(0, 0, 1.5))

explosion_cloud = Entity(model='sphere', color=color.black66, scale=0, enabled=False)

static_screen = Entity(parent=camera.ui, model='quad', color=color.dark_gray, scale=(2, 2), enabled=False)
static_text = Text(parent=static_screen, text='НЕТ СИГНАЛА / SIGNAL LOST', origin=(0, 0), scale=2, color=color.red)

state = 'on_ground' 
pitch_speed = 45.0
roll_speed = 60.0     
camera_mode = 'chase'

takeoff_btn = Button(text='Взлет', color=color.green, scale=(0.14, 0.06), position=(-0.72, 0.45), text_size=0.8)
landing_btn = Button(text='Посадка', color=color.red, scale=(0.14, 0.06), position=(-0.56, 0.45), text_size=0.8)

wind_btn = Button(text='Ветер: НЕТ', color=color.azure, scale=(0.20, 0.06), position=(-0.37, 0.45), text_size=0.7)

wind_force_down = Button(text='-', color=color.dark_gray, scale=(0.04, 0.06), position=(-0.23, 0.45))
wind_force_up = Button(text='+', color=color.dark_gray, scale=(0.04, 0.06), position=(-0.18, 0.45))
wind_rot_left = Button(text='<-', color=color.black66, scale=(0.04, 0.06), position=(-0.13, 0.45))
wind_rot_right = Button(text='->', color=color.black66, scale=(0.04, 0.06), position=(-0.08, 0.45))

drone_select_btn = Button(text='БПЛА: Тип 1', color=color.violet, scale=(0.24, 0.06), position=(0.07, 0.45), text_size=0.8)

telemetry_text = Text(text='', position=(-0.7, 0.33), scale=1.2, color=color.white)

altimeter_bg = Entity(parent=camera.ui, model='quad', color=color.black66, scale=(0.04, 0.5), position=(0.68, 0.2))
Text(parent=camera.ui, text='50м', position=(0.71, 0.43), scale=0.8)
Text(parent=camera.ui, text='25м', position=(0.71, 0.2), scale=0.8)
Text(parent=camera.ui, text='0м', position=(0.71, -0.03), scale=0.8)
altimeter_pointer = Entity(parent=camera.ui, model='quad', color=color.red, scale=(0.03, 0.01), position=(0.68, -0.03))

roll_bg = Entity(parent=camera.ui, model='circle', color=color.black66, scale=(0.14, 0.14), position=(0.68, -0.28))
Text(parent=camera.ui, text='Л', position=(0.59, -0.29), scale=0.7, color=color.light_gray)
Text(parent=camera.ui, text='П', position=(0.75, -0.29), scale=0.7, color=color.light_gray)
roll_pointer = Entity(parent=camera.ui, model='quad', color=color.orange, scale=(0.1, 0.008), position=(0.68, -0.28))

compass_digital = Text(parent=camera.ui, text='0°', position=(-0.02, 0.46), scale=1.4, color=color.yellow)
compass_marker = Entity(parent=camera.ui, model='quad', color=color.yellow, scale=(0.01, 0.02), position=(0, 0.41))
compass_tape = Entity(parent=camera.ui, position=(0, 0.38))
directions = [('С', 0), ('В', 90), ('Ю', 180), ('З', 270), ('С', 360)]

compass_texts = []
for label, heading in directions:
    t = Text(parent=compass_tape, text=label, scale=1.1, color=color.white if label != 'С' else color.red)
    compass_texts.append((t, heading))

def trigger_takeoff():
    global state, target_throttle, velocity
    if state == 'on_ground': 
        velocity = Vec3(0, 0, 0)
        state = 'takeoff'
        target_throttle = 1.0  
takeoff_btn.on_click = trigger_takeoff

def trigger_landing():
    global state
    if state in ['flight', 'takeoff']: 
        state = 'landing'
landing_btn.on_click = trigger_landing

def update_wind_ui():
    global wind_enabled, wind_force, wind_angle
    if not wind_enabled or wind_force == 0:
        wind_btn.text = 'Ветер: НЕТ'
        wind_btn.color = color.azure
    else:
        wind_btn.text = f"{int(wind_force)}м/с -> {int(wind_angle)}°"
        wind_btn.color = color.orange

def toggle_wind():
    global wind_enabled, wind_force
    wind_enabled = not wind_enabled
    if wind_enabled and wind_force == 0:
        wind_force = 6.0
    update_wind_ui()
wind_btn.on_click = toggle_wind

def change_wind_force(amount):
    global wind_force, wind_enabled
    if not wind_enabled:
        wind_enabled = True
    wind_force = clamp(wind_force + amount, 0, 25)
    update_wind_ui()

def change_wind_angle(amount):
    global wind_angle, wind_enabled
    if not wind_enabled:
        wind_enabled = True
    wind_angle = (wind_angle + amount) % 360
    update_wind_ui()

wind_force_down.on_click = lambda: change_wind_force(-2)
wind_force_up.on_click = lambda: change_wind_force(2)
wind_rot_left.on_click = lambda: change_wind_angle(-15)
wind_rot_right.on_click = lambda: change_wind_angle(15)

def change_drone_type():
    global current_drone_index, current_spec, velocity, target_throttle, current_throttle
    if state != 'on_ground':
        return
        
    current_drone_index = (current_drone_index + 1) % len(drone_keys)
    current_key = drone_keys[current_drone_index]
    current_spec = drone_specs[current_key]
    
    velocity = Vec3(0, 0, 0)
    target_throttle = 0.0
    current_throttle = 0.0
    
    wings.enabled = False
    tail_horizontal.enabled = False
    tail_vertical.enabled = False
    propeller.enabled = False
    
    if hasattr(drone, 'wing_parts'):
        for part in drone.wing_parts:
            destroy(part)
        del drone.wing_parts

    if current_key == 'plane':
        drone_select_btn.text = 'БПЛА: Разведчик'
        drone.scale = (0.5, 0.4, 3.0)
        drone.color = color.gray
        wings.enabled = True
        tail_horizontal.enabled = True
        tail_vertical.enabled = True
        propeller.enabled = True
        propeller.position = (0, 0, 1.5)

    elif current_key == 'scout_wing':
        drone_select_btn.text = 'БПЛА: Тип 2'
        drone.scale = (0.6, 0.2, 1.8)
        drone.color = color.dark_gray
        
        drone.wing_parts = []
        l_wing = Entity(parent=drone, model='cube', color=color.black, scale=(3.5, 0.06, 1.2), position=(-1.8, 0, 0.2), rotation_y=-20)
        r_wing = Entity(parent=drone, model='cube', color=color.black, scale=(3.5, 0.06, 1.2), position=(1.8, 0, 0.2), rotation_y=20)
        
        drone.wing_parts.extend([l_wing, r_wing])
        propeller.enabled = True
        propeller.position = (0, 0, -1.0) 

    drone.y = current_spec['min_height']

drone_select_btn.on_click = change_drone_type

def input(key):
    global camera_mode
    if key == 'c' and state != 'crashed':
        camera_mode = 'fpv' if camera_mode == 'chase' else 'chase'

smooth_pitch = 0.0

def update():
    global state, camera_mode, wind_force, wind_enabled, wind_angle, velocity, target_throttle, current_throttle, target_takeoff_height, smooth_pitch
    dt = time.dt

    if state == 'crashed':
        if static_screen.enabled:
            return
        if explosion_cloud.scale_x < 15.0:
            explosion_cloud.scale += Vec3(20, 20, 20) * dt
        else:
            explosion_cloud.color = lerp(explosion_cloud.color, color.clear, 1 * dt)
        return

    current_key = drone_keys[current_drone_index]
    spec = drone_specs[current_key]

    throttle_speed = 1.0 if current_key == 'plane' else 2.5
    current_throttle = lerp(current_throttle, target_throttle, throttle_speed * dt)
    speed = velocity.length()

    if propeller.enabled:
        propeller.rotation_z += (current_throttle * 5000 + 200) * dt

    target_pitch = 0
    target_roll = 0

    current_heading = int(drone.rotation_y) % 360
    if current_heading < 0:
        current_heading += 360

    wind_status = f" {int(wind_force)} м/с ({int(wind_angle)}°)" if (wind_enabled and wind_force > 0) else " НЕТ"
    telemetry_text.text = (
        f"Режим: {state.upper()} ({spec['name_display']})\n"
        f"Скорость: {round(speed, 1)} м/с\n"
        f"Высота: {round(drone.y, 1)} м\n"
        f"Крен: {int(-drone.rotation_z)}°\n"
        f"Тяга: {int(current_throttle * 100)}%\n"
        f"Ветер:{wind_status}"
    )

    clamped_y = clamp(drone.y - spec['min_height'], 0, 50)
    pointer_target_pos_y = -0.03 + (clamped_y / 50.0) * 0.46
    altimeter_pointer.y = lerp(altimeter_pointer.y, pointer_target_pos_y, 5 * dt)
    roll_pointer.rotation_z = drone.rotation_z
    compass_digital.text = f"{current_heading}°"
    for t, heading in compass_texts:
        diff = (heading - current_heading + 180) % 360 - 180
        t.x = diff * 0.0025 - 0.01

    if state == 'on_ground':
        drone_select_btn.color = color.violet
    else:
        drone_select_btn.color = color.gray.tint(-0.2)

    if state == 'on_ground':
        velocity = Vec3(0, 0, 0)       
        target_throttle = 0.0          
        drone.y = spec['min_height']   
        drone.rotation_x = 0           
        drone.rotation_z = 0           
        smooth_pitch = 0.0             
        target_pitch = 0
        target_roll = 0

    elif state == 'takeoff':
        target_throttle = 1.0
        takeoff_speed_needed = 21.0 if current_key == 'plane' else 25.0
        
        if speed > takeoff_speed_needed:
            target_pitch = -5  
            velocity.y = lerp(velocity.y, 1.8, 0.8 * dt) 
            if drone.y >= target_takeoff_height:
                state = 'flight'
                target_throttle = 0.75 if current_key == 'plane' else 0.50
        else:
            target_pitch = 0
            velocity.y = 0

    elif state == 'landing':
        target_roll = 0
        if drone.y <= spec['min_height'] + 0.05:
            drone.y = spec['min_height']
            state = 'on_ground'  
        else:
            idle_gas = 0.23 if current_key == 'plane' else 0.12       
            flare_gas = 0.42 if current_key == 'plane' else 0.20      
            
            if drone.y > 4.0:
                target_throttle = lerp(target_throttle, idle_gas, 0.8 * dt) 
                target_pitch = 0        
                velocity.x = lerp(velocity.x, drone.forward.x * 12, 0.5 * dt)
                velocity.z = lerp(velocity.z, drone.forward.z * 12, 0.5 * dt)
            else:
                target_pitch = -6       
                target_throttle = flare_gas  
                velocity.y = lerp(velocity.y, -0.2, 3.0 * dt) 
                
            drone.y += velocity.y * dt

    elif state == 'flight':
        if held_keys['w']:
            target_throttle = min(target_throttle + 1.0 * dt, 1.0)
        if held_keys['s']:
            target_throttle = max(target_throttle - 1.0 * dt, 0.0)

        # Плавные рули высоты от стрелок на клавиатуре
        if held_keys['up arrow']: 
            smooth_pitch = lerp(smooth_pitch, -25.0, 3.0 * dt) 
        elif held_keys['down arrow']: 
            smooth_pitch = lerp(smooth_pitch, 25.0, 3.0 * dt)  
        else:
            if current_key == 'scout_wing':
                smooth_pitch = lerp(smooth_pitch, -0.2, 4.0 * dt)
            else:
                smooth_pitch = lerp(smooth_pitch, 0.0, 4.0 * dt)   

        target_pitch = smooth_pitch

        roll_angle = 35 if current_key == 'plane' else 52
        if held_keys['left arrow']: target_roll = -roll_angle
        if held_keys['right arrow']: target_roll = roll_angle

    drone.rotation_x = lerp(drone.rotation_x, target_pitch, 2.5 * dt)
    drone.rotation_z = lerp(drone.rotation_z, target_roll, 2.5 * dt)

    if state in ['flight', 'takeoff', 'landing']:
        total_force = Vec3(0, 0, 0)

        gravity_force = Vec3(0, -spec['mass'] * GRAVITY, 0)
        total_force += gravity_force

        thrust_magnitude = current_throttle * spec['max_thrust']
        thrust_force = drone.forward * thrust_magnitude
        total_force += thrust_force

        forward_speed = max(0, velocity.dot(drone.forward))
        lift_magnitude = forward_speed * spec['lift_factor']  
        lift_force = drone.up * lift_magnitude
        total_force += lift_force

        if speed > 3.0:
            turn_speed = 0.8 if current_key == 'plane' else 1.4 
            drone.rotation_y -= drone.rotation_z * turn_speed * dt

        drag_force = -velocity * speed * spec['drag_coef']
        total_force += drag_force

        side_velocity = velocity.dot(drone.right)
        side_drag_force = -drone.right * side_velocity * spec['side_drag'] * speed
        total_force += side_drag_force

        if wind_enabled and wind_force > 0:
            rad = math.radians(wind_angle)
            wind_vector = Vec3(math.sin(rad) * wind_force, 0, math.cos(rad) * wind_force)

            wind_push_force = (wind_vector - velocity) * spec['side_drag'] * 2.0
            total_force += wind_push_force

        acceleration = total_force / spec['mass']
        velocity += acceleration * dt

        if state == 'flight' and drone.rotation_x > -5:
            velocity.y = lerp(velocity.y, 0, 1.5 * dt)

        if state != 'landing':
            drone.position += velocity * dt
        else:
            drone.x += velocity.x * dt
            drone.z += velocity.z * dt

    hit_obstacle = False

    for b in building_entities:
        half_x = b.scale_x / 2
        half_y = b.scale_y / 2
        half_z = b.scale_z / 2
        if (b.x - half_x <= drone.x <= b.x + half_x and
            b.y - half_y <= drone.y <= b.y + half_y and
            b.z - half_z <= drone.z <= b.z + half_z):
            hit_obstacle = True
            break

    if not hit_obstacle:
        for h in hills_entities:
            world_hx = h.world_x
            world_hy = h.world_y
            world_hz = h.world_z
            
            radius_x = h.scale_x / 2.0
            radius_y = h.scale_y / 2.0  
            radius_z = h.scale_z / 2.0
            
            if drone.y <= world_hy + radius_y:
                norm_x = (drone.x - world_hx) / radius_x
                norm_y = (drone.y - world_hy) / radius_y
                norm_z = (drone.z - world_hz) / radius_z
                
                if (norm_x**2 + norm_y**2 + norm_z**2) <= 1.0:
                    hit_obstacle = True
                    break

    if hit_obstacle or (state == 'flight' and drone.y < spec['min_height']):
        if camera_mode == 'fpv':
            static_screen.enabled = True
        else:
            explosion_cloud.position = drone.position
            explosion_cloud.enabled = True
            camera_mode = 'chase'
        drone.enabled = False
        state = 'crashed'
        return

    if drone.y < spec['min_height']:
        drone.y = spec['min_height']
        if state == 'flight':
            velocity.y = 0

    if camera_mode == 'chase':
        target_camera_pos = drone.position - (drone.forward * 15) + Vec3(0, 1, 0) * 4.0
        camera.position = lerp(camera.position, target_camera_pos, 4 * dt)
        
        if camera.y < 1.5:
            camera.y = 1.5
            
        camera.look_at(drone.position + drone.forward * 5)
        camera.rotation_z = 0
    elif camera_mode == 'fpv':
        camera.position = drone.position + drone.forward * 1.6 + drone.up * 0.2
        camera.rotation = drone.rotation

app.run()
