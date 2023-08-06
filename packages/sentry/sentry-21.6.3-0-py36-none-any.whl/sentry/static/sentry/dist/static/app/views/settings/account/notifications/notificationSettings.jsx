import { __assign, __extends } from "tslib";
import React from 'react';
import AlertLink from 'app/components/alertLink';
import AsyncComponent from 'app/components/asyncComponent';
import Link from 'app/components/links/link';
import { IconMail } from 'app/icons';
import { t } from 'app/locale';
import { NOTIFICATION_SETTINGS_TYPES, SELF_NOTIFICATION_SETTINGS_TYPES, } from 'app/views/settings/account/notifications/constants';
import FeedbackAlert from 'app/views/settings/account/notifications/feedbackAlert';
import { NOTIFICATION_SETTING_FIELDS } from 'app/views/settings/account/notifications/fields2';
import { decideDefault, getParentIds, getStateToPutForDefault, mergeNotificationSettings, } from 'app/views/settings/account/notifications/utils';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var NotificationSettings = /** @class */ (function (_super) {
    __extends(NotificationSettings, _super);
    function NotificationSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getStateToPutForDefault = function (changedData, notificationType) {
            /**
             * Update the current providers' parent-independent notification settings
             * with the new value. If the new value is "never", then also update all
             * parent-specific notification settings to "default". If the previous value
             * was "never", then assume providerList should be "email" only.
             */
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = getStateToPutForDefault(notificationType, notificationSettings, changedData, getParentIds(notificationType, notificationSettings));
            _this.setState({
                notificationSettings: mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        return _this;
    }
    NotificationSettings.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { notificationSettings: {}, legacyData: {} });
    };
    NotificationSettings.prototype.getEndpoints = function () {
        return [
            ['notificationSettings', "/users/me/notification-settings/"],
            ['legacyData', '/users/me/notifications/'],
        ];
    };
    NotificationSettings.prototype.getInitialData = function () {
        var notificationSettings = this.state.notificationSettings;
        return Object.fromEntries(NOTIFICATION_SETTINGS_TYPES.map(function (notificationType) { return [
            notificationType,
            decideDefault(notificationType, notificationSettings),
        ]; }));
    };
    NotificationSettings.prototype.getFields = function () {
        var _this = this;
        return NOTIFICATION_SETTINGS_TYPES.map(function (notificationType) {
            return Object.assign({}, NOTIFICATION_SETTING_FIELDS[notificationType], {
                getData: function (data) { return _this.getStateToPutForDefault(data, notificationType); },
                help: (<React.Fragment>
              {NOTIFICATION_SETTING_FIELDS[notificationType].help}
              &nbsp;
              <Link to={"/settings/account/notifications/" + notificationType}>
                Fine tune
              </Link>
            </React.Fragment>),
            });
        });
    };
    NotificationSettings.prototype.renderBody = function () {
        var legacyData = this.state.legacyData;
        return (<React.Fragment>
        <SettingsPageHeader title="Notifications"/>
        <TextBlock>Control alerts that you receive.</TextBlock>
        <FeedbackAlert />
        <Form saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={this.getInitialData()}>
          <JsonForm title={t('Notifications')} fields={this.getFields()}/>
        </Form>
        <Form initialData={legacyData} saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/">
          <JsonForm title={t('My Activity')} fields={SELF_NOTIFICATION_SETTINGS_TYPES.map(function (type) { return NOTIFICATION_SETTING_FIELDS[type]; })}/>
        </Form>
        <AlertLink to="/settings/account/emails" icon={<IconMail />}>
          {t('Looking to add or remove an email address? Use the emails panel.')}
        </AlertLink>
      </React.Fragment>);
    };
    return NotificationSettings;
}(AsyncComponent));
export default NotificationSettings;
//# sourceMappingURL=notificationSettings.jsx.map