var canvasWidth=0, canvasHeight=0;
Page({
    /**
     * 页面的初始数据
     */
    data: {
        url: 'http://127.0.0.1:5000',
        isClear: false,
        tabEraser: false,
        penColor: 'black',
        lineWidth: 20,
        curContexts: [],
        pathCount: 0,
        contextCount: 0,
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
        this.startX = e.changedTouches[0].x
        this.startY = e.changedTouches[0].y
        this.context = wx.createCanvasContext("myCanvas", this)
        var arr = new Array();
        this.data.curContexts[this.data.pathCount] = arr;
        this.setData({
          curContexts: this.data.curContexts,
          contextCount: 0,
        })
        if (this.data.isClear) { //判断是否启用的橡皮擦功能  ture表示清除  false表示画画
          this.context.setStrokeStyle('white') //设置线条样式 此处设置为画布的背景颜色  橡皮擦原理就是：利用擦过的地方被填充为画布的背景颜色一致 从而达到橡皮擦的效果
          this.context.setLineCap('round') //设置线条端点的样式
          this.context.setLineJoin('round') //设置两线相交处的样式
          this.context.setLineWidth(20) //设置线条宽度
          this.context.save();  //保存当前坐标轴的缩放、旋转、平移信息
          this.context.beginPath() //开始一个路径
          this.context.arc(this.startX, this.startY, 5, 0, 2 * Math.PI, true);  //添加一个弧形路径到当前路径，顺时针绘制  这里总共画了360度  也就是一个圆形
          this.context.fill();  //对当前路径进行填充
          this.context.restore();  //恢复之前保存过的坐标轴的缩放、旋转、平移信息
        } else {
          // 设置画笔颜色
          this.context.setStrokeStyle(this.data.penColor);
          // 设置线条宽度
          this.context.setLineWidth(this.data.lineWidth);
          this.context.setLineCap('round') // 让线条圆润
          this.context.beginPath()
        }
    },
    /**
     * 手指触摸后移动
     */
    touchMove: function(e) {
      var startX1 = e.changedTouches[0].x
      var startY1 = e.changedTouches[0].y
  
      if (this.data.isClear) { //判断是否启用的橡皮擦功能  ture表示清除  false表示画画
        this.context.save();  //保存当前坐标轴的缩放、旋转、平移信息
        this.context.moveTo(this.startX, this.startY);  //把路径移动到画布中的指定点，但不创建线条
        this.context.lineTo(startX1, startY1);  //添加一个新点，然后在画布中创建从该点到最后指定点的线条
        this.context.stroke();  //对当前路径进行描边
        this.context.restore();  //恢复之前保存过的坐标轴的缩放、旋转、平移信息
  
        this.startX = startX1;
        this.startY = startY1;
  
      } else {
        this.context.moveTo(this.startX, this.startY)
        this.context.lineTo(startX1, startY1)
        this.context.stroke()
  
        this.startX = startX1;
        this.startY = startY1;
      }
  
      //只是一个记录方法调用的容器，用于生成记录绘制行为的actions数组。
      var actions = this.context.getActions();
      this.data.curContexts[this.data.pathCount][this.data.contextCount] = actions;
      this.setData ({
        curContexts: this.data.curContexts
      })
      wx.drawCanvas({
        canvasId: 'myCanvas',
        reserve: true,
        actions: actions // 获取绘图动作数组
      });
      this.data.contextCount++;
    },
    /**
     * 触摸结束
     */
    touchEnd: function(e) {
      if (this.data.tabEraser) {
        console.log("别点啦3")
      } else{
        this.touchMove(e);
        this.setData({
          pathCount: (this.data.pathCount + 1),
          contextCount: 0
        });
      }
      this.setData({
        tabEraser: false
      });
    },
    /**
     * 撤销
     */
    drawRevoke: function (e) {
      if (this.data.pathCount <= 0) {
        console.log("没得撤销啦")
      } else{
        const ctx = wx.createCanvasContext('myCanvas');
        ctx.setFillStyle('white');
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);
        ctx.draw();
        // this.context.clearRect(0,0,canvasWidth, canvasHeight);
        // this.context.draw();
        if (this.data.pathCount > 0) {
          for (var i = 0; i < this.data.pathCount - 1; i++) {
            for (var j = 0; j < this.data.curContexts[i].length; j++) {
              wx.drawCanvas({
                canvasId: 'myCanvas',
                reserve: true,
                actions: this.data.curContexts[i][j] // 获取绘图动作数组
              });
            }
          }
    
          var pathCount = this.data.pathCount - 1;
          this.data.curContexts[pathCount] = null;
          this.setData({
            pathCount: pathCount,
            contextCount: 0,
          });
          // console.log(pathCount)
          if (pathCount <= 0) {
            this.clearCanvas(e)
          }
        }
      }
    },
    /**
     * 清除涂鸦信息
     */
    clearCanvas: function(e) {
      const ctx = wx.createCanvasContext('myCanvas');
      ctx.setFillStyle('white');
      ctx.fillRect(0, 0, canvasWidth, canvasHeight);
      ctx.draw();
      // this.context.clearRect(0,0,canvasWidth, canvasHeight);
      // this.context.draw();
      this.setData({
        result: null,
        pic: true,
        curContexts: [],
        pathCount: 0,
        contextCount: 0
      })
    },
    /**
     * 橡皮擦
     */
    eraser: function () {
      console.log("eraser");
      this.setData({
        isClear: true,
        tabEraser: true
      });
    },
    /**
     * 笔
     */
    pen: function () {
      console.log("pen");
      this.setData({
        isClear: false,
        tabEraser: true
      });
    },
    /**
     * 保存图片
     */
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
    /**
     * 识别图片
     */
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
            url: that.data.url + '/typeChange',
            data: {
              model_type: that.data.idx0,
              multi_char: that.data.idx1,
              num_letter: that.data.idx2
            },
            method: 'GET',
            success: function(res2){
              //上传
              wx.uploadFile({
                url: that.data.url + '/upload',
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
    onLoad(){
      this.setData({
        pic: true,
        curContexts: [],
        pathCount: 0,
        contextCount: 0
      })
      wx.createSelectorQuery().select('#myCanvas')
      .fields({ node: true, size: true })
      .exec((res) => {
        canvasWidth = res[0].width
        canvasHeight = res[0].height
      })
      const ctx = wx.createCanvasContext('myCanvas');
      ctx.setFillStyle('white');
      ctx.fillRect(0, 0, 1000, 1000);
      ctx.draw();
    }
})