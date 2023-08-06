import { __extends } from "tslib";
import * as React from 'react';
import ProjectsStore from 'app/stores/projectsStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Higher order component that uses ProjectsStore and provides a list of projects
 */
function withProjects(WrappedComponent) {
    var WithProjects = /** @class */ (function (_super) {
        __extends(WithProjects, _super);
        function WithProjects() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = ProjectsStore.getState();
            _this.unsubscribe = ProjectsStore.listen(function () { return _this.setState(ProjectsStore.getState()); }, undefined);
            return _this;
        }
        WithProjects.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithProjects.prototype.render = function () {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        };
        WithProjects.displayName = "withProjects(" + getDisplayName(WrappedComponent) + ")";
        return WithProjects;
    }(React.Component));
    return WithProjects;
}
export default withProjects;
//# sourceMappingURL=withProjects.jsx.map