import { __assign, __extends, __rest } from "tslib";
import * as React from 'react';
import SentryAppComponentsStore from 'app/stores/sentryAppComponentsStore';
import getDisplayName from 'app/utils/getDisplayName';
function withSentryAppComponents(WrappedComponent, _a) {
    var _b = _a === void 0 ? {} : _a, componentType = _b.componentType;
    var WithSentryAppComponents = /** @class */ (function (_super) {
        __extends(WithSentryAppComponents, _super);
        function WithSentryAppComponents() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { components: SentryAppComponentsStore.getAll() };
            _this.unsubscribe = SentryAppComponentsStore.listen(function () { return _this.setState({ components: SentryAppComponentsStore.getAll() }); }, undefined);
            return _this;
        }
        WithSentryAppComponents.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithSentryAppComponents.prototype.render = function () {
            var _a = this.props, components = _a.components, props = __rest(_a, ["components"]);
            return (<WrappedComponent {...__assign({ components: components !== null && components !== void 0 ? components : SentryAppComponentsStore.getComponentByType(componentType) }, props)}/>);
        };
        WithSentryAppComponents.displayName = "withSentryAppComponents(" + getDisplayName(WrappedComponent) + ")";
        return WithSentryAppComponents;
    }(React.Component));
    return WithSentryAppComponents;
}
export default withSentryAppComponents;
//# sourceMappingURL=withSentryAppComponents.jsx.map