import { __assign, __extends, __rest } from "tslib";
import { Component } from 'react';
import { metric } from 'app/utils/analytics';
import withTeams from 'app/utils/withTeams';
import { createDefaultRule, createRuleFromEventView, createRuleFromWizardTemplate, } from 'app/views/alerts/incidentRules/constants';
import RuleForm from './ruleForm';
/**
 * Show metric rules form with an empty rule. Redirects to alerts list after creation.
 */
var IncidentRulesCreate = /** @class */ (function (_super) {
    __extends(IncidentRulesCreate, _super);
    function IncidentRulesCreate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            var router = _this.props.router;
            var orgId = _this.props.params.orgId;
            metric.endTransaction({ name: 'saveAlertRule' });
            router.push("/organizations/" + orgId + "/alerts/rules/");
        };
        return _this;
    }
    IncidentRulesCreate.prototype.render = function () {
        var _a;
        var _b = this.props, project = _b.project, eventView = _b.eventView, wizardTemplate = _b.wizardTemplate, sessionId = _b.sessionId, teams = _b.teams, props = __rest(_b, ["project", "eventView", "wizardTemplate", "sessionId", "teams"]);
        var defaultRule = eventView
            ? createRuleFromEventView(eventView)
            : wizardTemplate
                ? createRuleFromWizardTemplate(wizardTemplate)
                : createDefaultRule();
        var userTeamIds = teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        });
        var projectTeamIds = new Set(project.teams.map(function (_a) {
            var id = _a.id;
            return id;
        }));
        var defaultOwnerId = (_a = userTeamIds.find(function (id) { return projectTeamIds.has(id); })) !== null && _a !== void 0 ? _a : null;
        defaultRule.owner = defaultOwnerId && "team:" + defaultOwnerId;
        return (<RuleForm onSubmitSuccess={this.handleSubmitSuccess} rule={__assign(__assign({}, defaultRule), { projects: [project.slug] })} sessionId={sessionId} project={project} userTeamIds={userTeamIds} {...props}/>);
    };
    return IncidentRulesCreate;
}(Component));
export default withTeams(IncidentRulesCreate);
//# sourceMappingURL=create.jsx.map