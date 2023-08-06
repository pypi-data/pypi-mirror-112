import { __assign, __extends } from "tslib";
import * as React from 'react';
import { getProjectRelease, getReleaseDeploys } from 'app/actionCreators/release';
import ReleaseStore from 'app/stores/releaseStore';
import getDisplayName from 'app/utils/getDisplayName';
function withRelease(WrappedComponent) {
    var WithRelease = /** @class */ (function (_super) {
        __extends(WithRelease, _super);
        function WithRelease(props, context) {
            var _this = _super.call(this, props, context) || this;
            _this.unsubscribe = ReleaseStore.listen(function () { return _this.onStoreUpdate(); }, undefined);
            var _a = _this.props, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            _this.state = __assign({}, releaseData);
            return _this;
        }
        WithRelease.prototype.componentDidMount = function () {
            this.fetchRelease();
            this.fetchDeploys();
        };
        WithRelease.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithRelease.prototype.fetchRelease = function () {
            var _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            var orgSlug = organization.slug;
            if ((!releaseData.release && !releaseData.releaseLoading) ||
                releaseData.releaseError) {
                getProjectRelease(api, { orgSlug: orgSlug, projectSlug: projectSlug, releaseVersion: releaseVersion });
            }
        };
        WithRelease.prototype.fetchDeploys = function () {
            var _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            var orgSlug = organization.slug;
            if ((!releaseData.deploys && !releaseData.deploysLoading) ||
                releaseData.deploysError) {
                getReleaseDeploys(api, { orgSlug: orgSlug, projectSlug: projectSlug, releaseVersion: releaseVersion });
            }
        };
        WithRelease.prototype.onStoreUpdate = function () {
            var _a = this.props, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            this.setState(__assign({}, releaseData));
        };
        WithRelease.prototype.render = function () {
            return (<WrappedComponent {...this.props} {...this.state}/>);
        };
        WithRelease.displayName = "withRelease(" + getDisplayName(WrappedComponent) + ")";
        return WithRelease;
    }(React.Component));
    return WithRelease;
}
export default withRelease;
//# sourceMappingURL=withRelease.jsx.map