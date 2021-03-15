OBJECT_DEFINITION = \
'object {\n\
    shape\n\
    #ifdef (mask)\n\
        pigment {color ${COLOR}}\n\
    #else\n\
        texture {\n\
            pigment{\n\
                color filter 1\n\
                #ifdef (Calib) transmit 1 #else transmit ${Trans} #end\n\
            }\n\
        }\n\
        interior {\n\
            ior ${IOR} \n\
            #ifndef (Calib)\n\
                fade_distance ${FadeD} fade_power ${FadeP}\n\
            #end\n\
        }\n\
    #end\n\
    scale     ${SC}\n\
    rotate    z*${RotZ}\n\
    rotate    y*${RotY}\n\
    translate x*${TX}\n\
    translate y*${TY}\n\
}'

camera_parameters = {
    'cl_x': [0.00], # Camera Location
    'cl_y': [0.00], 
    'cl_z': [-4.5, -3.5], 
    'lk_x': [0.00], # Camera Look At
    'lk_y': [0.00],
    'lk_z': [0.00],
    'cs_x': [0.00], # Camera Sky
    'cam_a': [1.00], # Aspect ratio
    'cam_z': [2.00, 2.50], # Zoom
    'bg_sc': [2.50, 3.50], # Background Scale
    'bg_pz': [3.02],
    'bg_rx': [0.00], # Background Rotation
    'bg_ry': [0.00], 
    'bg_rz': [0.00], 
    'Dim': [0.85, 1.00], # Ambient intensity
}

object_parameters = {
    'COLOR': [], # Category Color
    'Trans': [1.00], # Transmit
    'SC': [0.3, 0.5], # Scale
    'IOR': [1.3, 1.5], # Index of Refraction
    'RotZ': [-90, 90], # Object Rotation
    'RotY': [-45, 45],
    'TX': [-0.80, 0.80], # Object Translation
    'TY': [-0.80, 0.80],
    'FadeD': [1.63], # Fade Distance
    'FadeP': [1001.00], # Fade Power
}

COLORS = {
    'Cups': 'Green',
    'Lens': 'Red',
    'Glass': 'Blue',
    'Plane': 'Yellow',
    'Sphere': 'Cyan'
}
