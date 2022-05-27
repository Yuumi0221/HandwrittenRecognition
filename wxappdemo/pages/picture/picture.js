var src = '';
Page({
    /**
     * 页面的初始数据
     */
    data: {
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
    * 清空图片
    */
    clearCanvas: function(e) {
      const ctx = wx.createCanvasContext('myCanvas');
      ctx.draw();
      this.setData({
        pic: true
      });
      src = ''
    },
    /**
     * 提示菜单：[从相册中选择，拍照]
    */
    uploadImg: function(e) {
        let a = this;
        wx.showActionSheet({
            itemList: [ "从相册中选择", "拍照" ],
            itemColor: "#6C3D1A",
            success: function(e) {
            //album:相册   //camera拍照
                e.cancel || (0 == e.tapIndex ? a.chooseWxImageShop("album") : 1 == e.tapIndex && a.chooseWxImageShop("camera"));
            }
        });
    },
    /**
     * 选择照片或拍照，返回临时路径
     */
    //a：选择的类型  //album:相册   //camera拍照
    chooseWxImageShop: function(a) {
      var e = this;
      wx.chooseImage({
        sizeType: [ "original", "compressed" ],
        sourceType: [ a ],//类型
        count: 1,
        success: function(a) {
          if(a.tempFiles[0].size> 2097152){
            wx.showModal({
              title: "提示",
              content: "选择的图片过大，请上传不超过2M的图片",
              showCancel: !1,
              success: function(a) {
                  a.confirm;
              }
            })
          }else{
            src = a.tempFilePaths[0]
            wx.getImageInfo({
              src: src,
              success(res){
                const ctx = wx.createCanvasContext('myCanvas', this);
                let path = res.path //本地图片路径
                let width = res.width //图片的宽
                let height = res.height //图片的高
                ctx.width = width;
                ctx.height = height;
                //获取canvas宽高
                // wx.createSelectorQuery().selectAll('.myCanvas').boundingClientRect(function (rect) {
                //   console.log(rect[0].width)
                //   console.log(rect[0].height)
                // }).exec()  
                ctx.drawImage(path, 0, 0, 306, 306);
                // 再将图片填充到画布
                let pattern = ctx.createPattern(path,'no-repeat')
                ctx.fillStyle = pattern;
                ctx.draw();
                e.setData({
                  pic: false
                })
              }
            })
          }
        }
      });
    },
    /**
     * 识别数字
     */
    recPic: function(e) {
      var that = this;
      if (src==''){
        wx.showToast({
          title: '请上传图片',
          icon: 'error'
        })
      } else{
        wx.showLoading({
          title: "识别中"
        });
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
            // 上传
            wx.uploadFile({
              // url: 'http://192.168.1.100:5000/v1/upload',
              url: 'http://127.0.0.1:5000/v1/upload',
              filePath: src,
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
              fail() {
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
          }
        })
      }
    },
    /**
     * 提示文字
     */
    onLoad: function(){
      this.setData({
        pic: true
      })
    }
})