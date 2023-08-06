import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __rest } from "tslib";
import { Fragment } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import moment from 'moment';
import { restoreRelease } from 'app/actionCreators/release';
import { Client } from 'app/api';
import Feature from 'app/components/acl/feature';
import DateTime from 'app/components/dateTime';
import TransactionsList from 'app/components/discover/transactionsList';
import { Body, Main, Side } from 'app/components/layouts/thirds';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import PageTimeRangeSelector from 'app/components/organizations/timeRangeSelector/pageTimeRangeSelector';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getUtcDateString } from 'app/utils/dates';
import EventView from 'app/utils/discover/eventView';
import { WebVital } from 'app/utils/discover/fields';
import { formatVersion } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import routeTitleGen from 'app/utils/routeTitle';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import { DisplayModes } from 'app/views/performance/transactionSummary/charts';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { TrendChangeType } from 'app/views/performance/trends/types';
import { getReleaseParams, isReleaseArchived } from '../../utils';
import { ReleaseContext } from '..';
import ReleaseChart from './chart/';
import { EventType, YAxis } from './chart/releaseChartControls';
import CommitAuthorBreakdown from './commitAuthorBreakdown';
import Deploys from './deploys';
import Issues from './issues';
import OtherProjects from './otherProjects';
import ProjectReleaseDetails from './projectReleaseDetails';
import ReleaseArchivedNotice from './releaseArchivedNotice';
import ReleaseComparisonChart from './releaseComparisonChart';
import ReleaseDetailsRequest from './releaseDetailsRequest';
import ReleaseStats from './releaseStats';
import TotalCrashFreeUsers from './totalCrashFreeUsers';
var RELEASE_PERIOD_KEY = 'release';
export var TransactionsListOption;
(function (TransactionsListOption) {
    TransactionsListOption["FAILURE_COUNT"] = "failure_count";
    TransactionsListOption["TPM"] = "tpm";
    TransactionsListOption["SLOW"] = "slow";
    TransactionsListOption["SLOW_LCP"] = "slow_lcp";
    TransactionsListOption["REGRESSION"] = "regression";
    TransactionsListOption["IMPROVEMENT"] = "improved";
})(TransactionsListOption || (TransactionsListOption = {}));
var ReleaseOverview = /** @class */ (function (_super) {
    __extends(ReleaseOverview, _super);
    function ReleaseOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleYAxisChange = function (yAxis, project) {
            var _a = _this.props, location = _a.location, router = _a.router, organization = _a.organization;
            var _b = location.query, eventType = _b.eventType, vitalType = _b.vitalType, query = __rest(_b, ["eventType", "vitalType"]);
            trackAnalyticsEvent({
                eventKey: "release_detail.change_chart",
                eventName: "Release Detail: Change Chart",
                organization_id: parseInt(organization.id, 10),
                display: yAxis,
                eventType: eventType,
                vitalType: vitalType,
                platform: project.platform,
            });
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, query), { yAxis: yAxis }) }));
        };
        _this.handleEventTypeChange = function (eventType, project) {
            var _a = _this.props, location = _a.location, router = _a.router, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: "release_detail.change_chart",
                eventName: "Release Detail: Change Chart",
                organization_id: parseInt(organization.id, 10),
                display: YAxis.EVENTS,
                eventType: eventType,
                platform: project.platform,
            });
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { eventType: eventType }) }));
        };
        _this.handleVitalTypeChange = function (vitalType, project) {
            var _a = _this.props, location = _a.location, router = _a.router, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: "release_detail.change_chart",
                eventName: "Release Detail: Change Chart",
                organization_id: parseInt(organization.id, 10),
                display: YAxis.COUNT_VITAL,
                vitalType: vitalType,
                platform: project.platform,
            });
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { vitalType: vitalType }) }));
        };
        _this.handleRestore = function (project, successCallback) { return __awaiter(_this, void 0, void 0, function () {
            var _a, params, organization, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, params = _a.params, organization = _a.organization;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, restoreRelease(new Client(), {
                                orgSlug: organization.slug,
                                projectSlug: project.slug,
                                releaseVersion: params.release,
                            })];
                    case 2:
                        _c.sent();
                        successCallback();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleTransactionsListSortChange = function (value) {
            var location = _this.props.location;
            var target = {
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            browserHistory.push(target);
        };
        _this.handleDateChange = function (datetime) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var start = datetime.start, end = datetime.end, relative = datetime.relative, utc = datetime.utc;
            if (start && end) {
                var parser = utc ? moment.utc : moment;
                router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { pageStatsPeriod: undefined, pageStart: parser(start).format(), pageEnd: parser(end).format(), pageUtc: utc !== null && utc !== void 0 ? utc : undefined }) }));
                return;
            }
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { pageStatsPeriod: relative === RELEASE_PERIOD_KEY ? undefined : relative, pageStart: undefined, pageEnd: undefined, pageUtc: undefined }) }));
        };
        return _this;
    }
    ReleaseOverview.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleaseOverview.prototype.getYAxis = function (hasHealthData, hasPerformance) {
        var yAxis = this.props.location.query.yAxis;
        if (typeof yAxis === 'string') {
            if (Object.values(YAxis).includes(yAxis)) {
                return yAxis;
            }
        }
        if (hasHealthData) {
            return YAxis.SESSIONS;
        }
        if (hasPerformance) {
            return YAxis.FAILED_TRANSACTIONS;
        }
        return YAxis.EVENTS;
    };
    ReleaseOverview.prototype.getEventType = function (yAxis) {
        if (yAxis === YAxis.EVENTS) {
            var eventType = this.props.location.query.eventType;
            if (typeof eventType === 'string') {
                if (Object.values(EventType).includes(eventType)) {
                    return eventType;
                }
            }
        }
        return EventType.ALL;
    };
    ReleaseOverview.prototype.getVitalType = function (yAxis) {
        if (yAxis === YAxis.COUNT_VITAL) {
            var vitalType = this.props.location.query.vitalType;
            if (typeof vitalType === 'string') {
                if (Object.values(WebVital).includes(vitalType)) {
                    return vitalType;
                }
            }
        }
        return WebVital.LCP;
    };
    ReleaseOverview.prototype.getReleaseEventView = function (version, projectId, selectedSort, releaseBounds, defaultStatsPeriod) {
        var _a = this.props, selection = _a.selection, location = _a.location, organization = _a.organization;
        var environments = selection.environments;
        var _b = getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        }), start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod;
        var baseQuery = {
            id: undefined,
            version: 2,
            name: "Release " + formatVersion(version),
            query: "event.type:transaction release:" + version,
            fields: ['transaction', 'failure_count()', 'epm()', 'p50()'],
            orderby: '-failure_count',
            range: statsPeriod || undefined,
            environment: environments,
            projects: [projectId],
            start: start ? getUtcDateString(start) : undefined,
            end: end ? getUtcDateString(end) : undefined,
        };
        switch (selectedSort.value) {
            case TransactionsListOption.SLOW_LCP:
                return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " epm():>0.01 has:measurements.lcp", fields: ['transaction', 'failure_count()', 'epm()', 'p75(measurements.lcp)'], orderby: 'p75_measurements_lcp' }));
            case TransactionsListOption.SLOW:
                return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " epm():>0.01" }));
            case TransactionsListOption.FAILURE_COUNT:
                return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " failure_count():>0" }));
            default:
                return EventView.fromSavedQuery(baseQuery);
        }
    };
    ReleaseOverview.prototype.getReleaseTrendView = function (version, projectId, versionDate, releaseBounds, defaultStatsPeriod) {
        var _a = this.props, selection = _a.selection, location = _a.location, organization = _a.organization;
        var environments = selection.environments;
        var _b = getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        }), start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod;
        var trendView = EventView.fromSavedQuery({
            id: undefined,
            version: 2,
            name: "Release " + formatVersion(version),
            fields: ['transaction'],
            query: 'tpm():>0.01 trend_percentage():>0%',
            range: statsPeriod || undefined,
            environment: environments,
            projects: [projectId],
            start: start ? getUtcDateString(start) : undefined,
            end: end ? getUtcDateString(end) : undefined,
        });
        trendView.middle = versionDate;
        return trendView;
    };
    Object.defineProperty(ReleaseOverview.prototype, "pageDateTime", {
        get: function () {
            var query = this.props.location.query;
            var _a = getParams(query, {
                allowEmptyPeriod: true,
                allowAbsoluteDatetime: true,
                allowAbsolutePageDatetime: true,
            }), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, utcString = _a.utc;
            if (statsPeriod) {
                return { period: statsPeriod };
            }
            var utc = utcString === 'true';
            var parser = utc ? moment.utc : moment;
            if (start && end) {
                return {
                    start: parser(start).format(),
                    end: parser(end).format(),
                    utc: utc,
                };
            }
            return {};
        },
        enumerable: false,
        configurable: true
    });
    ReleaseOverview.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection, location = _a.location, api = _a.api, router = _a.router;
        var _b = this.pageDateTime, start = _b.start, end = _b.end, period = _b.period, utc = _b.utc;
        return (<ReleaseContext.Consumer>
        {function (_a) {
                var release = _a.release, project = _a.project, deploys = _a.deploys, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData, defaultStatsPeriod = _a.defaultStatsPeriod, isHealthLoading = _a.isHealthLoading, getHealthData = _a.getHealthData, hasHealthData = _a.hasHealthData, releaseBounds = _a.releaseBounds;
                var commitCount = release.commitCount, version = release.version;
                var hasDiscover = organization.features.includes('discover-basic');
                var hasPerformance = organization.features.includes('performance-view');
                var yAxis = _this.getYAxis(hasHealthData, hasPerformance);
                var eventType = _this.getEventType(yAxis);
                var vitalType = _this.getVitalType(yAxis);
                var _b = getTransactionsListSort(location), selectedSort = _b.selectedSort, sortOptions = _b.sortOptions;
                var releaseEventView = _this.getReleaseEventView(version, project.id, selectedSort, releaseBounds, defaultStatsPeriod);
                var titles = selectedSort.value !== TransactionsListOption.SLOW_LCP
                    ? [t('transaction'), t('failure_count()'), t('tpm()'), t('p50()')]
                    : [t('transaction'), t('failure_count()'), t('tpm()'), t('p75(lcp)')];
                var releaseTrendView = _this.getReleaseTrendView(version, project.id, releaseMeta.released, releaseBounds, defaultStatsPeriod);
                var generateLink = {
                    transaction: generateTransactionLink(version, project.id, selection, location.query.showTransactions),
                };
                return (<ReleaseDetailsRequest organization={organization} location={location} disable={!organization.features.includes('release-comparison')} version={version} releaseBounds={releaseBounds}>
              {function (_a) {
                        var thisRelease = _a.thisRelease, allReleases = _a.allReleases, loading = _a.loading, reloading = _a.reloading, errored = _a.errored;
                        return (<Body>
                  <Main>
                    {isReleaseArchived(release) && (<ReleaseArchivedNotice onRestore={function () { return _this.handleRestore(project, refetchData); }}/>)}
                    <Feature features={['release-comparison']}>
                      {function (_a) {
                                var _b;
                                var hasFeature = _a.hasFeature;
                                return hasFeature ? (<Fragment>
                            <StyledPageTimeRangeSelector organization={organization} relative={period !== null && period !== void 0 ? period : ''} start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} utc={utc !== null && utc !== void 0 ? utc : null} onUpdate={_this.handleDateChange} showAbsolute={false} relativeOptions={__assign((_b = {}, _b[RELEASE_PERIOD_KEY] = (<Fragment>
                                    {t('Entire Release Period')} (
                                    <DateTime date={releaseBounds.releaseStart} timeAndDate/>{' '}
                                    -{' '}
                                    <DateTime date={releaseBounds.releaseEnd} timeAndDate/>
                                    )
                                  </Fragment>), _b), DEFAULT_RELATIVE_PERIODS)} defaultPeriod={RELEASE_PERIOD_KEY}/>
                            <ReleaseComparisonChart release={release} releaseSessions={thisRelease} allSessions={allReleases} platform={project.platform} location={location} loading={loading} reloading={reloading} errored={errored} project={project}/>
                          </Fragment>) : ((hasDiscover || hasPerformance || hasHealthData) && (<ReleaseChart releaseMeta={releaseMeta} selection={selection} yAxis={yAxis} onYAxisChange={function (display) {
                                        return _this.handleYAxisChange(display, project);
                                    }} eventType={eventType} onEventTypeChange={function (type) {
                                        return _this.handleEventTypeChange(type, project);
                                    }} vitalType={vitalType} onVitalTypeChange={function (type) {
                                        return _this.handleVitalTypeChange(type, project);
                                    }} router={router} organization={organization} hasHealthData={hasHealthData} location={location} api={api} version={version} hasDiscover={hasDiscover} hasPerformance={hasPerformance} platform={project.platform} defaultStatsPeriod={defaultStatsPeriod} projectSlug={project.slug}/>));
                            }}
                    </Feature>

                    <Issues organization={organization} selection={selection} version={version} location={location} defaultStatsPeriod={defaultStatsPeriod} releaseBounds={releaseBounds} queryFilterDescription={t('In this release')} withChart/>
                    <Feature features={['performance-view']}>
                      <TransactionsList location={location} organization={organization} eventView={releaseEventView} trendView={releaseTrendView} selected={selectedSort} options={sortOptions} handleDropdownChange={_this.handleTransactionsListSortChange} titles={titles} generateLink={generateLink}/>
                    </Feature>
                  </Main>
                  <Side>
                    <ReleaseStats organization={organization} release={release} project={project} location={location} selection={selection} hasHealthData={hasHealthData} getHealthData={getHealthData} isHealthLoading={isHealthLoading}/>
                    <ProjectReleaseDetails release={release} releaseMeta={releaseMeta} orgSlug={organization.slug} projectSlug={project.slug}/>
                    {commitCount > 0 && (<CommitAuthorBreakdown version={version} orgId={organization.slug} projectSlug={project.slug}/>)}
                    {releaseMeta.projects.length > 1 && (<OtherProjects projects={releaseMeta.projects.filter(function (p) { return p.slug !== project.slug; })} location={location} version={version} organization={organization}/>)}
                    {hasHealthData && (<TotalCrashFreeUsers organization={organization} version={version} projectSlug={project.slug} location={location}/>)}
                    {deploys.length > 0 && (<Deploys version={version} orgSlug={organization.slug} deploys={deploys} projectId={project.id}/>)}
                  </Side>
                </Body>);
                    }}
            </ReleaseDetailsRequest>);
            }}
      </ReleaseContext.Consumer>);
    };
    return ReleaseOverview;
}(AsyncView));
function generateTransactionLink(version, projectId, selection, value) {
    return function (organization, tableRow, _query) {
        var transaction = tableRow.transaction;
        var trendTransaction = ['regression', 'improved'].includes(value);
        var environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period;
        return transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transaction,
            query: {
                query: trendTransaction ? '' : "release:" + version,
                environment: environments,
                start: start ? getUtcDateString(start) : undefined,
                end: end ? getUtcDateString(end) : undefined,
                statsPeriod: period,
            },
            projectID: projectId.toString(),
            display: trendTransaction ? DisplayModes.TREND : DisplayModes.DURATION,
        });
    };
}
function getDropdownOptions() {
    return [
        {
            sort: { kind: 'desc', field: 'failure_count' },
            value: TransactionsListOption.FAILURE_COUNT,
            label: t('Failing Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'epm' },
            value: TransactionsListOption.TPM,
            label: t('Frequent Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p50' },
            value: TransactionsListOption.SLOW,
            label: t('Slow Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p75_measurements_lcp' },
            value: TransactionsListOption.SLOW_LCP,
            label: t('Slow LCP'),
        },
        {
            sort: { kind: 'desc', field: 'trend_percentage()' },
            query: [['t_test()', '<-6']],
            trendType: TrendChangeType.REGRESSION,
            value: TransactionsListOption.REGRESSION,
            label: t('Trending Regressions'),
        },
        {
            sort: { kind: 'asc', field: 'trend_percentage()' },
            query: [['t_test()', '>6']],
            trendType: TrendChangeType.IMPROVED,
            value: TransactionsListOption.IMPROVEMENT,
            label: t('Trending Improvements'),
        },
    ];
}
function getTransactionsListSort(location) {
    var sortOptions = getDropdownOptions();
    var urlParam = decodeScalar(location.query.showTransactions, TransactionsListOption.FAILURE_COUNT);
    var selectedSort = sortOptions.find(function (opt) { return opt.value === urlParam; }) || sortOptions[0];
    return { selectedSort: selectedSort, sortOptions: sortOptions };
}
var StyledPageTimeRangeSelector = styled(PageTimeRangeSelector)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1.5));
export default withApi(withGlobalSelection(withOrganization(ReleaseOverview)));
var templateObject_1;
//# sourceMappingURL=index.jsx.map