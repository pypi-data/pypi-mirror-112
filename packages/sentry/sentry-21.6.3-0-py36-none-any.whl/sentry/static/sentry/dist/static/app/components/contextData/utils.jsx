export function looksLikeObjectRepr(value) {
    var a = value[0];
    var z = value[value.length - 1];
    if (a === '<' && z === '>') {
        return true;
    }
    if (a === '[' && z === ']') {
        return true;
    }
    if (a === '(' && z === ')') {
        return true;
    }
    if (z === ')' && value.match(/^[\w\d._-]+\(/)) {
        return true;
    }
    return false;
}
export function looksLikeMultiLineString(value) {
    return !!value.match(/[\r\n]/);
}
export function padNumbersInString(string) {
    return string.replace(/(\d+)/g, function (num) {
        var isNegative = false;
        var realNum = parseInt(num, 10);
        if (realNum < 0) {
            realNum *= -1;
            isNegative = true;
        }
        var s = '0000000000000' + realNum;
        s = s.substr(s.length - (isNegative ? 11 : 12));
        if (isNegative) {
            s = '-' + s;
        }
        return s;
    });
}
export function naturalCaseInsensitiveSort(a, b) {
    a = padNumbersInString(a).toLowerCase();
    b = padNumbersInString(b).toLowerCase();
    return a === b ? 0 : a < b ? -1 : 1;
}
export function analyzeStringForRepr(value) {
    var rv = {
        repr: value,
        isString: true,
        isMultiLine: false,
        isStripped: false,
    };
    // stripped for security reasons
    if (value.match(/^['"]?\*{8,}['"]?$/)) {
        rv.isStripped = true;
        return rv;
    }
    if (looksLikeObjectRepr(value)) {
        rv.isString = false;
        return rv;
    }
    rv.isMultiLine = looksLikeMultiLineString(value);
    return rv;
}
//# sourceMappingURL=utils.jsx.map