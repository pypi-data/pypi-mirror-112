import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import AsyncComponent from 'app/components/asyncComponent';
import SortLink from 'app/components/gridEditable/sortLink';
import Pagination from 'app/components/pagination';
import SearchBar from 'app/components/searchBar';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t } from 'app/locale';
import { DataCategory } from 'app/types';
import withProjects from 'app/utils/withProjects';
import UsageTable, { CellProject, CellStat } from './usageTable';
export var SortBy;
(function (SortBy) {
    SortBy["PROJECT"] = "project";
    SortBy["TOTAL"] = "total";
    SortBy["ACCEPTED"] = "accepted";
    SortBy["FILTERED"] = "filtered";
    SortBy["DROPPED"] = "dropped";
    SortBy["INVALID"] = "invalid";
    SortBy["RATE_LIMITED"] = "rate_limited";
})(SortBy || (SortBy = {}));
var UsageStatsProjects = /** @class */ (function (_super) {
    __extends(UsageStatsProjects, _super);
    function UsageStatsProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeSort = function (nextKey) {
            var handleChangeState = _this.props.handleChangeState;
            var _a = _this.tableSort, key = _a.key, direction = _a.direction;
            var nextDirection = 1; // Default to descending
            if (key === nextKey) {
                nextDirection = direction * -1; // Toggle if clicking on the same column
            }
            else if (nextKey === SortBy.PROJECT) {
                nextDirection = -1; // Default PROJECT to ascending
            }
            // The header uses SortLink, which takes a LocationDescriptor and pushes
            // that to the router. As such, we do not need to update the router in
            // handleChangeState
            return handleChangeState({ sort: "" + (nextDirection > 0 ? '-' : '') + nextKey }, { willUpdateRouter: false });
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, handleChangeState = _a.handleChangeState, tableQuery = _a.tableQuery;
            if (query === tableQuery) {
                return;
            }
            if (!query) {
                handleChangeState({ query: undefined, cursor: undefined });
                return;
            }
            handleChangeState({ query: query, cursor: undefined });
        };
        return _this;
    }
    UsageStatsProjects.prototype.componentDidUpdate = function (prevProps) {
        var prevDateTime = prevProps.dataDatetime, prevDataCategory = prevProps.dataCategory;
        var _a = this.props, currDateTime = _a.dataDatetime, currDataCategory = _a.dataCategory;
        if (prevDateTime.start !== currDateTime.start ||
            prevDateTime.end !== currDateTime.end ||
            prevDateTime.period !== currDateTime.period ||
            prevDateTime.utc !== currDateTime.utc ||
            currDataCategory !== prevDataCategory) {
            this.reloadData();
        }
    };
    UsageStatsProjects.prototype.getEndpoints = function () {
        return [['projectStats', this.endpointPath, { query: this.endpointQuery }]];
    };
    Object.defineProperty(UsageStatsProjects.prototype, "endpointPath", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/stats_v2/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "endpointQuery", {
        get: function () {
            var _a = this.props, dataDatetime = _a.dataDatetime, dataCategory = _a.dataCategory;
            var queryDatetime = dataDatetime.start && dataDatetime.end
                ? {
                    start: dataDatetime.start,
                    end: dataDatetime.end,
                    utc: dataDatetime.utc,
                }
                : {
                    statsPeriod: dataDatetime.period || DEFAULT_STATS_PERIOD,
                };
            // We do not need more granularity in the data so interval is '1d'
            return __assign(__assign({}, queryDatetime), { interval: '1d', groupBy: ['outcome', 'project'], field: ['sum(quantity)'], project: '-1', category: dataCategory.slice(0, -1) });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "tableData", {
        get: function () {
            var projectStats = this.state.projectStats;
            return __assign({ headers: this.tableHeader }, this.mapSeriesToTable(projectStats));
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "tableSort", {
        get: function () {
            var tableSort = this.props.tableSort;
            if (!tableSort) {
                return {
                    key: SortBy.TOTAL,
                    direction: 1,
                };
            }
            var key = tableSort;
            var direction = -1;
            if (tableSort.charAt(0) === '-') {
                key = key.slice(1);
                direction = 1;
            }
            switch (key) {
                case SortBy.PROJECT:
                case SortBy.TOTAL:
                case SortBy.ACCEPTED:
                case SortBy.FILTERED:
                case SortBy.DROPPED:
                    return { key: key, direction: direction };
                default:
                    return { key: SortBy.ACCEPTED, direction: -1 };
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "tableCursor", {
        get: function () {
            var tableCursor = this.props.tableCursor;
            var offset = Number(tableCursor === null || tableCursor === void 0 ? void 0 : tableCursor.split(':')[1]);
            return isNaN(offset) ? 0 : offset;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "pageLink", {
        /**
         * OrganizationStatsEndpointV2 does not have any performance issues. We use
         * client-side pagination to limit the number of rows on the table so the
         * page doesn't scroll too deeply for organizations with a lot of projects
         */
        get: function () {
            var numRows = this.filteredProjects.length;
            var offset = this.tableCursor;
            var prevOffset = offset - UsageStatsProjects.MAX_ROWS_USAGE_TABLE;
            var nextOffset = offset + UsageStatsProjects.MAX_ROWS_USAGE_TABLE;
            return "<link>; rel=\"previous\"; results=\"" + (prevOffset >= 0) + "\"; cursor=\"0:" + Math.max(0, prevOffset) + ":1\", <link>; rel=\"next\"; results=\"" + (nextOffset < numRows) + "\"; cursor=\"0:" + nextOffset + ":0\"";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "filteredProjects", {
        /**
         * Filter projects if there's a query
         */
        get: function () {
            var _a = this.props, projects = _a.projects, tableQuery = _a.tableQuery;
            return tableQuery
                ? projects.filter(function (p) { return p.slug.includes(tableQuery) && p.hasAccess; })
                : projects.filter(function (p) { return p.hasAccess; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "tableHeader", {
        get: function () {
            var _this = this;
            var _a = this.tableSort, key = _a.key, direction = _a.direction;
            var getArrowDirection = function (linkKey) {
                if (linkKey !== key) {
                    return undefined;
                }
                return direction > 0 ? 'desc' : 'asc';
            };
            return [
                {
                    key: SortBy.PROJECT,
                    title: t('Project'),
                    align: 'left',
                    direction: getArrowDirection(SortBy.PROJECT),
                    onClick: function () { return _this.handleChangeSort(SortBy.PROJECT); },
                },
                {
                    key: SortBy.TOTAL,
                    title: t('Total'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.TOTAL),
                    onClick: function () { return _this.handleChangeSort(SortBy.TOTAL); },
                },
                {
                    key: SortBy.ACCEPTED,
                    title: t('Accepted'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.ACCEPTED),
                    onClick: function () { return _this.handleChangeSort(SortBy.ACCEPTED); },
                },
                {
                    key: SortBy.FILTERED,
                    title: t('Filtered'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.FILTERED),
                    onClick: function () { return _this.handleChangeSort(SortBy.FILTERED); },
                },
                {
                    key: SortBy.DROPPED,
                    title: t('Dropped'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.DROPPED),
                    onClick: function () { return _this.handleChangeSort(SortBy.DROPPED); },
                },
            ].map(function (h) {
                var Cell = h.key === SortBy.PROJECT ? CellProject : CellStat;
                return (<Cell key={h.key}>
          <SortLink canSort title={h.title} align={h.align} direction={h.direction} generateSortLink={h.onClick}/>
        </Cell>);
            });
        },
        enumerable: false,
        configurable: true
    });
    UsageStatsProjects.prototype.getProjectLink = function (project) {
        var _a = this.props, dataCategory = _a.dataCategory, getNextLocations = _a.getNextLocations, organization = _a.organization;
        var _b = getNextLocations(project), performance = _b.performance, projectDetail = _b.projectDetail, settings = _b.settings;
        if (dataCategory === DataCategory.TRANSACTIONS &&
            organization.features.includes('performance-view')) {
            return {
                projectLink: performance,
                projectSettingsLink: settings,
            };
        }
        return {
            projectLink: projectDetail,
            projectSettingsLink: settings,
        };
    };
    UsageStatsProjects.prototype.mapSeriesToTable = function (projectStats) {
        var _a;
        var _this = this;
        if (!projectStats) {
            return { tableStats: [] };
        }
        var stats = {};
        try {
            var baseStat_1 = (_a = {},
                _a[SortBy.TOTAL] = 0,
                _a[SortBy.ACCEPTED] = 0,
                _a[SortBy.FILTERED] = 0,
                _a[SortBy.DROPPED] = 0,
                _a);
            var projectList = this.filteredProjects;
            var projectSet_1 = new Set(projectList.map(function (p) { return p.id; }));
            projectStats.groups.forEach(function (group) {
                var _a = group.by, outcome = _a.outcome, projectId = _a.project;
                // Backend enum is singlar. Frontend enum is plural.
                if (!projectSet_1.has(projectId.toString())) {
                    return;
                }
                if (!stats[projectId]) {
                    stats[projectId] = __assign({}, baseStat_1);
                }
                stats[projectId].total += group.totals['sum(quantity)'];
                if (outcome === SortBy.ACCEPTED ||
                    outcome === SortBy.FILTERED ||
                    outcome === SortBy.DROPPED) {
                    stats[projectId][outcome] += group.totals['sum(quantity)'];
                }
                else {
                    stats[projectId][SortBy.DROPPED] += group.totals['sum(quantity)'];
                }
            });
            // For projects without stats, fill in with zero
            var tableStats = projectList.map(function (proj) {
                var _a;
                var stat = (_a = stats[proj.id]) !== null && _a !== void 0 ? _a : __assign({}, baseStat_1);
                return __assign(__assign({ project: __assign({}, proj) }, _this.getProjectLink(proj)), stat);
            });
            var _b = this.tableSort, key_1 = _b.key, direction_1 = _b.direction;
            tableStats.sort(function (a, b) {
                if (key_1 === SortBy.PROJECT) {
                    return b.project.slug.localeCompare(a.project.slug) * direction_1;
                }
                return a[key_1] !== b[key_1]
                    ? (b[key_1] - a[key_1]) * direction_1
                    : a.project.slug.localeCompare(b.project.slug);
            });
            var offset = this.tableCursor;
            return {
                tableStats: tableStats.slice(offset, offset + UsageStatsProjects.MAX_ROWS_USAGE_TABLE),
            };
        }
        catch (err) {
            Sentry.withScope(function (scope) {
                scope.setContext('query', _this.endpointQuery);
                scope.setContext('body', projectStats);
                Sentry.captureException(err);
            });
            return {
                tableStats: [],
                error: err,
            };
        }
    };
    UsageStatsProjects.prototype.renderComponent = function () {
        var _a = this.state, error = _a.error, errors = _a.errors, loading = _a.loading;
        var _b = this.props, dataCategory = _b.dataCategory, loadingProjects = _b.loadingProjects, tableQuery = _b.tableQuery;
        var _c = this.tableData, headers = _c.headers, tableStats = _c.tableStats;
        return (<Fragment>
        <GridRow>
          <SearchBar defaultQuery="" query={tableQuery} placeholder={t('Filter your projects')} onSearch={this.handleSearch}/>
        </GridRow>

        <GridRow>
          <UsageTable isLoading={loading || loadingProjects} isError={error} errors={errors} // TODO(ts)
         isEmpty={tableStats.length === 0} headers={headers} dataCategory={dataCategory} usageStats={tableStats}/>
          <Pagination pageLinks={this.pageLink}/>
        </GridRow>
      </Fragment>);
    };
    UsageStatsProjects.MAX_ROWS_USAGE_TABLE = 25;
    return UsageStatsProjects;
}(AsyncComponent));
export default withProjects(UsageStatsProjects);
var GridRow = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-column: 1 / -1;\n"], ["\n  grid-column: 1 / -1;\n"])));
var templateObject_1;
//# sourceMappingURL=usageStatsProjects.jsx.map