import { __extends, __rest } from "tslib";
import { Component } from 'react';
import Button from 'app/components/button';
import TeamKeyTransaction from 'app/components/performance/teamKeyTransaction';
import * as TeamKeyTransactionManager from 'app/components/performance/teamKeyTransactionsManager';
import Tooltip from 'app/components/tooltip';
import { IconStar } from 'app/icons';
import { defined } from 'app/utils';
import withProjects from 'app/utils/withProjects';
import withTeams from 'app/utils/withTeams';
var TitleStar = /** @class */ (function (_super) {
    __extends(TitleStar, _super);
    function TitleStar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TitleStar.prototype.render = function () {
        var _a, _b;
        var _c = this.props, isOpen = _c.isOpen, keyedTeams = _c.keyedTeams, initialValue = _c.initialValue, props = __rest(_c, ["isOpen", "keyedTeams", "initialValue"]);
        var keyedTeamsCount = (_b = (_a = keyedTeams === null || keyedTeams === void 0 ? void 0 : keyedTeams.length) !== null && _a !== void 0 ? _a : initialValue) !== null && _b !== void 0 ? _b : 0;
        var star = (<IconStar color={keyedTeamsCount ? 'yellow300' : 'gray200'} isSolid={keyedTeamsCount > 0} data-test-id="team-key-transaction-column"/>);
        var button = <Button {...props} icon={star} borderless size="zero"/>;
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
    return TitleStar;
}(Component));
function TeamKeyTransactionField(_a) {
    var isKeyTransaction = _a.isKeyTransaction, counts = _a.counts, getKeyedTeams = _a.getKeyedTeams, project = _a.project, transactionName = _a.transactionName, props = __rest(_a, ["isKeyTransaction", "counts", "getKeyedTeams", "project", "transactionName"]);
    var keyedTeams = getKeyedTeams(project.id, transactionName);
    return (<TeamKeyTransaction counts={counts} keyedTeams={keyedTeams} title={TitleStar} project={project} transactionName={transactionName} initialValue={Number(isKeyTransaction)} {...props}/>);
}
function TeamKeyTransactionFieldWrapper(_a) {
    var isKeyTransaction = _a.isKeyTransaction, projects = _a.projects, projectSlug = _a.projectSlug, transactionName = _a.transactionName, props = __rest(_a, ["isKeyTransaction", "projects", "projectSlug", "transactionName"]);
    var project = projects.find(function (proj) { return proj.slug === projectSlug; });
    // All these fields need to be defined in order to toggle a team key
    // transaction. Since they are not defined, just render a plain star
    // with no interactions.
    if (!defined(project) || !defined(transactionName)) {
        return (<TitleStar isOpen={false} disabled keyedTeams={null} initialValue={Number(isKeyTransaction)}/>);
    }
    return (<TeamKeyTransactionManager.Consumer>
      {function (results) { return (<TeamKeyTransactionField isKeyTransaction={isKeyTransaction} project={project} transactionName={transactionName} {...props} {...results}/>); }}
    </TeamKeyTransactionManager.Consumer>);
}
export default withTeams(withProjects(TeamKeyTransactionFieldWrapper));
//# sourceMappingURL=teamKeyTransactionField.jsx.map