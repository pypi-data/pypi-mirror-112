import { __awaiter, __extends, __generator } from "tslib";
import { Component, Fragment } from 'react';
import { browserHistory } from 'react-router';
import moment from 'moment';
import { fetchOrgMembers } from 'app/actionCreators/members';
import Feature from 'app/components/acl/feature';
import DateTime from 'app/components/dateTime';
import { t } from 'app/locale';
import { getUtcDateString } from 'app/utils/dates';
import withApi from 'app/utils/withApi';
import { TimePeriod, TimeWindow } from 'app/views/alerts/incidentRules/types';
import { makeRuleDetailsQuery } from 'app/views/alerts/list/row';
import { fetchAlertRule, fetchIncident, fetchIncidentsForRule } from '../../utils';
import DetailsBody from './body';
import { TIME_OPTIONS, TIME_WINDOWS } from './constants';
import DetailsHeader from './header';
var AlertRuleDetails = /** @class */ (function (_super) {
    __extends(AlertRuleDetails, _super);
    function AlertRuleDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { isLoading: false, hasError: false };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, _b, orgId, ruleId, location, timePeriod, start, end, rulePromise, incidentsPromise, _err_1;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, _b = _a.params, orgId = _b.orgId, ruleId = _b.ruleId, location = _a.location;
                        this.setState({ isLoading: true, hasError: false });
                        if (!location.query.alert) return [3 /*break*/, 2];
                        return [4 /*yield*/, fetchIncident(api, orgId, location.query.alert)
                                .then(function (incident) { return _this.setState({ selectedIncident: incident }); })
                                .catch(function () { return _this.setState({ selectedIncident: null }); })];
                    case 1:
                        _c.sent();
                        return [3 /*break*/, 3];
                    case 2:
                        this.setState({ selectedIncident: null });
                        _c.label = 3;
                    case 3:
                        timePeriod = this.getTimePeriod();
                        start = timePeriod.start, end = timePeriod.end;
                        _c.label = 4;
                    case 4:
                        _c.trys.push([4, 6, , 7]);
                        rulePromise = fetchAlertRule(orgId, ruleId).then(function (rule) {
                            return _this.setState({ rule: rule });
                        });
                        incidentsPromise = fetchIncidentsForRule(orgId, ruleId, start, end).then(function (incidents) { return _this.setState({ incidents: incidents }); });
                        return [4 /*yield*/, Promise.all([rulePromise, incidentsPromise])];
                    case 5:
                        _c.sent();
                        this.setState({ isLoading: false, hasError: false });
                        return [3 /*break*/, 7];
                    case 6:
                        _err_1 = _c.sent();
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 7];
                    case 7: return [2 /*return*/];
                }
            });
        }); };
        _this.handleTimePeriodChange = function (value) {
            browserHistory.push({
                pathname: _this.props.location.pathname,
                query: {
                    period: value,
                },
            });
        };
        _this.handleZoom = function (start, end) { return __awaiter(_this, void 0, void 0, function () {
            var location;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        location = this.props.location;
                        return [4 /*yield*/, browserHistory.push({
                                pathname: location.pathname,
                                query: {
                                    start: start,
                                    end: end,
                                },
                            })];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRuleDetails.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, params = _a.params;
        fetchOrgMembers(api, params.orgId);
        this.fetchData();
    };
    AlertRuleDetails.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.location.search !== this.props.location.search ||
            prevProps.params.orgId !== this.props.params.orgId ||
            prevProps.params.ruleId !== this.props.params.ruleId) {
            this.fetchData();
        }
    };
    AlertRuleDetails.prototype.getTimePeriod = function () {
        var _a, _b;
        var location = this.props.location;
        var rule = this.state.rule;
        var defaultPeriod = (rule === null || rule === void 0 ? void 0 : rule.timeWindow) && (rule === null || rule === void 0 ? void 0 : rule.timeWindow) > TimeWindow.ONE_HOUR
            ? TimePeriod.SEVEN_DAYS
            : TimePeriod.ONE_DAY;
        var period = (_a = location.query.period) !== null && _a !== void 0 ? _a : defaultPeriod;
        if (location.query.start && location.query.end) {
            return {
                start: location.query.start,
                end: location.query.end,
                period: period,
                label: t('Custom time'),
                display: (<Fragment>
            <DateTime date={moment.utc(location.query.start)} timeAndDate/>
            {' — '}
            <DateTime date={moment.utc(location.query.end)} timeAndDate/>
          </Fragment>),
                custom: true,
            };
        }
        if (location.query.alert && this.state.selectedIncident) {
            var _c = makeRuleDetailsQuery(this.state.selectedIncident), start_1 = _c.start, end_1 = _c.end;
            return {
                start: start_1,
                end: end_1,
                period: period,
                label: t('Custom time'),
                display: (<Fragment>
            <DateTime date={moment.utc(start_1)} timeAndDate/>
            {' — '}
            <DateTime date={moment.utc(end_1)} timeAndDate/>
          </Fragment>),
                custom: true,
            };
        }
        var timeOption = (_b = TIME_OPTIONS.find(function (item) { return item.value === period; })) !== null && _b !== void 0 ? _b : TIME_OPTIONS[1];
        var start = getUtcDateString(moment(moment.utc().diff(TIME_WINDOWS[timeOption.value])));
        var end = getUtcDateString(moment.utc());
        return {
            start: start,
            end: end,
            period: period,
            label: timeOption.label,
            display: timeOption.label,
        };
    };
    AlertRuleDetails.prototype.render = function () {
        var _a = this.state, rule = _a.rule, incidents = _a.incidents, hasError = _a.hasError, selectedIncident = _a.selectedIncident;
        var _b = this.props, params = _b.params, organization = _b.organization;
        var timePeriod = this.getTimePeriod();
        return (<Fragment>
        <Feature organization={organization} features={['alert-details-redesign']}>
          <DetailsHeader hasIncidentRuleDetailsError={hasError} params={params} rule={rule}/>
          <DetailsBody {...this.props} rule={rule} incidents={incidents} timePeriod={timePeriod} selectedIncident={selectedIncident} handleTimePeriodChange={this.handleTimePeriodChange} handleZoom={this.handleZoom}/>
        </Feature>
      </Fragment>);
    };
    return AlertRuleDetails;
}(Component));
export default withApi(AlertRuleDetails);
//# sourceMappingURL=index.jsx.map