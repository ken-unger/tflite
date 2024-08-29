# SSD Mobilenet v1

### ssd_mobilenet_v1.f32.tflite
* From MLPerf inference Reference Models Zenodo [[LINK](https://zenodo.org/record/3361502#.YKYFz6gzaUk "LINK")]

### ssd_mobilenet_v1.uint8.tflite
* From Tensorflow hub  [[LINK](https://tfhub.dev/tensorflow/lite-model/ssd_mobilenet_v1/1/default/1 "LINK")]

### ssd_mobilenet_v1_mlperf.uint8.tflite
* From MLPerf inference Reference Models Zenodo [[LINK](https://zenodo.org/record/3439376#.YKYH8qgzaUk "LINK")]. The downloaded model is TF model, we need to convert it to TFLite model manually through [ssd frozen graph](https://github.com/tensorflow/models/tree/master/research/object_detection/ "ssd frozen graph") and  [TOCO](https://github.com/tensorflow/tensorflow/tree/r1.14/tensorflow/contrib/quantize#generating-fully-quantized-models "TOCO").<br>

#### Step 1:
``` shell
$ python  export_tflite_ssd_graph.py \
--pipeline_config_path=$CONFIG_FILE \
--trained_checkpoint_prefix=$CHECKPOINT_PATH \
--output_directory=$OUTPUT_DIR \
--add_postprocessing_op=True
```

#### Step 2:
``` shell
$ toco  \
--input_file=$OUTPUT_DIR/tflite_graph.pb \
--output_file=$OUTPUT_DIR/detect.tflite \
--input_shapes=1,300,300,3 \
--input_arrays=Placeholder \
--output_arrays='TFLite_Detection_PostProcess','TFLite_Detection_PostProcess:1','TFLite_Detection_PostProcess:2','TFLite_Detection_PostProcess:3'  \
--inference_input_type=QUANTIZED_UINT8 \
--inference_type=QUANTIZED_UINT8 \
--mean_values=128 \
--std_values=128 \
--allow_custom_ops
```
* The accuracy of `ssd_mobilenet_v1_mlperf.uint8.tflite` (mAP=22.76) is higher than `ssd_mobilenet_v1.uint8.tflite` (mAP=16.12).

### ssd_mobilenet_v1.f16.tflite [Experimental]
* Translated from `ssd_mobilenet_v1.f32.tflite` by sifive internal tool. If you are interested on it, please contact [sifive](https://www.sifive.com/contact "sifive").
