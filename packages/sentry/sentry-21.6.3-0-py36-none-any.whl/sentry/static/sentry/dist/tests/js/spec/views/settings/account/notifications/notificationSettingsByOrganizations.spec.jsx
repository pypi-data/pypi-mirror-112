import { mountWithTheme } from 'sentry-test/enzyme';
import { initializeOrg } from 'sentry-test/initializeOrg';
import NotificationSettingsByOrganization from 'app/views/settings/account/notifications/notificationSettingsByOrganization';
var createWrapper = function (notificationSettings) {
    var _a = initializeOrg(), organization = _a.organization, routerContext = _a.routerContext;
    return mountWithTheme(<NotificationSettingsByOrganization notificationType="alerts" notificationSettings={notificationSettings} organizations={[organization]} onChange={jest.fn()}/>, routerContext);
};
describe('NotificationSettingsByOrganization', function () {
    it('should render', function () {
        var wrapper = createWrapper({
            alerts: {
                user: { me: { email: 'always', slack: 'always' } },
                organization: { 1: { email: 'always', slack: 'always' } },
            },
        });
        expect(wrapper.find('Select')).toHaveLength(1);
    });
});
//# sourceMappingURL=notificationSettingsByOrganizations.spec.jsx.map