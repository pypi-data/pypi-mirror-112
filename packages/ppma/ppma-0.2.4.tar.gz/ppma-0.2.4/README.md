

![acuowkoa](C:\Users\Mike\Desktop\acuowkoa.png)

# 📦 Paddle Model Analysis

[![](https://img.shields.io/badge/Paddle-2.0-blue)](https://www.paddlepaddle.org.cn/)[![Documentation Status](https://img.shields.io/badge/Tutorial-最新-brightgreen.svg)](https://paddlepaddle.org.cn/documentation/docs/zh/guides/index_cn.html)[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)![](https://img.shields.io/badge/version-0.1-yellow)

这是基于飞桨开发的工具包，主要用于对分类任务模型进行快速分析![qaeewagy](C:\Users\Mike\Desktop\qaeewagy.png)

目前所支持的功能有：![oqrhsqot](C:\Users\Mike\Desktop\oqrhsqot.gif)

- [x] ImageNet 上快速验证模型
- [x] 测试图片 Top5 类别
- [x] 测试模型 Param、Thoughtout
- [x] CAM (Class Activation Mapping)
- [x] TTA (Test Time Augmention)
- [ ] 补充中 ...

## Install

```bash
pip install ppma -i https://pypi.python.org/simple
```

## Tutorial

### ImageNet 上快速验证模型

当训练了新的模型后，或者复现了某个模型，我们需要在 ImageNet 数据集上验证性能，先准备数据集结构如下

```bash
data/ILSVRC2012
		├─ ILSVRC2012_val_00000001.JPEG
		├─ ILSVRC2012_val_00000002.JPEG
		├─ ILSVRC2012_val_00000003.JPEG
		├─ ...
		├─ ILSVRC2012_val_00050000.JPEG
		└─ val.txt	# target
```

准备好数据集后，运行以下代码

```python
import ppma
import paddle

model = paddle.vision.models.resnet50(pretrained=True)	# 可以替换自己的模型
data_path = "data/ILSVRC2012"	                        # 数据路径

ppma.imagenet.val(model, data_path)
```

### 测试图片 Top5 类别

```python
import ppma
import paddle

img_path = 'test.jpg'                                    # 图片路径
model = paddle.vision.models.resnet50(pretrained=True)   # 可以替换自己的模型

ppma.imagenet.test_img(model, img_path)
```

### 测试模型 Param、Thoughtout

```python
import ppma
import paddle

model = paddle.vision.models.resnet50()   # 可以替换自己的模型

# Params
param = ppma.tools.param(model)
print('Params：{:,}'.format(param))

# Thoughtout
ppma.tools.throughput(model, image_size=224)
```

### CAM (Class Activation Mapping)

```python
import paddle
import matplotlib.pyplot as plt
from ppma import cam

img_path = 'img1.jpg'                                      # 图片路径
model = paddle.vision.models.resnet18(pretrained=True)     # 模型定义
target_layer = model.layer4[-1]                            # 提取模型某层的激活图
cam_extractor = cam.GradCAMPlusPlus(model, target_layer)   # 支持 GradCAM、XGradCAM、GradCAM++

# 提取激活图
activation_map = cam_extractor(img_path, label=None)   
plt.imshow(activation_map)
plt.axis('off')
plt.show()

# 与原图融合
cam_image = cam.overlay(img_path, activation_map)   
plt.imshow(cam_image)
plt.axis('off')
plt.show()
```

Note：迄今为止，模型风格分为三个部分：CNN、ViT、MLP，对于不同的模型，提取激活图的`target_layer`也不尽相同

- Resnet18 and 50: model.layer4[-1]
- VGG and densenet161: model.features[-1]
- mnasnet1_0: model.layers[-1]
- ViT: model.blocks[-1].norm1
- SwinT: model.layers[-1].blocks[-1].norm1

### TTA (Test Time Augmention)

