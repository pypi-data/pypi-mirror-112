import { __rest } from "tslib";
import * as AppStoreConnectContext from 'app/components/projects/appStoreConnectContext';
import UpdateAlert from './updateAlert';
function GlobalAppStoreConnectUpdateAlert(_a) {
    var project = _a.project, organization = _a.organization, rest = __rest(_a, ["project", "organization"]);
    return (<AppStoreConnectContext.Provider project={project} organization={organization}>
      <UpdateAlert project={project} organization={organization} {...rest}/>
    </AppStoreConnectContext.Provider>);
}
export default GlobalAppStoreConnectUpdateAlert;
//# sourceMappingURL=index.jsx.map