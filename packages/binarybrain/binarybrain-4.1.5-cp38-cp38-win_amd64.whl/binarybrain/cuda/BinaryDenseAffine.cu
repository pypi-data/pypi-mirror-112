#include <iostream>
#include <algorithm>

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include "bbcu/bbcu.h"
#include "bbcu/bbcu_util.h"

#include "Common.cuh"





// bit packing binary
template<typename T=float, int MAX_FRAME_UNIT=32, int MAX_NODE_UNIT=32>
__global__ void kernal_bit_BinaryDenseAffine_Forward
        (
            int const   *x_buf,
            int         *y_buf,
            T   const   *W_buf,
            T   const   *b_buf,
            T           *mean_buf,
            T           *rstd_buf,
            T           *running_mean_buf,
            T           *running_var_buf,
            T           gamma,
            T           beta,
            T           momentum,
            T           unbinarize_bias,
            T           reciprocal_frame_size,
            int         x_node_size,
            int         y_node_size,
            int         frame_size,
            int         frame_stride,
            int         lut_binarize
        )
{
    int y_node_id = threadIdx.y;
    int y_node    = blockIdx.y * blockDim.y + threadIdx.y;
    int id        = threadIdx.x;
    int id_step   = blockDim.x;

    __shared__  T           W[MAX_W_SIZE][MAX_NODE_UNIT];
                int   const *x_ptr[N];
                int         *y_ptr;
    
    if ( y_node < y_node_size ) {
        for (int x_node = id; x_node < x_node_size; x_node += id_step) {
            W[x_node][y_node_id] = W_buf[y_node*x_node_size + x_node]
        }
        b = b_buf[y_node];
    }

    __syncthreads();

    int bit_mask = (1 << (id & 0x1f));
    if ( y_node < y_node_size ) {
        for (int frame = id; frame < frame_size; frame += id_step) {
            T   y = b;
            for (int x_node = 0; x_node < x_node_size; ++x_node) {
                T   x = x_buf[frame_stride * x_node + (frame/32)];
                T   w = W[x_node][y_node_id];
                if ( x & bit_mask ) {
                    y += w;
                }
//              else {
//                  y -= w;
//              }
            }


        }
    }

    __syncthreads();



    if ( node < node_size ) {
        // read W
        for ( int i = id; i < (1 << N); i += id_step ) {
            W[i][node_id] = W_buf[node * (1 << N) + i];
            if ( lut_binarize ) {
                W[i][node_id] = W[i][node_id] > (T)0.5 ? (T)1.0 : (T)0.0;
            }
        }
        
        // read input index
        for ( int i = 0; i < N; ++i ) {
            x_ptr[i] = &x_buf[frame_stride * input_index[N*node + i]];
        }
                     
        y_ptr = &y_buf[node * frame_stride];
    }

    
    // 平均と分散計測
    T s1 = 0, c1 = 0, y1, t1;
    T s2 = 0, c2 = 0, y2, t2;
    for (int frame = id; frame < frame_size; frame += id_step) {
        if ( node < node_size ) {
            // Forward計算
            int bit  = (1 << (frame & 0x1f));
            int unit = (frame >> 5);
            T x[N];
            for ( int i = 0; i < N; ++i) {
                x[i] = (T)0.5 + ((x_ptr[i][unit] & bit) ? +unbinarize_bias : -unbinarize_bias);
            }
            T y = StochasticLut<N, T, MAX_NODE_UNIT>::NodeForward(node_id, x, W);
//          printf("[0] n=%3d f=%3d y=%10f\n", node, frame, y);

            // 集計
            y1 = y - c1;
            t1 = s1 + y1;
            c1 = (t1 - s1) - y1;
            s1 = t1;

            y2 = (y * y) - c2;
            t2 = s2 + y2;
            c2 = (t2 - s2) - y2;
            s2 = t2;
        }
    }

    s1 = device_LocalSumX<float>(s1, sbuf[node_id]);
    s2 = device_LocalSumX<float>(s2, sbuf[node_id]);

    T mean = s1 * reciprocal_frame_size;
    T var = max(1.0e-5f, (s2 * reciprocal_frame_size) - (mean * mean));
    T rstd = rsqrt(var);

//  if ( node < node_size && id == 0 ) {
////      printf("[0] n=%3d s1=%10f s2=%10f mean=%10f var=%10f rstd=%10f\n", node, s1, s2, mean, var, rstd);
//      printf("0\t%3d\t%.20e\t%.20e\t%.20e\t%.20e\t%.20e\n", node, s1, s2, mean, var, rstd);
//  }

    // 書き込み
    if (id == 0) {
        if ( node < node_size ) {
            running_mean_buf[node] = running_mean_buf[node] * momentum + mean * ((T)1.0 - momentum);
            running_var_buf[node]  = running_var_buf[node] * momentum + var * ((T)1.0 - momentum);
            mean_buf[node] = mean;
            rstd_buf[node] = rstd;
        }
    }

    // 正規化
    int loop_size = ((frame_size + blockDim.x - 1) & ~(blockDim.x - 1));
    for ( int frame = id; frame < loop_size; frame += id_step) {
        int unit     = (frame >> 5);
        int bit      = (frame & 0x1f);
        int bit_mask = (1 << bit);

        int y_mask = 0;
        if ( node < node_size && frame < frame_size) {
            // Forward計算
            T x[N];
            for ( int i = 0; i < N; ++i) {
                x[i] = (T)0.5 + ((x_ptr[i][unit] & bit_mask)  ? +unbinarize_bias : -unbinarize_bias);
            }
            T y = StochasticLut<N, T, MAX_NODE_UNIT>::NodeForward(node_id, x, W);

            y = (y - mean) * rstd;
            y = y * gamma + beta;

            if ( y > (T)0.5 ) {
                y_mask = bit_mask;
            }
        }

        y_mask = device_int_ShuffleOr(y_mask);

        if ( bit == 0 ) {
            if ( node < node_size && frame < frame_size ) {
                y_ptr[unit] = y_mask;
            }
        }
    }
}


