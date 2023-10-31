# OnlineStat
一个在线统计分析网页（用于Vue和Flask的学习）

## TODO

- [x] 实现文件上传的前后端
- [x] 实现数据展示与功能选择
- [x] 数据简单可视化
- [ ] 数据可视化的进阶
- [ ] 数据分析...

## Requirements

### 前端

```
node.js
vue
element-plus
antV
```

### 后端

```
python=3.10.13
flask
scikit-learn
matplotlib
```

### 依赖安装

1. 安装python和node.js（看百度）
2. 前端安装：进入client文件夹，执行`npm install`，安装依赖
3. 最后执行`npm install @antv/g2plot element-plus --save` 保存到本地
4. 然后安装python环境，执行`pip install flask scikit-learn matplotlib openpyxl flask-cors pandas`安装依赖

## 启动方法

**请一定按照规范启动！！启动前请确保安装python及其依赖以及node.js**

### 后端

在命令行中输入：
```shell
python ./server/app.py
```
即可启动。此时不用理会URL链接。

### 前端

启动完后端后，再启动前端。

在命令行中依次输入：
```shell
cd client
npm install
npm run dev
```
完成以上的步骤后，不出错的话，命令行中会出现一个链接，点击链接即可进入页面。