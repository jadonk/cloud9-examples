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

#define RES_X 480
#define RES_Y 480

#define MAX_EOPS 8

using namespace tidl;
using namespace cv;
using namespace std;

struct my_ctx {
    Configuration configuration;
    Executor * e_eve;
    Executor * e_dsp;
    std::vector<ExecutionObjectPipeline *> eops;
    int frame_idx;
    Mat * images[MAX_EOPS];
};

bool CreateExecutionObjectPipelines(uint32_t num_eves, uint32_t num_dsps,
                                    uint32_t num_layers_groups,
                                    struct my_ctx * ctx);
void AllocateMemory(const std::vector<ExecutionObjectPipeline*>& eops);
bool ProcessFrame(ExecutionObjectPipeline* eop, struct my_ctx * ctx,
                  Mat &src);
void DisplayFrame(const ExecutionObjectPipeline* eop, Mat& dst,
                  struct my_ctx * ctx);
int tf_postprocess(uchar *in, int size, struct my_ctx * ctx, int f_id);

// exports for the filter
extern "C" {
    bool filter_init(const char * args, void** filter_ctx);
    void filter_process(void* filter_ctx, Mat &src, Mat &dst);
    void filter_free(void* filter_ctx);
}

bool verbose = false;

/**
    Initializes the filter. If you return something, it will be passed to the
    filter_process function, and should be freed by the filter_free function
*/
bool filter_init(const char * args, void** filter_ctx) {
    uint32_t num_eves = 2;
    uint32_t num_dsps = 2;
    int num_layers_groups = 1;
    int i;

    // Read the TI DL configuration file
    /*
numFrames   = 999900
inData   = /home/debian/tidl-api/examples/test/testvecs/input/preproc_0_224x224.y
outData   = "/home/debian/tidl-api/examples/classification/stats_tool_out.bin"
netBinFile      = "/home/debian/tidl-api/examples/test/testvecs/config/tidl_models/tidl_net_imagenet_jacintonet11v2.bin"
paramsBinFile   = "/home/debian/tidl-api/examples/test/testvecs/config/tidl_models/tidl_param_imagenet_jacintonet11v2.bin"
preProcType = 0
inWidth = 224
inHeight = 224
inNumChannels = 3
layerIndex2LayerGroupId = { {12, 2}, {13, 2}, {14, 2} }
*/
    Configuration configuration;
    if (!configuration.ReadFromFile("stream_config_j11_v2.txt"))
        return false;

    if (verbose)
        configuration.enableApiTrace = true;

    if (num_layers_groups == 1)
        configuration.runFullNet = true; //Force all layers to be in the same group

    struct my_ctx * ctx = (struct my_ctx *)malloc(sizeof(struct my_ctx));
    if (!ctx)
        return false;
    *filter_ctx = ctx;

    try
    {
        // Create ExecutionObjectPipelines
        ctx->e_eve = nullptr;
        ctx->e_dsp = nullptr;
        if (! CreateExecutionObjectPipelines(num_eves, num_dsps,
                                        num_layers_groups, ctx))
            return false;

        // Allocate input/output memory for each EOP
        AllocateMemory(ctx->eops);

        int num_eops = ctx->eops.size();
        for (i=0; i < num_eops; i++)
        {
            ctx->images[i] = new Mat(Size(RES_X, RES_Y), CV_8UC4);
        }

        ctx->frame_idx = 0;

        std::cout << "About to start ProcessFrame loop!!" << std::endl;
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
    struct my_ctx * ctx = static_cast<struct my_ctx *>(filter_ctx);

    try
    {
        // Process frames with available EOPs in a pipelined manner
        // additional num_eops iterations to flush the pipeline (epilogue)
        int num_eops = ctx->eops.size();
        ExecutionObjectPipeline* eop = ctx->eops[ctx->frame_idx % num_eops];

        // Wait for previous frame on the same eo to finish processing
        if (eop->ProcessFrameWait())
        {
             DisplayFrame(eop, dst, ctx);
        }
        else
        {
            dst = src;
        }

        if (ProcessFrame(eop, ctx, src))
            eop->ProcessFrameStartAsync();

        if (ctx->frame_idx < ctx->configuration.numFrames + num_eops)
            ctx->frame_idx++;
        else
            ctx->frame_idx = 0;
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
    struct my_ctx * ctx = static_cast<struct my_ctx *>(filter_ctx);

    try
    {
        int num_eops = ctx->eops.size();

        // Cleanup
        for (auto eop : ctx->eops)
        {
            free(eop->GetInputBufferPtr());
            free(eop->GetOutputBufferPtr());
            delete eop;
        }
        if (ctx->e_dsp) delete ctx->e_dsp;
        if (ctx->e_eve) delete ctx->e_eve;

        for (int i=0; i < num_eops; i++)
        {
            delete ctx->images[i];
        }
    }
    catch (tidl::Exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    free(ctx);

    return;
}

bool CreateExecutionObjectPipelines(uint32_t num_eves, uint32_t num_dsps,
                                    uint32_t num_layers_groups,
                                    struct my_ctx * ctx)
{
    DeviceIds ids_eve, ids_dsp;
    for (uint32_t i = 0; i < num_eves; i++)
        ids_eve.insert(static_cast<DeviceId>(i));
    for (uint32_t i = 0; i < num_dsps; i++)
        ids_dsp.insert(static_cast<DeviceId>(i));
    const uint32_t buffer_factor = 2;

    switch(num_layers_groups)
    {
    case 1: // Single layers group
        ctx->e_eve = num_eves == 0 ? nullptr :
                new Executor(DeviceType::EVE, ids_eve, ctx->configuration);
        ctx->e_dsp = num_dsps == 0 ? nullptr :
                new Executor(DeviceType::DSP, ids_dsp, ctx->configuration);

        // Construct ExecutionObjectPipeline with single Execution Object to
        // process each frame. This is parallel processing of frames with
        // as many DSP and EVE cores that we have on hand.
        // If buffer_factor == 2, duplicating EOPs for double buffering
        // and overlapping host pre/post-processing with device processing
        for (uint32_t j = 0; j < buffer_factor; j++)
        {
            for (uint32_t i = 0; i < num_eves; i++)
                ctx->eops.push_back(new ExecutionObjectPipeline({(*(ctx->e_eve))[i]}));
            for (uint32_t i = 0; i < num_dsps; i++)
                ctx->eops.push_back(new ExecutionObjectPipeline({(*(ctx->e_dsp))[i]}));
        }
        break;

    case 2: // Two layers group
        // Create Executors with the approriate core type, number of cores
        // and configuration specified
        // EVE will run layersGroupId 1 in the network, while
        // DSP will run layersGroupId 2 in the network
        ctx->e_eve = num_eves == 0 ? nullptr :
                new Executor(DeviceType::EVE, ids_eve, ctx->configuration, 1);
        ctx->e_dsp = num_dsps == 0 ? nullptr :
                new Executor(DeviceType::DSP, ids_dsp, ctx->configuration, 2);

        // Construct ExecutionObjectPipeline that utilizes multiple
        // ExecutionObjects to process a single frame, each ExecutionObject
        // processes one layerGroup of the network
        // If buffer_factor == 2, duplicating EOPs for pipelining at
        // EO level rather than at EOP level, in addition to double buffering
        // and overlapping host pre/post-processing with device processing
        for (uint32_t j = 0; j < buffer_factor; j++)
        {
            for (uint32_t i = 0; i < std::max(num_eves, num_dsps); i++)
                ctx->eops.push_back(new ExecutionObjectPipeline(
                                {(*(ctx->e_eve))[i%num_eves], (*(ctx->e_dsp))[i%num_dsps]}));
        }
        break;

    default:
        std::cout << "Layers groups can be either 1 or 2!" << std::endl;
        return false;
        break;
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


bool ProcessFrame(ExecutionObjectPipeline* eop, struct my_ctx * ctx,
                  Mat &src)
{
    Mat image;
    Rect rectCrop;

    //Crop central square portion
    int loc_xmin = (src.size().width - src.size().height) / 2; //Central position
    int loc_ymin = 0;
    int loc_w = src.size().height;
    int loc_h = src.size().height;

    cv::resize(src(Rect(loc_xmin, loc_ymin, loc_w, loc_h)), image, Size(RES_X, RES_Y));

    *(ctx->images[ctx->frame_idx]) = Mat(image, rectCrop);

    imgutil::PreprocessImage(*(ctx->images[ctx->frame_idx]), 
                             eop->GetInputBufferPtr(), ctx->configuration);
    eop->SetFrameIndex(ctx->frame_idx);
    eop->ProcessFrameStartAsync();
        
    return false;
}


void DisplayFrame(const ExecutionObjectPipeline* eop, Mat& dst,
                  struct my_ctx * ctx)
{
    int f_id = eop->GetFrameIndex();
    int is_object = tf_postprocess((uchar*) eop->GetOutputBufferPtr(), ctx, f_id);
    if(is_object > 0)
    {
        std::cout << "(" << is_object << ")="
                  << labels_classes[is_object].c_str() << std::endl;
#ifdef PERF_VERBOSE
        std::cout << "Device:" << eop->GetDeviceName() << " eops("
                  << num_eops << "), FPS:" << avg_fps << std::endl;
#endif
    }
}


char imagenet_win[160];
char tmp_classwindow_string[160];

Mat in_image, image, r_image, cnn_image, show_image, bgr_frames[3];
Mat to_stream;
Rect rectCrop;
// Report average FPS across a sliding window of 16 frames
AvgFPSWindow fps_window(16);



extern std::string labels_classes[];
extern int IMAGE_CLASSES_NUM;
extern int selected_items_size;
extern int selected_items[];
extern int populate_selected_items (char *filename);

std::string labels_classes[MAX_CLASSES];
int IMAGE_CLASSES_NUM = 0;



// Function to filter all the reported decisions
bool tf_expected_id(int id)
{
   // Filter out unexpected IDs
   for (int i = 0; i < selected_items_size; i ++)
   {
       if(id == selected_items[i]) return true;
   }
   return false;
}

int tf_postprocess(uchar *in, struct my_ctx * ctx, int f_id)
{
  //prob_i = exp(TIDL_Lib_output_i) / sum(exp(TIDL_Lib_output))
  // sort and get k largest values and corresponding indices
  const int k = TOP_CANDIDATES;
  int rpt_id = -1;

  typedef std::pair<uchar, int> val_index;
  auto constexpr cmp = [](val_index &left, val_index &right) { return left.first > right.first; };
  std::priority_queue<val_index, std::vector<val_index>, decltype(cmp)> queue(cmp);
  // initialize priority queue with smallest value on top
  for (int i = 0; i < k; i++) {
    queue.push(val_index(in[i], i));
  }
  // for rest input, if larger than current minimum, pop mininum, push new val
  for (int i = k; i < size; i++)
  {
    if (in[i] > queue.top().first)
    {
      queue.pop();
      queue.push(val_index(in[i], i));
    }
  }

  // output top k values in reverse order: largest val first
  std::vector<val_index> sorted;
  while (! queue.empty())
   {
    sorted.push_back(queue.top());
    queue.pop();
  }

  for (int i = 0; i < k; i++)
  {
      int id = sorted[i].second;

      if (tf_expected_id(id))
      {
        std::cout << "Frame:" << ctx->frame_idx << "," << f_id << "]: rank="
                  << k-i << ", outval=" << (float)sorted[i].first / 255 << ", "
                  << labels_classes[sorted[i].second] << std::endl;
        rpt_id = id;
      }
  }
  return rpt_id;
}

