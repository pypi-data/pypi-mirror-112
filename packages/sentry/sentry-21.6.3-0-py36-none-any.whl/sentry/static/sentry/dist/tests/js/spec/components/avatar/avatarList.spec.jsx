import { __assign } from "tslib";
import { mountWithTheme } from 'sentry-test/reactTestingLibrary';
import AvatarList from 'app/components/avatar/avatarList';
function renderComponent(avatarUsersSixUsers) {
    return mountWithTheme(<AvatarList users={avatarUsersSixUsers}/>);
}
describe('AvatarList', function () {
    // @ts-expect-error
    var user = TestStubs.User();
    it('renders with user letter avatars', function () {
        var users = [
            __assign(__assign({}, user), { id: '1', name: 'AB' }),
            __assign(__assign({}, user), { id: '2', name: 'BC' }),
        ];
        var _a = renderComponent(users), container = _a.container, queryByTestId = _a.queryByTestId, getByText = _a.getByText;
        expect(getByText('A')).toBeTruthy();
        expect(getByText('B')).toBeTruthy();
        expect(queryByTestId('avatarList-collapsedusers')).toBeNull();
        expect(container).toSnapshot();
    });
    it('renders with collapsed avatar count if > 5 users', function () {
        var users = [
            __assign(__assign({}, user), { id: '1', name: 'AB' }),
            __assign(__assign({}, user), { id: '2', name: 'BC' }),
            __assign(__assign({}, user), { id: '3', name: 'CD' }),
            __assign(__assign({}, user), { id: '4', name: 'DE' }),
            __assign(__assign({}, user), { id: '5', name: 'EF' }),
            __assign(__assign({}, user), { id: '6', name: 'FG' }),
        ];
        var _a = renderComponent(users), container = _a.container, getByTestId = _a.getByTestId, queryByText = _a.queryByText, queryAllByText = _a.queryAllByText;
        expect(queryAllByText(users[0].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[1].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[2].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[3].name.charAt(0))).toBeTruthy();
        expect(queryAllByText(users[4].name.charAt(0))).toBeTruthy();
        expect(queryByText(users[5].name.charAt(0))).toBeNull();
        expect(getByTestId('avatarList-collapsedusers')).toBeTruthy();
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=avatarList.spec.jsx.map