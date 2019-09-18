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
int top_candidates = 3;
int size = 0;
int selected_items_size;
int * selected_items;
std::string * labels_classes[MAX_CLASSES];
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
int tf_postprocess(uchar *in);
bool tf_expected_id(int id);
void populate_labels(const char* filename);

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

    populate_labels("/home/debian/tidl-api/examples/classification/imagenet.txt");

    selected_items_size = 10;
    selected_items = (int *)malloc(selected_items_size*sizeof(int));
    if (!selected_items) {
        std::cout << "selected_items malloc failed" << std::endl;
        return false;
    }
    selected_items[0] = 429; /* baseball */
    selected_items[1] = 837; /* sunglasses */
    selected_items[2] = 504; /* coffee_mug */
    selected_items[3] = 441; /* beer_glass */
    selected_items[4] = 898; /* water_bottle */
    selected_items[5] = 931; /* bagel */
    selected_items[6] = 531; /* digital_watch */
    selected_items[7] = 487; /* cellular_telephone */
    selected_items[8] = 722; /* ping-pong_ball */
    selected_items[9] = 720; /* pill_bottle */

    std::cout << "loading configuration" << std::endl;
    configuration.numFrames = 0;
    configuration.inData = 
        "/home/debian/tidl-api/examples/test/testvecs/input/preproc_0_224x224.y";
    configuration.outData = 
        "/home/debian/tidl-api/examples/classification/stats_tool_out.bin";
    configuration.netBinFile = 
        "/home/debian/tidl-api/examples/test/testvecs/config/tidl_models/tidl_net_imagenet_jacintonet11v2.bin";
    configuration.paramsBinFile = 
        "/home/debian/tidl-api/examples/test/testvecs/config/tidl_models/tidl_param_imagenet_jacintonet11v2.bin";
    configuration.preProcType = 0;
    configuration.inWidth = 224;
    configuration.inHeight = 224;
    configuration.inNumChannels = 3;
    configuration.layerIndex2LayerGroupId = { {12, 2}, {13, 2}, {14, 2} };
    configuration.enableApiTrace = false;
    configuration.runFullNet = true;

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
    dst = src;
    if(configuration.enableApiTrace)
        std::cout << "postprocess()" << std::endl;
    int is_object = tf_postprocess((uchar*) eop->GetOutputBufferPtr());
    if(is_object >= 0)
    {
        cv::putText(
            dst,
            (*(labels_classes[is_object])).c_str(),
            cv::Point(15, 60),
            cv::FONT_HERSHEY_SIMPLEX,
            1.5,
            cv::Scalar(0,255,0),
            3,  /* thickness */
            8
        );
    }
    if(last_rpt_id != is_object) {
        if(is_object >= 0)
        {
            std::cout << "(" << is_object << ")="
                      << (*(labels_classes[is_object])).c_str() << std::endl;
        }
        last_rpt_id = is_object;
    }
}

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

int tf_postprocess(uchar *in)
{
  //prob_i = exp(TIDL_Lib_output_i) / sum(exp(TIDL_Lib_output))
  // sort and get k largest values and corresponding indices
  const int k = top_candidates;
  int rpt_id = -1;

  typedef std::pair<uchar, int> val_index;
  auto constexpr cmp = [](val_index &left, val_index &right) { return left.first > right.first; };
  std::priority_queue<val_index, std::vector<val_index>, decltype(cmp)> queue(cmp);
  // initialize priority queue with smallest value on top
  for (int i = 0; i < k; i++) {
    if(configuration.enableApiTrace)
        std::cout << "push(" << i << "):"
                  << in[i] << std::endl;
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
        rpt_id = id;
      }
  }
  return rpt_id;
}

void populate_labels(const char* filename)
{
  ifstream file(filename);
  if(file.is_open())
  {
    string inputLine;

    while (getline(file, inputLine) )                 //while the end of file is NOT reached
    {
      labels_classes[size++] = new string(inputLine);
    }
    file.close();
  }
#if 0
  std::cout << "==Total of " << size << " items!" << std::endl;
  for (int i = 0; i < size; i ++)
    std::cout << i << ") " << *(labels_classes[i]) << std::endl;
#endif
}

