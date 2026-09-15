<div align="center">

![首页预览](images/home.png)

# LoveFlipTimer 💖

**一个浪漫主题的恋爱计时 + 照片墙网页** · 纯 HTML / CSS / JavaScript，无需构建、无需后端

[在线演示](https://www.j142.vip/love/) · [功能特性](#-功能特性) · [快速上手](#-快速上手) · [配置指南](#-配置指南)

</div>

---

## ✨ 功能特性

- ⏳ **翻页式恋爱计时器** —— 集成 [Fliptimer](https://github.com/bei9/fliptimer) 库，精确到秒记录在一起的时光
- 🌌 **加载爱心进度屏** —— 打开页面时粉色粒子爱心随加载进度逐渐点亮
- 🖼️ **无限滚动照片墙** —— 随机不重复洗牌展示、悬停暂停并轻微放大、内存自动回收，226+ 张照片长时间挂机也不卡
- ✨ **光斑汇聚灯箱** —— 点击照片，朦胧光斑从屏幕四边汇聚成圆角照片：颜色取自照片本身像素，经过"光斑 → 原图模糊 → 清晰成形"三段过渡，收尾时照片边缘还会散发出同色光斑
- 📷 **拍摄日期角标** —— 大图左下角浮现毛玻璃日期徽章（自动从照片 EXIF 提取）
- 🩷 **漂浮爱心** —— 页面上下始终有粉色小爱心缓缓上浮
- 📱 **响应式布局** —— 按屏宽 5 / 4 / 3 列自适应，拖拽窗口实时重建列数
- 🖱️ **完整灯箱交互** —— 左右方向键 / 箭头切换、Esc 或点击空白关闭，支持触屏

| 加载屏 | 光斑汇聚 | 圆角模糊成形 | 清晰大图 + 日期 |
|:---:|:---:|:---:|:---:|
| ![加载](images/loading.png) | ![汇聚](images/converge.png) | ![模糊成形](images/blur.png) | ![大图](images/lightbox.png) |

## 🚀 快速上手

```bash
git clone https://github.com/jysir99/LoveFlipTimer.git
```

浏览器直接打开 `index.html` 即可，无需安装任何依赖。

## ⚙️ 配置指南

### 1. 配置照片链接（`urls.js`）

编辑 `photoUrls` 数组，填入你自己的照片直链（推荐先传到对象存储 / 图床）：

```javascript
const photoUrls = [
  'https://example.com/photo1.jpg',
  'https://example.com/photo2.jpg'
];
```

### 2. 设置恋爱纪念日（`index.html`）

找到 `startTime`，改成你们的特别时刻：

```javascript
var startTime = new Date("2024-08-30T22:00:00").getTime() / 1000;
```

### 3. 显示拍摄日期（可选，`dates.js`）

`dates.js` 提供每张照片的拍摄日期，格式如下；没有此文件或某张照片缺数据时，日期角标自动隐藏：

```javascript
window.photoDates = {
  "photo1.jpg": "2024-05-01"
};
```

日期可以从照片 EXIF 批量提取，仓库内的 `make_dates.py` 演示了从阿里云 OSS 读取对象头部 EXIF 的做法（`python make_dates.py` 生成 `dates.js`，需要 `pip install oss2 pillow`）。

## 📁 项目结构

```
LoveFlipTimer/
├── index.html      # 主页面（在此设置纪念日时间）
├── urls.js         # 照片链接配置
├── dates.js        # 拍摄日期数据（可选）
├── style.css       # 样式（照片墙 / 灯箱 / 爱心 / 响应式）
└── fliptimer/      # Fliptimer 翻页计时库
```

## 💡 实现说明

- 照片墙采用**列式瀑布流 + 洗牌抽牌**，同屏绝不重复；滚出屏幕的照片转为等高占位块并及时释放内存
- 灯箱光斑效果基于 Canvas：点击后用 200px 小图快速取色（约百毫秒），生成带照片原色的羽化光斑从四边飞入；原图模糊版预渲染为**圆角 + 边缘羽化**，与最终照片卡片轮廓无缝衔接
- 大图显现由定时器 + CSS 过渡驱动，与动画画布解耦，并带兜底保险——任何环境下照片最迟 2.5 秒必显
- 尊重系统"减少动态效果"偏好（`prefers-reduced-motion`）时自动关闭动画

## 🤝 参与贡献

欢迎提交 Issue 和 PR，一起完善此项目 💖

## 📄 许可协议

本项目基于 [MIT](LICENSE) 许可证发布。

---

💌 用一场唯美的计时和影像墙，共同纪念属于你们的爱情故事！
