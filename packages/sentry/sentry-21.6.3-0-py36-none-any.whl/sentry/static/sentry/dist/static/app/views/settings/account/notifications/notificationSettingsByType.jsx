import { __assign, __extends } from "tslib";
import React from 'react';
import AsyncComponent from 'app/components/asyncComponent';
import { t } from 'app/locale';
import FeedbackAlert from 'app/views/settings/account/notifications/feedbackAlert';
import { ACCOUNT_NOTIFICATION_FIELDS } from 'app/views/settings/account/notifications/fields';
import { NOTIFICATION_SETTING_FIELDS } from 'app/views/settings/account/notifications/fields2';
import NotificationSettingsByOrganization from 'app/views/settings/account/notifications/notificationSettingsByOrganization';
import NotificationSettingsByProjects from 'app/views/settings/account/notifications/notificationSettingsByProjects';
import { getCurrentDefault, getCurrentProviders, getParentIds, getStateToPutForDefault, getStateToPutForParent, getStateToPutForProvider, isEverythingDisabled, isGroupedByProject, mergeNotificationSettings, providerListToString, } from 'app/views/settings/account/notifications/utils';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var NotificationSettingsByType = /** @class */ (function (_super) {
    __extends(NotificationSettingsByType, _super);
    function NotificationSettingsByType() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /* Methods responsible for updating state and hitting the API. */
        _this.getStateToPutForProvider = function (changedData) {
            var notificationType = _this.props.notificationType;
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = getStateToPutForProvider(notificationType, notificationSettings, changedData);
            _this.setState({
                notificationSettings: mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        _this.getStateToPutForDefault = function (changedData) {
            var notificationType = _this.props.notificationType;
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = getStateToPutForDefault(notificationType, notificationSettings, changedData, getParentIds(notificationType, notificationSettings));
            _this.setState({
                notificationSettings: mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        _this.getStateToPutForParent = function (changedData, parentId) {
            var notificationType = _this.props.notificationType;
            var notificationSettings = _this.state.notificationSettings;
            var updatedNotificationSettings = getStateToPutForParent(notificationType, notificationSettings, changedData, parentId);
            _this.setState({
                notificationSettings: mergeNotificationSettings(notificationSettings, updatedNotificationSettings),
            });
            return updatedNotificationSettings;
        };
        return _this;
    }
    NotificationSettingsByType.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { notificationSettings: {} });
    };
    NotificationSettingsByType.prototype.getEndpoints = function () {
        var notificationType = this.props.notificationType;
        var query = { type: notificationType };
        return [['notificationSettings', "/users/me/notification-settings/", { query: query }]];
    };
    /* Methods responsible for rendering the page. */
    NotificationSettingsByType.prototype.getInitialData = function () {
        var _a;
        var notificationType = this.props.notificationType;
        var notificationSettings = this.state.notificationSettings;
        var initialData = (_a = {},
            _a[notificationType] = getCurrentDefault(notificationType, notificationSettings),
            _a);
        if (!isEverythingDisabled(notificationType, notificationSettings)) {
            initialData.provider = providerListToString(getCurrentProviders(notificationType, notificationSettings));
        }
        return initialData;
    };
    NotificationSettingsByType.prototype.getFields = function () {
        var _this = this;
        var notificationType = this.props.notificationType;
        var notificationSettings = this.state.notificationSettings;
        var fields = [
            Object.assign({}, NOTIFICATION_SETTING_FIELDS[notificationType], {
                help: t('This is the default for all projects.'),
                getData: function (data) { return _this.getStateToPutForDefault(data); },
            }),
        ];
        if (!isEverythingDisabled(notificationType, notificationSettings)) {
            fields.push(Object.assign({
                help: t('Where personal notifications will be sent.'),
                getData: function (data) { return _this.getStateToPutForProvider(data); },
            }, NOTIFICATION_SETTING_FIELDS.provider));
        }
        return fields;
    };
    NotificationSettingsByType.prototype.renderBody = function () {
        var notificationType = this.props.notificationType;
        var notificationSettings = this.state.notificationSettings;
        var _a = ACCOUNT_NOTIFICATION_FIELDS[notificationType], title = _a.title, description = _a.description;
        return (<React.Fragment>
        <SettingsPageHeader title={title}/>
        {description && <TextBlock>{description}</TextBlock>}
        <FeedbackAlert />
        <Form saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={this.getInitialData()}>
          <JsonForm title={isGroupedByProject(notificationType)
                ? t('All Projects')
                : t('All Organizations')} fields={this.getFields()}/>
        </Form>
        {!isEverythingDisabled(notificationType, notificationSettings) &&
                (isGroupedByProject(notificationType) ? (<NotificationSettingsByProjects notificationType={notificationType} notificationSettings={notificationSettings} onChange={this.getStateToPutForParent}/>) : (<NotificationSettingsByOrganization notificationType={notificationType} notificationSettings={notificationSettings} onChange={this.getStateToPutForParent}/>))}
      </React.Fragment>);
    };
    return NotificationSettingsByType;
}(AsyncComponent));
export default NotificationSettingsByType;
//# sourceMappingURL=notificationSettingsByType.jsx.map