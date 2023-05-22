import cv2
import numpy as np

class CubeProjection:
    def __init__(self, img_name):
        self._img = img_name
        [self._height, self._width, _] = self._img.shape
    
    def GetCube(self, rotation_matrix=None):
        cube_img = np.zeros((self._height, self._width*4, 3), dtype=np.uint8)

        # Face 1 - Front
        cube_img[:, :self._width] = cv2.resize(self._img, (self._width, self._height))

        # Face 2 - Right
        cube_img[:, self._width:self._width*2] = cv2.resize(self._img, (self._width, self._height))
        cube_img[:, self._width:self._width*2] = cv2.flip(cube_img[:, self._width:self._width*2], 1)

        # Face 3 - Back
        cube_img[:, self._width*2:self._width*3] = cv2.resize(self._img, (self._width, self._height))
        cube_img[:, self._width*2:self._width*3] = cv2.flip(cube_img[:, self._width*2:self._width*3], 1)
        cube_img[:, self._width*2:self._width*3] = cv2.flip(cube_img[:, self._width*2:self._width*3], 0)

        # Face 4 - Left
        cube_img[:, self._width*3:] = cv2.resize(self._img, (self._width, self._height))
        cube_img[:, self._width*3:] = cv2.flip(cube_img[:, self._width*3:], 1)

        if rotation_matrix is not None:
            cube_img = self.apply_rotation(cube_img, rotation_matrix)

        return cube_img
    
    def GetPerspective(self, rotation_matrix=None):
        if rotation_matrix is None:
            return self.GetCube(rotation_matrix=None)

        # Apply rotation to the cube faces individually
        cube_img = self.GetCube(rotation_matrix=None)
        rotated_cube_img = self.apply_rotation(cube_img, rotation_matrix)

        return rotated_cube_img


    def apply_rotation(self, cube_img, rotation_matrix):
        rotated_cube_img = np.zeros_like(cube_img)

        for i in range(4):
            face_img = cube_img[:, self._width*i:self._width*(i+1)]
            rotated_face_img = cv2.warpAffine(face_img, rotation_matrix, (self._width, self._height))
            rotated_cube_img[:, self._width*i:self._width*(i+1)] = rotated_face_img

        return rotated_cube_img
