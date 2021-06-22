import cv2
import numpy as np
import os
from pathlib import Path
dir = Path(r'C:\Users\palad\PycharmProjects\get_file_name\fisheye_calib_images')
arr = os.listdir(dir)
num = 0
for name in arr:
    fullname = os.path.join(dir, name)
    print(f"image {fullname}")
    img = cv2.imread(fullname)
    num += 1
    if img.size == 0:
        print("Could not read the image01: ")
        exit(1)
        img_shape = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	Size boardSize, imageSize;
	boardSize.width = 18;
	boardSize.height = 17;
	int winSize = 11;
	Mat image,imageGray;
	//vector<vector<Point2f> > imagePoints;
	for (int i = 1; i <= 10; i++)
	{
		string filename = "E:\\标定测试\\" + to_string(i) + ".bmp";
		image = imread(filename);
		vector<Point2f> pointbuf;
		cvtColor(image, imageGray, COLOR_BGR2GRAY);
		bool found;
		/*found = findChessboardCorners(image, boardSize, pointbuf,
			CALIB_CB_ADAPTIVE_THRESH | CALIB_CB_FAST_CHECK | CALIB_CB_FILTER_QUADS);*/
		found = findChessboardCornersSB(image, boardSize, pointbuf,
			CALIB_CB_EXHAUSTIVE | CALIB_CB_ACCURACY);
		if (found) {
			/*cornerSubPix(imageGray, pointbuf, Size(winSize, winSize),
				Size(-1, -1), TermCriteria(TermCriteria::EPS + TermCriteria::COUNT, 30, 0.1));*/
			drawChessboardCorners(image, boardSize, Mat(pointbuf), found);
			std::ofstream myfile;
			string txtName = "corner" + to_string(i) + ".txt";
			myfile.open (txtName,ios::out);
			for (unsigned int j = 0; j < pointbuf.size(); j++)
			{
					float x_pos = pointbuf.at(j).x;
					float y_pos = pointbuf.at(j).y;

					#保存角点坐标
					myfile << x_pos << " " << y_pos << std::endl;
			}
			myfile.close();
		}
		cv::namedWindow("image", WINDOW_NORMAL);
		cv::imshow("image", image);
		cv::waitKey(0);


