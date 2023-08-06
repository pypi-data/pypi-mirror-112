export function createListeners(type) {
    var eventTarget = type === 'window' ? window : document;
    var listeners = [];
    var handler = function (eventData, event) {
        var _a, _b, _c, _d;
        var filteredListeners = listeners.filter(function (listener) {
            return listener.hasOwnProperty(event);
        });
        if ((eventData === null || eventData === void 0 ? void 0 : eventData.key) === 'Escape') {
            return (_b = (_a = filteredListeners[1]) === null || _a === void 0 ? void 0 : _a[event]) === null || _b === void 0 ? void 0 : _b.call(_a, eventData);
        }
        return (_d = (_c = filteredListeners[0]) === null || _c === void 0 ? void 0 : _c[event]) === null || _d === void 0 ? void 0 : _d.call(_c, eventData);
    };
    eventTarget.addEventListener = jest.fn(function (event, cb) {
        var _a;
        listeners.push((_a = {},
            _a[event] = cb,
            _a));
    });
    eventTarget.removeEventListener = jest.fn(function (event) {
        listeners = listeners.filter(function (listener) { return !listener.hasOwnProperty(event); });
    });
    return {
        mouseDown: function (domEl) { return handler({ target: domEl }, 'mousedown'); },
        keyDown: function (key) { return handler({ key: key }, 'keydown'); },
    };
}
//# sourceMappingURL=createListeners.jsx.map