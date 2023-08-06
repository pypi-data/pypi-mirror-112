print("***********")
### 对`NumPy.ndarray`格式数据进行预测
import cv2
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50')
infer_imgs = cv2.imread("docs/images/whl/demo.jpg")
result=clas.predict(infer_imgs)
print(next(result))
exit()

print("***********")
### 保存预测结果
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50', save_dir='./output_pre_label/')
infer_imgs = 'docs/images/whl/' # it can be infer_imgs folder path which contains all of images you want to predict.
result=clas.predict(infer_imgs)
print(next(result))


print("***********")
# 快速开始
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50')
infer_imgs='docs/images/whl/demo.jpg'
result=clas.predict(infer_imgs)
print(next(result))

print("***********")
# 使用384输入模型
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ViT_base_patch16_384', resize_short=384, crop_size=384)

print("***********")
### 使用PaddleClas提供的预训练模型进行预测
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50')
infer_imgs = 'docs/images/whl/demo.jpg'
result=clas.predict(infer_imgs)
print(next(result))

print("***********")
### 使用本地模型文件预测
from paddleclas import PaddleClas
clas = PaddleClas(inference_model_dir='./inference/')
infer_imgs = 'docs/images/whl/demo.jpg'
result=clas.predict(infer_imgs)
print(next(result))

print("***********")
### 批量预测
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50', batch_size=2)
infer_imgs = 'docs/images/'
result=clas.predict(infer_imgs)
for r in result:
    print(r)




print("***********")
### 指定label name
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50', class_id_map_file='./ppcls/utils/imagenet1k_label_list.txt')
infer_imgs = 'docs/images/whl/demo.jpg'
result=clas.predict(infer_imgs)
print(next(result))


print("***********")
### 对网络图片进行预测
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50')
infer_imgs = 'https://github.com/paddlepaddle/paddleclas/blob/release%2F2.2/docs/images/whl/demo.jpg'
result=clas.predict(infer_imgs)
print(next(result))
