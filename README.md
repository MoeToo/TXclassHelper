# **疼讯课堂小助手 TXclass Helper** v0.6
**_请在运行该程序前阅读本文档_**

## 使用
运行main.py，选择使用环境后点击开始运行即可
- 如发现不能正确识别（字体及其他差异导致），可以自行对签到按钮截图并将pc.png（客户端）或web.png（网页端）按钮图片进行替换
- 如需exe文件可百度教程自行打包
- 基本功能已经实现，本项目不再更新
[介绍视频(av595623381)](https://www.bilibili.com/video/av595623381)

## 原理
1. 读取目标按钮图片（支持网页版、PC客户端）
2. 定时每5秒截取屏幕进行检测
3. 如果发现相似度>=0.9则计算相似部位中心点
4. 移动鼠标至中心点并尝试点击，同时发出蜂鸣提示
5. 点击后1s对点击结果进行截取并保存

## Todo List
- [x] 执行点击操作后进行截图以便检查点击结果
- [x] 尝试点击签到时发出蜂鸣声进行提示
- [x] 执行时进行提示并记录时间
- [x] 支持网页版、客户端双端签到
- [x] 发生错误自动发出蜂鸣强提醒

### 提示
1. 如果签到窗口被其他窗口覆盖，将无法准确检测
2. 客户端如果开启*窗口置顶*有可能会将签到窗口遮挡

## 免责声明
> 本项目为Python学习练手程序，请勿滥用。  

__*因滥用本程序带来的后果作者概不负责！*__

## 许可证
Licensed under The MIT License
