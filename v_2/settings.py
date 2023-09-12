# 1) Сколько л\га мы задаем на полив.
# 2) Высота полива (на какой дрон летает)
# 3) Скорость дрона

drone_litr_ga = 4
drone_lirt_per_min = 0.3  #(одна форсунка)
drone_fly_height = 3 # не используется
drone_speed = ...
pixel_meter = 4 # пиксель на метр


# Настройки исследоваемого полигона
x_list = [1156, 1226, 1050, 980]
y_list = [811, 880, 1058, 988]

# bush-команда для газебы на прослушивание
cmd = "gz topic -e --json-output -t /world/sitl/pose/info -n 1"  

#временной шаг через сколько наносим опыленную территорию в секунлу
timestamp = 0.5 

# соответсвенно за одну итерацию будет наноситься drone_lirt_per_min/60*timestamp * 1000  -> это все в миллилитрах
fertilizer_per_iteration = drone_lirt_per_min/60*timestamp*1000


# высчитаем нормативное количество распыления на метр и возьмем градацию в несолкьо порядков после.
recommended_fertz_for_pixel = drone_litr_ga / 10 / pixel_meter


# пути для работы openCV - надо указать нужную папку, путь к v2
path_to_small_map = '/home/wasabi/Desktop/UAF/PolivProcessing/Poliv/v_2/small_map.png'
path_to_saved_mission = '/home/wasabi/Desktop/UAF/PolivProcessing/Poliv/v_2/try_to_transport.png'