import { mountWithTheme } from 'sentry-test/enzyme';
import { initializeOrg } from 'sentry-test/initializeOrg';
import NotificationSettingsByType from 'app/views/settings/account/notifications/notificationSettingsByType';
var createWrapper = function (notificationSettings) {
    var routerContext = initializeOrg().routerContext;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notification-settings/',
        method: 'GET',
        body: notificationSettings,
    });
    return mountWithTheme(<NotificationSettingsByType notificationType="alerts"/>, routerContext);
};
describe('NotificationSettingsByType', function () {
    it('should render when everything is disabled', function () {
        var wrapper = createWrapper({
            alerts: { user: { me: { email: 'never', slack: 'never' } } },
        });
        // There is only one field and it is the default and it is set to "off".
        var fields = wrapper.find('Field');
        expect(fields).toHaveLength(1);
        expect(fields.at(0).find('FieldLabel').text()).toEqual('Issue Alert Notifications');
        expect(fields.at(0).find('Select').text()).toEqual('Off');
    });
});
//# sourceMappingURL=notificationSettingsByType.spec.jsx.map