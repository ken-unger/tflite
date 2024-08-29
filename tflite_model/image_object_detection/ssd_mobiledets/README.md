# SSD MobileDets

### ssd_mobiledets.f32.tflite
* From MLPerf mobile_models repo [[LINK](https://github.com/mlcommons/mobile_models/tree/main/v1_0/tflite "LINK")]. The `mobiledet.tflite` in [LINK](https://github.com/mlcommons/mobile_models/tree/main/v1_0/tflite "LINK") is the same as `ssd_mobiledets.f32.tflite`.

### ssd_mobiledets.uint8.tflite
* From MLPerf mobile_models repo [[LINK](https://github.com/mlcommons/mobile_models/tree/main/v1_0/tflite "LINK")]. 
* The `mobiledet_qat.tflite` in [LINK](https://github.com/mlcommons/mobile_models/tree/main/v1_0/tflite "LINK") is the same as `ssd_mobiledets.uint8.tflite`.

---

### How to convert ssd mobiledets from TF model to TFLite model

- TF model downlaod link: [http://download.tensorflow.org/models/object_detection/ssdlite_mobiledet_edgetpu_320x320_coco_2020_05_19.tar.gz](http://download.tensorflow.org/models/object_detection/ssdlite_mobiledet_edgetpu_320x320_coco_2020_05_19.tar.gz)

- To transform TF model to TFLite model, model needs to be manually converted through [ssd frozen graph](https://github.com/tensorflow/models/tree/master/research/object_detection/ "ssd frozen graph") and  [TOCO](https://github.com/tensorflow/tensorflow/tree/r1.14/tensorflow/contrib/quantize#generating-fully-quantized-models "TOCO").<br> 

#### ssd_mobiledets.f32.tflite
* After downloading, edit the `score_threshold` to 0.3 in `fp32/pipeline.config` and export the frozen graph using `export_tflite_ssd_graph.py` with regular nms post-processing:
    ```
    export_tflite_ssd_graph.py \ 
    --input_type image_tensor \
    --pipeline_config_path ${TF_MODEL_DIR}/fp32/pipeline.config \
    --trained_checkpoint_prefix ${TF_MODEL_DIR}/fp32/model.ckpt-400000 \
    --output_directory ${TFLITE_MODEL_DIR}/fp32/ \
    --add_postprocessing_op=true \
    --use_regular_nms=true \
    --max_detections=10
    ```
*   Then this `tflite_graph.pb` is converted to TFLite format using TOCO:
    ```
    toco \
    --input_file=/path/to/ssdlite_mobiledet_edgetpu_320x320_coco_2020_05_19/fp32/tflite_graph.pb \
    --output_file=/path/to/research/ ssdlite_mobiledet_edgetpu_320x320_coco_2020_05_19/fp32/mobiledet.tflite \
    --input_shapes=1,320,320,3 \
    --input_arrays=normalized_input_image_tensor \
    --output_arrays='TFLite_Detection_PostProcess','TFLite_Detection_PostProcess:1','TFLite_Detection_PostProcess:2','TFLite_Detection_PostProcess:3' \
    --inference_type=FLOAT \
    --allow_custom_ops
    ```

#### ssd_mobiledets.uint8.tflite
*   Edit the `score_threshold` to 0.3 in `uint8/pipeline.config`, and export the frozen graph using 
    `export_tflite_ssd_graph.py` with regular nms post-processing:

    ```
    export_tflite_ssd_graph.py \
    --input_type image_tensor \
    --pipeline_config_path ${TF_MODEL_DIR}/uint8/pipeline.config \
    --trained_checkpoint_prefix ${TF_MODEL_DIR}/uint8/model.ckpt-400000 \
    --output_directory \
    ${TFLITE_MODEL_DIR}/uint8/ \
    --add_postprocessing_op=true \
    --use_regular_nms=true \
    --max_detections=10
    ```

*   Then this `tflite_graph.pb` is converted to TFLite format using TOCO:
    ```
    toco \
    --input_file=/path/to/ssdlite_mobiledet_edgetpu_320x320_coco_2020_05_19/uint8/tflite_graph.pb \
    --output_file=/path/to/ssdlite_mobiledet_edgetpu_320x320_coco_2020_05_19/uint8/mobiledet_qat.tflite \
    --input_shapes=1,320,320,3 \
    --input_arrays=normalized_input_image_tensor \
    --output_arrays='TFLite_Detection_PostProcess','TFLite_Detection_PostProcess:1','TFLite_Detection_PostProcess:2','TFLite_Detection_PostProcess:3'  \
    --inference_type=QUANTIZED_UINT8 \
    --allow_custom_ops \
    --mean_values=128 --std_values=128
    ```

