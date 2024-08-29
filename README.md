# TensorFlow Lite for PIC64-HPSC-HX

This page describes how to build the TensorFlow Lite library and several examples for PIC64-HPSC-HX and then run these on qemu+debian environment.

## Cross Compiling TensorFlow Lite for the X280 target

This section describes how to build and use the TensorFlow Lite library with CMake tool, and closely follows the instructions here:
https://www.tensorflow.org/lite/guide/build_cmake
https://www.tensorflow.org/lite/guide/build_cmake_arm

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

Substitute the path in RISCVCC_PREFIX to the riscv64 toolchain in your environment.

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

> Note: The following fix may be required for riscv64 in CMakeLists.txt 
>> line 172  'if (NOT CMAKE_SYSTEM_PROCESSOR OR CMAKE_SYSTEM_PROCESSOR MATCHES "x86" OR CMAKE_SYSTEM_PROCESSOR MATCHES "riscv64")'

### Step 4. Build the example applications

```bash
$ cmake --build . -j -t benchmark_model
$ cmake --build . -j -t label_image  
```

> Note: fix for benchmark_model compilation
>>

> Note: fix for label_image compilation
>>

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

### Copy the binaries and the tflite_model onto QEMU/Debian.

TBD exact steps.



### Execute the benchmark example on QEMU

```bash
$ ./benchmark_model --num_runs=1 --num_threads=1 --graph=../hpsc/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.uint8.tflite
$ ./benchmark_model --num_runs=1 --num_threads=1 --graph=../hpsc/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.f32.tflite

$ ./benchmark_model --num_runs=1 --num_threads=8 --graph=../hpsc/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.uint8.tflite
$ ./benchmark_model --num_runs=1 --num_threads=8 --graph=../hpsc/tflite_model/image_classification/mobilenet_v1/mobilenet_v1_1.0_224.f32.tflite
```

### Execute the label_image example on QEMU

-----------------------------------