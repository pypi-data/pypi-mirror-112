import { __extends } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import withOrganization from 'app/utils/withOrganization';
import ProjectPerformance from './projectPerformance';
var ProjectPerformanceContainer = /** @class */ (function (_super) {
    __extends(ProjectPerformanceContainer, _super);
    function ProjectPerformanceContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectPerformanceContainer.prototype.render = function () {
        return (<Feature features={['project-transaction-threshold']}>
        <ProjectPerformance {...this.props}/>
      </Feature>);
    };
    return ProjectPerformanceContainer;
}(React.Component));
export default withOrganization(ProjectPerformanceContainer);
//# sourceMappingURL=index.jsx.map