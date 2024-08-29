# MobilenetV3
* The models are download from [models/research/slim/nets/mobilenet/README.md](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet/README.md) in [tensorflow model garden repo](https://github.com/tensorflow/models).

### mobilenet_v3_large_1.0_224.f32.tflite
* Come from Mobilenet V3 Imagenet Checkpoints with setting `Large dm=1 (float)`   [[LINK](https://storage.googleapis.com/mobilenet_v3/checkpoints/v3-large_224_1.0_float.tgz "LINK")]
    * Untar and extract `v3-large_224_1.0_float.tflite` which is the same as `mobilenet_v3_large_1.0_224.f32.tflite`

### mobilenet_v3_large_1.0_224.uint8.tflite
* Come from  Mobilenet V3 Imagenet Checkpoints with setting `Large dm=1 (8-bit)`  [[LINK](https://storage.googleapis.com/mobilenet_v3/checkpoints/v3-large_224_1.0_uint8.tgz "LINK")]
    * Untar and extract `v3-large_224_1.0_uint8.tflite` which is the same as `mobilenet_v3_large_1.0_224.uint8.tflite`

### mobilenet_v3_small_1.0_224.f32.tflite
* Come from Mobilenet V3 Imagenet Checkpoints with setting `Small dm=1 (float)`   [[LINK](https://storage.googleapis.com/mobilenet_v3/checkpoints/v3-small_224_1.0_float.tgz "LINK")]
    * Untar and extract `v3-small_224_1.0_float.tflite` which is the same as `mobilenet_v3_small_1.0_224.f32.tflite`

### mobilenet_v3_small_1.0_224.uint8.tflite
* Come from  Mobilenet V3 Imagenet Checkpoints with setting `Small dm=1 (8-bit)`  [[LINK](https://storage.googleapis.com/mobilenet_v3/checkpoints/v3-small_224_1.0_uint8.tgz "LINK")]
    * Untar and extract `v3-small_224_1.0_uint8.tflite` which is the same as `mobilenet_v3_small_1.0_224.uint8.tflite`

### labels.txt
* MobilenetV3 model is training with 1001 categories (including background) - [Labels file](https://github.com/google-coral/edgetpu/blob/master/test_data/imagenet_labels.txt "LINK").
