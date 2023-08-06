import { __assign } from "tslib";
import EditableText from 'app/components/editableText';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
function DashboardTitle(_a) {
    var dashboard = _a.dashboard, isEditing = _a.isEditing, organization = _a.organization, onUpdate = _a.onUpdate;
    return (<div>
      {!dashboard ? (t('Dashboards')) : (<EditableText isDisabled={!isEditing} value={organization.features.includes('dashboards-edit') &&
                dashboard.id === 'default-overview'
                ? 'Default Dashboard'
                : dashboard.title} onChange={function (newTitle) { return onUpdate(__assign(__assign({}, dashboard), { title: newTitle })); }} errorMessage={t('Please set a title for this dashboard')} successMessage={t('Dashboard title updated successfully')}/>)}
    </div>);
}
export default withOrganization(DashboardTitle);
//# sourceMappingURL=title.jsx.map