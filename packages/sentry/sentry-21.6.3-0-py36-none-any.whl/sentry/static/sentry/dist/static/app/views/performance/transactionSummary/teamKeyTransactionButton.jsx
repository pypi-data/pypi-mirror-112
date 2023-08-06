import { __extends, __rest } from "tslib";
import { Component } from 'react';
import Button from 'app/components/button';
import TeamKeyTransactionComponent from 'app/components/performance/teamKeyTransaction';
import * as TeamKeyTransactionManager from 'app/components/performance/teamKeyTransactionsManager';
import Tooltip from 'app/components/tooltip';
import { IconStar } from 'app/icons';
import { t, tn } from 'app/locale';
import { defined } from 'app/utils';
import { isActiveSuperuser } from 'app/utils/isActiveSuperuser';
import withProjects from 'app/utils/withProjects';
import withTeams from 'app/utils/withTeams';
/**
 * This can't be a function component because `TeamKeyTransaction` uses
 * `DropdownControl` which in turn uses passes a ref to this component.
 */
var TitleButton = /** @class */ (function (_super) {
    __extends(TitleButton, _super);
    function TitleButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TitleButton.prototype.render = function () {
        var _a;
        var _b = this.props, isOpen = _b.isOpen, keyedTeams = _b.keyedTeams, props = __rest(_b, ["isOpen", "keyedTeams"]);
        var keyedTeamsCount = (_a = keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length) !== null && _a !== void 0 ? _a : 0;
        var button = (<Button {...props} icon={keyedTeamsCount ? <IconStar color="yellow300" isSolid/> : <IconStar />}>
        {keyedTeamsCount
                ? tn('Starred for Team', 'Starred for Teams', keyedTeamsCount)
                : t('Star for Team')}
      </Button>);
        if (!isOpen && (keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length)) {
            var teamSlugs = keyedTeams.map(function (_a) {
                var slug = _a.slug;
                return slug;
            }).join(', ');
            return <Tooltip title={teamSlugs}>{button}</Tooltip>;
        }
        else {
            return button;
        }
    };
    return TitleButton;
}(Component));
function TeamKeyTransactionButton(_a) {
    var counts = _a.counts, getKeyedTeams = _a.getKeyedTeams, project = _a.project, transactionName = _a.transactionName, props = __rest(_a, ["counts", "getKeyedTeams", "project", "transactionName"]);
    var keyedTeams = getKeyedTeams(project.id, transactionName);
    return (<TeamKeyTransactionComponent counts={counts} keyedTeams={keyedTeams} title={TitleButton} project={project} transactionName={transactionName} {...props}/>);
}
function TeamKeyTransactionButtonWrapper(_a) {
    var eventView = _a.eventView, organization = _a.organization, teams = _a.teams, projects = _a.projects, props = __rest(_a, ["eventView", "organization", "teams", "projects"]);
    if (eventView.project.length !== 1) {
        return <TitleButton isOpen={false} disabled keyedTeams={null}/>;
    }
    var projectId = String(eventView.project[0]);
    var project = projects.find(function (proj) { return proj.id === projectId; });
    if (!defined(project)) {
        return <TitleButton isOpen={false} disabled keyedTeams={null}/>;
    }
    var isSuperuser = isActiveSuperuser();
    var userTeams = teams.filter(function (_a) {
        var isMember = _a.isMember;
        return isMember || isSuperuser;
    });
    return (<TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={[String(projectId)]}>
      <TeamKeyTransactionManager.Consumer>
        {function (results) { return (<TeamKeyTransactionButton organization={organization} project={project} {...props} {...results}/>); }}
      </TeamKeyTransactionManager.Consumer>
    </TeamKeyTransactionManager.Provider>);
}
export default withTeams(withProjects(TeamKeyTransactionButtonWrapper));
//# sourceMappingURL=teamKeyTransactionButton.jsx.map