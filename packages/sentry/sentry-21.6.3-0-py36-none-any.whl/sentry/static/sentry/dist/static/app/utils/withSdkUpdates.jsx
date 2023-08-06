import { __extends } from "tslib";
import * as React from 'react';
import { loadSdkUpdates } from 'app/actionCreators/sdkUpdates';
import SdkUpdatesStore from 'app/stores/sdkUpdatesStore';
import withApi from './withApi';
import withOrganization from './withOrganization';
function withSdkUpdates(WrappedComponent) {
    var WithProjectSdkSuggestions = /** @class */ (function (_super) {
        __extends(WithProjectSdkSuggestions, _super);
        function WithProjectSdkSuggestions() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { sdkUpdates: [] };
            _this.unsubscribe = SdkUpdatesStore.listen(function () { return _this.onSdkUpdatesUpdate(); }, undefined);
            return _this;
        }
        WithProjectSdkSuggestions.prototype.componentDidMount = function () {
            var orgSlug = this.props.organization.slug;
            var updates = SdkUpdatesStore.getUpdates(orgSlug);
            // Load SdkUpdates
            if (updates !== undefined) {
                this.onSdkUpdatesUpdate();
                return;
            }
            loadSdkUpdates(this.props.api, orgSlug);
        };
        WithProjectSdkSuggestions.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithProjectSdkSuggestions.prototype.onSdkUpdatesUpdate = function () {
            var _a;
            var sdkUpdates = (_a = SdkUpdatesStore.getUpdates(this.props.organization.slug)) !== null && _a !== void 0 ? _a : null;
            this.setState({ sdkUpdates: sdkUpdates });
        };
        WithProjectSdkSuggestions.prototype.render = function () {
            // TODO(ts) This unknown cast isn't great but Typescript complains about arbitrary
            // types being possible. I think this is related to the additional HoC wrappers causing type data to
            // be lost.
            return (<WrappedComponent {...this.props} sdkUpdates={this.state.sdkUpdates}/>);
        };
        return WithProjectSdkSuggestions;
    }(React.Component));
    return withOrganization(withApi(WithProjectSdkSuggestions));
}
export default withSdkUpdates;
//# sourceMappingURL=withSdkUpdates.jsx.map