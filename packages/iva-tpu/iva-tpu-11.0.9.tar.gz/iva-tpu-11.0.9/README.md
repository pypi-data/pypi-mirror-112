# IVA TPU Python API
## Main entities
### TPUDevice
TPUDevice is a device handle

### TPUProgram
TPUProgram contains TPU instructions and weigths data

### TPUInference
TPUInference contains input/output data

## Example
```python
import asyncio
import numpy as np
from iva_tpu import TPUDevice, TPUProgram, TPUProgramInfo, TPUInference

from iva_applications.resnet50 import image_to_tensor
from iva_applications.imagenet import tpu_tensor_to_classes
from PIL import Image

image = Image.open('ILSVRC2012_val_00000045.JPEG')
tensor = image_to_tensor(image)

device = TPUDevice()
program = TPUProgram("resnet50.tpu", TPUProgramInfo()) #default TPUProgramInfo is totally fine
device.load_program(program)
inference = TPUInference(program)
inference.load_tensors([tensor])
status_future = device.load_inference(inference)  # device returns future for inference status
event_loop = asyncio.get_event_loop()
status = event_loop.run_until_complete(status_future)
assert status.is_success # check that there is no errors during inference
output = inference.get_tensors() # get results
tpu_tensor_to_classes(output[0], top=1)
```

## TPU Dictionary interface
```
...
program = TPUProgram("resnet50.tpu", TPUProgramInfo())
inference = TPUInference(program)
inference.load_tensors_dict({"Placeholder:0": tensor})
...
assert status.is_success
output = inference.get_tensors_dict()
tpu_tensor_to_classes(output["logits:0"], top=1)
```

## TPU Blocking interface
```
status = device.load_inference_sync(inference) #would block until completion
```

## TPU Raw buffer examples
```
import asyncio
from iva_tpu import TPUDevice, TPUProgram, TPUProgramInfo, TPUInference
program = TPUProgram("omega_program_dnn_quant_3.0.0.tpu", TPUProgramInfo())
device = TPUDevice()
device.load_program(program)
inference = TPUInference(program)

with open("f.bin", "rb") as f:
    buf=f.read()

inference.load_raw([buf])
asyncio.get_event_loop().run_until_complete(device.load_inference(inference))
outputs = inference.get_raw()

for i in range(3):
  o = outputs[i]
  with open(f"o{i}.bin", "wb") as f:
    f.write(o)
```
