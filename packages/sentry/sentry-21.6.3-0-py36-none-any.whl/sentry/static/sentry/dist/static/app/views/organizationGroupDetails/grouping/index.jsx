import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import withOrganization from 'app/utils/withOrganization';
import Grouping from './grouping';
function GroupingContainer(_a) {
    var organization = _a.organization, params = _a.params, location = _a.location, router = _a.router;
    return (<Feature features={['grouping-tree-ui']} organization={organization} renderDisabled={function () { return (<PageContent>
          <Alert type="warning">{t("You don't have access to this feature")}</Alert>
        </PageContent>); }}>
      <Grouping location={location} groupId={params.groupId} organization={organization} router={router}/>
    </Feature>);
}
export default withOrganization(GroupingContainer);
//# sourceMappingURL=index.jsx.map