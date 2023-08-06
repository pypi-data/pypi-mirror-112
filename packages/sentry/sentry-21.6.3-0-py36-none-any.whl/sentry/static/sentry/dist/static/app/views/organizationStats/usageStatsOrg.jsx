import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import moment from 'moment';
import AsyncComponent from 'app/components/asyncComponent';
import OptionSelector from 'app/components/charts/optionSelector';
import { InlineContainer, SectionHeading } from 'app/components/charts/styles';
import { getSeriesApiInterval } from 'app/components/charts/utils';
import NotAvailable from 'app/components/notAvailable';
import ScoreCard from 'app/components/scoreCard';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { parsePeriodToHours } from 'app/utils/dates';
import { FORMAT_DATETIME_DAILY, FORMAT_DATETIME_HOURLY, getDateFromMoment, } from './usageChart/utils';
import { Outcome } from './types';
import UsageChart, { CHART_OPTIONS_DATA_TRANSFORM, ChartDataTransform, } from './usageChart';
import UsageStatsPerMin from './usageStatsPerMin';
import { formatUsageWithUnits, getFormatUsageOptions, isDisplayUtc } from './utils';
var UsageStatsOrganization = /** @class */ (function (_super) {
    __extends(UsageStatsOrganization, _super);
    function UsageStatsOrganization() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderChartFooter = function () {
            var handleChangeState = _this.props.handleChangeState;
            var _a = _this.state, loading = _a.loading, error = _a.error;
            var _b = _this.chartData, chartDateInterval = _b.chartDateInterval, chartTransform = _b.chartTransform, chartDateStartDisplay = _b.chartDateStartDisplay, chartDateEndDisplay = _b.chartDateEndDisplay, chartDateTimezoneDisplay = _b.chartDateTimezoneDisplay;
            return (<Footer>
        <InlineContainer>
          <FooterDate>
            <SectionHeading>{t('Date Range:')}</SectionHeading>
            <span>
              {loading || error ? (<NotAvailable />) : (tct('[start] — [end] ([timezone] UTC, [interval] interval)', {
                    start: chartDateStartDisplay,
                    end: chartDateEndDisplay,
                    timezone: chartDateTimezoneDisplay,
                    interval: chartDateInterval,
                }))}
            </span>
          </FooterDate>
        </InlineContainer>
        <InlineContainer>
          <OptionSelector title={t('Type')} selected={chartTransform} options={CHART_OPTIONS_DATA_TRANSFORM} onChange={function (val) {
                    return handleChangeState({ transform: val });
                }}/>
        </InlineContainer>
      </Footer>);
        };
        return _this;
    }
    UsageStatsOrganization.prototype.componentDidUpdate = function (prevProps) {
        var prevDateTime = prevProps.dataDatetime;
        var currDateTime = this.props.dataDatetime;
        if (prevDateTime.start !== currDateTime.start ||
            prevDateTime.end !== currDateTime.end ||
            prevDateTime.period !== currDateTime.period ||
            prevDateTime.utc !== currDateTime.utc) {
            this.reloadData();
        }
    };
    UsageStatsOrganization.prototype.getEndpoints = function () {
        return [['orgStats', this.endpointPath, { query: this.endpointQuery }]];
    };
    Object.defineProperty(UsageStatsOrganization.prototype, "endpointPath", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/stats_v2/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "endpointQuery", {
        get: function () {
            var dataDatetime = this.props.dataDatetime;
            var queryDatetime = dataDatetime.start && dataDatetime.end
                ? {
                    start: dataDatetime.start,
                    end: dataDatetime.end,
                    utc: dataDatetime.utc,
                }
                : {
                    statsPeriod: dataDatetime.period || DEFAULT_STATS_PERIOD,
                };
            return __assign(__assign({}, queryDatetime), { interval: getSeriesApiInterval(dataDatetime), groupBy: ['category', 'outcome'], field: ['sum(quantity)'] });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "chartData", {
        get: function () {
            var orgStats = this.state.orgStats;
            return __assign(__assign(__assign({}, this.mapSeriesToChart(orgStats)), this.chartDateRange), this.chartTransform);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "chartTransform", {
        get: function () {
            var chartTransform = this.props.chartTransform;
            switch (chartTransform) {
                case ChartDataTransform.CUMULATIVE:
                case ChartDataTransform.PERIODIC:
                    return { chartTransform: chartTransform };
                default:
                    return { chartTransform: ChartDataTransform.PERIODIC };
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "chartDateRange", {
        get: function () {
            var orgStats = this.state.orgStats;
            var dataDatetime = this.props.dataDatetime;
            var interval = getSeriesApiInterval(dataDatetime);
            // Use fillers as loading/error states will not display datetime at all
            if (!orgStats || !orgStats.intervals) {
                return {
                    chartDateInterval: interval,
                    chartDateStart: '',
                    chartDateEnd: '',
                    chartDateUtc: true,
                    chartDateStartDisplay: '',
                    chartDateEndDisplay: '',
                    chartDateTimezoneDisplay: '',
                };
            }
            var intervals = orgStats.intervals;
            var intervalHours = parsePeriodToHours(interval);
            // Keep datetime in UTC until we want to display it to users
            var startTime = moment(intervals[0]).utc();
            var endTime = intervals.length < 2
                ? moment(startTime) // when statsPeriod and interval is the same value
                : moment(intervals[intervals.length - 1]).utc();
            var useUtc = isDisplayUtc(dataDatetime);
            // If interval is a day or more, use UTC to format date. Otherwise, the date
            // may shift ahead/behind when converting to the user's local time.
            var FORMAT_DATETIME = intervalHours >= 24 ? FORMAT_DATETIME_DAILY : FORMAT_DATETIME_HOURLY;
            var xAxisStart = moment(startTime);
            var xAxisEnd = moment(endTime);
            var displayStart = useUtc ? moment(startTime).utc() : moment(startTime).local();
            var displayEnd = useUtc ? moment(endTime).utc() : moment(endTime).local();
            if (intervalHours < 24) {
                displayEnd.add(intervalHours, 'h');
            }
            return {
                chartDateInterval: interval,
                chartDateStart: xAxisStart.format(),
                chartDateEnd: xAxisEnd.format(),
                chartDateUtc: useUtc,
                chartDateStartDisplay: displayStart.format(FORMAT_DATETIME),
                chartDateEndDisplay: displayEnd.format(FORMAT_DATETIME),
                chartDateTimezoneDisplay: displayStart.format('Z'),
            };
        },
        enumerable: false,
        configurable: true
    });
    UsageStatsOrganization.prototype.mapSeriesToChart = function (orgStats) {
        var _a;
        var _this = this;
        var cardStats = {
            total: undefined,
            accepted: undefined,
            dropped: undefined,
            filtered: undefined,
        };
        var chartStats = {
            accepted: [],
            dropped: [],
            projected: [],
        };
        if (!orgStats) {
            return { cardStats: cardStats, chartStats: chartStats };
        }
        try {
            var dataCategory_1 = this.props.dataCategory;
            var _b = this.chartDateRange, chartDateInterval_1 = _b.chartDateInterval, chartDateUtc_1 = _b.chartDateUtc;
            var usageStats_1 = orgStats.intervals.map(function (interval) {
                var dateTime = moment(interval);
                return {
                    date: getDateFromMoment(dateTime, chartDateInterval_1, chartDateUtc_1),
                    total: 0,
                    accepted: 0,
                    filtered: 0,
                    dropped: { total: 0 },
                };
            });
            // Tally totals for card data
            var count_1 = (_a = {
                    total: 0
                },
                _a[Outcome.ACCEPTED] = 0,
                _a[Outcome.FILTERED] = 0,
                _a[Outcome.DROPPED] = 0,
                _a[Outcome.INVALID] = 0,
                _a[Outcome.RATE_LIMITED] = 0,
                _a);
            orgStats.groups.forEach(function (group) {
                var _a = group.by, outcome = _a.outcome, category = _a.category;
                // HACK: The backend enum are singular, but the frontend enums are plural
                if (!dataCategory_1.includes("" + category)) {
                    return;
                }
                count_1.total += group.totals['sum(quantity)'];
                count_1[outcome] += group.totals['sum(quantity)'];
                group.series['sum(quantity)'].forEach(function (stat, i) {
                    if (outcome === Outcome.ACCEPTED || outcome === Outcome.FILTERED) {
                        usageStats_1[i][outcome] += stat;
                        return;
                    }
                    // Breaking down into reasons for dropped is not needed
                    usageStats_1[i].dropped.total += stat;
                });
            });
            // Invalid and rate_limited data is combined with dropped
            count_1[Outcome.DROPPED] += count_1[Outcome.INVALID];
            count_1[Outcome.DROPPED] += count_1[Outcome.RATE_LIMITED];
            usageStats_1.forEach(function (stat) {
                stat.total = stat.accepted + stat.filtered + stat.dropped.total;
                // Chart Data
                chartStats.accepted.push({ value: [stat.date, stat.accepted] });
                chartStats.dropped.push({ value: [stat.date, stat.dropped.total] });
            });
            return {
                cardStats: {
                    total: formatUsageWithUnits(count_1.total, dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                    accepted: formatUsageWithUnits(count_1[Outcome.ACCEPTED], dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                    dropped: formatUsageWithUnits(count_1[Outcome.DROPPED], dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                    filtered: formatUsageWithUnits(count_1[Outcome.FILTERED], dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                },
                chartStats: chartStats,
            };
        }
        catch (err) {
            Sentry.withScope(function (scope) {
                scope.setContext('query', _this.endpointQuery);
                scope.setContext('body', orgStats);
                Sentry.captureException(err);
            });
            return {
                cardStats: cardStats,
                chartStats: chartStats,
                dataError: new Error('Failed to parse stats data'),
            };
        }
    };
    UsageStatsOrganization.prototype.renderCards = function () {
        var _a = this.props, dataCategory = _a.dataCategory, dataCategoryName = _a.dataCategoryName, organization = _a.organization;
        var loading = this.state.loading;
        var _b = this.chartData.cardStats, total = _b.total, accepted = _b.accepted, dropped = _b.dropped, filtered = _b.filtered;
        var cardMetadata = [
            {
                title: tct('Total [dataCategory]', { dataCategory: dataCategoryName }),
                value: total,
            },
            {
                title: t('Accepted'),
                help: tct('Accepted [dataCategory] were successfully processed by Sentry', {
                    dataCategory: dataCategory,
                }),
                value: accepted,
                secondaryValue: (<UsageStatsPerMin organization={organization} dataCategory={dataCategory}/>),
            },
            {
                title: t('Filtered'),
                help: tct('Filtered [dataCategory] were blocked due to your inbound data filter rules', { dataCategory: dataCategory }),
                value: filtered,
            },
            {
                title: t('Dropped'),
                help: tct('Dropped [dataCategory] were discarded due to invalid data, rate-limits, quota limits, or spike protection', { dataCategory: dataCategory }),
                value: dropped,
            },
        ];
        return cardMetadata.map(function (card, i) { return (<StyledScoreCard key={i} title={card.title} score={loading ? undefined : card.value} help={card.help} trend={card.secondaryValue}/>); });
    };
    UsageStatsOrganization.prototype.renderChart = function () {
        var dataCategory = this.props.dataCategory;
        var _a = this.state, error = _a.error, errors = _a.errors, loading = _a.loading;
        var _b = this.chartData, chartStats = _b.chartStats, dataError = _b.dataError, chartDateInterval = _b.chartDateInterval, chartDateStart = _b.chartDateStart, chartDateEnd = _b.chartDateEnd, chartDateUtc = _b.chartDateUtc, chartTransform = _b.chartTransform;
        var hasError = error || !!dataError;
        var chartErrors = dataError ? __assign(__assign({}, errors), { data: dataError }) : errors; // TODO(ts): AsyncComponent
        return (<UsageChart isLoading={loading} isError={hasError} errors={chartErrors} title=" " // Force the title to be blank
         footer={this.renderChartFooter()} dataCategory={dataCategory} dataTransform={chartTransform} usageDateStart={chartDateStart} usageDateEnd={chartDateEnd} usageDateShowUtc={chartDateUtc} usageDateInterval={chartDateInterval} usageStats={chartStats}/>);
    };
    UsageStatsOrganization.prototype.renderComponent = function () {
        return (<Fragment>
        {this.renderCards()}
        <ChartWrapper>{this.renderChart()}</ChartWrapper>
      </Fragment>);
    };
    return UsageStatsOrganization;
}(AsyncComponent));
export default UsageStatsOrganization;
var StyledScoreCard = styled(ScoreCard)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-column: auto / span 1;\n  margin: 0;\n"], ["\n  grid-column: auto / span 1;\n  margin: 0;\n"])));
var ChartWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1 / -1;\n"], ["\n  grid-column: 1 / -1;\n"])));
var Footer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  padding: ", " ", ";\n  border-top: 1px solid ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  padding: ", " ", ";\n  border-top: 1px solid ", ";\n"])), space(1), space(3), function (p) { return p.theme.border; });
var FooterDate = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n\n  > ", " {\n    margin-right: ", ";\n  }\n\n  > span:last-child {\n    font-weight: 400;\n    font-size: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n\n  > ", " {\n    margin-right: ", ";\n  }\n\n  > span:last-child {\n    font-weight: 400;\n    font-size: ", ";\n  }\n"])), SectionHeading, space(1.5), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=usageStatsOrg.jsx.map