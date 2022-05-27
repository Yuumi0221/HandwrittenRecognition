//var config = require("../../utils/config.js");
Page({
    /**
     * 页面的初始数据
     */
    data: {
        penColor: 'black',
        lineWidth: 20,
        Imgurl: "",
        applyList0:[
          {Item_id: "0", Item_Name: "CNN"},
          {Item_id: "1", Item_Name: "FCNN"},
          {Item_id: "2", Item_Name: "KNN"},
          {Item_id: "3", Item_Name: "SVM"},
          {Item_id: "4", Item_Name: "RF"}
        ],
        idx0:'0',
        applyList1:[
          {Item_id: "0", Item_Name: "单字符"},
          {Item_id: "1", Item_Name: "多字符"}
        ],
        idx1:'0',
        applyList2:[
          {Item_id: "0", Item_Name: "数字"},
          {Item_id: "1", Item_Name: "字母"}
        ],
        idx2:'0',
        pic: true
    },
    /*
    * 选模型
    */
    selectApply0:function(e){
      let id = e.target.dataset.id
      this.setData({
        idx0: id
      })
      // console.log(this.data.idx0)
    },
    /**
     * 选多字符
     */
    selectApply1:function(e){
      let id = e.target.dataset.id
      this.setData({
        idx1: id
      })
      // console.log(this.data.idx1)
    },
    /**
     * 选数字字母
     */
    selectApply2:function(e){
      let id = e.target.dataset.id
      this.setData({
        idx2: id
      })
      // console.log(this.data.idx2)
    },
    /**
     * 触摸开始
     */
    touchStart: function(e) {
        this.setData({
          pic: false
        });
        //得到触摸点的坐标
        this.startX = e.changedTouches[0].x;
        this.startY = e.changedTouches[0].y;
        this.context = wx.createCanvasContext("myCanvas", this);
        // 设置画笔颜色
        this.context.setStrokeStyle(this.data.penColor);
        // 设置线条宽度
        this.context.setLineWidth(this.data.lineWidth);
        this.context.setLineCap('round'); // 让线条圆润
        this.context.beginPath();
    },
    /**
     * 手指触摸后移动
     */
    touchMove: function(e) {
        var startX1 = e.changedTouches[0].x;
        var startY1 = e.changedTouches[0].y;
        this.context.moveTo(this.startX, this.startY);
        this.context.lineTo(startX1, startY1);
        this.context.stroke();

        this.startX = startX1;
        this.startY = startY1;
        //只是一个记录方法调用的容器，用于生成记录绘制行为的actions数组。context跟<canvas/>不存在对应关系，一个context生成画布的绘制动作数组可以应用于多个<canvas/>
        wx.drawCanvas({
            canvasId: 'myCanvas',
            reserve: true,
            actions: this.context.getActions() // 获取绘图动作数组
        })
    },
    /**
     * 触摸结束
     */
    touchEnd: function(e) {
        this.touchMove(e);
    },
    /**
     * 清除涂鸦信息
     */
    clearCanvas: function(e) {
      const ctx = wx.createCanvasContext('myCanvas');
      ctx.setFillStyle('white');
      ctx.fillRect(0, 0, 1000, 1000);
      ctx.draw();
      this.setData({
        result: null,
        pic: true
      })
    },
    SaveImg: function() {
      wx.canvasToTempFilePath({
        canvasId: 'myCanvas',
        fileType: 'png',
        success: function(res) {
          //将图片下载到本地
          wx.saveImageToPhotosAlbum({
            // 下载图片
            filePath: res.tempFilePath,
            success: function() {
              wx.showToast({
                title: "保存成功",
                icon: "success"
              })
            }
          })
        }
      })
    },
    recImg() {
      var that = this;
      wx.showLoading({
        title: '识别中',
      })
      wx.canvasToTempFilePath({
        canvasId: 'myCanvas',
        fileType: 'png',
        success(res1) {
          // 更改识别类型
          wx.request({  
            // url: 'http://192.168.1.100:5000/v1/typeChange',
            url: 'http://127.0.0.1:5000/v1/typeChange',
            data: {
              model_type: that.data.idx0,
              multi_char: that.data.idx1,
              num_letter: that.data.idx2
            },
            method: 'GET',
            success: function(res2){
              //上传
              wx.uploadFile({
                // url: 'http://192.168.1.100:5000/v1/upload',
                url: 'http://127.0.0.1:5000/v1/upload',
                filePath: res1.tempFilePath,
                name: 'file',
                formData: null,
                success: function(res) {
                  wx.hideLoading();
                  if (JSON.parse(res.data).code == '200') {
                    wx.showModal({
                      title: "识别结果: "+JSON.parse(res.data).result,
                      content: "算法: "+res2.data.model_name+"\r\n用时: "+JSON.parse(res.data).time.slice(0,4)+"秒",
                      confirmText: "返回",
                      showCancel: false,
                      success: function (res) {
                        if (res.confirm) {
                          //点击确定按钮
                        } else if (res.cancel) {
                          //点击取消按钮
                        }
                      }
                    })
                  } else {
                    wx.showToast({
                      title: '识别失败',
                      icon: 'error'
                    })
                  }
                }, 
                fail(res) {
                  wx.hideLoading();
                  wx.showToast({
                    title: '识别失败',
                    icon: 'error'
                  })
                }
              })
            },  
            fail: function(res) {
              wx.showToast({
                title: '识别失败',
                icon: 'error'
              })
            },
          })
        }
      })
    },
    /**
     * 加个白色背景
     */
    onLoad: function(){
      this.setData({
        pic: true
      })
      const ctx = wx.createCanvasContext('myCanvas');
      ctx.setFillStyle('white');
      ctx.fillRect(0, 0, 1000, 1000);
      ctx.draw();
    }
})