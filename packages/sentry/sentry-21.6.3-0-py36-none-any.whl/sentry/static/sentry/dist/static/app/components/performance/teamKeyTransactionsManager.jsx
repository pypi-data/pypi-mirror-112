import { __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import { Component, createContext } from 'react';
import isEqual from 'lodash/isEqual';
import { fetchTeamKeyTransactions, toggleKeyTransaction, } from 'app/actionCreators/performance';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
var TeamKeyTransactionsManagerContext = createContext({
    teams: [],
    isLoading: false,
    error: null,
    counts: null,
    getKeyedTeams: function () { return null; },
    handleToggleKeyTransaction: function () { },
});
var UnwrappedProvider = /** @class */ (function (_super) {
    __extends(UnwrappedProvider, _super);
    function UnwrappedProvider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            keyFetchID: null,
            isLoading: true,
            error: null,
            teamKeyTransactions: [],
        };
        _this.getKeyedTeams = function (projectId, transactionName) {
            var teamKeyTransactions = _this.state.teamKeyTransactions;
            var keyedTeams = new Set();
            teamKeyTransactions.forEach(function (_a) {
                var team = _a.team, keyed = _a.keyed;
                var isKeyedByTeam = keyed.find(function (keyedTeam) {
                    return keyedTeam.project_id === projectId && keyedTeam.transaction === transactionName;
                });
                if (isKeyedByTeam) {
                    keyedTeams.add(team);
                }
            });
            return keyedTeams;
        };
        _this.handleToggleKeyTransaction = function (selection) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, teamKeyTransactions, action, project, transactionName, teamIds, isKeyTransaction, teamIdSet, newTeamKeyTransactions, err_1;
            var _b, _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        teamKeyTransactions = this.state.teamKeyTransactions;
                        action = selection.action, project = selection.project, transactionName = selection.transactionName, teamIds = selection.teamIds;
                        isKeyTransaction = action === 'unkey';
                        teamIdSet = new Set(teamIds);
                        newTeamKeyTransactions = teamKeyTransactions.map(function (_a) {
                            var team = _a.team, count = _a.count, keyed = _a.keyed;
                            if (!teamIdSet.has(team)) {
                                return { team: team, count: count, keyed: keyed };
                            }
                            if (isKeyTransaction) {
                                return {
                                    team: team,
                                    count: count - 1,
                                    keyed: keyed.filter(function (keyTransaction) {
                                        return keyTransaction.project_id !== project.id ||
                                            keyTransaction.transaction !== transactionName;
                                    }),
                                };
                            }
                            else {
                                return {
                                    team: team,
                                    count: count + 1,
                                    keyed: __spreadArray(__spreadArray([], __read(keyed)), [
                                        {
                                            project_id: project.id,
                                            transaction: transactionName,
                                        },
                                    ]),
                                };
                            }
                        });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, toggleKeyTransaction(api, isKeyTransaction, organization.slug, [project.id], transactionName, teamIds)];
                    case 2:
                        _d.sent();
                        this.setState({ teamKeyTransactions: newTeamKeyTransactions });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _d.sent();
                        this.setState({
                            error: (_c = (_b = err_1.responseJSON) === null || _b === void 0 ? void 0 : _b.detail) !== null && _c !== void 0 ? _c : null,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    UnwrappedProvider.prototype.componentDidMount = function () {
        this.fetchData();
    };
    UnwrappedProvider.prototype.componentDidUpdate = function (prevProps) {
        var orgSlugChanged = prevProps.organization.slug !== this.props.organization.slug;
        var selectedTeamsChanged = !isEqual(prevProps.selectedTeams, this.props.selectedTeams);
        var selectedProjectsChanged = !isEqual(prevProps.selectedProjects, this.props.selectedProjects);
        if (orgSlugChanged || selectedTeamsChanged || selectedProjectsChanged) {
            this.fetchData();
        }
    };
    UnwrappedProvider.prototype.fetchData = function () {
        var _a, _b;
        return __awaiter(this, void 0, void 0, function () {
            var _c, api, organization, selectedTeams, selectedProjects, keyFetchID, teamKeyTransactions, error, err_2;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _c = this.props, api = _c.api, organization = _c.organization, selectedTeams = _c.selectedTeams, selectedProjects = _c.selectedProjects;
                        keyFetchID = Symbol('keyFetchID');
                        this.setState({ isLoading: true, keyFetchID: keyFetchID });
                        teamKeyTransactions = [];
                        error = null;
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchTeamKeyTransactions(api, organization.slug, selectedTeams, selectedProjects)];
                    case 2:
                        teamKeyTransactions = _d.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _d.sent();
                        error = (_b = (_a = err_2.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : t('Error fetching team key transactions');
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({
                            isLoading: false,
                            keyFetchID: undefined,
                            error: error,
                            teamKeyTransactions: teamKeyTransactions,
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    UnwrappedProvider.prototype.getCounts = function () {
        var teamKeyTransactions = this.state.teamKeyTransactions;
        var counts = new Map();
        teamKeyTransactions.forEach(function (_a) {
            var team = _a.team, count = _a.count;
            counts.set(team, count);
        });
        return counts;
    };
    UnwrappedProvider.prototype.render = function () {
        var teams = this.props.teams;
        var _a = this.state, isLoading = _a.isLoading, error = _a.error;
        var childrenProps = {
            teams: teams,
            isLoading: isLoading,
            error: error,
            counts: this.getCounts(),
            getKeyedTeams: this.getKeyedTeams,
            handleToggleKeyTransaction: this.handleToggleKeyTransaction,
        };
        return (<TeamKeyTransactionsManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </TeamKeyTransactionsManagerContext.Provider>);
    };
    return UnwrappedProvider;
}(Component));
export var Provider = withApi(UnwrappedProvider);
export var Consumer = TeamKeyTransactionsManagerContext.Consumer;
//# sourceMappingURL=teamKeyTransactionsManager.jsx.map