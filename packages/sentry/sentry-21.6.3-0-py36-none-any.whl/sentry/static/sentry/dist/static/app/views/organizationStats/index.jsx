import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import pick from 'lodash/pick';
import moment from 'moment';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import ErrorBoundary from 'app/components/errorBoundary';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import PageTimeRangeSelector from 'app/components/organizations/timeRangeSelector/pageTimeRangeSelector';
import PageHeading from 'app/components/pageHeading';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { DEFAULT_RELATIVE_PERIODS, DEFAULT_STATS_PERIOD } from 'app/constants';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { DataCategory, DataCategoryName, } from 'app/types';
import withOrganization from 'app/utils/withOrganization';
import { CHART_OPTIONS_DATACATEGORY } from './usageChart';
import UsageStatsOrg from './usageStatsOrg';
import UsageStatsProjects from './usageStatsProjects';
var PAGE_QUERY_PARAMS = [
    'pageStatsPeriod',
    'pageStart',
    'pageEnd',
    'pageUtc',
    'dataCategory',
    'transform',
    'sort',
    'query',
    'cursor',
];
var OrganizationStats = /** @class */ (function (_super) {
    __extends(OrganizationStats, _super);
    function OrganizationStats() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getNextLocations = function (project) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var nextLocation = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { project: project.id }) });
            // Do not leak out page-specific keys
            nextLocation.query = omit(nextLocation.query, PAGE_QUERY_PARAMS);
            return {
                performance: __assign(__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/performance/" }),
                projectDetail: __assign(__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/projects/" + project.slug + "/" }),
                issueList: __assign(__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/issues/" }),
                settings: {
                    pathname: "/settings/" + organization.slug + "/projects/" + project.slug + "/",
                },
            };
        };
        _this.handleUpdateDatetime = function (datetime) {
            var start = datetime.start, end = datetime.end, relative = datetime.relative, utc = datetime.utc;
            if (start && end) {
                var parser = utc ? moment.utc : moment;
                return _this.setStateOnUrl({
                    pageStatsPeriod: undefined,
                    pageStart: parser(start).format(),
                    pageEnd: parser(end).format(),
                    pageUtc: utc !== null && utc !== void 0 ? utc : undefined,
                });
            }
            return _this.setStateOnUrl({
                pageStatsPeriod: relative || undefined,
                pageStart: undefined,
                pageEnd: undefined,
                pageUtc: undefined,
            });
        };
        /**
         * TODO: Enable user to set dateStart/dateEnd
         *
         * See PAGE_QUERY_PARAMS for list of accepted keys on nextState
         */
        _this.setStateOnUrl = function (nextState, options) {
            if (options === void 0) { options = {
                willUpdateRouter: true,
            }; }
            var _a = _this.props, location = _a.location, router = _a.router;
            var nextQueryParams = pick(nextState, PAGE_QUERY_PARAMS);
            var nextLocation = __assign(__assign({}, location), { query: __assign(__assign({}, location === null || location === void 0 ? void 0 : location.query), nextQueryParams) });
            if (options.willUpdateRouter) {
                router.push(nextLocation);
            }
            return nextLocation;
        };
        _this.renderPageControl = function () {
            var organization = _this.props.organization;
            var _a = _this.dataDatetime, start = _a.start, end = _a.end, period = _a.period, utc = _a.utc;
            return (<Fragment>
        <StyledPageTimeRangeSelector organization={organization} relative={period !== null && period !== void 0 ? period : ''} start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} utc={utc !== null && utc !== void 0 ? utc : null} onUpdate={_this.handleUpdateDatetime} relativeOptions={omit(DEFAULT_RELATIVE_PERIODS, ['1h'])}/>

        <DropdownDataCategory label={<DropdownLabel>
              <span>{t('Event Type: ')}</span>
              <span>{_this.dataCategoryName}</span>
            </DropdownLabel>}>
          {CHART_OPTIONS_DATACATEGORY.map(function (option) { return (<DropdownItem key={option.value} eventKey={option.value} onSelect={function (val) {
                        return _this.setStateOnUrl({ dataCategory: val });
                    }}>
              {option.label}
            </DropdownItem>); })}
        </DropdownDataCategory>
      </Fragment>);
        };
        return _this;
    }
    Object.defineProperty(OrganizationStats.prototype, "dataCategory", {
        get: function () {
            var _a, _b;
            var dataCategory = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.dataCategory;
            switch (dataCategory) {
                case DataCategory.ERRORS:
                case DataCategory.TRANSACTIONS:
                case DataCategory.ATTACHMENTS:
                    return dataCategory;
                default:
                    return DataCategory.ERRORS;
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "dataCategoryName", {
        get: function () {
            var _a;
            var dataCategory = this.dataCategory;
            return (_a = DataCategoryName[dataCategory]) !== null && _a !== void 0 ? _a : t('Unknown Data Category');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "dataDatetime", {
        get: function () {
            var _a, _b;
            var query = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) !== null && _b !== void 0 ? _b : {};
            var _c = getParams(query, {
                allowEmptyPeriod: true,
                allowAbsoluteDatetime: true,
                allowAbsolutePageDatetime: true,
            }), start = _c.start, end = _c.end, statsPeriod = _c.statsPeriod, utcString = _c.utc;
            if (!statsPeriod && !start && !end) {
                return { period: DEFAULT_STATS_PERIOD };
            }
            // Following getParams, statsPeriod will take priority over start/end
            if (statsPeriod) {
                return { period: statsPeriod };
            }
            var utc = utcString === 'true';
            if (start && end) {
                return utc
                    ? {
                        start: moment.utc(start).format(),
                        end: moment.utc(end).format(),
                        utc: utc,
                    }
                    : {
                        start: moment(start).utc().format(),
                        end: moment(end).utc().format(),
                        utc: utc,
                    };
            }
            return { period: DEFAULT_STATS_PERIOD };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "chartTransform", {
        // Validation and type-casting should be handled by chart
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.transform;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "tableSort", {
        // Validation and type-casting should be handled by table
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.sort;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "tableQuery", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.query;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "tableCursor", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.cursor;
        },
        enumerable: false,
        configurable: true
    });
    OrganizationStats.prototype.render = function () {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title="Usage Stats">
        <PageContent>
          <PageHeader>
            <PageHeading>{t('Organization Usage Stats')}</PageHeading>
          </PageHeader>

          <p>
            {t('We collect usage metrics on three types of events: errors, transactions, and attachments. The charts below reflect events that Sentry has received across your entire organization. You can also find them broken down by project in the table.')}
          </p>

          <PageGrid>
            {this.renderPageControl()}

            <ErrorBoundary mini>
              <UsageStatsOrg organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataDatetime} chartTransform={this.chartTransform} handleChangeState={this.setStateOnUrl}/>
            </ErrorBoundary>
            <ErrorBoundary mini>
              <UsageStatsProjects organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataDatetime} tableSort={this.tableSort} tableQuery={this.tableQuery} tableCursor={this.tableCursor} handleChangeState={this.setStateOnUrl} getNextLocations={this.getNextLocations}/>
            </ErrorBoundary>
          </PageGrid>
        </PageContent>
      </SentryDocumentTitle>);
    };
    return OrganizationStats;
}(Component));
export { OrganizationStats };
export default withOrganization(OrganizationStats);
var PageGrid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, 1fr);\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, 1fr);\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
var DropdownDataCategory = styled(DropdownControl)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 42px;\n  grid-column: auto / span 1;\n  justify-self: stretch;\n  align-self: stretch;\n\n  button {\n    width: 100%;\n    height: 100%;\n\n    > span {\n      display: flex;\n      justify-content: space-between;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 1;\n  }\n"], ["\n  height: 42px;\n  grid-column: auto / span 1;\n  justify-self: stretch;\n  align-self: stretch;\n\n  button {\n    width: 100%;\n    height: 100%;\n\n    > span {\n      display: flex;\n      justify-content: space-between;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 1;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
var StyledPageTimeRangeSelector = styled(PageTimeRangeSelector)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-column: auto / span 1;\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 3;\n  }\n"], ["\n  grid-column: auto / span 1;\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 3;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
var DropdownLabel = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"], ["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map