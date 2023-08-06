import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import { Fragment } from 'react';
import { browserHistory } from 'react-router';
import { withTheme } from '@emotion/react';
import styled from '@emotion/styled';
import round from 'lodash/round';
import moment from 'moment';
import ErrorPanel from 'app/components/charts/errorPanel';
import { ChartContainer } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import Count from 'app/components/count';
import NotAvailable from 'app/components/notAvailable';
import { Panel, PanelTable } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import Radio from 'app/components/radio';
import { IconArrow, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { ReleaseComparisonChartType, SessionField, } from 'app/types';
import { defined, percent } from 'app/utils';
import { decodeScalar } from 'app/utils/queryString';
import { getCount, getCrashFreeRate, getCrashFreeSeries } from 'app/utils/sessions';
import { displayCrashFreePercent } from 'app/views/releases/utils';
import { generateReleaseMarkLine, releaseComparisonChartLabels } from '../../utils';
import { fillChartDataFromSessionsResponse, initSessionsBreakdownChartData, } from '../chart/utils';
import SessionsChart from './sessionsChart';
function ReleaseComparisonChart(_a) {
    var release = _a.release, project = _a.project, releaseSessions = _a.releaseSessions, allSessions = _a.allSessions, platform = _a.platform, location = _a.location, loading = _a.loading, reloading = _a.reloading, errored = _a.errored, theme = _a.theme;
    var activeChart = decodeScalar(location.query.chart, ReleaseComparisonChartType.CRASH_FREE_SESSIONS);
    var releaseCrashFreeSessions = getCrashFreeRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, SessionField.SESSIONS);
    var allCrashFreeSessions = getCrashFreeRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, SessionField.SESSIONS);
    var diffCrashFreeSessions = defined(releaseCrashFreeSessions) && defined(allCrashFreeSessions)
        ? releaseCrashFreeSessions - allCrashFreeSessions
        : null;
    var releaseCrashFreeUsers = getCrashFreeRate(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, SessionField.USERS);
    var allCrashFreeUsers = getCrashFreeRate(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, SessionField.USERS);
    var diffCrashFreeUsers = defined(releaseCrashFreeUsers) && defined(allCrashFreeUsers)
        ? releaseCrashFreeUsers - allCrashFreeUsers
        : null;
    var releaseSessionsCount = getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, SessionField.SESSIONS);
    var allSessionsCount = getCount(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, SessionField.SESSIONS);
    var diffSessionsCount = defined(releaseSessions) && defined(allSessions)
        ? percent(releaseSessionsCount - allSessionsCount, allSessionsCount)
        : null;
    var releaseUsersCount = getCount(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, SessionField.USERS);
    var allUsersCount = getCount(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, SessionField.USERS);
    var diffUsersCount = defined(releaseUsersCount) && defined(allUsersCount)
        ? percent(releaseUsersCount - allUsersCount, allUsersCount)
        : null;
    var charts = [
        {
            type: ReleaseComparisonChartType.CRASH_FREE_SESSIONS,
            thisRelease: defined(releaseCrashFreeSessions)
                ? displayCrashFreePercent(releaseCrashFreeSessions)
                : null,
            allReleases: defined(allCrashFreeSessions)
                ? displayCrashFreePercent(allCrashFreeSessions)
                : null,
            diff: defined(diffCrashFreeSessions)
                ? Math.abs(round(diffCrashFreeSessions, 3)) + "%"
                : null,
            diffDirection: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: diffCrashFreeSessions
                ? diffCrashFreeSessions > 0
                    ? 'green300'
                    : 'red300'
                : null,
        },
        {
            type: ReleaseComparisonChartType.CRASH_FREE_USERS,
            thisRelease: defined(releaseCrashFreeUsers)
                ? displayCrashFreePercent(releaseCrashFreeUsers)
                : null,
            allReleases: defined(allCrashFreeUsers)
                ? displayCrashFreePercent(allCrashFreeUsers)
                : null,
            diff: defined(diffCrashFreeUsers)
                ? Math.abs(round(diffCrashFreeUsers, 3)) + "%"
                : null,
            diffDirection: diffCrashFreeUsers ? (diffCrashFreeUsers > 0 ? 'up' : 'down') : null,
            diffColor: diffCrashFreeUsers
                ? diffCrashFreeUsers > 0
                    ? 'green300'
                    : 'red300'
                : null,
        },
        {
            type: ReleaseComparisonChartType.SESSION_COUNT,
            thisRelease: defined(releaseSessionsCount) ? (<Count value={releaseSessionsCount}/>) : null,
            allReleases: defined(allSessionsCount) ? <Count value={allSessionsCount}/> : null,
            diff: defined(diffSessionsCount)
                ? Math.abs(round(diffSessionsCount, 0)) + "%"
                : null,
            diffDirection: defined(diffSessionsCount)
                ? diffSessionsCount > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: null,
        },
        {
            type: ReleaseComparisonChartType.USER_COUNT,
            thisRelease: defined(releaseUsersCount) ? (<Count value={releaseUsersCount}/>) : null,
            allReleases: defined(allUsersCount) ? <Count value={allUsersCount}/> : null,
            diff: defined(diffUsersCount) ? Math.abs(round(diffUsersCount, 0)) + "%" : null,
            diffDirection: defined(diffUsersCount)
                ? diffUsersCount > 0
                    ? 'up'
                    : 'down'
                : null,
            diffColor: null,
        },
    ];
    function getSeries(chartType) {
        var _a;
        if (!releaseSessions) {
            return {};
        }
        var adoptionStages = (_a = release.adoptionStages) === null || _a === void 0 ? void 0 : _a[project.slug];
        var markLines = [
            generateReleaseMarkLine(t('Release Created'), moment(release.dateCreated).valueOf(), theme),
        ];
        if (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages.adopted) {
            markLines.push(generateReleaseMarkLine(t('Adopted'), moment(adoptionStages.adopted).valueOf(), theme));
        }
        if (adoptionStages === null || adoptionStages === void 0 ? void 0 : adoptionStages.unadopted) {
            markLines.push(generateReleaseMarkLine(t('Unadopted'), moment(adoptionStages.unadopted).valueOf(), theme));
        }
        switch (chartType) {
            case ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                return {
                    series: [
                        {
                            seriesName: t('This Release'),
                            connectNulls: true,
                            data: getCrashFreeSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, SessionField.SESSIONS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: t('All Releases'),
                            data: getCrashFreeSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, SessionField.SESSIONS),
                        },
                    ],
                    markLines: markLines,
                };
            case ReleaseComparisonChartType.CRASH_FREE_USERS:
                return {
                    series: [
                        {
                            seriesName: t('This Release'),
                            connectNulls: true,
                            data: getCrashFreeSeries(releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.groups, releaseSessions === null || releaseSessions === void 0 ? void 0 : releaseSessions.intervals, SessionField.USERS),
                        },
                    ],
                    previousSeries: [
                        {
                            seriesName: t('All Releases'),
                            data: getCrashFreeSeries(allSessions === null || allSessions === void 0 ? void 0 : allSessions.groups, allSessions === null || allSessions === void 0 ? void 0 : allSessions.intervals, SessionField.USERS),
                        },
                    ],
                    markLines: markLines,
                };
            case ReleaseComparisonChartType.SESSION_COUNT:
                return {
                    series: Object.values(fillChartDataFromSessionsResponse({
                        response: releaseSessions,
                        field: SessionField.SESSIONS,
                        groupBy: 'session.status',
                        chartData: initSessionsBreakdownChartData(),
                    })),
                    markLines: markLines,
                };
            case ReleaseComparisonChartType.USER_COUNT:
                return {
                    series: Object.values(fillChartDataFromSessionsResponse({
                        response: releaseSessions,
                        field: SessionField.USERS,
                        groupBy: 'session.status',
                        chartData: initSessionsBreakdownChartData(),
                    })),
                    markLines: markLines,
                };
            default:
                return {};
        }
    }
    function handleChartChange(chartType) {
        browserHistory.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { chart: chartType }) }));
    }
    var _b = getSeries(activeChart), series = _b.series, previousSeries = _b.previousSeries, markLines = _b.markLines;
    if (errored) {
        return (<Panel>
        <ErrorPanel>
          <IconWarning color="gray300" size="lg"/>
        </ErrorPanel>
      </Panel>);
    }
    return (<Fragment>
      <ChartPanel>
        <ChartContainer>
          <TransitionChart loading={loading} reloading={reloading}>
            <TransparentLoadingMask visible={reloading}/>

            <SessionsChart series={__spreadArray(__spreadArray([], __read((series !== null && series !== void 0 ? series : []))), __read((markLines !== null && markLines !== void 0 ? markLines : [])))} previousSeries={previousSeries !== null && previousSeries !== void 0 ? previousSeries : []} chartType={activeChart} platform={platform}/>
          </TransitionChart>
        </ChartContainer>
      </ChartPanel>
      <ChartTable headers={[
            <Cell key="stability" align="left">
            {t('Stability')}
          </Cell>,
            <Cell key="releases" align="right">
            {t('All Releases')}
          </Cell>,
            <Cell key="release" align="right">
            {t('This Release')}
          </Cell>,
            <Cell key="change" align="right">
            {t('Change')}
          </Cell>,
        ]}>
        {charts.map(function (_a) {
            var type = _a.type, thisRelease = _a.thisRelease, allReleases = _a.allReleases, diff = _a.diff, diffDirection = _a.diffDirection, diffColor = _a.diffColor;
            return (<Fragment key={type}>
                <Cell align="left">
                  <ChartToggle htmlFor={type}>
                    <Radio id={type} disabled={false} checked={type === activeChart} onChange={function () { return handleChartChange(type); }}/>
                    {releaseComparisonChartLabels[type]}
                  </ChartToggle>
                </Cell>
                <Cell align="right">
                  {loading ? <Placeholder height="20px"/> : allReleases}
                </Cell>
                <Cell align="right">
                  {loading ? <Placeholder height="20px"/> : thisRelease}
                </Cell>
                <Cell align="right">
                  {loading ? (<Placeholder height="20px"/>) : defined(diff) ? (<Change color={defined(diffColor) ? diffColor : undefined}>
                      {defined(diffDirection) && (<IconArrow direction={diffDirection} size="xs"/>)}{' '}
                      {diff}
                    </Change>) : (<NotAvailable />)}
                </Cell>
              </Fragment>);
        })}
      </ChartTable>
    </Fragment>);
}
var ChartPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom: none;\n  border-bottom-right-radius: 0;\n"], ["\n  margin-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom: none;\n  border-bottom-right-radius: 0;\n"])));
var ChartTable = styled(PanelTable)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr 1fr 1fr;\n  }\n"], ["\n  border-top-left-radius: 0;\n  border-top-right-radius: 0;\n\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr 1fr 1fr;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var Cell = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: ", ";\n  ", "\n"], ["\n  text-align: ", ";\n  ", "\n"])), function (p) { return p.align; }, overflowEllipsis);
var ChartToggle = styled('label')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-weight: 400;\n  margin-bottom: 0;\n  input {\n    flex-shrink: 0;\n    margin-right: ", " !important;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  font-weight: 400;\n  margin-bottom: 0;\n  input {\n    flex-shrink: 0;\n    margin-right: ", " !important;\n  }\n"])), space(1));
var Change = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return p.color && "color: " + p.theme[p.color]; });
export default withTheme(ReleaseComparisonChart);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map