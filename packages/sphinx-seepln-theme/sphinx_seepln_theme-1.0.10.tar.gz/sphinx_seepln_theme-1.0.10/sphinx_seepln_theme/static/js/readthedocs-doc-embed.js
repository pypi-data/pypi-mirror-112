!
    function o(a, s, l) {
        function d(t, e) {
            if (!s[t]) {
                if (!a[t]) {
                    var i = "function" == typeof require && require;
                    if (!e && i) return i(t, !0);
                    if (c) return c(t, !0);
                    var r = new Error("Cannot find module '" + t + "'");
                    throw r.code = "MODULE_NOT_FOUND",
                    r
                }
                var n = s[t] = {
                    exports: {}
                };
                a[t][0].call(n.exports,
                    function (e) {
                        return d(a[t][1][e] || e)
                    },
                    n, n.exports, o, a, s, l)
            }
            return s[t].exports
        }
        for (var c = "function" == typeof require && require,
            e = 0; e < l.length; e++) d(l[e]);
        return d
    }({
        1: [function (e, t, i) {
            var r = "undefined" != typeof window ? window.jQuery : e("jquery");
            t.exports.ThemeNav = {
                navBar: null,
                win: null,
                winScroll: !1,
                winResize: !1,
                linkScroll: !1,
                winPosition: 0,
                winHeight: null,
                docHeight: null,
                isRunning: !1,
                enable: function (t) {
                    var i = this;
                    "undefined" == typeof withStickNav && (t = !0),
                        i.isRunning || (i.isRunning = !0, r(function (e) {
                            i.init(e),
                                i.reset(),
                                i.win.on("hashchange", i.reset),
                                t && i.win.on("scroll",
                                    function () {
                                        i.linkScroll || i.winScroll || (i.winScroll = !0, requestAnimationFrame(function () {
                                            i.onScroll()
                                        }))
                                    }),
                                i.win.on("resize",
                                    function () {
                                        i.winResize || (i.winResize = !0, requestAnimationFrame(function () {
                                            i.onResize()
                                        }))
                                    }),
                                i.onResize()
                        }))
                },
                enableSticky: function () {
                    this.enable(!0)
                },
                init: function (i) {
                    i(document);
                    var r = this;

                    this.navBar = i("div.wy-side-scroll:first"),
                        this.win = i(window),
                        i(document).on("click", "[data-toggle='wy-nav-top']",
                            function () {
                                i("[data-toggle='wy-nav-shift']").toggleClass("shift"),
                                    i("[data-toggle='rst-versions']").toggleClass("shift")
                            }).on("click", ".enos-doc-toc .current ul li a",
                                function () {
                                    var e = i(this);
                                    i("[data-toggle='wy-nav-shift']").removeClass("shift"),
                                        i("[data-toggle='rst-versions']").toggleClass("shift"),
                                        r.toggleCurrent(e),
                                        r.hashChange()
                                }).on("click", "[data-toggle='rst-current-version']",
                                    function () {
                                        i("[data-toggle='rst-versions']").toggleClass("shift-up")
                                    }),
                        i("table.docutils:not(.field-list,.footnote,.citation)").wrap("<div class='wy-table-responsive'></div>"),
                        i("table.docutils.footnote").wrap("<div class='wy-table-responsive footnote'></div>"),
                        i("table.docutils.citation").wrap("<div class='wy-table-responsive citation'></div>"),
                        // i(".wy-menu-vertical ul").not(".simple").siblings("a").each(function () {
                        //     var t = i(this);
                        //     expand = i('<span class="toctree-expand"></span>'),
                        //         expand.on("click",
                        //             function (e) {
                        //                 return r.toggleCurrent(t),
                        //                     e.stopPropagation(),
                        //                     !1
                        //             }),
                        //         t.prepend(expand)
                        // }),
                        i(".enos-doc-toc ul").not(".current").siblings("a").each(function () {

                            // .toctree - l1 a[href ^= "#"]
                            console.log($(".enos-doc-toc ul").not(".current").siblings("a").siblings('ul').find("a[href ^= '#']").length)
                            var t = i(this);
                            var expand
                            const num = $(".enos-doc-toc ul").not(".current").siblings("a").siblings('ul').find("a[href ^= '#']").length
                            num === 0 ? expand = i('<span class="toctree-expand"></span>') : ''
                            // expand.on("click",
                            //     function (e) {
                            //         console.log(t.siblings('ul').length)
                            //         // t.siblings('ul').toggle()
                            //         var ty = $(`.enos-doc-toc .reference.internal[href='#']  + ul`);
                            //         if ($(`.enos-doc-toc .reference.internal`).attr("href") === "#") {
                            //             // if(ty.length > 0 ){
                            //             console.log("#")
                            //             if (!ty.hasClass("no_side")) {
                            //                 ty.addClass("no_side")
                            //                 ty.removeClass("yes_side")
                            //                 $('.toctree-expand').addClass("toctree-expand-hid")
                            //                 // a.removeClass('current')
                            //             } else {
                            //                 console.log('123333')
                            //                 ty.addClass("yes_side")
                            //                 ty.removeClass("no_side")
                            //                 $('.toctree-expand').removeClass("toctree-expand-hid")
                            //                 // a.addClass('current')
                            //             }
                            //             // }
                            //         } else if ($(`.enos-doc-toc .reference.internal`).attr("href") === "index.html") {
                            //             console.log("#")

                            //             if (!ty.hasClass("no_side")) {
                            //                 ty.addClass("no_side")
                            //                 ty.removeClass("yes_side")
                            //                 $('.toctree-expand').addClass("toctree-expand-hid")
                            //                 // a.removeClass('current')
                            //             } else {
                            //                 ty.addClass("yes_side")
                            //                 ty.removeClass("no_side")
                            //                 $('.toctree-expand').removeClass("toctree-expand-hid")
                            //                 // a.addClass('current')
                            //             }
                            //         } else if ($(`.enos-doc-toc .reference.internal`).attr("href") === "../index.html") {
                            //             if (!ty.hasClass("no_side")) {
                            //                 ty.addClass("no_side")
                            //                 ty.removeClass("yes_side")
                            //                 $('.toctree-expand').addClass("toctree-expand-hid")
                            //                 // a.removeClass('current')
                            //             } else {
                            //                 ty.addClass("yes_side")
                            //                 ty.removeClass("no_side")
                            //                 $('.toctree-expand').removeClass("toctree-expand-hid")
                            //                 // a.addClass('current')
                            //             }
                            //         }
                            //         // console.log(t.siblings('ul').is(':hidden'))
                            //         // if ($(this).siblings('ul').is(':hidden')) {
                            //         //     console.log('321')
                            //         //     console.log($(this).siblings('ul'))
                            //         //     t.siblings('ul').removeClass("no_side")
                            //         //     t.siblings('ul').addClass("yes_side")
                            //         //     $('.toctree-expand').addClass("toctree-expand-hid")
                            //         //     //处理业务
                            //         // } else {
                            //         //     console.log('123')
                            //         //     t.siblings('ul').removeClass("yes_side")
                            //         //     t.siblings('ul').addClass("no_side")
                            //         //     $('.toctree-expand').removeClass("toctree-expand-hid")
                            //         //     //处理业务
                            //         // }
                            //         return r.toggleCurrent(t),
                            //             e.stopPropagation(),
                            //             !1
                            //     }),
                            t.prepend(expand)
                        })
                },
                reset: function () {
                    var e = encodeURI(window.location.hash) || "#";
                    try {
                        var t = $(".enos-doc-toc"),
                            i = t.find('[href="' + e + '"]');
                        if (0 === i.length) {
                            var r = $('.document [id="' + e.substring(1) + '"]').closest("div.section");
                            0 === (i = t.find('[href="#' + r.attr("id") + '"]')).length && (i = t.find('[href="#"]'))
                        }
                        0 < i.length && ($(".enos-doc-toc .current").removeClass("current"), i.addClass("current"), i.closest("li.toctree-l1").addClass("current"), i.closest("li.toctree-l1").parent().addClass("current"), i.closest("li.toctree-l1").addClass("current"), i.closest("li.toctree-l2").addClass("current"), i.closest("li.toctree-l3").addClass("current"), i.closest("li.toctree-l4").addClass("current"))
                    } catch (e) {
                        console.log("Error expanding nav for anchor", e)
                    }
                },
                onScroll: function () {
                    this.winScroll = !1;
                    var e = this.win.scrollTop(),
                        t = e + this.winHeight,
                        i = this.navBar.scrollTop() + (e - this.winPosition);
                    e < 0 || t > this.docHeight || (this.navBar.scrollTop(i), this.winPosition = e)
                },
                onResize: function () {
                    this.winResize = !1,
                        this.winHeight = this.win.height(),
                        this.docHeight = $(document).height()
                },
                hashChange: function () {
                    this.linkScroll = !0,
                        this.win.one("hashchange",
                            function () {
                                this.linkScroll = !1
                            })
                },
                toggleCurrent: function (e) {
                    var t = e.closest("li");
                    t.siblings("li.current").removeClass("current"),
                        t.siblings().find("li.current").removeClass("current"),
                        t.find("> ul li.current").removeClass("current"),
                        t.toggleClass("current")
                }
            },
                "undefined" != typeof window && (window.SphinxRtdTheme = {
                    Navigation: t.exports.ThemeNav,
                    StickyNav: t.exports.ThemeNav
                }),
                function () {
                    for (var o = 0,
                        e = ["ms", "moz", "webkit", "o"], t = 0; t < e.length && !window.requestAnimationFrame; ++t) window.requestAnimationFrame = window[e[t] + "RequestAnimationFrame"],
                            window.cancelAnimationFrame = window[e[t] + "CancelAnimationFrame"] || window[e[t] + "CancelRequestAnimationFrame"];
                    window.requestAnimationFrame || (window.requestAnimationFrame = function (e, t) {
                        var i = (new Date).getTime(),
                            r = Math.max(0, 16 - (i - o)),
                            n = window.setTimeout(function () {
                                e(i + r)
                            },
                                r);
                        return o = i + r,
                            n
                    }),
                        window.cancelAnimationFrame || (window.cancelAnimationFrame = function (e) {
                            clearTimeout(e)
                        })
                }()
        },
        {
            jquery: "jquery"
        }],
        2: [function (e, t, i) {
            var r = e("cssfilter").FilterCSS,
                n = e("cssfilter").getDefaultWhiteList,
                u = e("./util");
            function o() {
                return {
                    a: ["target", "href", "title"],
                    abbr: ["title"],
                    address: [],
                    area: ["shape", "coords", "href", "alt"],
                    article: [],
                    aside: [],
                    audio: ["autoplay", "controls", "loop", "preload", "src"],
                    b: [],
                    bdi: ["dir"],
                    bdo: ["dir"],
                    big: [],
                    blockquote: ["cite"],
                    br: [],
                    caption: [],
                    center: [],
                    cite: [],
                    code: [],
                    col: ["align", "valign", "span", "width"],
                    colgroup: ["align", "valign", "span", "width"],
                    dd: [],
                    del: ["datetime"],
                    details: ["open"],
                    div: [],
                    dl: [],
                    dt: [],
                    em: [],
                    font: ["color", "size", "face"],
                    footer: [],
                    h1: [],
                    h2: [],
                    h3: [],
                    h4: [],
                    h5: [],
                    h6: [],
                    header: [],
                    hr: [],
                    i: [],
                    img: ["src", "alt", "title", "width", "height"],
                    ins: ["datetime"],
                    li: [],
                    mark: [],
                    nav: [],
                    ol: [],
                    p: [],
                    pre: [],
                    s: [],
                    section: [],
                    small: [],
                    span: [],
                    sub: [],
                    sup: [],
                    strong: [],
                    table: ["width", "border", "align", "valign"],
                    tbody: ["align", "valign"],
                    td: ["width", "rowspan", "colspan", "align", "valign"],
                    tfoot: ["align", "valign"],
                    th: ["width", "rowspan", "colspan", "align", "valign"],
                    thead: ["align", "valign"],
                    tr: ["rowspan", "align", "valign"],
                    tt: [],
                    u: [],
                    ul: [],
                    video: ["autoplay", "controls", "loop", "preload", "src", "height", "width"]
                }
            }
            var a = new r;
            function s(e) {
                return e.replace(l, "&lt;").replace(d, "&gt;")
            }
            var l = /</g,
                d = />/g,
                c = /"/g,
                p = /&quot;/g,
                f = /&#([a-zA-Z0-9]*);?/gim,
                h = /&colon;?/gim,
                g = /&newline;?/gim,
                m = /((j\s*a\s*v\s*a|v\s*b|l\s*i\s*v\s*e)\s*s\s*c\s*r\s*i\s*p\s*t\s*|m\s*o\s*c\s*h\s*a)\:/gi,
                v = /e\s*x\s*p\s*r\s*e\s*s\s*s\s*i\s*o\s*n\s*\(.*/gi,
                w = /u\s*r\s*l\s*\(.*/gi;
            function b(e) {
                return e.replace(c, "&quot;")
            }
            function y(e) {
                return e.replace(p, '"')
            }
            function _(e) {
                return e.replace(f,
                    function (e, t) {
                        return "x" === t[0] || "X" === t[0] ? String.fromCharCode(parseInt(t.substr(1), 16)) : String.fromCharCode(parseInt(t, 10))
                    })
            }
            function x(e) {
                return e.replace(h, ":").replace(g, " ")
            }
            function k(e) {
                for (var t = "",
                    i = 0,
                    r = e.length; i < r; i++) t += e.charCodeAt(i) < 32 ? " " : e.charAt(i);
                return u.trim(t)
            }
            function T(e) {
                return e = k(e = x(e = _(e = y(e))))
            }
            function E(e) {
                return e = s(e = b(e))
            }
            var S = /<!--[\s\S]*?-->/g;
            i.whiteList = {
                a: ["target", "href", "title"],
                abbr: ["title"],
                address: [],
                area: ["shape", "coords", "href", "alt"],
                article: [],
                aside: [],
                audio: ["autoplay", "controls", "loop", "preload", "src"],
                b: [],
                bdi: ["dir"],
                bdo: ["dir"],
                big: [],
                blockquote: ["cite"],
                br: [],
                caption: [],
                center: [],
                cite: [],
                code: [],
                col: ["align", "valign", "span", "width"],
                colgroup: ["align", "valign", "span", "width"],
                dd: [],
                del: ["datetime"],
                details: ["open"],
                div: [],
                dl: [],
                dt: [],
                em: [],
                font: ["color", "size", "face"],
                footer: [],
                h1: [],
                h2: [],
                h3: [],
                h4: [],
                h5: [],
                h6: [],
                header: [],
                hr: [],
                i: [],
                img: ["src", "alt", "title", "width", "height"],
                ins: ["datetime"],
                li: [],
                mark: [],
                nav: [],
                ol: [],
                p: [],
                pre: [],
                s: [],
                section: [],
                small: [],
                span: [],
                sub: [],
                sup: [],
                strong: [],
                table: ["width", "border", "align", "valign"],
                tbody: ["align", "valign"],
                td: ["width", "rowspan", "colspan", "align", "valign"],
                tfoot: ["align", "valign"],
                th: ["width", "rowspan", "colspan", "align", "valign"],
                thead: ["align", "valign"],
                tr: ["rowspan", "align", "valign"],
                tt: [],
                u: [],
                ul: [],
                video: ["autoplay", "controls", "loop", "preload", "src", "height", "width"]
            },
                i.getDefaultWhiteList = o,
                i.onTag = function (e, t, i) { },
                i.onIgnoreTag = function (e, t, i) { },
                i.onTagAttr = function (e, t, i) { },
                i.onIgnoreTagAttr = function (e, t, i) { },
                i.safeAttrValue = function (e, t, i, r) {
                    if (i = T(i), "href" === t || "src" === t) {
                        if ("#" === (i = u.trim(i))) return "#";
                        if ("http://" !== i.substr(0, 7) && "https://" !== i.substr(0, 8) && "mailto:" !== i.substr(0, 7) && "tel:" !== i.substr(0, 4) && "#" !== i[0] && "/" !== i[0]) return ""
                    } else if ("background" === t) {
                        if (m.lastIndex = 0, m.test(i)) return ""
                    } else if ("style" === t) {
                        if (v.lastIndex = 0, v.test(i)) return "";
                        if (w.lastIndex = 0, w.test(i) && (m.lastIndex = 0, m.test(i))) return ""; !1 !== r && (i = (r = r || a).process(i))
                    }
                    return i = E(i)
                },
                i.escapeHtml = s,
                i.escapeQuote = b,
                i.unescapeQuote = y,
                i.escapeHtmlEntities = _,
                i.escapeDangerHtml5Entities = x,
                i.clearNonPrintableCharacter = k,
                i.friendlyAttrValue = T,
                i.escapeAttrValue = E,
                i.onIgnoreTagStripAll = function () {
                    return ""
                },
                i.StripTagBody = function (a, s) {
                    "function" != typeof s && (s = function () { });
                    var l = !Array.isArray(a),
                        d = [],
                        c = !1;
                    return {
                        onIgnoreTag: function (e, t, i) {
                            if (o = e, l || -1 !== u.indexOf(a, o)) {
                                if (i.isClosing) {
                                    var r = "[/removed]",
                                        n = i.position + r.length;
                                    return d.push([!1 !== c ? c : i.position, n]),
                                        c = !1,
                                        r
                                }
                                return c || (c = i.position),
                                    "[removed]"
                            }
                            return s(e, t, i);
                            var o
                        }, remove: function (t) {
                            var i = "",
                                r = 0;
                            return u.forEach(d,
                                function (e) {
                                    i += t.slice(r, e[0]),
                                        r = e[1]
                                }),
                                i += t.slice(r)
                        }
                    }
                },
                i.stripCommentTag = function (e) {
                    return e.replace(S, "")
                },
                i.stripBlankChar = function (e) {
                    var t = e.split("");
                    return (t = t.filter(function (e) {
                        var t = e.charCodeAt(0);
                        return !(127 === t || t <= 31 && 10 !== t && 13 !== t)
                    })).join("")
                },
                i.cssFilter = a,
                i.getDefaultCSSWhiteList = n
        },
        {
            "./util": 5,
            cssfilter: 10
        }],
        3: [function (e, t, i) {
            var r = e("./default"),
                n = e("./parser"),
                o = e("./xss");
            for (var a in (i = t.exports = function (e, t) {
                return new o(t).process(e)
            }).FilterXSS = o, r) i[a] = r[a];
            for (var a in n) i[a] = n[a];
            "undefined" != typeof window && (window.filterXSS = t.exports)
        },
        {
            "./default": 2,
            "./parser": 4,
            "./xss": 6
        }],
        4: [function (e, t, i) {
            var c = e("./util");
            function p(e) {
                var t = c.spaceIndex(e);
                if (- 1 === t) var i = e.slice(1, -1);
                else i = e.slice(1, t + 1);
                return "/" === (i = c.trim(i).toLowerCase()).slice(0, 1) && (i = i.slice(1)),
                    "/" === i.slice(- 1) && (i = i.slice(0, -1)),
                    i
            }
            var u = /[^a-zA-Z0-9_:\.\-]/gim;
            function f(e, t) {
                for (; t < e.length; t++) {
                    var i = e[t];
                    if (" " !== i) return "=" === i ? t : -1
                }
            }
            function h(e, t) {
                for (; 0 < t; t--) {
                    var i = e[t];
                    if (" " !== i) return "=" === i ? t : -1
                }
            }
            function g(e) {
                return '"' === (t = e)[0] && '"' === t[t.length - 1] || "'" === t[0] && "'" === t[t.length - 1] ? e.substr(1, e.length - 2) : e;
                var t
            }
            i.parseTag = function (e, t, i) {
                "user strict";
                var r = "",
                    n = 0,
                    o = !1,
                    a = !1,
                    s = 0,
                    l = e.length,
                    d = "",
                    c = "";
                for (s = 0; s < l; s++) {
                    var u = e.charAt(s);
                    if (!1 === o) {
                        if ("<" === u) {
                            o = s;
                            continue
                        }
                    } else if (!1 === a) {
                        if ("<" === u) {
                            r += i(e.slice(n, s)),
                                n = o = s;
                            continue
                        }
                        if (">" === u) {
                            r += i(e.slice(n, o)),
                                c = p(d = e.slice(o, s + 1)),
                                r += t(o, r.length, c, d, "</" === d.slice(0, 2)),
                                n = s + 1,
                                o = !1;
                            continue
                        }
                        if (('"' === u || "'" === u) && "=" === e.charAt(s - 1)) {
                            a = u;
                            continue
                        }
                    } else if (u === a) {
                        a = !1;
                        continue
                    }
                }
                return n < e.length && (r += i(e.substr(n))),
                    r
            },
                i.parseAttr = function (e, r) {
                    "user strict";
                    var t = 0,
                        n = [],
                        i = !1,
                        o = e.length;
                    function a(e, t) {
                        if (!((e = (e = c.trim(e)).replace(u, "").toLowerCase()).length < 1)) {
                            var i = r(e, t || "");
                            i && n.push(i)
                        }
                    }
                    for (var s = 0; s < o; s++) {
                        var l, d = e.charAt(s);
                        if (!1 !== i || "=" !== d) if (!1 === i || s !== t || '"' !== d && "'" !== d || "=" !== e.charAt(s - 1)) {
                            if (/\s|\n|\t/.test(d)) {
                                if (e = e.replace(/\s|\n|\t/g, " "), !1 === i) {
                                    if (- 1 === (l = f(e, s))) {
                                        a(c.trim(e.slice(t, s))),
                                            i = !1,
                                            t = s + 1;
                                        continue
                                    }
                                    s = l - 1;
                                    continue
                                }
                                if (- 1 === (l = h(e, s - 1))) {
                                    a(i, g(c.trim(e.slice(t, s)))),
                                        i = !1,
                                        t = s + 1;
                                    continue
                                }
                            }
                        } else {
                            if (- 1 === (l = e.indexOf(d, s + 1))) break;
                            a(i, c.trim(e.slice(t + 1, l))),
                                i = !1,
                                t = (s = l) + 1
                        } else i = e.slice(t, s),
                            t = s + 1
                    }
                    return t < e.length && (!1 === i ? a(e.slice(t)) : a(i, g(c.trim(e.slice(t))))),
                        c.trim(n.join(" "))
                }
        },
        {
            "./util": 5
        }],
        5: [function (e, t, i) {
            t.exports = {
                indexOf: function (e, t) {
                    var i, r;
                    if (Array.prototype.indexOf) return e.indexOf(t);
                    for (i = 0, r = e.length; i < r; i++) if (e[i] === t) return i;
                    return - 1
                },
                forEach: function (e, t, i) {
                    var r, n;
                    if (Array.prototype.forEach) return e.forEach(t, i);
                    for (r = 0, n = e.length; r < n; r++) t.call(i, e[r], r, e)
                },
                trim: function (e) {
                    return String.prototype.trim ? e.trim() : e.replace(/(^\s*)|(\s*$)/g, "")
                },
                spaceIndex: function (e) {
                    var t = /\s|\n|\t/.exec(e);
                    return t ? t.index : -1
                }
            }
        },
        {}],
        6: [function (e, t, i) {
            var r = e("cssfilter").FilterCSS,
                n = e("./default"),
                o = e("./parser"),
                a = o.parseTag,
                w = o.parseAttr,
                b = e("./util");
            function y(e) {
                return null == e
            }
            function s(e) {
                (e = function (e) {
                    var t = {};
                    for (var i in e) t[i] = e[i];
                    return t
                }(e || {})).stripIgnoreTag && (e.onIgnoreTag && console.error('Notes: cannot use these two options "stripIgnoreTag" and "onIgnoreTag" at the same time'), e.onIgnoreTag = n.onIgnoreTagStripAll),
                    e.whiteList = e.whiteList || n.whiteList,
                    e.onTag = e.onTag || n.onTag,
                    e.onTagAttr = e.onTagAttr || n.onTagAttr,
                    e.onIgnoreTag = e.onIgnoreTag || n.onIgnoreTag,
                    e.onIgnoreTagAttr = e.onIgnoreTagAttr || n.onIgnoreTagAttr,
                    e.safeAttrValue = e.safeAttrValue || n.safeAttrValue,
                    e.escapeHtml = e.escapeHtml || n.escapeHtml,
                    !1 === (this.options = e).css ? this.cssFilter = !1 : (e.css = e.css || {},
                        this.cssFilter = new r(e.css))
            }
            s.prototype.process = function (e) {
                if (!(e = (e = e || "").toString())) return "";
                var t = this.options,
                    c = t.whiteList,
                    u = t.onTag,
                    p = t.onIgnoreTag,
                    f = t.onTagAttr,
                    h = t.onIgnoreTagAttr,
                    g = t.safeAttrValue,
                    m = t.escapeHtml,
                    v = this.cssFilter;
                t.stripBlankChar && (e = n.stripBlankChar(e)),
                    t.allowCommentTag || (e = n.stripCommentTag(e));
                var i = !1;
                if (t.stripIgnoreTagBody) {
                    i = n.StripTagBody(t.stripIgnoreTagBody, p);
                    p = i.onIgnoreTag
                }
                var r = a(e,
                    function (e, t, n, i, r) {
                        var o, a = {
                            sourcePosition: e,
                            position: t,
                            isClosing: r,
                            isWhite: n in c
                        };
                        if (!y(o = u(n, i, a))) return o;
                        if (a.isWhite) {
                            if (a.isClosing) return "</" + n + ">";
                            var s = function (e) {
                                var t = b.spaceIndex(e);
                                if (- 1 === t) return {
                                    html: "",
                                    closing: "/" === e[e.length - 2]
                                };
                                var i = "/" === (e = b.trim(e.slice(t + 1, -1)))[e.length - 1];
                                return i && (e = b.trim(e.slice(0, -1))),
                                {
                                    html: e,
                                    closing: i
                                }
                            }(i),
                                l = c[n],
                                d = w(s.html,
                                    function (e, t) {
                                        var i, r = -1 !== b.indexOf(l, e);
                                        return y(i = f(n, e, t, r)) ? r ? (t = g(n, e, t, v)) ? e + '="' + t + '"' : e : y(i = h(n, e, t, r)) ? void 0 : i : i
                                    });
                            i = "<" + n;
                            return d && (i += " " + d),
                                s.closing && (i += " /"),
                                i += ">"
                        }
                        return y(o = p(n, i, a)) ? m(i) : o
                    },
                    m);
                return i && (r = i.remove(r)),
                    r
            },
                t.exports = s
        },
        {
            "./default": 2,
            "./parser": 4,
            "./util": 5,
            cssfilter: 10
        }],
        7: [function (e, t, i) {
            var r, n;
            r = this,
                n = function () {
                    var T = !0;
                    function a(i) {
                        function e(e) {
                            var t = i.match(e);
                            return t && 1 < t.length && t[1] || ""
                        }
                        function t(e) {
                            var t = i.match(e);
                            return t && 1 < t.length && t[2] || ""
                        }
                        var r, n = e(/(ipod|iphone|ipad)/i).toLowerCase(),
                            o = !/like android/i.test(i) && /android/i.test(i),
                            a = /nexus\s*[0-6]\s*/i.test(i),
                            s = !a && /nexus\s*[0-9]+/i.test(i),
                            l = /CrOS/.test(i),
                            d = /silk/i.test(i),
                            c = /sailfish/i.test(i),
                            u = /tizen/i.test(i),
                            p = /(web|hpw)os/i.test(i),
                            f = /windows phone/i.test(i),
                            h = (/SamsungBrowser/i.test(i), !f && /windows/i.test(i)),
                            g = !n && !d && /macintosh/i.test(i),
                            m = !o && !c && !u && !p && /linux/i.test(i),
                            v = t(/edg([ea]|ios)\/(\d+(\.\d+)?)/i),
                            w = e(/version\/(\d+(\.\d+)?)/i),
                            b = /tablet/i.test(i) && !/tablet pc/i.test(i),
                            y = !b && /[^-]mobi/i.test(i),
                            _ = /xbox/i.test(i);
                        /opera/i.test(i) ? r = {
                            name: "Opera",
                            opera: T,
                            version: w || e(/(?:opera|opr|opios)[\s\/](\d+(\.\d+)?)/i)
                        } : /opr\/|opios/i.test(i) ? r = {
                            name: "Opera",
                            opera: T,
                            version: e(/(?:opr|opios)[\s\/](\d+(\.\d+)?)/i) || w
                        } : /SamsungBrowser/i.test(i) ? r = {
                            name: "Samsung Internet for Android",
                            samsungBrowser: T,
                            version: w || e(/(?:SamsungBrowser)[\s\/](\d+(\.\d+)?)/i)
                        } : /coast/i.test(i) ? r = {
                            name: "Opera Coast",
                            coast: T,
                            version: w || e(/(?:coast)[\s\/](\d+(\.\d+)?)/i)
                        } : /yabrowser/i.test(i) ? r = {
                            name: "Yandex Browser",
                            yandexbrowser: T,
                            version: w || e(/(?:yabrowser)[\s\/](\d+(\.\d+)?)/i)
                        } : /ucbrowser/i.test(i) ? r = {
                            name: "UC Browser",
                            ucbrowser: T,
                            version: e(/(?:ucbrowser)[\s\/](\d+(?:\.\d+)+)/i)
                        } : /mxios/i.test(i) ? r = {
                            name: "Maxthon",
                            maxthon: T,
                            version: e(/(?:mxios)[\s\/](\d+(?:\.\d+)+)/i)
                        } : /epiphany/i.test(i) ? r = {
                            name: "Epiphany",
                            epiphany: T,
                            version: e(/(?:epiphany)[\s\/](\d+(?:\.\d+)+)/i)
                        } : /puffin/i.test(i) ? r = {
                            name: "Puffin",
                            puffin: T,
                            version: e(/(?:puffin)[\s\/](\d+(?:\.\d+)?)/i)
                        } : /sleipnir/i.test(i) ? r = {
                            name: "Sleipnir",
                            sleipnir: T,
                            version: e(/(?:sleipnir)[\s\/](\d+(?:\.\d+)+)/i)
                        } : /k-meleon/i.test(i) ? r = {
                            name: "K-Meleon",
                            kMeleon: T,
                            version: e(/(?:k-meleon)[\s\/](\d+(?:\.\d+)+)/i)
                        } : f ? (r = {
                            name: "Windows Phone",
                            osname: "Windows Phone",
                            windowsphone: T
                        },
                            v ? (r.msedge = T, r.version = v) : (r.msie = T, r.version = e(/iemobile\/(\d+(\.\d+)?)/i))) : /msie|trident/i.test(i) ? r = {
                                name: "Internet Explorer",
                                msie: T,
                                version: e(/(?:msie |rv:)(\d+(\.\d+)?)/i)
                            } : l ? r = {
                                name: "Chrome",
                                osname: "Chrome OS",
                                chromeos: T,
                                chromeBook: T,
                                chrome: T,
                                version: e(/(?:chrome|crios|crmo)\/(\d+(\.\d+)?)/i)
                            } : /edg([ea]|ios)/i.test(i) ? r = {
                                name: "Microsoft Edge",
                                msedge: T,
                                version: v
                            } : /vivaldi/i.test(i) ? r = {
                                name: "Vivaldi",
                                vivaldi: T,
                                version: e(/vivaldi\/(\d+(\.\d+)?)/i) || w
                            } : c ? r = {
                                name: "Sailfish",
                                osname: "Sailfish OS",
                                sailfish: T,
                                version: e(/sailfish\s?browser\/(\d+(\.\d+)?)/i)
                            } : /seamonkey\//i.test(i) ? r = {
                                name: "SeaMonkey",
                                seamonkey: T,
                                version: e(/seamonkey\/(\d+(\.\d+)?)/i)
                            } : /firefox|iceweasel|fxios/i.test(i) ? (r = {
                                name: "Firefox",
                                firefox: T,
                                version: e(/(?:firefox|iceweasel|fxios)[ \/](\d+(\.\d+)?)/i)
                            },
                                /\((mobile|tablet);[^\)]*rv:[\d\.]+\)/i.test(i) && (r.firefoxos = T, r.osname = "Firefox OS")) : d ? r = {
                                    name: "Amazon Silk",
                                    silk: T,
                                    version: e(/silk\/(\d+(\.\d+)?)/i)
                                } : /phantom/i.test(i) ? r = {
                                    name: "PhantomJS",
                                    phantom: T,
                                    version: e(/phantomjs\/(\d+(\.\d+)?)/i)
                                } : /slimerjs/i.test(i) ? r = {
                                    name: "SlimerJS",
                                    slimer: T,
                                    version: e(/slimerjs\/(\d+(\.\d+)?)/i)
                                } : /blackberry|\bbb\d+/i.test(i) || /rim\stablet/i.test(i) ? r = {
                                    name: "BlackBerry",
                                    osname: "BlackBerry OS",
                                    blackberry: T,
                                    version: w || e(/blackberry[\d]+\/(\d+(\.\d+)?)/i)
                                } : p ? (r = {
                                    name: "WebOS",
                                    osname: "WebOS",
                                    webos: T,
                                    version: w || e(/w(?:eb)?osbrowser\/(\d+(\.\d+)?)/i)
                                },
                                    /touchpad\//i.test(i) && (r.touchpad = T)) : /bada/i.test(i) ? r = {
                                        name: "Bada",
                                        osname: "Bada",
                                        bada: T,
                                        version: e(/dolfin\/(\d+(\.\d+)?)/i)
                                    } : u ? r = {
                                        name: "Tizen",
                                        osname: "Tizen",
                                        tizen: T,
                                        version: e(/(?:tizen\s?)?browser\/(\d+(\.\d+)?)/i) || w
                                    } : /qupzilla/i.test(i) ? r = {
                                        name: "QupZilla",
                                        qupzilla: T,
                                        version: e(/(?:qupzilla)[\s\/](\d+(?:\.\d+)+)/i) || w
                                    } : /chromium/i.test(i) ? r = {
                                        name: "Chromium",
                                        chromium: T,
                                        version: e(/(?:chromium)[\s\/](\d+(?:\.\d+)?)/i) || w
                                    } : /chrome|crios|crmo/i.test(i) ? r = {
                                        name: "Chrome",
                                        chrome: T,
                                        version: e(/(?:chrome|crios|crmo)\/(\d+(\.\d+)?)/i)
                                    } : o ? r = {
                                        name: "Android",
                                        version: w
                                    } : /safari|applewebkit/i.test(i) ? (r = {
                                        name: "Safari",
                                        safari: T
                                    },
                                        w && (r.version = w)) : n ? (r = {
                                            name: "iphone" == n ? "iPhone" : "ipad" == n ? "iPad" : "iPod"
                                        },
                                            w && (r.version = w)) : r = /googlebot/i.test(i) ? {
                                                name: "Googlebot",
                                                googlebot: T,
                                                version: e(/googlebot\/(\d+(\.\d+))/i) || w
                                            } : {
                                                name: e(/^(.*)\/(.*) /),
                                                version: t(/^(.*)\/(.*) /)
                                            },
                            !r.msedge && /(apple)?webkit/i.test(i) ? (/(apple)?webkit\/537\.36/i.test(i) ? (r.name = r.name || "Blink", r.blink = T) : (r.name = r.name || "Webkit", r.webkit = T), !r.version && w && (r.version = w)) : !r.opera && /gecko\//i.test(i) && (r.name = r.name || "Gecko", r.gecko = T, r.version = r.version || e(/gecko\/(\d+(\.\d+)?)/i)),
                            r.windowsphone || !o && !r.silk ? !r.windowsphone && n ? (r[n] = T, r.ios = T, r.osname = "iOS") : g ? (r.mac = T, r.osname = "macOS") : _ ? (r.xbox = T, r.osname = "Xbox") : h ? (r.windows = T, r.osname = "Windows") : m && (r.linux = T, r.osname = "Linux") : (r.android = T, r.osname = "Android");
                        var x = "";
                        r.windows ? x = function (e) {
                            switch (e) {
                                case "NT":
                                    return "NT";
                                case "XP":
                                    return "XP";
                                case "NT 5.0":
                                    return "2000";
                                case "NT 5.1":
                                    return "XP";
                                case "NT 5.2":
                                    return "2003";
                                case "NT 6.0":
                                    return "Vista";
                                case "NT 6.1":
                                    return "7";
                                case "NT 6.2":
                                    return "8";
                                case "NT 6.3":
                                    return "8.1";
                                case "NT 10.0":
                                    return "10";
                                default:
                                    return
                            }
                        }(e(/Windows ((NT|XP)( \d\d?.\d)?)/i)) :
                            r.windowsphone ? x = e(/windows phone (?:os)?\s?(\d+(\.\d+)*)/i) : r.mac ? x = (x = e(/Mac OS X (\d+([_\.\s]\d+)*)/i)).replace(/[_\s]/g, ".") : n ? x = (x = e(/os (\d+([_\s]\d+)*) like mac os x/i)).replace(/[_\s]/g, ".") : o ? x = e(/android[ \/-](\d+(\.\d+)*)/i) : r.webos ? x = e(/(?:web|hpw)os\/(\d+(\.\d+)*)/i) : r.blackberry ? x = e(/rim\stablet\sos\s(\d+(\.\d+)*)/i) : r.bada ? x = e(/bada\/(\d+(\.\d+)*)/i) : r.tizen && (x = e(/tizen[\/\s](\d+(\.\d+)*)/i)),
                            x && (r.osversion = x);
                        var k = !r.windows && x.split(".")[0];
                        return b || s || "ipad" == n || o && (3 == k || 4 <= k && !y) || r.silk ? r.tablet = T : (y || "iphone" == n || "ipod" == n || o || a || r.blackberry || r.webos || r.bada) && (r.mobile = T),
                            r.msedge || r.msie && 10 <= r.version || r.yandexbrowser && 15 <= r.version || r.vivaldi && 1 <= r.version || r.chrome && 20 <= r.version || r.samsungBrowser && 4 <= r.version || r.firefox && 20 <= r.version || r.safari && 6 <= r.version || r.opera && 10 <= r.version || r.ios && r.osversion && 6 <= r.osversion.split(".")[0] || r.blackberry && 10.1 <= r.version || r.chromium && 20 <= r.version ? r.a = T : r.msie && r.version < 10 || r.chrome && r.version < 20 || r.firefox && r.version < 20 || r.safari && r.version < 6 || r.opera && r.version < 10 || r.ios && r.osversion && r.osversion.split(".")[0] < 6 || r.chromium && r.version < 20 ? r.c = T : r.x = T,
                            r
                    }
                    var s = a("undefined" != typeof navigator && navigator.userAgent || "");
                    function r(e) {
                        return e.split(".").length
                    }
                    function n(e, t) {
                        var i, r = [];
                        if (Array.prototype.map) return Array.prototype.map.call(e, t);
                        for (i = 0; i < e.length; i++) r.push(t(e[i]));
                        return r
                    }
                    function l(e) {
                        for (var i = Math.max(r(e[0]), r(e[1])), t = n(e,
                            function (e) {
                                var t = i - r(e);
                                return n((e += new Array(t + 1).join(".0")).split("."),
                                    function (e) {
                                        return new Array(20 - e.length).join("0") + e
                                    }).reverse()
                            }); 0 <= --i;) {
                            if (t[0][i] > t[1][i]) return 1;
                            if (t[0][i] !== t[1][i]) return - 1;
                            if (0 === i) return 0
                        }
                    }
                    function o(e, t, i) {
                        var r = s;
                        "string" == typeof t && (i = t, t = void 0),
                            void 0 === t && (t = !1),
                            i && (r = a(i));
                        var n = "" + r.version;
                        for (var o in e) if (e.hasOwnProperty(o) && r[o]) {
                            if ("string" != typeof e[o]) throw new Error("Browser version in the minVersion map should be a string: " + o + ": " + String(e));
                            return l([n, e[o]]) < 0
                        }
                        return t
                    }
                    return s.test = function (e) {
                        for (var t = 0; t < e.length; ++t) {
                            var i = e[t];
                            if ("string" == typeof i && i in s) return !0
                        }
                        return !1
                    },
                        s.isUnsupportedBrowser = o,
                        s.compareVersions = l,
                        s.check = function (e, t, i) {
                            return !o(e, t, i)
                        },
                        s._detect = a,
                        s.detect = a,
                        s
                },
                void 0 !== t && t.exports ? t.exports = n() : "function" == typeof define && define.amd ? define("bowser", n) : r.bowser = n()
        },
        {}],
        8: [function (e, t, i) {
            var r = e("./default"),
                n = e("./parser");
            e("./util");
            function p(e) {
                return null == e
            }
            function o(e) {
                (e = e || {}).whiteList = e.whiteList || r.whiteList,
                    e.onAttr = e.onAttr || r.onAttr,
                    e.onIgnoreAttr = e.onIgnoreAttr || r.onIgnoreAttr,
                    this.options = e
            }
            o.prototype.process = function (e) {
                if (!(e = (e = e || "").toString())) return "";
                var t = this.options,
                    d = t.whiteList,
                    c = t.onAttr,
                    u = t.onIgnoreAttr;
                return n(e,
                    function (e, t, i, r, n) {
                        var o = d[i],
                            a = !1; !0 === o ? a = o : "function" == typeof o ? a = o(r) : o instanceof RegExp && (a = o.test(r)),
                                !0 !== a && (a = !1);
                        var s, l = {
                            position: t,
                            sourcePosition: e,
                            source: n,
                            isWhite: a
                        };
                        return a ? p(s = c(i, r, l)) ? i + ":" + r : s : p(s = u(i, r, l)) ? void 0 : s
                    })
            },
                t.exports = o
        },
        {
            "./default": 9,
            "./parser": 11,
            "./util": 12
        }],
        9: [function (e, t, i) {
            function r() {
                var e = {
                    "align-content": !1,
                    "align-items": !1,
                    "align-self": !1,
                    "alignment-adjust": !1,
                    "alignment-baseline": !1,
                    all: !1,
                    "anchor-point": !1,
                    animation: !1,
                    "animation-delay": !1,
                    "animation-direction": !1,
                    "animation-duration": !1,
                    "animation-fill-mode": !1,
                    "animation-iteration-count": !1,
                    "animation-name": !1,
                    "animation-play-state": !1,
                    "animation-timing-function": !1,
                    azimuth: !1,
                    "backface-visibility": !1,
                    background: !0,
                    "background-attachment": !0,
                    "background-clip": !0,
                    "background-color": !0,
                    "background-image": !0,
                    "background-origin": !0,
                    "background-position": !0,
                    "background-repeat": !0,
                    "background-size": !0,
                    "baseline-shift": !1,
                    binding: !1,
                    bleed: !1,
                    "bookmark-label": !1,
                    "bookmark-level": !1,
                    "bookmark-state": !1,
                    border: !0,
                    "border-bottom": !0,
                    "border-bottom-color": !0,
                    "border-bottom-left-radius": !0,
                    "border-bottom-right-radius": !0,
                    "border-bottom-style": !0,
                    "border-bottom-width": !0,
                    "border-collapse": !0,
                    "border-color": !0,
                    "border-image": !0,
                    "border-image-outset": !0,
                    "border-image-repeat": !0,
                    "border-image-slice": !0,
                    "border-image-source": !0,
                    "border-image-width": !0,
                    "border-left": !0,
                    "border-left-color": !0,
                    "border-left-style": !0,
                    "border-left-width": !0,
                    "border-radius": !0,
                    "border-right": !0,
                    "border-right-color": !0,
                    "border-right-style": !0,
                    "border-right-width": !0,
                    "border-spacing": !0,
                    "border-style": !0,
                    "border-top": !0,
                    "border-top-color": !0,
                    "border-top-left-radius": !0,
                    "border-top-right-radius": !0,
                    "border-top-style": !0,
                    "border-top-width": !0,
                    "border-width": !0,
                    bottom: !1,
                    "box-decoration-break": !0,
                    "box-shadow": !0,
                    "box-sizing": !0,
                    "box-snap": !0,
                    "box-suppress": !0,
                    "break-after": !0,
                    "break-before": !0,
                    "break-inside": !0,
                    "caption-side": !1,
                    chains: !1,
                    clear: !0,
                    clip: !1,
                    "clip-path": !1,
                    "clip-rule": !1,
                    color: !0,
                    "color-interpolation-filters": !0,
                    "column-count": !1,
                    "column-fill": !1,
                    "column-gap": !1,
                    "column-rule": !1,
                    "column-rule-color": !1,
                    "column-rule-style": !1,
                    "column-rule-width": !1,
                    "column-span": !1,
                    "column-width": !1,
                    columns: !1,
                    contain: !1,
                    content: !1,
                    "counter-increment": !1,
                    "counter-reset": !1,
                    "counter-set": !1,
                    crop: !1,
                    cue: !1,
                    "cue-after": !1,
                    "cue-before": !1,
                    cursor: !1,
                    direction: !1,
                    display: !0,
                    "display-inside": !0,
                    "display-list": !0,
                    "display-outside": !0,
                    "dominant-baseline": !1,
                    elevation: !1,
                    "empty-cells": !1,
                    filter: !1,
                    flex: !1,
                    "flex-basis": !1,
                    "flex-direction": !1,
                    "flex-flow": !1,
                    "flex-grow": !1,
                    "flex-shrink": !1,
                    "flex-wrap": !1,
                    float: !1,
                    "float-offset": !1,
                    "flood-color": !1,
                    "flood-opacity": !1,
                    "flow-from": !1,
                    "flow-into": !1,
                    font: !0,
                    "font-family": !0,
                    "font-feature-settings": !0,
                    "font-kerning": !0,
                    "font-language-override": !0,
                    "font-size": !0,
                    "font-size-adjust": !0,
                    "font-stretch": !0,
                    "font-style": !0,
                    "font-synthesis": !0,
                    "font-variant": !0,
                    "font-variant-alternates": !0,
                    "font-variant-caps": !0,
                    "font-variant-east-asian": !0,
                    "font-variant-ligatures": !0,
                    "font-variant-numeric": !0,
                    "font-variant-position": !0,
                    "font-weight": !0,
                    grid: !1,
                    "grid-area": !1,
                    "grid-auto-columns": !1,
                    "grid-auto-flow": !1,
                    "grid-auto-rows": !1,
                    "grid-column": !1,
                    "grid-column-end": !1,
                    "grid-column-start": !1,
                    "grid-row": !1,
                    "grid-row-end": !1,
                    "grid-row-start": !1,
                    "grid-template": !1,
                    "grid-template-areas": !1,
                    "grid-template-columns": !1,
                    "grid-template-rows": !1,
                    "hanging-punctuation": !1,
                    height: !0,
                    hyphens: !1,
                    icon: !1,
                    "image-orientation": !1,
                    "image-resolution": !1,
                    "ime-mode": !1,
                    "initial-letters": !1,
                    "inline-box-align": !1,
                    "justify-content": !1,
                    "justify-items": !1,
                    "justify-self": !1,
                    left: !1,
                    "letter-spacing": !0,
                    "lighting-color": !0,
                    "line-box-contain": !1,
                    "line-break": !1,
                    "line-grid": !1,
                    "line-height": !1,
                    "line-snap": !1,
                    "line-stacking": !1,
                    "line-stacking-ruby": !1,
                    "line-stacking-shift": !1,
                    "line-stacking-strategy": !1,
                    "list-style": !0,
                    "list-style-image": !0,
                    "list-style-position": !0,
                    "list-style-type": !0,
                    margin: !0,
                    "margin-bottom": !0,
                    "margin-left": !0,
                    "margin-right": !0,
                    "margin-top": !0,
                    "marker-offset": !1,
                    "marker-side": !1,
                    marks: !1,
                    mask: !1,
                    "mask-box": !1,
                    "mask-box-outset": !1,
                    "mask-box-repeat": !1,
                    "mask-box-slice": !1,
                    "mask-box-source": !1,
                    "mask-box-width": !1,
                    "mask-clip": !1,
                    "mask-image": !1,
                    "mask-origin": !1,
                    "mask-position": !1,
                    "mask-repeat": !1,
                    "mask-size": !1,
                    "mask-source-type": !1,
                    "mask-type": !1,
                    "max-height": !0,
                    "max-lines": !1,
                    "max-width": !0,
                    "min-height": !0,
                    "min-width": !0,
                    "move-to": !1,
                    "nav-down": !1,
                    "nav-index": !1,
                    "nav-left": !1,
                    "nav-right": !1,
                    "nav-up": !1,
                    "object-fit": !1,
                    "object-position": !1,
                    opacity: !1,
                    order: !1,
                    orphans: !1,
                    outline: !1,
                    "outline-color": !1,
                    "outline-offset": !1,
                    "outline-style": !1,
                    "outline-width": !1,
                    overflow: !1,
                    "overflow-wrap": !1,
                    "overflow-x": !1,
                    "overflow-y": !1,
                    padding: !0,
                    "padding-bottom": !0,
                    "padding-left": !0,
                    "padding-right": !0,
                    "padding-top": !0,
                    page: !1,
                    "page-break-after": !1,
                    "page-break-before": !1,
                    "page-break-inside": !1,
                    "page-policy": !1,
                    pause: !1,
                    "pause-after": !1,
                    "pause-before": !1,
                    perspective: !1,
                    "perspective-origin": !1,
                    pitch: !1,
                    "pitch-range": !1,
                    "play-during": !1,
                    position: !1,
                    "presentation-level": !1,
                    quotes: !1,
                    "region-fragment": !1,
                    resize: !1,
                    rest: !1,
                    "rest-after": !1,
                    "rest-before": !1,
                    richness: !1,
                    right: !1,
                    rotation: !1,
                    "rotation-point": !1,
                    "ruby-align": !1,
                    "ruby-merge": !1,
                    "ruby-position": !1,
                    "shape-image-threshold": !1,
                    "shape-outside": !1,
                    "shape-margin": !1,
                    size: !1,
                    speak: !1,
                    "speak-as": !1,
                    "speak-header": !1,
                    "speak-numeral": !1,
                    "speak-punctuation": !1,
                    "speech-rate": !1,
                    stress: !1,
                    "string-set": !1,
                    "tab-size": !1,
                    "table-layout": !1,
                    "text-align": !0,
                    "text-align-last": !0,
                    "text-combine-upright": !0,
                    "text-decoration": !0,
                    "text-decoration-color": !0,
                    "text-decoration-line": !0,
                    "text-decoration-skip": !0,
                    "text-decoration-style": !0,
                    "text-emphasis": !0,
                    "text-emphasis-color": !0,
                    "text-emphasis-position": !0,
                    "text-emphasis-style": !0,
                    "text-height": !0,
                    "text-indent": !0,
                    "text-justify": !0,
                    "text-orientation": !0,
                    "text-overflow": !0,
                    "text-shadow": !0,
                    "text-space-collapse": !0,
                    "text-transform": !0,
                    "text-underline-position": !0,
                    "text-wrap": !0,
                    top: !1,
                    transform: !1,
                    "transform-origin": !1,
                    "transform-style": !1,
                    transition: !1,
                    "transition-delay": !1,
                    "transition-duration": !1,
                    "transition-property": !1,
                    "transition-timing-function": !1,
                    "unicode-bidi": !1,
                    "vertical-align": !1,
                    visibility: !1,
                    "voice-balance": !1,
                    "voice-duration": !1,
                    "voice-family": !1,
                    "voice-pitch": !1,
                    "voice-range": !1,
                    "voice-rate": !1,
                    "voice-stress": !1,
                    "voice-volume": !1,
                    volume: !1,
                    "white-space": !1,
                    widows: !1,
                    width: !0,
                    "will-change": !1,
                    "word-break": !0,
                    "word-spacing": !0,
                    "word-wrap": !0,
                    "wrap-flow": !1,
                    "wrap-through": !1,
                    "writing-mode": !1,
                    "z-index": !1
                };
                return e
            }
            i.whiteList = r(),
                i.getDefaultWhiteList = r,
                i.onAttr = function (e, t, i) { },
                i.onIgnoreAttr = function (e, t, i) { }
        },
        {}],
        10: [function (e, t, i) {
            var r = e("./default"),
                n = e("./css");
            for (var o in (i = t.exports = function (e, t) {
                return new n(t).process(e)
            }).FilterCSS = n, r) i[o] = r[o];
            "undefined" != typeof window && (window.filterCSS = t.exports)
        },
        {
            "./css": 8,
            "./default": 9
        }],
        11: [function (e, t, i) {
            var u = e("./util");
            t.exports = function (o, a) {
                ";" !== (o = u.trimRight(o))[o.length - 1] && (o += ";");
                var e = o.length,
                    s = !1,
                    l = 0,
                    d = 0,
                    c = "";
                function t() {
                    if (!s) {
                        var e = u.trim(o.slice(l, d)),
                            t = e.indexOf(":");
                        if (- 1 !== t) {
                            var i = u.trim(e.slice(0, t)),
                                r = u.trim(e.slice(t + 1));
                            if (i) {
                                var n = a(l, c.length, i, r, e);
                                n && (c += n + "; ")
                            }
                        }
                    }
                    l = d + 1
                }
                for (; d < e; d++) {
                    var i = o[d];
                    if ("/" === i && "*" === o[d + 1]) {
                        var r = o.indexOf("*/", d + 2);
                        if (- 1 === r) break;
                        l = (d = r + 1) + 1,
                            s = !1
                    } else "(" === i ? s = !0 : ")" === i ? s = !1 : ";" === i ? s || t() : "\n" === i && t()
                }
                return u.trim(c)
            }
        },
        {
            "./util": 12
        }],
        12: [function (e, t, i) {
            t.exports = {
                indexOf: function (e, t) {
                    var i, r;
                    if (Array.prototype.indexOf) return e.indexOf(t);
                    for (i = 0, r = e.length; i < r; i++) if (e[i] === t) return i;
                    return - 1
                },
                forEach: function (e, t, i) {
                    var r, n;
                    if (Array.prototype.forEach) return e.forEach(t, i);
                    for (r = 0, n = e.length; r < n; r++) t.call(i, e[r], r, e)
                },
                trim: function (e) {
                    return String.prototype.trim ? e.trim() : e.replace(/(^\s*)|(\s*$)/g, "")
                },
                trimRight: function (e) {
                    return String.prototype.trimRight ? e.trimRight() : e.replace(/(\s*$)/g, "")
                }
            }
        },
        {}],
        13: [function (e, t, i) {
            var r, n;
            r = this,
                n = function () {
                    var e = {},
                        i = "undefined" != typeof window && window,
                        t = "undefined" != typeof document && document,
                        r = t && t.documentElement,
                        n = i.matchMedia || i.msMatchMedia,
                        o = n ?
                            function (e) {
                                return !!n.call(i, e).matches
                            } : function () {
                                return !1
                            },
                        a = e.viewportW = function () {
                            var e = r.clientWidth,
                                t = i.innerWidth;
                            return e < t ? t : e
                        },
                        s = e.viewportH = function () {
                            var e = r.clientHeight,
                                t = i.innerHeight;
                            return e < t ? t : e
                        };
                    function l() {
                        return {
                            width: a(),
                            height: s()
                        }
                    }
                    function d(e, t) {
                        return !(!(e = e && !e.nodeType ? e[0] : e) || 1 !== e.nodeType) && (i = e.getBoundingClientRect(), r = +(r = t) || 0, (n = {}).width = (n.right = i.right + r) - (n.left = i.left - r), n.height = (n.bottom = i.bottom + r) - (n.top = i.top - r), n);
                        var i, r, n
                    }
                    return e.mq = o,
                        e.matchMedia = n ?
                            function () {
                                return n.apply(i, arguments)
                            } : function () {
                                return {}
                            },
                        e.viewport = l,
                        e.scrollX = function () {
                            return i.pageXOffset || r.scrollLeft
                        },
                        e.scrollY = function () {
                            return i.pageYOffset || r.scrollTop
                        },
                        e.rectangle = d,
                        e.aspect = function (e) {
                            var t = (e = null == e ? l() : 1 === e.nodeType ? d(e) : e).height,
                                i = e.width;
                            return t = "function" == typeof t ? t.call(e) : t,
                                (i = "function" == typeof i ? i.call(e) : i) / t
                        },
                        e.inX = function (e, t) {
                            var i = d(e, t);
                            return !!i && 0 <= i.right && i.left <= a()
                        },
                        e.inY = function (e, t) {
                            var i = d(e, t);
                            return !!i && 0 <= i.bottom && i.top <= s()
                        },
                        e.inViewport = function (e, t) {
                            var i = d(e, t);
                            return !!i && 0 <= i.bottom && 0 <= i.right && i.top <= s() && i.left <= a()
                        },
                        e
                },
                void 0 !== t && t.exports ? t.exports = n() : r.verge = n()
        },
        {}],
        14: [function (e, t, i) {
            (i = {
                THEME_RTD: "sphinx_rtd_theme",
                THEME_ALABASTER: "alabaster",
                THEME_MKDOCS_RTD: "readthedocs",
                THEME_CELERY: "sphinx_celery",
                THEME_BABEL: "babel",
                THEME_CLICK: "click",
                THEME_FLASK_SQLALCHEMY: "flask-sqlalchemy",
                THEME_FLASK: "flask",
                THEME_JINJA: "jinja",
                THEME_PLATTER: "platter",
                THEME_POCOO: "pocoo",
                THEME_WERKZEUG: "werkzeug",
                DEFAULT_PROMO_PRIORITY: 5,
                MINIMUM_PROMO_PRIORITY: 10,
                MAXIMUM_PROMO_PRIORITY: 1,
                LOW_PROMO_PRIORITY: 10
            }).ALABASTER_LIKE_THEMES = [i.THEME_ALABASTER, i.THEME_CELERY, i.THEME_BABEL, i.THEME_CLICK, i.THEME_FLASK_SQLALCHEMY, i.THEME_FLASK, i.THEME_JINJA, i.THEME_PLATTER, i.THEME_POCOO, i.THEME_WERKZEUG],
                i.PROMO_TYPES = {
                    LEFTNAV: "doc",
                    FOOTER: "site-footer",
                    FIXED_FOOTER: "fixed-footer"
                },
                t.exports = i
        },
        {}],
        15: [function (e, t, i) {
            var r = e("./rtd-data"),
                n = e("./version-compare");
            t.exports = {
                init: function () {
                    var e = r.get(),
                        t = {
                            project: e.project,
                            version: e.version,
                            page: e.page,
                            theme: e.get_theme_name(),
                            format: "jsonp"
                        };
                    "docroot" in e && (t.docroot = e.docroot),
                        "source_suffix" in e && (t.source_suffix = e.source_suffix),
                        0 === window.location.pathname.indexOf("/projects/") && (t.subproject = !0),
                        $.ajax({
                            url: e.api_host + "/api/v2/footer_html/",
                            crossDomain: !0,
                            xhrFields: {
                                withCredentials: !0
                            },
                            dataType: "jsonp",
                            data: t,
                            success: function (e) {
                                var t, i;
                                e.show_version_warning && n.init(e.version_compare),
                                    t = e,
                                    (i = r.get()).is_sphinx_builder() && i.is_rtd_like_theme() ? $("div.rst-other-versions").html(t.html) : $("body").append(t.html),
                                    t.version_active ? t.version_supported : $(".rst-current-version").addClass("rst-out-of-date"),
                                    $.ajaxSetup({
                                        beforeSend: function (e, t) {
                                            var i;
                                            i = t.type,
                                                /^(GET|HEAD|OPTIONS|TRACE)$/.test(i) || e.setRequestHeader("X-CSRFToken", $("a.bookmark[token]").attr("token"))
                                        }
                                    })
                            },
                            error: function () {
                                console.error("Error loading Read the Docs footer")
                            }
                        })
                }
            }
        },
        {
            "./rtd-data": 16,
            "./version-compare": 20
        }],
        16: [function (e, t, i) {
            var r = e("./constants"),
                n = {
                    is_rtd_like_theme: function () {
                        return 1 === $("div.rst-other-versions").length || (this.theme === r.THEME_RTD || this.theme === r.THEME_MKDOCS_RTD)
                    },
                    is_alabaster_like_theme: function () {
                        return - 1 < r.ALABASTER_LIKE_THEMES.indexOf(this.get_theme_name())
                    },
                    theme_supports_promo: function () {
                        return this.is_rtd_like_theme() || this.is_alabaster_like_theme()
                    },
                    is_sphinx_builder: function () {
                        return !("builder" in this) || "mkdocs" !== this.builder
                    },
                    is_mkdocs_builder: function () {
                        return "builder" in this && "mkdocs" === this.builder
                    },
                    get_theme_name: function () {
                        return this.theme
                    },
                    show_promo: function () {
                        return "https://readthedocs.com" !== this.api_host && this.theme_supports_promo()
                    }
                };
            t.exports = {
                get: function () {
                    var e = Object.create(n);
                    return $.extend(e, {
                        api_host: "https://readthedocs.org",
                        ad_free: !1
                    },
                        window.READTHEDOCS_DATA),
                        e
                }
            }
        },
        {
            "./constants": 14
        }],
        17: [function (e, t, i) {
            var r = e("./rtd-data"),
                u = e("./../../../../../../bower_components/xss/lib/index");
            t.exports = {
                init: function () {
                    !
                        function (e) {
                            var c = e.project,
                                t = e.version,
                                i = e.language || "en",
                                n = e.api_host;
                            if ("undefined" != typeof Search && c && t && (!e.features || !e.features.docsearch_disabled)) {
                                var r = Search.query;
                                Search.query_fallback = r,
                                    Search.query = function (d) {
                                        var r = $.Deferred(),
                                            e = document.createElement("a");
                                        e.href = n,
                                            e.pathname = "/api/v2/docsearch/",
                                            e.search = "?q=" + $.urlencode(d) + "&project=" + c + "&version=" + t + "&language=" + i,
                                            r.then(function (e) {
                                                var t = (e.hits || {}).hits || [];
                                                if (t.length) for (var i in t) {
                                                    var r = t[i],
                                                        n = r.fields || {},
                                                        o = $('<li style="display: none;"></li>'),
                                                        a = document.createElement("a"),
                                                        s = r.highlight;
                                                    if (a.href += n.link + DOCUMENTATION_OPTIONS.FILE_SUFFIX, a.search = "?highlight=" + $.urlencode(d), o.append($("<a />").attr("href", a).html(n.title)), -1 === n.project.indexOf(c) && o.append($("<span>").text(" (from project " + n.project + ")")), s.content.length) {
                                                        var l = $('<div class="context">').html(u(s.content[0]));
                                                        l.find("em").addClass("highlighted"),
                                                            o.append(l)
                                                    }
                                                    Search.output.append(o),
                                                        o.slideDown(5)
                                                }
                                                t.length ? Search.status.text(_("Search finished, found %s page(s) matching the search query.").replace("%s", t.length)) : Search.query_fallback(d)
                                            }).fail(function (e) {
                                                Search.query_fallback(d)
                                            }).always(function () {
                                                $("#search-progress").empty(),
                                                    Search.stopPulse(),
                                                    Search.title.text(_("Search Results")),
                                                    Search.status.fadeIn(500)
                                            }),
                                            $.ajax({
                                                url: e.href,
                                                crossDomain: !0,
                                                xhrFields: {
                                                    withCredentials: !0
                                                },
                                                complete: function (e, t) {
                                                    return void 0 === e.responseJSON || void 0 === e.responseJSON.results ? r.reject() : r.resolve(e.responseJSON.results)
                                                }
                                            }).fail(function (e, t, i) {
                                                return r.reject()
                                            })
                                    }
                            }
                            $(document).ready(function () {
                                "undefined" != typeof Search && Search.init()
                            })
                        }(r.get())
                }
            }
        },
        {
            "./../../../../../../bower_components/xss/lib/index": 3,
            "./rtd-data": 16
        }],
        18: [function (n, e, t) {
            var o = n("./rtd-data");
            e.exports = {
                init: function () {
                    var e = o.get();
                    if ($(document).on("click", "[data-toggle='rst-current-version']",
                        function () {
                            var e = $("[data-toggle='rst-versions']").hasClass("shift-up") ? "was_open" : "was_closed";
                            "undefined" != typeof ga ? ga("rtfd.send", "event", "Flyout", "Click", e) : "undefined" != typeof _gaq && _gaq.push(["rtfd._setAccount", "UA-17997319-1"], ["rtfd._trackEvent", "Flyout", "Click", e])
                        }), void 0 === window.SphinxRtdTheme) {
                        var t = n("./../../../../../../bower_components/sphinx-rtd-theme/js/theme.js").ThemeNav;
                        if ($(document).ready(function () {
                            setTimeout(function () {
                                t.navBar || t.enable()
                            },
                                1e3)
                        }), e.is_rtd_like_theme() && !$("div.wy-side-scroll:first").length) {
                            console.log("Applying theme sidebar fix...");
                            var i = $("nav.wy-nav-side:first"),
                                r = $("<div />").addClass("wy-side-scroll");
                            i.children().detach().appendTo(r),
                                r.prependTo(i),
                                t.navBar = r
                        }
                    }
                }
            }
        },
        {
            "./../../../../../../bower_components/sphinx-rtd-theme/js/theme.js": 1,
            "./rtd-data": 16
        }],
        19: [function (e, t, i) {
            var u, p = e("./constants"),
                f = e("./rtd-data"),
                r = e("bowser"),
                h = "#ethical-ad-placement";
            function g() {
                var e, t, i = "rtd-" + (Math.random() + 1).toString(36).substring(4),
                    r = p.PROMO_TYPES.LEFTNAV,
                    n = p.DEFAULT_PROMO_PRIORITY,
                    o = null;
                return u.is_mkdocs_builder() && u.is_rtd_like_theme() ? (o = "nav.wy-nav-side", e = "ethical-rtd ethical-dark-theme") : u.is_rtd_like_theme() ? (o = "nav.wy-nav-side > div.wy-side-scroll", e = "ethical-rtd ethical-dark-theme") : u.is_alabaster_like_theme() && (o = "div.sphinxsidebar > div.sphinxsidebarwrapper", e = "ethical-alabaster"),
                    o ? ($("<div />").attr("id", i).addClass(e).appendTo(o), (!(t = $("#" + i).offset()) || t.top > $(window).height()) && (n = p.LOW_PROMO_PRIORITY), {
                        div_id: i,
                        display_type: r,
                        priority: n
                    }) : null
            }
            function m() {
                var e, t, i = "rtd-" + (Math.random() + 1).toString(36).substring(4),
                    r = p.PROMO_TYPES.FOOTER,
                    n = p.DEFAULT_PROMO_PRIORITY,
                    o = null;
                return u.is_rtd_like_theme() ? (o = $("<div />").insertAfter("footer hr"), e = "ethical-rtd") : u.is_alabaster_like_theme() && (o = "div.bodywrapper .body", e = "ethical-alabaster"),
                    o ? ($("<div />").attr("id", i).addClass(e).appendTo(o), (!(t = $("#" + i).offset()) || t.top < $(window).height()) && (n = p.LOW_PROMO_PRIORITY), {
                        div_id: i,
                        display_type: r,
                        priority: n
                    }) : null
            }
            function v() {
                var e = "rtd-" + (Math.random() + 1).toString(36).substring(4),
                    t = p.PROMO_TYPES.FIXED_FOOTER;
                return r && r.mobile ? ($("<div />").attr("id", e).appendTo("body"), {
                    div_id: e,
                    display_type: t,
                    priority: p.MAXIMUM_PROMO_PRIORITY
                }) : null
            }
            function w(e) {
                this.id = e.id,
                    this.div_id = e.div_id || "",
                    this.html = e.html || "",
                    this.display_type = e.display_type || "",
                    this.view_tracking_url = e.view_url,
                    this.click_handler = function () {
                        "undefined" != typeof ga ? ga("rtfd.send", "event", "Promo", "Click", e.id) : "undefined" != typeof _gaq && _gaq.push(["rtfd._setAccount", "UA-17997319-1"], ["rtfd._trackEvent", "Promo", "Click", e.id])
                    }
            }
            w.prototype.display = function () {
                var e = "#" + this.div_id,
                    t = this.view_tracking_url;
                $(e).html(this.html),
                    $(e).find('a[href*="/sustainability/click/"]').on("click", this.click_handler);
                var i = function () {
                    $.inViewport($(e), -3) && ($("<img />").attr("src", t).css("display", "none").appendTo(e), $(window).off(".rtdinview"), $(".wy-side-scroll").off(".rtdinview"))
                };
                $(window).on("DOMContentLoaded.rtdinview load.rtdinview scroll.rtdinview resize.rtdinview", i),
                    $(".wy-side-scroll").on("scroll.rtdinview", i),
                    this.post_promo_display()
            },
                w.prototype.disable = function () {
                    $("#" + this.div_id).hide()
                },
                w.prototype.post_promo_display = function () {
                    this.display_type === p.PROMO_TYPES.FOOTER && ($("<hr />").insertAfter("#" + this.div_id), $("<hr />").insertBefore("#" + this.div_id + ".ethical-alabaster .ethical-footer"))
                },
                t.exports = {
                    Promo: w,
                    init: function () {
                        var e, t, i, r, n, o = {
                            format: "jsonp"
                        },
                            a = [],
                            s = [],
                            l = [],
                            d = [m, g, v];
                        if (u = f.get(), r = "rtd-" + (Math.random() + 1).toString(36).substring(4), n = p.PROMO_TYPES.LEFTNAV, i = u.is_rtd_like_theme() ? "ethical-rtd ethical-dark-theme" : "ethical-alabaster", t = 0 < $(h).length ? ($("<div />").attr("id", r).addClass(i).appendTo(h), {
                            div_id: r,
                            display_type: n
                        }) : null) a.push(t.div_id),
                            s.push(t.display_type),
                            l.push(t.priority || p.DEFAULT_PROMO_PRIORITY);
                        else {
                            if (!u.show_promo()) return;
                            for (var c = 0; c < d.length; c += 1)(t = d[c]()) && (a.push(t.div_id), s.push(t.display_type), l.push(t.priority || p.DEFAULT_PROMO_PRIORITY))
                        }
                        o.div_ids = a.join("|"),
                            o.display_types = s.join("|"),
                            o.priorities = l.join("|"),
                            o.project = u.project,
                            "undefined" != typeof URL && "undefined" != typeof URLSearchParams && ((e = new URL(window.location).searchParams).get("force_promo") && (o.force_promo = e.get("force_promo")), e.get("force_campaign") && (o.force_campaign = e.get("force_campaign"))),
                            $.ajax({
                                url: u.api_host + "/api/v2/sustainability/",
                                crossDomain: !0,
                                xhrFields: {
                                    withCredentials: !0
                                },
                                dataType: "jsonp",
                                data: o,
                                success: function (e) {
                                    e && e.div_id && e.html && new w(e).display()
                                },
                                error: function () {
                                    var e, t, i;
                                    console.error("Error loading Read the Docs promo"),
                                        !u.ad_free && "https://readthedocs.org" === u.api_host && (i = !1, $("<div />").attr("id", "rtd-detection").attr("class", "ethical-rtd").html("&nbsp;").appendTo("body"), 0 === $("#rtd-detection").height() && (i = !0), $("#rtd-detection").remove(), i) && (console.log("---------------------------------------------------------------------------------------"), console.log("Read the Docs hosts documentation for tens of thousands of open source projects."), console.log("We fund our development (we are open source) and operations through advertising."), console.log("We promise to:"), console.log(" - never let advertisers run 3rd party JavaScript"), console.log(" - never sell user data to advertisers or other 3rd parties"), console.log(" - only show advertisements of interest to developers"), console.log("Read more about our approach to advertising here: https://docs.readthedocs.io/en/latest/ethical-advertising.html"), console.log("%cPlease allow our Ethical Ads or go ad-free:", "font-size: 2em"), console.log("https://docs.readthedocs.io/en/latest/advertising/ad-blocking.html"), console.log("--------------------------------------------------------------------------------------"), e = g(), t = null, e && e.div_id && (t = $("#" + e.div_id).attr("class", "keep-us-sustainable"), $("<p />").text("Support Read the Docs!").appendTo(t), $("<p />").html('Please help keep us sustainable by <a href="https://docs.readthedocs.io/en/latest/advertising/ad-blocking.html#allowing-ethical-ads">allowing our Ethical Ads in your ad blocker</a> or <a href="https://readthedocs.org/sustainability/">go ad-free</a> by subscribing.').appendTo(t), $("<p />").text("Thank you! ❤️").appendTo(t)))
                                }
                            })
                    }
                }
        },
        {
            "./constants": 14,
            "./rtd-data": 16,
            bowser: 7
        }],
        20: [function (e, t, i) {
            var o = e("./rtd-data");
            t.exports = {
                init: function (e) {
                    var t = o.get();
                    if (!e.is_highest) {
                        var i = window.location.pathname.replace(t.version, e.slug),
                            r = $('<div class="admonition warning"> <p class="first admonition-title">Note</p> <p class="last"> You are not reading the most recent version of this documentation. <a href="#"></a> is the latest version available.</p></div>');
                        r.find("a").attr("href", i).text(e.slug);
                        var n = $("div.body");
                        n.length || (n = $("div.document")),
                            n.prepend(r)
                    }
                }
            }
        },
        {
            "./rtd-data": 16
        }],
        21: [function (e, t, i) {
            var r = e("./doc-embed/sponsorship"),
                n = e("./doc-embed/footer.js"),
                o = (e("./doc-embed/rtd-data"), e("./doc-embed/sphinx")),
                a = e("./doc-embed/search");
            $.extend(e("verge")),
                $(document).ready(function () {
                    n.init(),
                        o.init(),
                        a.init(),
                        r.init()
                })
        },
        {
            "./doc-embed/footer.js": 15,
            "./doc-embed/rtd-data": 16,
            "./doc-embed/search": 17,
            "./doc-embed/sphinx": 18,
            "./doc-embed/sponsorship": 19,
            verge: 13
        }]
    },
        {},
        [21]);