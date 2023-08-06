import { __extends } from "tslib";
import { Component } from 'react';
import withOrganization from 'app/utils/withOrganization';
import ProjectProguard from './projectProguard';
var ProjectProguardContainer = /** @class */ (function (_super) {
    __extends(ProjectProguardContainer, _super);
    function ProjectProguardContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectProguardContainer.prototype.render = function () {
        return <ProjectProguard {...this.props}/>;
    };
    return ProjectProguardContainer;
}(Component));
export default withOrganization(ProjectProguardContainer);
//# sourceMappingURL=index.jsx.map