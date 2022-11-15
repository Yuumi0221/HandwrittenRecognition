# Handwritten Recognition - V0.2.3

该项目为2022学年第一学期多媒体技术课程大作业期末项目。可下载内容为该项目的完整代码，包括微信小程序前端代码以及后端服务器代码。



## 文件组织结构

下载后解压可以看到文件结构：

```
Group11 Handwritten Recognition
├── HandwrittenRecognition-0.2.3	// 后端代码
|   ├── main.py		// 运行以启动后端服务器
|   ├── model		// 五种算法各两个模型，共十个模型
|   ├── imgs
|   |   └── temp.png	// 识别图片将存在这里
|   ├── letter_acc_test	// 手写字母识别测试，详情见其中的README文件
|   └── ...
├── wxappdemo	// 小程序前端代码
|   ├── pages	// 前端页面代码
|   └── ...
└── README.md	// 此文档
```



## 下载

- [**GitHub**](https://github.com/Yuumi0221/HandwrittenRecognition)

  ```bash
  git clone git@github.com:Yuumi0221/HandwrittenRecognition.git
  ```
  
  由于GitHub存在上传限制，KNN、SVM和RF算法的模型体积较大，不便上传。如需测试，请自行运行 */letter/\{算法名}\_letter_model.py* 以及 */number/\{算法名}\_num_model.py* 文件，生成模型后再运行 *main.py* 启动后端服务器。


- [**GitLab**](http://202.120.87.186:49080/MultiMediaCourse-2022-Tue/group11-handwritten-recognition)

  提交作业用链接，仅在校园网内可以访问，校外请连接学校VPN

  ```bash
  git clone http://202.120.87.186:49080/MultiMediaCourse-2022-Tue/group11-handwritten-recognition.git
  ```




## 配置清单

后端服务器使用 Python 编写，所需依赖环境如下：

```
opencv-python~=4.5.3.56
numpy~=1.21.2
halo~=0.0.31
sklearn~=0.0
scikit-learn~=0.23.2
keras~=2.8.0
matplotlib~=3.4.3
uvicorn~=0.17.6
pillow~=8.0.1
fastapi~=0.76.0
```



## 运行

1. **启动后端服务器**

   确保模型下载完毕后，双击打开 *HandwrittenRecognition-0.2.3* 目录下的 *main.py* 文件，看到提示 `Application startup complete.` 即为运行成功。

   使用 Ctrl+C（Windows系统）或 Command+Q（MacOS）可以退出程序。

2. **启动微信小程序前端**

   打开微信开发者工具，导入 *wxappdemo* 目录，编译完成后即可正常运行使用。
