import pygame
import math
import MoiTruong
import CamBien

pygame.init()
environment = MoiTruong.buildEnvironment((600, 1200))
environment.originalMap = environment.map.copy()
laser = CamBien.LaserSensor(200, environment.originalMap, uncertainty=(0.5, 0.01))
environment.map.fill((0, 0, 0))  #phủ lên dispaly bằng màu đen
environment.infomap = environment.map.copy()

running = True #Cửa sổ sẽ không tắt

while running:
    sensorON = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #nút thoát khỏi display
        if pygame.mouse.get_focused():
            sensorON = True #con trỏ khi trong display mới được bật
        elif not pygame.mouse.get_focused():
            sensorON = False

    if sensorON:
        position = pygame.mouse.get_pos() #Vị trí sẽ lấy vị trí con trỏ hiện tại
        laser.position = position
        sensor_data = laser.sense_obstacles()
        environment.dataStorage(sensor_data)
        environment.show_sensorData()
    environment.map.blit(environment.infomap, (0, 0)) #hàm biểu diễn hình ảnh lên display
    pygame.display.update() #bản đồ phải cập nhật mới mỗi khi được vẽ một vật cản