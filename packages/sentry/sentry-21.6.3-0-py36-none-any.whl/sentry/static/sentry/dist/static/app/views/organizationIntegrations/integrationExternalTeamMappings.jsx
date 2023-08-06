import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import * as React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import AsyncComponent from 'app/components/asyncComponent';
import IntegrationExternalMappingForm from 'app/components/integrationExternalMappingForm';
import IntegrationExternalMappings from 'app/components/integrationExternalMappings';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
var IntegrationExternalTeamMappings = /** @class */ (function (_super) {
    __extends(IntegrationExternalTeamMappings, _super);
    function IntegrationExternalTeamMappings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (mapping) { return __awaiter(_this, void 0, void 0, function () {
            var organization, teams, team, endpoint, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        organization = this.props.organization;
                        teams = this.state.teams;
                        team = teams.find(function (item) { return item.id === mapping.teamId; });
                        if (!team) {
                            throw new Error('Cannot find correct team slug.');
                        }
                        endpoint = "/teams/" + organization.slug + "/" + team.slug + "/external-teams/" + mapping.id + "/";
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 1:
                        _b.sent();
                        // remove config and update state
                        addSuccessMessage(t('Deletion successful'));
                        this.fetchData();
                        return [3 /*break*/, 3];
                    case 2:
                        _a = _b.sent();
                        // no 4xx errors should happen on delete
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmitSuccess = function () {
            _this.fetchData();
        };
        _this.handleSubmit = function (data, onSubmitSuccess, onSubmitError, _, model, mapping) {
            // We need to dynamically set the endpoint bc it requires the slug of the selected team in the form.
            try {
                var organization = _this.props.organization;
                var queryResults = _this.state.queryResults;
                var team = queryResults.find(function (item) { return item.id === data.teamId; });
                if (!team) {
                    throw new Error('Cannot find team slug.');
                }
                var baseEndpoint = "/teams/" + organization.slug + "/" + team.slug + "/external-teams/";
                var apiEndpoint = mapping ? "" + baseEndpoint + mapping.id + "/" : baseEndpoint;
                var apiMethod = mapping ? 'PUT' : 'POST';
                model.setFormOptions({
                    onSubmitSuccess: onSubmitSuccess,
                    onSubmitError: onSubmitError,
                    apiEndpoint: apiEndpoint,
                    apiMethod: apiMethod,
                });
                model.saveForm();
            }
            catch (_a) {
                // no 4xx errors should happen on delete
                addErrorMessage(t('An error occurred'));
            }
        };
        _this.openModal = function (mapping) {
            var _a = _this.props, organization = _a.organization, integration = _a.integration;
            openModal(function (_a) {
                var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal;
                return (<React.Fragment>
        <Header closeButton>{t('Configure External Team Mapping')}</Header>
        <Body>
          <IntegrationExternalMappingForm organization={organization} integration={integration} onSubmitSuccess={function () {
                        _this.handleSubmitSuccess();
                        closeModal();
                    }} mapping={mapping} sentryNamesMapper={_this.sentryNamesMapper} type="team" url={"/organizations/" + organization.slug + "/teams/"} onCancel={closeModal} onSubmit={function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    return _this.handleSubmit.apply(_this, __spreadArray(__spreadArray([], __read(args)), [mapping]));
                }} onResults={function (results) { return _this.setState({ queryResults: results }); }}/>
        </Body>
      </React.Fragment>);
            });
        };
        return _this;
    }
    IntegrationExternalTeamMappings.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { teams: [], queryResults: [] });
    };
    IntegrationExternalTeamMappings.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [
            [
                'teams',
                "/organizations/" + organization.slug + "/teams/",
                { query: { query: 'hasExternalTeams:true' } },
            ],
        ];
    };
    Object.defineProperty(IntegrationExternalTeamMappings.prototype, "mappings", {
        get: function () {
            var integration = this.props.integration;
            var teams = this.state.teams;
            var externalTeamMappings = teams.reduce(function (acc, team) {
                var externalTeams = team.externalTeams;
                acc.push.apply(acc, __spreadArray([], __read(externalTeams
                    .filter(function (externalTeam) { return externalTeam.provider === integration.provider.key; })
                    .map(function (externalTeam) { return (__assign(__assign({}, externalTeam), { sentryName: team.slug })); }))));
                return acc;
            }, []);
            return externalTeamMappings.sort(function (a, b) { return parseInt(a.id, 10) - parseInt(b.id, 10); });
        },
        enumerable: false,
        configurable: true
    });
    IntegrationExternalTeamMappings.prototype.sentryNamesMapper = function (teams) {
        return teams.map(function (_a) {
            var id = _a.id, slug = _a.slug;
            return ({ id: id, name: slug });
        });
    };
    IntegrationExternalTeamMappings.prototype.renderBody = function () {
        var integration = this.props.integration;
        return (<IntegrationExternalMappings integration={integration} type="team" mappings={this.mappings} onCreateOrEdit={this.openModal} onDelete={this.handleDelete}/>);
    };
    return IntegrationExternalTeamMappings;
}(AsyncComponent));
export default withOrganization(IntegrationExternalTeamMappings);
//# sourceMappingURL=integrationExternalTeamMappings.jsx.map