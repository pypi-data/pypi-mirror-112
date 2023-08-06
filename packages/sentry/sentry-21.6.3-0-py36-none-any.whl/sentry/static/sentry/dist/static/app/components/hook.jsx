import { __extends, __rest } from "tslib";
import * as React from 'react';
import HookStore from 'app/stores/hookStore';
/**
 * Instead of accessing the HookStore directly, use this.
 *
 * If the hook slot needs to perform anything w/ the hooks, you can pass a
 * function as a child and you will receive an object with a `hooks` key
 *
 * Example:
 *
 *   <Hook name="my-hook">
 *     {({hooks}) => hooks.map(hook => (
 *       <Wrapper>{hook}</Wrapper>
 *     ))}
 *   </Hook>
 */
function Hook(_a) {
    var name = _a.name, props = __rest(_a, ["name"]);
    var HookComponent = /** @class */ (function (_super) {
        __extends(HookComponent, _super);
        function HookComponent() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                hooks: HookStore.get(name).map(function (cb) { return cb(props); }),
            };
            _this.unsubscribe = HookStore.listen(function (hookName, hooks) { return _this.handleHooks(hookName, hooks); }, undefined);
            return _this;
        }
        HookComponent.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        HookComponent.prototype.handleHooks = function (hookName, hooks) {
            // Make sure that the incoming hook update matches this component's hook name
            if (hookName !== name) {
                return;
            }
            this.setState({ hooks: hooks.map(function (cb) { return cb(props); }) });
        };
        HookComponent.prototype.render = function () {
            var children = props.children;
            if (!this.state.hooks || !this.state.hooks.length) {
                return null;
            }
            if (typeof children === 'function') {
                return children({ hooks: this.state.hooks });
            }
            return this.state.hooks;
        };
        HookComponent.displayName = "Hook(" + name + ")";
        return HookComponent;
    }(React.Component));
    return <HookComponent />;
}
export default Hook;
//# sourceMappingURL=hook.jsx.map