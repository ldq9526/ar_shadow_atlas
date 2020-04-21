# 目录说明
* doc目录包含所有的项目文档
* ARShadowDemo目录为项目的目录，包含可直接在30版本DDK下运行的模型文件

# 
# 详细的开发部署指导以及模型转换请参照readme-1.3.0.doc
# 
# 请使用 1.3.0.0版本MindStudio
# AR阴影生成
开发者可以将本Demo部署至Atlas 200 DK上实现AR图像的虚拟物体阴影生成。
## 前提条件
部署此Demo前，需要准备好以下环境：
* 已完成MindStudio的安装，详细请参考Mind Studio安装指南《Ascend 310 Mind Studio工具安装指南》。
* 已完成Atlas 200 DK开发者板与Mind Studio的连接，交叉编译器的安装，SD卡的制作及基本信息的配置等，详细请参考Atlas 200 DK使用指南《Ascend 310 开发者板使用指导（Atlas 200 DK）》。
## 原模型训练
需要按照以下地址获取文件和数据集，详细使用请看开发指导书。
* 链接: https://pan.baidu.com/s/120f8pHF2_Tn1AqGcFo35zw (提取码: 2j7b)
* 数据集制作两种工具exe文件以及工具说明手册分别位于目录"需要标记物的数据制作工具"与"无需标记物的数据制作工具"
* 获取数据集、TensorFlow模型训练、测试与转换代码请下载目录"ShadowGAN"