BBCU_DLL_EXPORT int bbcu_bit_BinaryDenseAffine_Forward
        (
            int   const     *dev_x_buf,
            int             *dev_y_buf,
            float const     *dev_W,
            float           *dev_mean_buf,
            float           *dev_rstd_buf,
            float           *dev_running_mean_buf,
            float           *dev_running_var_buf,
            float           gamma,
            float           beta,
            float           momentum,
            float           unbinarize_bias,
            int             node_size,
            int             frame_size,
            int             frame_stride,
            int             lut_binarize,
            cudaStream_t    streamId
        )
{
    BBCU_DEBUG_ASSERT(bbcu_IsDeviceAvailable());

    unsigned int const THREAD_SIZE    = 256;
    unsigned int const MAX_FRAME_UNIT = 256;
    unsigned int const MAX_NODE_UNIT  = 8;  // THREAD_SIZE/32 より小さくすること

#if 0
    dim3    block(MAX_FRAME_UNIT, THREAD_SIZE / MAX_FRAME_UNIT);
    while ( (int)block.x / 2 >= frame_size && block.x > 32 ) { block.x /= 2; block.y *= 2; }
    while ( (int)block.y / 2 >= node_size                  ) { block.y /= 2; }
#else
    dim3    block(THREAD_SIZE / MAX_NODE_UNIT, MAX_NODE_UNIT);
    while ( (int)block.y / 2 >= node_size  )                { block.y /= 2; block.x *= 2;}
    while ( (int)block.x / 2 >= frame_size && block.x > 32) { block.x /= 2; }
#endif

    block.x = std::min(block.x, MAX_FRAME_UNIT);
    block.y = std::min(block.y, MAX_NODE_UNIT);
    dim3    grid(1, (node_size + (block.y - 1)) / block.y);
    
    kernal_bit_DifferentiableLut_ForwardTraining<N, float, MAX_FRAME_UNIT, MAX_NODE_UNIT><<<grid, block, 0, streamId>>>(
            dev_x_buf,
            dev_y_buf,
            dev_input_index,
            dev_W,
            dev_mean_buf,
            dev_rstd_buf,
            dev_running_mean_buf,
            dev_running_var_buf,
            gamma,
            beta,
            momentum,
            unbinarize_bias,
            1.0f / (float)frame_size,
            node_size,
            frame_size,
            frame_stride,
            lut_binarize
        );
    BB_CUDA_CHECK_LAST_ERROR();
    
    return 0;
}




// end of file
