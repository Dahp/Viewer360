import cv2
import numpy as np
import pytest
from Equirec2Perspec import Equirectangular

# Тестирование метода GetPerspective класса Equirectangular
def test_GetPerspective():
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    equi = Equirectangular(img)

    for _ in range(10):
        # Генерация случайных значений для параметров теста
        FOV = np.random.uniform(60, 120)
        THETA = np.random.uniform(-180, 180)
        PHI = np.random.uniform(-90, 90)
        height = np.random.randint(50, 150)
        width = np.random.randint(100, 250)

        result = equi.GetPerspective(FOV, THETA, PHI, height, width)
        assert result.shape == (height, width, 3)

# Запуск теста
if __name__ == '__main__':
    pytest.main([__file__])
