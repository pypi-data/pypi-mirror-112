import { __assign, __extends } from "tslib";
import * as React from 'react';
import { getCommitters } from 'app/actionCreators/committers';
import CommitterStore from 'app/stores/committerStore';
import getDisplayName from 'app/utils/getDisplayName';
var initialState = {
    committers: [],
};
function withCommitters(WrappedComponent) {
    var WithCommitters = /** @class */ (function (_super) {
        __extends(WithCommitters, _super);
        function WithCommitters(props, context) {
            var _this = _super.call(this, props, context) || this;
            _this.unsubscribe = CommitterStore.listen(function () { return _this.onStoreUpdate(); }, undefined);
            var _a = _this.props, organization = _a.organization, project = _a.project, event = _a.event;
            var repoData = CommitterStore.get(organization.slug, project.slug, event.id);
            _this.state = __assign(__assign({}, initialState), repoData);
            return _this;
        }
        WithCommitters.prototype.componentDidMount = function () {
            var group = this.props.group;
            // No committers if group doesn't have any releases
            if (!!(group === null || group === void 0 ? void 0 : group.firstRelease)) {
                this.fetchCommitters();
            }
        };
        WithCommitters.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithCommitters.prototype.fetchCommitters = function () {
            var _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, event = _a.event;
            var repoData = CommitterStore.get(organization.slug, project.slug, event.id);
            if ((!repoData.committers && !repoData.committersLoading) ||
                repoData.committersError) {
                getCommitters(api, {
                    orgSlug: organization.slug,
                    projectSlug: project.slug,
                    eventId: event.id,
                });
            }
        };
        WithCommitters.prototype.onStoreUpdate = function () {
            var _a = this.props, organization = _a.organization, project = _a.project, event = _a.event;
            var repoData = CommitterStore.get(organization.slug, project.slug, event.id);
            this.setState({ committers: repoData.committers });
        };
        WithCommitters.prototype.render = function () {
            var _a = this.state.committers, committers = _a === void 0 ? [] : _a;
            // XXX: We do not pass loading/error states because the components using
            // this HOC (suggestedOwners, eventCause) do not have loading/error states
            return (<WrappedComponent {...this.props} committers={committers}/>);
        };
        WithCommitters.displayName = "withCommitters(" + getDisplayName(WrappedComponent) + ")";
        return WithCommitters;
    }(React.Component));
    return WithCommitters;
}
export default withCommitters;
//# sourceMappingURL=withCommitters.jsx.map