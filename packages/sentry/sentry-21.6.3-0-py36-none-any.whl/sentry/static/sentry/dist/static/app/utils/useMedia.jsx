import { __read } from "tslib";
import { useEffect, useState } from 'react';
/**
 * Hook that updates when a media query result changes
 */
export default function useMedia(query) {
    if (!window.matchMedia) {
        return false;
    }
    var _a = __read(useState(function () { return window.matchMedia(query).matches; }), 2), state = _a[0], setState = _a[1];
    useEffect(function () {
        var mounted = true;
        var mql = window.matchMedia(query);
        var onChange = function () {
            if (!mounted) {
                return;
            }
            setState(!!mql.matches);
        };
        mql.addListener(onChange);
        setState(mql.matches);
        return function () {
            mounted = false;
            mql.removeListener(onChange);
        };
    }, [query]);
    return state;
}
//# sourceMappingURL=useMedia.jsx.map