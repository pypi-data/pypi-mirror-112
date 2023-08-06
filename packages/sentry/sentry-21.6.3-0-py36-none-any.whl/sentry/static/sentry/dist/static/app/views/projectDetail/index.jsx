import * as React from 'react';
import withOrganization from 'app/utils/withOrganization';
import ProjectDetail from './projectDetail';
function ProjectDetailContainer(props) {
    return <ProjectDetail {...props}/>;
}
export default withOrganization(ProjectDetailContainer);
//# sourceMappingURL=index.jsx.map