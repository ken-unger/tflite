
# MobileBert

Two mobilebert tflite models (fp32/int8) are provided. Both of them are converted from pretrained tensorflow model by TFLite_converter.

## Prepare models and Calibration data

### Download pretrained models
The pretrained models comes from [google-research/google-research/mobilebert](https://github.com/google-research/google-research/tree/master/mobilebert). The models download link: [link](https://storage.googleapis.com/cloud-tpu-checkpoints/mobilebert/mobilebert_squad_savedmodels.tar.gz).
Please use following command to downlaod the models.
```
$ curl -L https://storage.googleapis.com/cloud-tpu-checkpoints/mobilebert/mobilebert_squad_savedmodels.tar.gz --output mobilebert_squad_savedmodels.tar.gz
$ tar zxvf mobilebert_squad_savedmodels.tar.gz
```
* mobilebert.fp32.tflite: converter from the tensorflow model which is in `./mobilebert_squad_savedmodels/float`.
* mobilebert.int8.tflite: converter from the tensorflow model which is in `./mobilebert_squad_savedmodels/quant_saved_model`.

### Calibration data
* To generate INT8 tflite model, calibration data is required.
* Calibration data (vocab.txt and train-v1.1.json) is prepared in `./data` to perform calibration.
* `export_mobilebert.py` uses 100 train data to calibrate the model to INT8.

## Convert tensorflow model to tflite model
This script is to convert tensorflow model to tflite model. It's modified from [google-research/google-research/mobilebert](https://github.com/google-research/google-research/tree/master/mobilebert).

-  This script has tested in `tensorflow 2.5.0`.

### Export FP32 model
```
$ python3 export_mobilebert.py --export_dir $(export_dir)

# Example
$ python3 export_mobilebert.py --export_dir ./
```
After runnig the script, the output model is stroed in `$(export_dir)/mobilebert.fp32.tflite`.

### Export INT8 model
```
$ python3 export_mobilebert.py --vocab_file $(vocab_file) --train_file $(train_file) --quant --export_dir $(export_dir)

# Example
$ python3 export_mobilebert.py --vocab_file ./data/vocab.txt --train_file ./data/train-v1.1.json --quant export_dir ./
```
After runnig the script, the output model is stroed in `$(export_dir)/mobilebert.int8.tflite`.

