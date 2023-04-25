var md5 = require("md5");

for (var _0xeb6638 = {
        boe: !1,
        aid: 0,
        dfp: !1,
        sdi: !1,
        enablePathList: [],
        _enablePathListRegex: [],
        urlRewriteRules: [],
        _urlRewriteRules: [],
        initialized: !1,
        enableTrack: !1,
        track: {
            unitTime: 0,
            unitAmount: 0,
            fre: 0
        },
        triggerUnload: !1,
        region: "",
        regionConf: {},
        umode: 0,
        v: !1,
        _enableSignature: [],
        perf: !1,
        xxbg: !0
    },  _0x5b3b1e = "0123456789abcdef".split(""), _0x1aef18 = [], _0x19ae48 = [], _0x52eb4c = 0; _0x52eb4c < 256; _0x52eb4c++) {
        _0x1aef18[_0x52eb4c] = _0x5b3b1e[_0x52eb4c >> 4 & 15] + _0x5b3b1e[15 & _0x52eb4c],
        _0x52eb4c < 16 && (_0x52eb4c < 10 ? _0x19ae48[48 + _0x52eb4c] = _0x52eb4c : _0x19ae48[87 + _0x52eb4c] = _0x52eb4c);
    }

_0x1f3b8d = function(a) {
        for (var b = a.length >> 1, c = b << 1, e = new Uint8Array(b), d = 0, t = 0; t < c; ) {
            e[d++] = _0x19ae48[a.charCodeAt(t++)] << 4 | _0x19ae48[a.charCodeAt(t++)];
        }
        return e;
};

function _0x2f2740(a, c, e, b, d, f, t, n, o, i, r, _, x, u, s, l, v, h, g) {
    let w = new Uint8Array(19);
    return w[0] = a,
    w[1] = r,
    w[2] = c,
    w[3] = _,
    w[4] = e,
    w[5] = x,
    w[6] = b,
    w[7] = u,
    w[8] = d,
    w[9] = s,
    w[10] = f,
    w[11] = l,
    w[12] = t,
    w[13] = v,
    w[14] = n,
    w[15] = h,
    w[16] = o,
    w[17] = g,
    w[18] = i,
    String.fromCharCode.apply(null, w);
}

function _0x46fa4c(a, c) {
    let e, b = [], d = 0, f = "";
    for (let a = 0; a < 256; a++) {
        b[a] = a;
    }
    for (let c = 0; c < 256; c++) {
        d = (d + b[c] + a.charCodeAt(c % a.length)) % 256,
        e = b[c],
        b[c] = b[d],
        b[d] = e;
    }
    let t = 0;
    d = 0;
    for (let a = 0; a < c.length; a++) {
        t = (t + 1) % 256,
        d = (d + b[t]) % 256,
        e = b[t],
        b[t] = b[d],
        b[d] = e,
        f += String.fromCharCode(c.charCodeAt(a) ^ b[(b[t] + b[d]) % 256]);
    }
    return f;
}

function _0x2b6720(a, c, e) {
    return String.fromCharCode(a) + String.fromCharCode(c) + e;
}


