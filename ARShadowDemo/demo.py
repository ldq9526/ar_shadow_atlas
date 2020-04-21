# coding=utf-8

import os
import os.path as osp
import numpy as np
import cv2 as cv
import time
import hiai
from hiai.nn_tensor_lib import DataType

# OM model path
omModelName = osp.join('models', 'model.om')

# image data folder
testDataDir = 'data'

# folder to restore result images
outputDir = 'output'

# input size of network model
inputWidth = 256
inputHeight = 256


def CreateGraph(model):
    # Get default graph, then arrange the pipeline
    myGraph = hiai.hiai._global_default_graph_stack.get_default_graph()
    if myGraph is None:
        print("[ERROR] Fail to get default graph.")
        return None

    nnTensorList = hiai.NNTensorList()
    hiai.inference(nnTensorList, model, None)

    if hiai.HiaiPythonStatust.HIAI_PYTHON_OK == myGraph.create_graph():
        print("[OK] Finish creating graph.")
        return myGraph
    else:
        print("[ERROR] Fail to create graph, please check Davinc log.")
        return None


def DestroyGraph():
    # Destroy graph
    hiai.hiai._global_default_graph_stack.get_default_graph().destroy()


def GraphInference(graphHandle, inputTensorList):
    if not isinstance(graphHandle, hiai.Graph):
        print("[ERROR] graphHandle is not a Graph object.")
        return None

    resultList = graphHandle.proc(inputTensorList)
    return resultList


def ReadImage(fileName, channels):
    if channels != 1 and channels != 3:
        print("[ERROR] Wrong image channel parameter.")
        return None
    if channels == 3:
        image = cv.imread(fileName, cv.IMREAD_COLOR)
    else:
        image = cv.imread(fileName, cv.IMREAD_GRAYSCALE)
    if image.shape[0] != inputHeight or image.shape[1] != inputWidth:
        image = cv.resize(image, (inputWidth, inputHeight), interpolation=cv.INTER_CUBIC)
    if image.ndim == 2:
        image = np.expand_dims(image, axis=2)
    return image.astype(np.float32)


def SaveResult(resultList, fileName):
    # Data format conversion: result -> (reshape) -> NCHW -> (transpose, copy) -> NHWC
    # [https://ascend.huawei.com/doc/Atlas200DK/1.3.0.0/zh/zh-cn_topic_0161025328.html]
    resultArray = resultList[0].reshape([1, 3, inputHeight, inputWidth])
    resultImage = resultArray[0].transpose([1, 2, 0]).copy()
    resultImage = ((resultImage + 1.0) * 127.5).astype(np.uint8)
    cv.imwrite(osp.join(outputDir, fileName), resultImage)


def main():
    inferenceModel = hiai.AIModelDescription('ShadowGAN', omModelName)
    myGraph = CreateGraph(inferenceModel)
    if myGraph is None:
        exit(0)

    if not osp.exists(outputDir):
        os.makedirs(outputDir)

    # Read images and corresponding masks
    inputImage = ReadImage(osp.join(testDataDir, 'noshadow', 'demo.jpg'), channels=3)
    if inputImage is None:
        print("[ERROR] No input image.")
        DestroyGraph()
        exit(0)
    inputMask = ReadImage(osp.join(testDataDir, 'mask', 'demo.jpg'), channels=1)
    if inputMask is None:
        print("[ERROR] No input mask.")
        DestroyGraph()
        exit(0)

    # Normalize to [-1.0, 1.0]
    inputImage = inputImage / 127.5 - 1.0
    inputMask = 1.0 - inputMask / 127.5

    # Convert HWC format to CHW
    # Note: hiai.NNTensor() only takes NCHW data as input.
    # [https://ascend.huawei.com/doc/Atlas200DK/1.3.0.0/zh/zh-cn_topic_0161025273.html]
    inputImage = inputImage.transpose([2, 0, 1]).copy()
    inputMask = inputMask.transpose([2, 0, 1]).copy()
    inputImageTensor = hiai.NNTensor(inputImage, inputWidth, inputHeight, 3, 'input_image',
                                     DataType.FLOAT32_T, inputWidth * inputHeight * 3)
    inputMaskTensor = hiai.NNTensor(inputMask, inputWidth, inputHeight, 1, 'input_mask',
                                    DataType.FLOAT32_T, inputWidth * inputHeight * 1)
    nntensorList = hiai.NNTensorList([inputImageTensor, inputMaskTensor])

    print("Inference start...")
    startTime = time.time()
    resultList = GraphInference(myGraph, nntensorList)
    if resultList is None:
        print("[ERROR] Inference failed.")
        DestroyGraph()
        exit(0)
    endTime = time.time()
    inferenceTime = endTime - startTime
    SaveResult(resultList, 'demo.jpg')

    DestroyGraph()
    print("Inference finished. Inference time: %.3fms" % (inferenceTime * 1000))


if __name__ == "__main__":
    main()
