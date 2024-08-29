# Mobilenet Edge TPU
*  The models are download from [models/research/slim/nets/mobilenet/README.md](https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet/README.md) in [tensorflow model garden repo](https://github.com/tensorflow/models). Edge TPU checkpoints with setting: `MobilenetEdgeTPU dm=1 (8-bit)`[[LINK](https://storage.cloud.google.com/mobilenet_edgetpu/checkpoints/mobilenet_edgetpu_224_1.0.tgz "LINK")]. 
### mobilenet_edgetpu_1.0_224.f32.tflite
* Same as `mobilenet_edgetpu_224_1.0_float.tflite` which downlaods from [[LINK](https://storage.cloud.google.com/mobilenet_edgetpu/checkpoints/mobilenet_edgetpu_224_1.0.tgz "LINK")].

### mobilenet_edgetpu_1.0_224.int8.tflite
* Same as `mobilenet_edgetpu_224_1.0_int8.tflite` ｓwhich downlaods from [[LINK](https://storage.cloud.google.com/mobilenet_edgetpu/checkpoints/mobilenet_edgetpu_224_1.0.tgz "LINK")].

### mobilenet_edgetpu_1.0_224.uint8.tflite
* Same as `mobilenet_edgetpu_224_1.0_uint8.tflite` which downlaods from [[LINK](https://storage.cloud.google.com/mobilenet_edgetpu/checkpoints/mobilenet_edgetpu_224_1.0.tgz "LINK")].

### labels.txt
* Mobilenet Edge TPU model is training with 1001 categories (including background) - [Labels file](https://github.com/google-coral/edgetpu/blob/master/test_data/imagenet_labels.txt "LINK").