function get_array(originalString, str_1, str_2, str_3, str_4, str_5) {
    var array1 = _0x1f3b8d(md5(_0x1f3b8d(md5(originalString))));
    var fixedString1 = new Date().getTime()/1000;
    // var fixedString1 = 1675414283.44;
    // var fixedString2 = 536919696;
    var fixedString2 = str_1;
    // var fixedString2 = 1978764126;
    // var axm= [64,0.00390625,1,8,array1[14],array1[15],69,63,168,215,fixedString1>>24&255,fixedString1>>16&255,fixedString1>>8&255,fixedString1>>0&255,fixedString2>>24&255,fixedString2>>16&255,fixedString2>>8&255,fixedString2>>0&255];
    // var axm= [64,0.00390625,1,8,array1[14],array1[15],69,63,16,83,fixedString1>>24&255,fixedString1>>16&255,fixedString1>>8&255,fixedString1>>0&255,fixedString2>>24&255,fixedString2>>16&255,fixedString2>>8&255,fixedString2>>0&255];
    // var axm= [64,0.00390625,1,8,array1[14],array1[15],69,63,16,83,fixedString1>>24&255,fixedString1>>16&255,fixedString1>>8&255,fixedString1>>0&255,fixedString2>>24&255,fixedString2>>16&255,fixedString2>>8&255,fixedString2>>0&255];
    // var axm= [64,0.00390625,1,14,array1[14],array1[15],69,63,224,26,fixedString1>>24&255,fixedString1>>16&255,fixedString1>>8&255,fixedString1>>0&255,fixedString2>>24&255,fixedString2>>16&255,fixedString2>>8&255,fixedString2>>0&255];
    var axm= [64,0.00390625,str_2,str_3,array1[14],array1[15],69,63,str_4,str_5,fixedString1>>24&255,fixedString1>>16&255,fixedString1>>8&255,fixedString1>>0&255,fixedString2>>24&255,fixedString2>>16&255,fixedString2>>8&255,fixedString2>>0&255];
    axm.push(axm.reduce(function(a, b) { return a ^ b;}));
    console.log(axm);
    console.log([axm[0],axm[2],axm[4],axm[6],axm[8],axm[10],axm[12],axm[14],axm[16],axm[18],axm[1],axm[3],axm[5],axm[7],axm[9],axm[11],axm[13],axm[15],axm[17]])
    return [axm[0],axm[2],axm[4],axm[6],axm[8],axm[10],axm[12],axm[14],axm[16],axm[18],axm[1],axm[3],axm[5],axm[7],axm[9],axm[11],axm[13],axm[15],axm[17]]
}

function getGarbledString(originalString, str_1, str_2, str_3, str_4, str_5) {
    var array2 = get_array(originalString, str_1, str_2, str_3, str_4, str_5);
    var u1 = _0x2f2740.apply(null,array2);
    var u2 = _0x46fa4c.apply(null,[String.fromCharCode(255),u1]);
    u = _0x2b6720.apply(null,[2,255,u2]);
    return u

}

function getXBogus(originalString, str_1, str_2, str_3, str_4, str_5){
    // 生成乱码字符串
    var garbledString = getGarbledString(originalString, str_1, str_2, str_3, str_4, str_5);
    // console.log(garbledString);
    var XBogus = "";
    // 依次生成七组字符串
    var short_str = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=";
    for (var i = 0; i <= 20; i += 3) {
        var charCodeAtNum0 = garbledString.charCodeAt(i);
        var charCodeAtNum1 = garbledString.charCodeAt(i + 1);
        var charCodeAtNum2 = garbledString.charCodeAt(i + 2);
        var baseNum = charCodeAtNum2 | charCodeAtNum1 << 8 | charCodeAtNum0 << 16;
        // 依次生成四个字符
        var str1 = short_str[(baseNum & 16515072) >> 18];
        var str2 = short_str[(baseNum & 258048) >> 12];
        var str3 = short_str[(baseNum & 4032) >> 6];
        var str4 = short_str[baseNum & 63];
        XBogus += str1 + str2 + str3 + str4;
    }
    return XBogus;
}


console.log(getXBogus("device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=MS4wLjABAAAA8U_l6rBzmy7bcy6xOJel4v0RzoR_wfAubGPeJimN__4&max_cursor=1674172954000&locate_query=false&show_live_replay_strategy=1&count=10&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=109.0.0.0&browser_online=true&engine_name=Blink&engine_version=109.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7195073751037232640&msToken=b3owtulT0h7opY9EE-JCKcXtZZxfg3JX0i-g4KcwoyPv2E-cR-YJMEX2ghDqwEwOlrWiNMAWc0k0ucNV1MiGJxOUrHscrPCWvpd7z_4i0YNNwxyiml0383htMZzg2w=="))