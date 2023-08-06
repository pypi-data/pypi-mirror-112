import { __extends } from "tslib";
import * as React from 'react';
import TeamStore from 'app/stores/teamStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Higher order component that uses TeamStore and provides a list of teams
 */
function withTeams(WrappedComponent) {
    var WithTeams = /** @class */ (function (_super) {
        __extends(WithTeams, _super);
        function WithTeams() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                teams: TeamStore.getAll(),
            };
            _this.unsubscribe = TeamStore.listen(function () { return _this.setState({ teams: TeamStore.getAll() }); }, undefined);
            return _this;
        }
        WithTeams.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithTeams.prototype.render = function () {
            return (<WrappedComponent {...this.props} teams={this.state.teams}/>);
        };
        WithTeams.displayName = "withTeams(" + getDisplayName(WrappedComponent) + ")";
        return WithTeams;
    }(React.Component));
    return WithTeams;
}
export default withTeams;
//# sourceMappingURL=withTeams.jsx.map