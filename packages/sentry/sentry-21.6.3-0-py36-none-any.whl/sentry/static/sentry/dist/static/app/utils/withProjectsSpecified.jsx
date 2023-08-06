import { __extends } from "tslib";
import * as React from 'react';
import isEqual from 'lodash/isEqual';
import ProjectsStore from 'app/stores/projectsStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Higher order component that takes specificProjectSlugs and provides list of that projects from ProjectsStore
 */
function withProjectsSpecified(WrappedComponent) {
    var WithProjectsSpecified = /** @class */ (function (_super) {
        __extends(WithProjectsSpecified, _super);
        function WithProjectsSpecified() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = ProjectsStore.getState(_this.props.specificProjectSlugs);
            _this.unsubscribe = ProjectsStore.listen(function () {
                var storeState = ProjectsStore.getState(_this.props.specificProjectSlugs);
                if (!isEqual(_this.state, storeState)) {
                    _this.setState(storeState);
                }
            }, undefined);
            return _this;
        }
        WithProjectsSpecified.getDerivedStateFromProps = function (nextProps) {
            return ProjectsStore.getState(nextProps.specificProjectSlugs);
        };
        WithProjectsSpecified.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithProjectsSpecified.prototype.render = function () {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        };
        WithProjectsSpecified.displayName = "withProjectsSpecified(" + getDisplayName(WrappedComponent) + ")";
        return WithProjectsSpecified;
    }(React.Component));
    return WithProjectsSpecified;
}
export default withProjectsSpecified;
//# sourceMappingURL=withProjectsSpecified.jsx.map