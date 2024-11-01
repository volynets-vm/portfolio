#this partial code is supposed to be implemented into image processing code of the project
import pyrealsense2 as rs

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    pipeline.start(config)        
    frames = pipeline.wait_for_frames()
    while True:
        width  = camera.get(cv2.CAP_PROP_FRAME_WIDTH) 
        height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        distance = depth.get_distance(int(width/2),int(height/2))
        distance_in_cm = distance*100
        print(distance_in_cm)