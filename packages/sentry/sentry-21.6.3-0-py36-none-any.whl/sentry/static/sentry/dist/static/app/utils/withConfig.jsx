import { __assign, __extends, __rest } from "tslib";
import * as React from 'react';
import ConfigStore from 'app/stores/configStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Higher order component that passes the config object to the wrapped component
 */
function withConfig(WrappedComponent) {
    var WithConfig = /** @class */ (function (_super) {
        __extends(WithConfig, _super);
        function WithConfig() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { config: ConfigStore.getConfig() };
            _this.unsubscribe = ConfigStore.listen(function () { return _this.setState({ config: ConfigStore.getConfig() }); }, undefined);
            return _this;
        }
        WithConfig.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithConfig.prototype.render = function () {
            var _a = this.props, config = _a.config, props = __rest(_a, ["config"]);
            return (<WrappedComponent {...__assign({ config: config !== null && config !== void 0 ? config : this.state.config }, props)}/>);
        };
        WithConfig.displayName = "withConfig(" + getDisplayName(WrappedComponent) + ")";
        return WithConfig;
    }(React.Component));
    return WithConfig;
}
export default withConfig;
//# sourceMappingURL=withConfig.jsx.map