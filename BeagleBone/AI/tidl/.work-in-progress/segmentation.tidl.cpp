/******************************************************************************
 * Copyright (c) 2018, Texas Instruments Incorporated - http://www.ti.com/
 *   All rights reserved.
 *
 *   Redistribution and use in source and binary forms, with or without
 *   modification, are permitted provided that the following conditions are met:
 *       * Redistributions of source code must retain the above copyright
 *         notice, this list of conditions and the following disclaimer.
 *       * Redistributions in binary form must reproduce the above copyright
 *         notice, this list of conditions and the following disclaimer in the
 *         documentation and/or other materials provided with the distribution.
 *       * Neither the name of Texas Instruments Incorporated nor the
 *         names of its contributors may be used to endorse or promote products
 *         derived from this software without specific prior written permission.
 *
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 *   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 *   THE POSSIBILITY OF SUCH DAMAGE.
 *****************************************************************************/
#include <signal.h>
#include <getopt.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cassert>
#include <string>
#include <functional>
#include <queue>
#include <algorithm>
#include <time.h>
#include <memory.h>
#include <string.h>

#include "executor.h"
#include "execution_object.h"
#include "execution_object_pipeline.h"
#include "configuration.h"
#include "imgutil.h"

#include "opencv2/opencv.hpp"
#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/videoio.hpp"

#define MAX_EOPS 8
#define MAX_CLASSES 1100

using namespace tidl;
using namespace cv;
using namespace std;

int current_eop = 0;
int num_eops = 0;
Configuration configuration;
Executor *e_eve = nullptr;
Executor *e_dsp = nullptr;
std::vector<ExecutionObjectPipeline *> eops;
int last_rpt_id = -1;

bool CreateExecutionObjectPipelines(uint32_t num_eves, uint32_t num_dsps,
                                    uint32_t num_layers_groups);
void AllocateMemory(const std::vector<ExecutionObjectPipeline*>& eops);
bool ProcessFrame(ExecutionObjectPipeline* eop, Mat &src);
void DisplayFrame(const ExecutionObjectPipeline* eop, Mat& src, Mat& dst);
void CreateMask(uchar *classes, uchar *mb, uchar *mg, uchar* mr,
                int channel_size);

// exports for the filter
extern "C" {
    bool filter_init(const char* args, void** filter_ctx);
    void filter_process(void* filter_ctx, Mat& src, Mat& dst);
    void filter_free(void* filter_ctx);
}

bool verbose = false;

/**
    Initializes the filter. If you return something, it will be passed to the
    filter_process function, and should be freed by the filter_free function
*/
bool filter_init(const char* args, void** filter_ctx) {
    uint32_t num_eves = 0;
    uint32_t num_dsps = 2;
    int num_layers_groups = 1;

    std::cout << "Initializing filter" << std::endl;

    std::cout << "loading configuration" << std::endl;
    configuration.numFrames = 1;
    configuration.preProcType = 0;
    configuration.inData = 
        "/usr/share/ti/examples/tidl/test/testvecs/input/input/000100_1024x512_bgr.y";
    configuration.outData = 
        "./stats_tool_out.bin";
    configuration.netBinFile = 
        "/usr/share/ti/examples/tidl/test/testvecs/config/tidl_models/tidl_net_jsegnet21v2.bin";
    configuration.paramsBinFile = 
        "/usr/share/ti/examples/tidl/test/testvecs/config/tidl_models/tidl_param_jsegnet21v2.bin";
    configuration.inWidth = 1024;
    configuration.inHeight = 512;
    configuration.inNumChannels = 3;
    //configuration.layerIndex2LayerGroupId = { {12, 2}, {13, 2}, {14, 2} };
    //configuration.enableApiTrace = false;
    //configuration.runFullNet = true;

    try
    {
        std::cout << "allocating execution object pipelines (EOP)" << std::endl;
        
        // Create ExecutionObjectPipelines
        if (! CreateExecutionObjectPipelines(num_eves, num_dsps,
                                        num_layers_groups))
            return false;

        // Allocate input/output memory for each EOP
        std::cout << "allocating I/O memory for each EOP" << std::endl;
        AllocateMemory(eops);
        num_eops = eops.size();
        std::cout << "num_eops=" << num_eops << std::endl;
        std::cout << "About to start ProcessFrame loop!!" << std::endl;
        std::cout << "http://localhost:8080/?action=stream" << std::endl;
    }
    catch (tidl::Exception &e)
    {
        std::cerr << e.what() << std::endl;
        return false;
    }

    return true;
}

/**
    Called by the OpenCV plugin upon each frame
*/
void filter_process(void* filter_ctx, Mat& src, Mat& dst) {
    try
    {
        // Process frames with available EOPs in a pipelined manner
        // additional num_eops iterations to flush the pipeline (epilogue)
        ExecutionObjectPipeline* eop = eops[current_eop];

        // Wait for previous frame on the same eo to finish processing
        //std::cout << "+" << std::endl;
        if (eop->ProcessFrameWait())
        {
            //std::cout << "-" << std::endl;
            if(configuration.enableApiTrace)
                std::cout << "display()" << std::endl;
            DisplayFrame(eop, src, dst);
        }
        else
        {
            //std::cout << "." << std::endl;
            if(configuration.enableApiTrace)
                std::cout << "copy()" << std::endl;
            dst = src;
        }

        if(configuration.enableApiTrace)
            std::cout << "process()" << std::endl;

        ProcessFrame(eop, src);
        
        current_eop++;
        if(current_eop >= num_eops)
            current_eop = 0;
    }
    catch (tidl::Exception &e)
    {
        std::cerr << e.what() << std::endl;
        dst = src;
    }

    return;
}

