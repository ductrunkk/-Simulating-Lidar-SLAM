import pygame
import math
import numpy as np

pygame.init()
#hàm thể hiện độ không chắc chắn của cảm biến bằng cách lấy giá trị ngẫu nhiên
def uncertainly_add(distance, angle, sigma):
    mean = np.array(([distance, angle]))
    covariance = np.diag(sigma ** 2) #Tính ra ma trận 'hiệp phương sai'
    distance, angle = np.random.multivariate_normal(mean, covariance)

    # Sử dụng hàm Max để nhận giá trị dương
    distance = max(distance, 0)
    angle = max(angle, 0)
    return [distance, angle]  #Trả về dạng mảng

class LaserSensor:
    def __init__(self, range, map, uncertainty):
        self.range = range  # khoảng sai số nhiễu
        self.speed = 4  # round per second
        self.sigma = np.array([uncertainty[0], uncertainty[1]])  #độ nhiễu
        self.position = (0, 0)  #vị trí ban đầu của robot

        # lấy kích thước map
        self.map = map
        self.W, self.H = pygame.display.get_surface().get_size()

        # mảng lưu trữ các khoảng cách giữa 2 điểm trong không gian #
        self.sensedObstacles = []

    # Hàm tính khoảng cách bằng CT Euclid#
    def distance(self, obstaclePosition):
        px = (obstaclePosition[0] - self.position[0])**2
        py = (obstaclePosition[1] - self.position[1])**2
        return math.sqrt(px+py)

    #hàm đo các vật cản
    def sense_obstacles(self):
        data = [] #Mảng chứa các dữ liêu
        x1, y1 = self.position[0], self.position[1]
        for angle in np.linspace(0, 2*math.pi, 60, False): #Sử dụng linspace để quyết định độ phân giải của map
            x2,y2 = (x1 + self.range * math.cos(angle), y1 - self.range * math.sin(angle))
            for i in range(0, 100): #Tính tọa độ 1 điểm trong đoạn đường đi tới bằng CT nội suy
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))

                if(0 < x < self.W and 0 < y < self.H):
                    color = self.map.get_at((x, y)) #Nếu điểm nằm trong bản đồ thì sẽ in ra màu chính xác của điểm đó
                    if(color[0], color[1], color[2]) == (0, 0, 0): #Nếu điểm đó màu đen
                        distance = self.distance((x, y))  # Thì tính khoảng cách đó với robot
                        output = uncertainly_add(distance, angle, self.sigma)  #  Thêm độ không chắc chắn vào mảng

                        output.append(output)#Lưu trữ vị trị hiện tại của robot
                        break # kết thúc vòng lặp khi mà gặp vật cản

        #mô phỏng tia laser của LIDAR

        #Khi đã quét xong thì đã vẽ được 1 điểm trên bản đồ
        if(len(data) > 0):
            return data
        else:
            return False

