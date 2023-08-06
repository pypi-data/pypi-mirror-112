import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import withOrganizations from 'app/utils/withOrganizations';
import { getParentData, getParentField, } from 'app/views/settings/account/notifications/utils';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
var NotificationSettingsByOrganization = /** @class */ (function (_super) {
    __extends(NotificationSettingsByOrganization, _super);
    function NotificationSettingsByOrganization() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NotificationSettingsByOrganization.prototype.render = function () {
        var _a = this.props, notificationType = _a.notificationType, notificationSettings = _a.notificationSettings, onChange = _a.onChange, organizations = _a.organizations;
        return (<Form saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={getParentData(notificationType, notificationSettings, organizations)}>
        <JsonForm title={t('Organizations')} fields={organizations.map(function (organization) {
                return getParentField(notificationType, notificationSettings, organization, onChange);
            })}/>
      </Form>);
    };
    return NotificationSettingsByOrganization;
}(React.Component));
export default withOrganizations(NotificationSettingsByOrganization);
//# sourceMappingURL=notificationSettingsByOrganization.jsx.map