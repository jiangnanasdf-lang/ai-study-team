# AI学习队官网

一个纯 HTML + CSS + 原生 JavaScript 的静态官网，参考 `jyyzmmc.github.io` 的技术思路搭建：

- **零框架、零构建**：不需要 npm、不需要编译，浏览器直接打开就能看
- **GitHub Pages 托管**：推送到 GitHub 后自动上线
- **响应式**：手机 / 平板 / 桌面自适应

## 一、目录结构

```
coordinate system/
├── index.html          # 页面结构（唯一的页面，所有内容都在这）
├── css/style.css       # 全部样式（配色、布局、动画、响应式）
├── js/main.js          # 全部交互（菜单、滚动渐显、导航高亮）
├── assets/
│   ├── logo.svg        # 站点 logo（SVG 矢量图，纯文本可编辑）
│   └── game/           # 游戏安装包等下载文件（占位）
├── .github/workflows/
│   └── pages.yml       # GitHub Pages 自动部署配置
└── robots.txt          # 搜索引擎爬虫规则
```

## 二、本地预览（任选一种）

1. **最简单**：双击 `index.html`，浏览器直接打开
2. **VS Code**：装 Live Server 插件 → 右键 `index.html` → Open with Live Server（推荐，改代码自动刷新）
3. **命令行**：
   ```bash
   python -m http.server 8000
   # 然后浏览器访问 http://localhost:8000
   ```

## 三、逐步学习路线

### 第 1 步：看懂 index.html

页面是"一页式"结构，从上到下：

```html
<header>  导航栏（固定在顶部）
<main>
  <section id="hero">    首屏大标题
  <section id="about">   关于我们
  <section id="team">    团队成员
  <section id="awards">  荣誉奖项
  <section id="events">  活动
  <section id="join">    加入我们
</main>
<footer>  页脚
```

导航栏里的链接 `href="#about"` 就是锚点：点击后浏览器平滑滚动到对应 `<section>`。新增一个栏目 = 加一个 `<section>` + 在导航里加一个 `<a>`。

### 第 2 步：看懂 css/style.css

整个文件最上面有一段 `:root { ... }`，这是**全局变量**：

```css
:root {
    --accent: #00b4d8;   /* 主题高亮色 */
    --bg-surface: #111622; /* 卡片背景 */
    --text-primary: #e6ecf3; /* 主文字颜色 */
}
```

后面所有颜色都写成 `var(--accent)` 的形式。**想换主题色，只改这一个文件里的变量即可**，全站一起变。

布局用的是 **CSS Grid**（卡片网格）和 **Flexbox**（导航、按钮排布），文件底部是媒体查询（`@media`），窄屏时自动改成单列布局并启用汉堡菜单。

### 第 3 步：看懂 js/main.js

一共 5 个小功能，每个都有注释：

1. 滚动时给导航加阴影
2. 移动端汉堡菜单开合
3. **滚动渐显**：`IntersectionObserver` 监听元素进入视口 → 添加 `.visible` 类 → CSS 过渡显示
4. **导航高亮**：同样用 `IntersectionObserver`，当前看到的区块对应链接变亮
5. 页脚年份自动更新

想给页面加"元素进入视口才出现"的效果，只需给那个元素加 `class="reveal"`。

### 第 4 步：替换成你的内容

- **改站名/标题**：`index.html` 里的 `<title>`、`nav-brand`、`hero-title`
- **改团队**：复制一个 `.flip-card` 整块，改名字、角色、头像首字（`<div class="avatar">` 里的字）和 `style="--hue:200"`（颜色色相，0-360 任意值）
- **改荣誉**：复制 `.award-card` 整块，年份改 `<span class="award-year">`
- **改联系方式**：`#join` 区块里的邮箱、QQ 群号（现在都是占位）
- **换 logo**：替换 `assets/logo.svg` 文件内容即可

## 四、部署到 GitHub Pages

1. 在 GitHub 上新建一个仓库（**名字不要带空格**，例如 `ai-study-team`）
2. 在项目目录执行：
   ```bash
   git remote add origin https://github.com/<你的用户名>/ai-study-team.git
   git push -u origin main
   ```
3. **开启 GitHub Pages**：仓库 Settings → 左侧 **Pages** → Source 选 **GitHub Actions** → Save
4. 等 1~2 分钟，仓库 **Actions** 页里 `Deploy to GitHub Pages` 变绿
5. 访问 `https://<你的用户名>.github.io/ai-study-team/`

> 以后每次 `git push` 都会自动重新部署。若首次部署失败：① 确认 Pages Source 已选 GitHub Actions；② 确认 Settings → Actions → General 里允许工作流运行。

> 如果仓库名是 `<你的用户名>.github.io`，则站点在根路径：`https://<你的用户名>.github.io/`

## 五、进阶：仿照 jyyzmmc.github.io 加跳转壳页

原站的做法：`jyyzmmc.github.io` 只放一个跳转 `index.html`，用 `Math.random()` 随机跳转到内容站。如果你想给站点加一个"门面"地址，可以新建一个仓库，放这样的页面：

```html
<script>
  // 90% 概率跳主站，10% 概率跳备用页
  window.location.replace(
    Math.random() < 0.9
      ? 'https://<你的用户名>.github.io/ai-study-team/'
      : 'https://<你的用户名>.github.io/ai-study-team/fallback.html'
  );
</script>
```

## 六、链接的三种写法（下载 / 跳转 / 问卷）

### 1. 下载站内文件（游戏安装包、PDF 等）

把文件放进仓库（如 `assets/game/prison_eng.exe`），链接直接指向它：

```html
<a href="assets/game/prison_eng.exe" download>Windows 便携版下载</a>
```

- `download` 属性强制浏览器"下载"而不是打开文件
- GitHub 对单文件有大小限制（约 100MB），更大的文件建议放网盘/对象存储，`href` 直接换成外链

### 2. 站内跳转（锚点 / 子页面）

```html
<a href="#game-download">进入下载游戏</a>   <!-- 跳到本页某个区块 -->
<a href="game.html">进入下载游戏</a>        <!-- 跳到另一个页面 -->
```

### 3. 跳转外链（腾讯问卷 / QQ群 / 任意网址）

```html
<a href="https://wj.qq.com/s2/23398546/ad18" target="_blank" rel="noopener">报名意向表</a>
```

- `target="_blank"`：在新标签页打开，不离开你的站点
- `rel="noopener"`：安全规范，防止新页面反向控制原页面

## 七、游戏下载区块怎么改成你的游戏

`#game` 区块在 `index.html` 里（搜索 `GAME` 注释），分两部分：

1. **宣传卡片**：改游戏名（`<h3>`）和口号（`<p class="game-tagline">`）
2. **下载面板**：
   - 把安装包放进 `assets/game/`，把下载按钮的 `href` 改成你的文件名
   - 版本、SHA256、文件名单那几行改成真实信息。Windows 算 SHA256：
     ```bash
     certutil -hashfile 你的文件.exe SHA256
     ```
   - macOS / Linux 还没做就保留 `is-disabled` 置灰按钮

## 八、常见问题

- **字体加载慢**：站点用了 Google Fonts CDN，国内访问可能慢。删掉 `index.html` 里 `<head>` 的 Google Fonts 三行即可回退到系统字体
- **想加图片**：图片放进 `assets/images/`，HTML 里写 `<img src="assets/images/xxx.jpg">`
- **想加子页面**：新建 `xxx.html`，导航里改成 `href="xxx.html"` 即可
