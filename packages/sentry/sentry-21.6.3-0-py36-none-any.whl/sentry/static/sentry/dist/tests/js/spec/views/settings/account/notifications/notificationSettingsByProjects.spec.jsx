import { __read, __spreadArray } from "tslib";
import { mountWithTheme } from 'sentry-test/enzyme';
import { initializeOrg } from 'sentry-test/initializeOrg';
import NotificationSettingsByProjects from 'app/views/settings/account/notifications/notificationSettingsByProjects';
var createWrapper = function (projects) {
    var routerContext = initializeOrg().routerContext;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/projects/',
        method: 'GET',
        body: projects,
    });
    var notificationSettings = {
        alerts: {
            user: { me: { email: 'always', slack: 'always' } },
            project: Object.fromEntries(projects.map(function (project) { return [project.id, { email: 'never', slack: 'never' }]; })),
        },
    };
    return mountWithTheme(<NotificationSettingsByProjects notificationType="alerts" notificationSettings={notificationSettings} onChange={jest.fn()}/>, routerContext);
};
describe('NotificationSettingsByProjects', function () {
    it('should render when there are no projects', function () {
        var wrapper = createWrapper([]);
        expect(wrapper.find('EmptyMessage').text()).toEqual('No projects found');
        expect(wrapper.find('AsyncComponentSearchInput')).toHaveLength(0);
        expect(wrapper.find('Pagination')).toHaveLength(0);
    });
    it('should show search bar when there are enough projects', function () {
        // @ts-expect-error
        var organization = TestStubs.Organization();
        var projects = __spreadArray([], __read(Array(3).keys())).map(function (id) {
            // @ts-expect-error
            return TestStubs.Project({ organization: organization, id: id });
        });
        var wrapper = createWrapper(projects);
        expect(wrapper.find('AsyncComponentSearchInput')).toHaveLength(1);
    });
});
//# sourceMappingURL=notificationSettingsByProjects.spec.jsx.map