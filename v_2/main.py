from settings import pixel_meter, timestamp
from loader import mission_manager
import time

for i in range(2):
    mission_manager.catch_point_and_place_on_matrix()
    time.sleep(timestamp)

# mission_manager.save_to_png()
mission_manager.colour_image_matrix()