/**
    Called when the input plugin is cleaning up
*/
void filter_free(void* filter_ctx) {
    try
    {
        // Cleanup
        for (auto eop : eops)
        {
            free(eop->GetInputBufferPtr());
            free(eop->GetOutputBufferPtr());
            delete eop;
        }
        if (e_dsp) delete e_dsp;
        if (e_eve) delete e_eve;
    }
    catch (tidl::Exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    return;
}

bool CreateExecutionObjectPipelines(uint32_t num_eves, uint32_t num_dsps,
                                    uint32_t num_layers_groups)
{
    DeviceIds ids_eve, ids_dsp;
    for (uint32_t i = 0; i < num_eves; i++)
        ids_eve.insert(static_cast<DeviceId>(i));
    for (uint32_t i = 0; i < num_dsps; i++)
        ids_dsp.insert(static_cast<DeviceId>(i));
    const uint32_t buffer_factor = 1;

    std::cout << "allocating executors" << std::endl;
    e_eve = num_eves == 0 ? nullptr :
            new Executor(DeviceType::EVE, ids_eve, configuration);
    e_dsp = num_dsps == 0 ? nullptr :
            new Executor(DeviceType::DSP, ids_dsp, configuration);

    // Construct ExecutionObjectPipeline with single Execution Object to
    // process each frame. This is parallel processing of frames with
    // as many DSP and EVE cores that we have on hand.
    // If buffer_factor == 2, duplicating EOPs for double buffering
    // and overlapping host pre/post-processing with device processing
    std::cout << "allocating individual EOPs" << std::endl;
    for (uint32_t j = 0; j < buffer_factor; j++)
    {
        for (uint32_t i = 0; i < num_eves; i++)
            eops.push_back(new ExecutionObjectPipeline({(*e_eve)[i]}));
        for (uint32_t i = 0; i < num_dsps; i++)
            eops.push_back(new ExecutionObjectPipeline({(*e_dsp)[i]}));
    }

    return true;
}


void AllocateMemory(const std::vector<ExecutionObjectPipeline*>& eops)
{
    for (auto eop : eops)
    {
        size_t in_size  = eop->GetInputBufferSizeInBytes();
        size_t out_size = eop->GetOutputBufferSizeInBytes();
        std::cout << "Allocating input and output buffers" << std::endl;
        void*  in_ptr   = malloc(in_size);
        void*  out_ptr  = malloc(out_size);
        assert(in_ptr != nullptr && out_ptr != nullptr);
        
        ArgInfo in(in_ptr,   in_size);
        ArgInfo out(out_ptr, out_size);
        eop->SetInputOutputBuffer(in, out);
    }
}


bool ProcessFrame(ExecutionObjectPipeline* eop, Mat &src)
{
    if(configuration.enableApiTrace)
        std::cout << "preprocess()" << std::endl;
    imgutil::PreprocessImage(src, 
                             eop->GetInputBufferPtr(), configuration);
    eop->ProcessFrameStartAsync();
        
    return false;
}


void DisplayFrame(const ExecutionObjectPipeline* eop, Mat& src, Mat& dst)
{
    unsigned char *out = (unsigned char *) eop->GetOutputBufferPtr();
    int width          = configuration.inWidth;
    int height         = configuration.inHeight;
    int channel_size   = width * height;

    Mat mask, frame, blend, r_blend, bgr[3];
    // Create overlay mask
    bgr[0] = Mat(height, width, CV_8UC(1));
    bgr[1] = Mat(height, width, CV_8UC(1));
    bgr[2] = Mat(height, width, CV_8UC(1));
    CreateMask(out, bgr[0].ptr(), bgr[1].ptr(), bgr[2].ptr(), channel_size);
    cv::merge(bgr, 3, mask);

    // Asseembly original frame
    unsigned char *in = (unsigned char *) eop.GetInputBufferPtr();
    bgr[0] = Mat(height, width, CV_8UC(1), in);
    bgr[1] = Mat(height, width, CV_8UC(1), in + channel_size);
    bgr[2] = Mat(height, width, CV_8UC(1), in + channel_size*2);
    cv::merge(bgr, 3, frame);

    // Create overlayed frame
    cv::addWeighted(frame, 0.7, mask, 0.3, 0.0, blend);

    // Resize to output width/height, keep aspect ratio
    uint32_t output_width = opts.output_width;
    if (output_width == 0)  output_width = orig_width;
    uint32_t output_height = (output_width*1.0f) / orig_width * orig_height;
    cv::resize(blend, r_blend, Size(output_width, output_height));

    dst = r_blend;
}

// Create Overlay mask for pixel-level segmentation
void CreateMask(uchar *classes, uchar *mb, uchar *mg, uchar* mr,
                int channel_size)
{
    for (int i = 0; i < channel_size; i++)
    {
        const ObjectClass& object_class = object_classes->At(classes[i]);
        mb[i] = object_class.color.blue;
        mg[i] = object_class.color.green;
        mr[i] = object_class.color.red;
    }
}

