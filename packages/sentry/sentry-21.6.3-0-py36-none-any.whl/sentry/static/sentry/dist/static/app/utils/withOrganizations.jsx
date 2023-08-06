import { __assign, __extends, __rest } from "tslib";
import * as React from 'react';
import OrganizationsStore from 'app/stores/organizationsStore';
import getDisplayName from 'app/utils/getDisplayName';
function withOrganizations(WrappedComponent) {
    var WithOrganizations = /** @class */ (function (_super) {
        __extends(WithOrganizations, _super);
        function WithOrganizations() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { organizations: OrganizationsStore.getAll() };
            _this.unsubscribe = OrganizationsStore.listen(function (organizations) { return _this.setState({ organizations: organizations }); }, undefined);
            return _this;
        }
        WithOrganizations.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithOrganizations.prototype.render = function () {
            var _a = this.props, organizationsLoading = _a.organizationsLoading, organizations = _a.organizations, props = __rest(_a, ["organizationsLoading", "organizations"]);
            return (<WrappedComponent {...__assign({ organizationsLoading: organizationsLoading !== null && organizationsLoading !== void 0 ? organizationsLoading : !OrganizationsStore.loaded, organizations: organizations !== null && organizations !== void 0 ? organizations : this.state.organizations }, props)}/>);
        };
        WithOrganizations.displayName = "withOrganizations(" + getDisplayName(WrappedComponent) + ")";
        return WithOrganizations;
    }(React.Component));
    return WithOrganizations;
}
export default withOrganizations;
//# sourceMappingURL=withOrganizations.jsx.map