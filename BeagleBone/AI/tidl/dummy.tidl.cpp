// dummy.tidl.cpp - empty filter to test mjpg-streamer only
#include "opencv2/opencv.hpp"
#include "opencv2/core.hpp"

// exports for the filter
extern "C" {
    bool filter_init(const char* args, void** filter_ctx);
    void filter_process(void* filter_ctx, Mat& src, Mat& dst);
    void filter_free(void* filter_ctx);
}

/**
    Initializes the filter. If you return something, it will be passed to the
    filter_process function, and should be freed by the filter_free function
*/
bool filter_init(const char* args, void** filter_ctx) {
    return true;
}

/**
    Called by the OpenCV plugin upon each frame
*/
void filter_process(void* filter_ctx, cv::Mat& src, cv::Mat& dst) {
    dst = src;
    return;
}

/**
    Called when the input plugin is cleaning up
*/
void filter_free(void* filter_ctx) {
    return;
}
