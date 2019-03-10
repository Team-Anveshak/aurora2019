//Execute with:   g++ opencv_gst.cpp -o app `pkg-config --cflags --libs opencv`
// Install accepted answer in https://devtalk.nvidia.com/default/topic/1020915/opencv-and-webcam-problem-pixel-format-of-incoming-image-is-unsupported-by-opencv/

#include <stdio.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include "opencv2/core/core.hpp"
#include <iostream>
using namespace std;
using namespace cv;

int main(int argc, char** argv) {

    cv::VideoCapture cap1("v4l2src device=\"/dev/video0\" ! video/x-raw, width=640, height=480, format=RGB ! videoconvert ! appsink");
    if (!cap1.isOpened()) {
        printf("=ERR= can't create video capture\n");
        return -1;
    }

    cv::VideoCapture cap2("v4l2src device=\"/dev/video1\" ! video/x-raw, width=640, height=480, format=RGB ! videoconvert ! appsink");
    if (!cap2.isOpened()) {
        printf("=ERR= can't create video capture\n");
        return -1;
    }
    
    cv::VideoCapture cap3("v4l2src device=\"/dev/video2\" ! video/x-raw, width=640, height=480, format=RGB ! videoconvert ! appsink");
    if (!cap2.isOpened()) {
        printf("=ERR= can't create video capture\n");
        return -1;
    }

    cv::VideoCapture cap4("v4l2src device=\"/dev/video3\" ! video/x-raw, width=640, height=480, format=RGB ! videoconvert ! appsink");
    if (!cap2.isOpened()) {
        printf("=ERR= can't create video capture\n");
        return -1;
    }
   

    // second part of sender pipeline
    cv::VideoWriter writer1;
    writer1.open("appsrc ! videoconvert ! x264enc noise-reduction=10000 tune=zerolatency byte-stream=true bitrate=3000 threads=2 ! h264parse config-interval=1 ! rtph264pay ! udpsink host=10.42.0.1 port=5002", 0, (double)30, cv::Size(960, 720), true);
    if (!writer1.isOpened()) {
        printf("=ERR= can't create video writer\n");
        return -1;
    }


    cv::Mat frame1;
    cv::Mat frame2;
    cv::Mat frame3;
    cv::Mat frame4;
    
    int key;
    Mat both;
int width = 480, height = 360;
both = Mat(height * 2, (width * 2), CV_MAKETYPE(8, 3), CV_RGB(100, 100, 100));

    while (true) {

        cap2 >> frame1;
        if (frame1.empty())
            break;
        cap2 >> frame2;
	if (frame2.empty())
	    break;
	cap3 >> frame3;
        if (frame1.empty())
            break;
        cap4 >> frame4;
	if (frame2.empty())
	    break;
      
 /* Process the frame here */
 	cv::resize(frame1,frame1,cv::Size(),0.75,0.75);
 	cv::resize(frame2,frame2,cv::Size(),0.75,0.75);
 	cv::resize(frame3,frame3,cv::Size(),0.75,0.75);
 	cv::resize(frame4,frame4,cv::Size(),0.75,0.75);
	frame1.copyTo(Mat(both, Rect(0, 0, width, height)));
	frame2.copyTo(Mat(both, Rect(480, 0, width, height)));
	frame3.copyTo(Mat(both, Rect(0, 360, width, height)));
	frame4.copyTo(Mat(both, Rect(480, 360, width, height)));

	//imshow("images", both);
	writer1 << both;
        //key = cv::waitKey( 1 );
    }
}

