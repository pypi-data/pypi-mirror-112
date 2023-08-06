import { mountWithTheme } from 'sentry-test/enzyme';
import { initializeOrg } from 'sentry-test/initializeOrg';
import NotificationSettings from 'app/views/settings/account/notifications/notificationSettings';
var createWrapper = function (notificationSettings) {
    var routerContext = initializeOrg().routerContext;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notification-settings/',
        method: 'GET',
        body: notificationSettings,
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/users/me/notifications/',
        method: 'GET',
        body: {
            personalActivityNotifications: true,
            selfAssignOnResolve: true,
            weeklyReports: true,
        },
    });
    return mountWithTheme(<NotificationSettings />, routerContext);
};
describe('NotificationSettings', function () {
    it('should render', function () {
        var wrapper = createWrapper({
            alerts: { user: { me: { email: 'never', slack: 'never' } } },
            deploy: { user: { me: { email: 'never', slack: 'never' } } },
            workflow: { user: { me: { email: 'never', slack: 'never' } } },
        });
        // There are 7 notification setting Selects/Toggles.
        var fields = wrapper.find('Field');
        expect(fields).toHaveLength(7);
    });
});
//# sourceMappingURL=notificationSettings.spec.jsx.map