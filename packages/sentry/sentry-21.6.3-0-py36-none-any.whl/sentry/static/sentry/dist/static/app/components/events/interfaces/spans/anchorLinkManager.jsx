import { __extends } from "tslib";
import React from 'react';
var AnchorLinkManagerContext = React.createContext({
    registerScrollFn: function () { return function () { return undefined; }; },
    scrollToHash: function () { return undefined; },
});
var Provider = /** @class */ (function (_super) {
    __extends(Provider, _super);
    function Provider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.scrollFns = new Map();
        _this.scrollToHash = function (hash) {
            var _a;
            (_a = _this.scrollFns.get(hash)) === null || _a === void 0 ? void 0 : _a();
        };
        _this.registerScrollFn = function (hash, fn) {
            _this.scrollFns.set(hash, fn);
        };
        return _this;
    }
    Provider.prototype.componentDidMount = function () {
        this.scrollToHash(location.hash);
    };
    Provider.prototype.render = function () {
        var childrenProps = {
            registerScrollFn: this.registerScrollFn,
            scrollToHash: this.scrollToHash,
        };
        return (<AnchorLinkManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </AnchorLinkManagerContext.Provider>);
    };
    return Provider;
}(React.Component));
export { Provider };
export var Consumer = AnchorLinkManagerContext.Consumer;
//# sourceMappingURL=anchorLinkManager.jsx.map