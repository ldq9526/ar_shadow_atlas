# 说明
* 本目录包含AR阴影生成在Atlas 200 DK开发者板上的运行示例

# 模型
* model.om: Ascend 310直接支持执行的网络模型

# 网络推断代码
* demo.py: 实现在Atlas 200 DK开发者板上执行网络推断，输入无虚拟阴影的AR图像与虚拟物体mask，输出包含虚拟阴影的AR图像
* display.py: 网络推断前后的图像显示

# 部署脚本
* deploy.sh: 示例的部署脚本，运行该脚本可将所需要的示例代码部署到Atlas 200 DK开发者板
* demo.sh: 示例的运行脚本，实现输入图像的传送，在Atlas 200 DK开发者板执行网络推断，再将结果拷贝回调用方的主机

# 样例数据
* data/: 该目录提供了三组样例图片可供开发者测试示例，有noshadow与mask两个子目录，要求两个子目录中对应的图片具有相同的文件名，完整的数据集可从 https://pan.baidu.com/s/120f8pHF2_Tn1AqGcFo35zw (提取码: 2j7b) 的ShadowGAN目录下载data.zip

# 
# 详细的开发部署指导以及模型转换请参照readme-1.3.0.doc
# 
