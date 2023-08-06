import { __extends } from "tslib";
import * as React from 'react';
import isEqual from 'lodash/isEqual';
import TeamStore from 'app/stores/teamStore';
import Badge from './badge';
var TeamBadgeContainer = /** @class */ (function (_super) {
    __extends(TeamBadgeContainer, _super);
    function TeamBadgeContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { team: _this.props.team };
        _this.unlistener = TeamStore.listen(function (team) { return _this.onTeamStoreUpdate(team); }, undefined);
        return _this;
    }
    TeamBadgeContainer.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.state.team === nextProps.team) {
            return;
        }
        if (isEqual(this.state.team, nextProps.team)) {
            return;
        }
        this.setState({ team: nextProps.team });
    };
    TeamBadgeContainer.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    TeamBadgeContainer.prototype.onTeamStoreUpdate = function (updatedTeam) {
        if (!updatedTeam.has(this.state.team.id)) {
            return;
        }
        var team = TeamStore.getById(this.state.team.id);
        if (!team || isEqual(team.avatar, this.state.team.avatar)) {
            return;
        }
        this.setState({ team: team });
    };
    TeamBadgeContainer.prototype.render = function () {
        return <Badge {...this.props} team={this.state.team}/>;
    };
    return TeamBadgeContainer;
}(React.Component));
export default TeamBadgeContainer;
//# sourceMappingURL=index.jsx.map