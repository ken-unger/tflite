# TensorFlow Lite for PIC64-HPSC

This page describes how to build the TensorFlow Lite library and several examples for PIC64-HPSC-HX and then run these on qemu+debian environment.

## Cross Compiling TensorFlow Lite for the X280 target

This section describes how to build and use the TensorFlow Lite library with CMake tool, and closely follows the instructions here:
- https://www.tensorflow.org/lite/guide/build_cmake
- https://www.tensorflow.org/lite/guide/build_cmake_arm

These steps assume that you have downloaded and installed the HPSC SDK, including the cross-compiler toolchain, QEMU, and Debian image.

### Step 1. Clone the TensorFlow repository

```bash
$ git clone https://github.com/tensorflow/tensorflow.git tensorflow_src
```

### Step 2. Build the TensorFlow binaries for the host (x86) 

This is needed to generate some host side tools used in step 3 

```bash
$ mkdir tflite_build
$ cd tflite_build

$ cmake ../tensorflow_src/tensorflow/lite
$ cmake --build . -j
```

### Step 3. Build the TensorFlow binaries for the X280 (riscv64) 

> Note: The following fix may be required for riscv64 in tensorflow_src/tensorflow/lite/CMakeLists.txt 
>> line 172  'if (NOT CMAKE_SYSTEM_PROCESSOR OR CMAKE_SYSTEM_PROCESSOR MATCHES "x86" OR CMAKE_SYSTEM_PROCESSOR MATCHES "riscv64")'

Substitute the path in RISCVCC_PREFIX below to the riscv64 toolchain in your environment.  The path to TFLITE_HOST_TOOLS_DIR may need to be modified depending upon your folder structure.

```bash
$ mkdir tflite_build_rvv
$ cd tflite_build_rvv

$ RISCVCC_PREFIX=${HOME}/riscv-toolchain/HpscTools-1.4.0-x86_64-linux-ubuntu22/riscv64-unknown-linux-gnu-toolsuite-1.0.6/bin/riscv64-unknown-linux-gnu-
$ RISCVCC_FLAGS="-mabi=lp64d -march=rv64imafdcv_zic64b_zicbop_zicboz_ziccamoa_ziccif_ziccrse_zicsr_zifencei_zihintntl_zihintpause_za64rs_zfh_zba_zbb_zbs_zkt_zvfh_sscofpmf_svinval_svnapot_zvl512b -funsafe-math-optimizations"

$ cmake -DCMAKE_C_COMPILER=${RISCVCC_PREFIX}clang \
  -DCMAKE_CXX_COMPILER=${RISCVCC_PREFIX}clang++ \
  -DCMAKE_C_FLAGS="${RISCVCC_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RISCVCC_FLAGS}" \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_SYSTEM_NAME=Linux \
  -DCMAKE_SYSTEM_PROCESSOR=riscv64 \
  -DTFLITE_HOST_TOOLS_DIR=${HOME}/tflite_build \
  ../tensorflow_src/tensorflow/lite/
$ cmake --build . -j
```

### Step 4. Build the example applications

> Note: fix for label_image linking
>> Remove 'protobuf' from tensorflow_src\tensorflow\lite\examples\label_image\CMakelists.txt line 87 since protobuf is already included as a static library.  On a clean machine, -lprotobuf may not be present

```bash
$ cmake --build . -j -t benchmark_model
$ cmake --build . -j -t label_image  
```

### Copy the binaries and the tflite_model onto QEMU/Debian.

Use the steps outlined in https://hpsc.microchip.com/docs/debian_support_on_p64h.html (Sharing files between the host and the target) to mount the host path into QEMU/Debian, to enable copying of the generated binaries to the local filesystem in QEMU/Debian

From within QEMU/Debian --
```bash
# cp /mnt/tflite_build_rvv/tools/benchmark/benchmark_model .
# cp /mnt/tflite_build_rvv/examples/label_image/label_image .
```

## Running TensorFlow Lite on the X280 target (QEMU/Debian)

The following models are included in tflite_model:
- Image classification:
  - EfficientNet-lite 0 (f32, int8)
  - MobileNetV1 (f32, uint8)
  - MobileNetV2 (f32, uint8)
  - MobileNetV3-large (f32, uint8)
  - MobileNetV3-small (f32, uint8)
  - MobileNetEdgeTPU (f32, uint8)
  - Resnet50 (f32, int8)
- Object detection:
  - SSD MobileNetV1 (f32, uint8)
  - MobileDETs (f32, uint8)
- Natural Language Processing:
  - MobileBERT (f32, uint8)


> Note:  One can copy the tflite_model contents to the QEMU/Debian filesystem, but this package is large and so this README illustrates using that from the host filesystem relative to its mount point (/mnt) within QEMU/Debian.  Some paths may be different depending upon the user's installation.

### TensorFlow Lite Model Benchmarking Tool

The TensorFlow benchmark model tool (benchmark_model) can be used to benchmark any TensorFlow Lote model and its individual operators.  This tool takes a TensorFlow Lite model, generates random inputs, and runs the model for a specified number of runs.  The aggregate latency statistics can be reported at the completion of execution. For more information on this tool consult https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/tools/benchmark/README.md

```bash
# ./benchmark_model --num_runs=1 --num_threads=1 --enable_op_profiling=true --graph=/mnt/hpsc/tflite/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.uint8.tflite
# ./benchmark_model --num_runs=1 --num_threads=1 --enable_op_profiling=true --graph=/mnt/hpsc/tflite/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.f32.tflite

# ./benchmark_model --num_runs=1 --num_threads=8 --enable_op_profiling=true --graph=/mnt/hpsc/tflite/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.uint8.tflite
# ./benchmark_model --num_runs=1 --num_threads=8 --enable_op_profiling=true --graph=/mnt/hpsc/tflite/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.f32.tflite
```

> Note:  QEMU does not accurately model caches, instruction latencies and many other things, and so the performance numbers generated here are not indicative of true performance.  In fact, RVV performance far exceeds what is reported when running on QEMU.  A comparative performance chart will be provided for these examples in the future.  Nevertheless, QEMU can be used for functional correctness tests prior to execution on real silicon (or hardware emulation)

### TensorFlow Lite Image Classification Demo

The TensorFlow label image example (label_image) demonstrates how to load a pre-trained and converted TensorFlow Lite model and use it to recognize objects in images.  The demo is further described in https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/examples/label_image

![grace_hopper.bmp](/examples/label_image/grace_hopper.bmp)

```bash
# ./label_image -i /mnt/hpsc/tflite/examples/label_image/grace_hopper.bmp -m /mnt/hpsc/tflite/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.uint8.tflite -l /mnt/hpsc/tflite/tflite_model/image_classification/mobilenet_v1/labels.txt
INFO: total proces:1 process_num:0
INFO: Loaded model /mnt/hpsc/tflite/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.uint8.tflite
INFO: resolved reporter
INFO: use imagenet:0 total process:1
INFO: read_bmp: 831.791 ms
INFO: image width:517 image height:606 image channels:3
INFO: wanted width:224 wanted height:224 wanted channels:3
INFO: resize: 154.662 ms

INFO: resize: 167.814 ms
INFO: 0.756863: 653 653:military uniform
INFO: 0.121569: 907 907:Windsor tie
INFO: 0.0156863: 458 458:bow tie, bow-tie, bowtie
INFO: 0.0117647: 466 466:bulletproof vest
INFO: 0.00784314: 835 835:suit, suit of clothes
```

### TensorFlow Lite Object Detection Demo

To be completed ...

-----------------------------------
