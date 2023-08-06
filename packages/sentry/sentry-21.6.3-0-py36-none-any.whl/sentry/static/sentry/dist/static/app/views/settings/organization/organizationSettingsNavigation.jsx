import { __extends } from "tslib";
import * as React from 'react';
import HookStore from 'app/stores/hookStore';
import withOrganization from 'app/utils/withOrganization';
import SettingsNavigation from 'app/views/settings/components/settingsNavigation';
import navigationConfiguration from 'app/views/settings/organization/navigationConfiguration';
var OrganizationSettingsNavigation = /** @class */ (function (_super) {
    __extends(OrganizationSettingsNavigation, _super);
    function OrganizationSettingsNavigation() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getHooks();
        /**
         * TODO(epurkhiser): Becase the settings organization navigation hooks
         * do not conform to a normal component style hook, and take a single
         * parameter 'organization', we cannot use the `Hook` component here,
         * and must resort to using listening to the HookStore to retrieve hook data.
         *
         * We should update the hook interface for the two hooks used here
         */
        _this.unsubscribe = HookStore.listen(function (hookName, hooks) {
            _this.handleHooks(hookName, hooks);
        }, undefined);
        return _this;
    }
    OrganizationSettingsNavigation.prototype.componentDidMount = function () {
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState(this.getHooks());
    };
    OrganizationSettingsNavigation.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    OrganizationSettingsNavigation.prototype.getHooks = function () {
        // Allow injection via getsentry et all
        var organization = this.props.organization;
        return {
            hookConfigs: HookStore.get('settings:organization-navigation-config').map(function (cb) {
                return cb(organization);
            }),
            hooks: HookStore.get('settings:organization-navigation').map(function (cb) {
                return cb(organization);
            }),
        };
    };
    OrganizationSettingsNavigation.prototype.handleHooks = function (name, hooks) {
        var org = this.props.organization;
        if (name !== 'settings:organization-navigation-config') {
            return;
        }
        this.setState({ hookConfigs: hooks.map(function (cb) { return cb(org); }) });
    };
    OrganizationSettingsNavigation.prototype.render = function () {
        var _a = this.state, hooks = _a.hooks, hookConfigs = _a.hookConfigs;
        var organization = this.props.organization;
        var access = new Set(organization.access);
        var features = new Set(organization.features);
        return (<SettingsNavigation navigationObjects={navigationConfiguration} access={access} features={features} organization={organization} hooks={hooks} hookConfigs={hookConfigs}/>);
    };
    return OrganizationSettingsNavigation;
}(React.Component));
export default withOrganization(OrganizationSettingsNavigation);
//# sourceMappingURL=organizationSettingsNavigation.jsx.map