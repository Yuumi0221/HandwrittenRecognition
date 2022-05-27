Component({
  options: {
    addGlobalClass: true,
  },
  data: {
    elements: [{
        title: '手写识别',
        name: 'handwrite',
        color: 'blue',
        icon: 'writefill'
      },
      {
        title: '图片识别',
        name: 'picture',
        color: 'cyan',
        icon: 'upload'
      },
      {
        title: '历史记录',
        name: 'history',
        color: 'green',
        icon: '<view class="iconfont icon-lishi"></view>'
      }
    ],
  }
})