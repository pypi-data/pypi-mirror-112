var hasEventListener = false;
var queued = [];
function onDomContentLoaded() {
    var _a;
    if (!queued.length) {
        return;
    }
    while (queued.length) {
        (_a = queued.pop()) === null || _a === void 0 ? void 0 : _a();
    }
    // We can remove this listener immediately since `DOMContentLoaded` should only be fired once
    document.removeEventListener('DOMContentLoaded', onDomContentLoaded);
    hasEventListener = false;
}
export function renderOnDomReady(renderFn) {
    if (document.readyState !== 'loading') {
        renderFn();
        return;
    }
    queued.push(renderFn);
    if (!hasEventListener) {
        document.addEventListener('DOMContentLoaded', onDomContentLoaded);
        hasEventListener = true;
    }
}
//# sourceMappingURL=renderOnDomReady.jsx.map