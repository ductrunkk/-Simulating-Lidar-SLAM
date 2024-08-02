import pygame
import math


class buildEnvironment:
    def __init__(self, MapDimensions):
        pygame.init()
        self.pointCloud = []  # khai báo danh sách để lưu trữ đám mây điểm thể hiện bằng [x,y]#
        self.externalMap = pygame.image.load('map01.png')
        self.maph, self.mapw = MapDimensions  # kích thước bản đồ
        self.MapWindowName = 'SLAM'      #Tên cửa sổ
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(self.externalMap, (0, 0))  #phủ ảnh lên cửa sổ

        #color
        self.black = (0, 0, 0)
        self.grey = (70, 70, 70)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

    #Hàm biến dữ liệu thành tọa độ Descartes
    def AD2pos(self, distance, angle, robotPosition):
        x = distance * math.cos(angle) + robotPosition[0]
        y = -distance * math.sin(angle) + robotPosition[1]
        return (int(x), int(y))

    #Hàm lưu trữ các tạo độ
    def dataStorage(self, data):
        print(len(self.pointCloud))
        if (data != False):
            for element in data:
                point = self.AD2pos(element[0], element[1], element[2])
                if point not in self.pointCloud: #Kiểm tra dữ liệu điểm, nếu không có thì thêm vào mảng
                    self.pointCloud.append(point)

    #Hàm hiển thị dữ liệu cảm biến
    def show_sensorData(self):
        self.infomap = self.map.copy()
        for point in self.pointCloud: #Những điểm vật cản sẽ biến thành màu đỏ
            self.infomap.set_at((int(point[0]), int(point[1])), (0, 0, 255))
