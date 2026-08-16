/* ============================================================
   AI学习队 · 官网交互脚本
   学习提示：全部是原生 JS，没有框架。三个功能分别看下面注释。
   ============================================================ */

(function () {
    'use strict';

    // 标记 JS 已启用：.reveal 元素才进入"先隐藏再渐显"模式
    document.documentElement.classList.remove('no-js');

    /* ---------- 1. 吸顶导航：滚动后加阴影 ---------- */
    const header = document.querySelector('.site-header');
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 10);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ---------- 2. 移动端菜单开关 ---------- */
    const nav = document.querySelector('.nav');
    const navToggle = document.querySelector('.nav-toggle');

    navToggle.addEventListener('click', () => {
        const open = nav.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', String(open));
        navToggle.setAttribute('aria-label', open ? '关闭菜单' : '打开菜单');
    });

    // 点任意导航链接后自动收起移动端菜单
    nav.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            nav.classList.remove('open');
            navToggle.setAttribute('aria-expanded', 'false');
        });
    });

    /* ---------- 3. 滚动渐显：元素进入视口时添加 .visible ---------- */
    const revealEls = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealObserver.unobserve(entry.target); // 只动画一次
                }
            });
        },
        { threshold: 0.12 }
    );
    revealEls.forEach((el) => revealObserver.observe(el));

    /* ---------- 4. 导航高亮：当前可见区块对应的链接加 .active ---------- */
    const sections = document.querySelectorAll('main section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');
    const sectionObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                navLinks.forEach((link) => {
                    link.classList.toggle(
                        'active',
                        link.getAttribute('href') === '#' + entry.target.id
                    );
                });
            });
        },
        { rootMargin: '-45% 0px -50% 0px' } // 视口中间区域判定
    );
    sections.forEach((sec) => sectionObserver.observe(sec));

    /* ---------- 5. 页脚年份自动更新 ---------- */
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = String(new Date().getFullYear());
})();
