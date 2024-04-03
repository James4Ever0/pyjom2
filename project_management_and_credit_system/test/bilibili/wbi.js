function N(t, e) {
    e || (e = {});
    var n, r, o = function(t) {
        var e;
        if (t.useAssignKey)
            return {
                imgKey: t.wbiImgKey,
                subKey: t.wbiSubKey
            };
        var n = (null === (e = function(t) {
            try {
                return localStorage.getItem(t)
            } catch (t) {
                return null
            }
        }("wbi_img_urls")) || void 0 === e ? void 0 : e.split("-")) || []
          , r = n[0]
          , o = n[1]
          , i = r ? M(r) : t.wbiImgKey
          , a = o ? M(o) : t.wbiSubKey;
        return {
            imgKey: i,
            subKey: a
        }
    }(e), i = o.imgKey, a = o.subKey;
    if (i && a) {
        for (var c = (n = i + a,
        r = [],
        [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52].forEach((function(t) {
            n.charAt(t) && r.push(n.charAt(t))
        }
        )),
        r.join("").slice(0, 32)), u = Math.round(Date.now() / 1e3), s = Object.assign({}, t, {
            wts: u
        }), l = Object.keys(s).sort(), f = [], p = /[!'()*]/g, d = 0; d < l.length; d++) {
            var h = l[d]
              , v = s[h];
            v && "string" == typeof v && (v = v.replace(p, "")),
            null != v && f.push("".concat(encodeURIComponent(h), "=").concat(encodeURIComponent(v)))
        }
        var y = f.join("&");
        return {
            w_rid: I(y + c),
            wts: u.toString()
        }
    }
    return null
}
