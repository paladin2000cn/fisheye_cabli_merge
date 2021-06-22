import cv2
import numpy as np
import os
from pathlib import Path

# Checkboard dimensions
CHECKERBOARD = (7, 7)
subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC  + cv2.fisheye.CALIB_FIX_SKEW + cv2.fisheye.CALIB_CHECK_COND
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

### read images and for each image:


dir = Path(r'.\fisheye_calib_images')
arr = os.listdir(dir)
print(f'dir is {dir}')
num = 0
for name in arr:
    fullname = os.path.join(dir, name)
    print(f"image {fullname}")
    img = cv2.imread(fullname)

    if img.size == 0:
        print("Could not read the image01: ")
        exit(1)

    img_shape = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    # ret, corners = cv2.findChessboardCornersSB(gray, CHECKERBOARD,cv2.CALIB_CB_EXHAUSTIVE | cv2.CALIB_CB_ACCURACY);
    # If found, add object points, image points (after refining them)
    print(f"return {ret}; corners {corners}")
    if ret == True:
        num += 1
        objpoints.append(objp)
        cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), subpix_criteria)
        imgpoints.append(corners)
#        image=cv2.drawChessboardCorners(gray, CHECKERBOARD, corners, ret);
###


print(f"num of imag {num}")
# calculate K & D
N_imm = num  # number of calibration images
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_imm)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_imm)]
retval, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    K,
    D,
    rvecs,
    tvecs,
    calibration_flags,
    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6))

# un-distortion an image
img = cv2.imread(r".\20210608_104614.jpg")
#img = cv2.imread(r"C:\Users\palad\PycharmProjects\get_file_name\20210608_105850.jpg")
DIM = img.shape[:2][::-1]
print(f"DIM: {DIM}")
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
cv2.namedWindow("image", cv2.WINDOW_NORMAL);
cv2.imshow("image", undistorted_img);
cv2.imwrite(r".\undistored.jpg", undistorted_img);
cv2.waitKey(0);