import { __assign, __extends, __read, __rest, __spreadArray } from "tslib";
import * as React from 'react';
import assign from 'lodash/assign';
import MemberListStore from 'app/stores/memberListStore';
import TagStore from 'app/stores/tagStore';
import TeamStore from 'app/stores/teamStore';
import getDisplayName from 'app/utils/getDisplayName';
var uuidPattern = /[0-9a-f]{32}$/;
var getUsername = function (_a) {
    var isManaged = _a.isManaged, username = _a.username, email = _a.email;
    // Users created via SAML receive unique UUID usernames. Use
    // their email in these cases, instead.
    if (username && uuidPattern.test(username)) {
        return email;
    }
    else {
        return !isManaged && username ? username : email;
    }
};
/**
 * HOC for getting tags and many useful issue attributes as 'tags' for use
 * in autocomplete selectors or condition builders.
 */
function withIssueTags(WrappedComponent) {
    var WithIssueTags = /** @class */ (function (_super) {
        __extends(WithIssueTags, _super);
        function WithIssueTags(props, context) {
            var _this = _super.call(this, props, context) || this;
            _this.unsubscribeMembers = MemberListStore.listen(function (users) {
                _this.setState({ users: users });
                _this.setAssigned();
            }, undefined);
            _this.unsubscribeTeams = TeamStore.listen(function () {
                _this.setState({ teams: TeamStore.getAll() });
                _this.setAssigned();
            }, undefined);
            _this.unsubscribeTags = TagStore.listen(function (storeTags) {
                var tags = assign({}, storeTags, TagStore.getIssueAttributes(), TagStore.getBuiltInTags());
                _this.setState({ tags: tags });
                _this.setAssigned();
            }, undefined);
            var tags = assign({}, TagStore.getAllTags(), TagStore.getIssueAttributes(), TagStore.getBuiltInTags());
            var users = MemberListStore.getAll();
            var teams = TeamStore.getAll();
            _this.state = { tags: tags, users: users, teams: teams };
            return _this;
        }
        WithIssueTags.prototype.componentWillUnmount = function () {
            this.unsubscribeMembers();
            this.unsubscribeTeams();
            this.unsubscribeTags();
        };
        WithIssueTags.prototype.setAssigned = function () {
            var _a = this.state, tags = _a.tags, users = _a.users, teams = _a.teams;
            var usernames = users.map(getUsername);
            var teamnames = teams
                .filter(function (team) { return team.isMember; })
                .map(function (team) { return "#" + team.slug; });
            var allAssigned = __spreadArray(['[me, none]'], __read(usernames.concat(teamnames)));
            allAssigned.unshift('me');
            usernames.unshift('me');
            this.setState({
                tags: __assign(__assign({}, tags), { assigned: __assign(__assign({}, tags.assigned), { values: allAssigned }), bookmarks: __assign(__assign({}, tags.bookmarks), { values: usernames }), assigned_or_suggested: __assign(__assign({}, tags.assigned_or_suggested), { values: allAssigned }) }),
            });
        };
        WithIssueTags.prototype.render = function () {
            var _a = this.props, tags = _a.tags, props = __rest(_a, ["tags"]);
            return <WrappedComponent {...__assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        };
        WithIssueTags.displayName = "withIssueTags(" + getDisplayName(WrappedComponent) + ")";
        return WithIssueTags;
    }(React.Component));
    return WithIssueTags;
}
export default withIssueTags;
//# sourceMappingURL=withIssueTags.jsx.map