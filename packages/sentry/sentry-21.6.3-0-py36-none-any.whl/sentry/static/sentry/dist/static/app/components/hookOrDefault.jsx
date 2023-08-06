import { __extends } from "tslib";
import * as React from 'react';
import HookStore from 'app/stores/hookStore';
/**
 * Use this instead of the usual ternery operator when using getsentry hooks.
 * So in lieu of:
 *
 *  HookStore.get('component:org-auth-view').length
 *   ? HookStore.get('component:org-auth-view')[0]()
 *   : OrganizationAuth
 *
 * do this instead:
 *
 *   const HookedOrganizationAuth = HookOrDefault({
 *     hookName:'component:org-auth-view',
 *     defaultComponent: OrganizationAuth,
 *   })
 *
 * Note, you will need to add the hookstore function in getsentry [0] first and
 * then register the types [2] and validHookName [1] in sentry.
 *
 * [0] /getsentry/static/getsentry/gsApp/registerHooks.jsx
 * [1] /sentry/app/stores/hookStore.tsx
 * [2] /sentry/app/types/hooks.ts
 */
function HookOrDefault(_a) {
    var hookName = _a.hookName, defaultComponent = _a.defaultComponent, defaultComponentPromise = _a.defaultComponentPromise;
    var HookOrDefaultComponent = /** @class */ (function (_super) {
        __extends(HookOrDefaultComponent, _super);
        function HookOrDefaultComponent() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                hooks: HookStore.get(hookName),
            };
            _this.unlistener = HookStore.listen(function (name, hooks) {
                return name === hookName && _this.setState({ hooks: hooks });
            }, undefined);
            return _this;
        }
        HookOrDefaultComponent.prototype.componentWillUnmount = function () {
            var _a;
            (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
        };
        Object.defineProperty(HookOrDefaultComponent.prototype, "defaultComponent", {
            get: function () {
                // If `defaultComponentPromise` is passed, then return a Suspended component
                if (defaultComponentPromise) {
                    var Component_1 = React.lazy(defaultComponentPromise);
                    return function (props) { return (<React.Suspense fallback={null}>
            <Component_1 {...props}/>
          </React.Suspense>); };
                }
                return defaultComponent;
            },
            enumerable: false,
            configurable: true
        });
        HookOrDefaultComponent.prototype.render = function () {
            var _a, _b;
            var hookExists = this.state.hooks && this.state.hooks.length;
            var componentFromHook = (_b = (_a = this.state.hooks)[0]) === null || _b === void 0 ? void 0 : _b.call(_a);
            var HookComponent = hookExists && componentFromHook ? componentFromHook : this.defaultComponent;
            return HookComponent ? <HookComponent {...this.props}/> : null;
        };
        HookOrDefaultComponent.displayName = "HookOrDefaultComponent(" + hookName + ")";
        return HookOrDefaultComponent;
    }(React.Component));
    return HookOrDefaultComponent;
}
export default HookOrDefault;
//# sourceMappingURL=hookOrDefault.jsx.map