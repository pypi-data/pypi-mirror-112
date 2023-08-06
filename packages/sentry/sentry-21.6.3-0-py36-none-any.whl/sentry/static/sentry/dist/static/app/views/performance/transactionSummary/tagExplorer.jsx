var _a;
import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import * as React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import { GuideAnchor } from 'app/components/assistant/guideAnchor';
import FeatureBadge from 'app/components/featureBadge';
import GridEditable, { COL_WIDTH_UNDEFINED, } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import Pagination from 'app/components/pagination';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { fromSorts, isFieldSortable } from 'app/utils/discover/eventView';
import { fieldAlignment } from 'app/utils/discover/fields';
import { formatPercentage } from 'app/utils/formatters';
import SegmentExplorerQuery from 'app/utils/performance/segmentExplorer/segmentExplorerQuery';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import CellAction, { Actions, updateQuery } from 'app/views/eventsV2/table/cellAction';
import { PerformanceDuration, platformAndConditionsToPerformanceType, PROJECT_PERFORMANCE_TYPE, } from '../utils';
import { tagsRouteWithQuery } from './transactionTags/utils';
import { SpanOperationBreakdownFilter } from './filter';
var TAGS_CURSOR_NAME = 'tags_cursor';
var COLUMN_ORDER = [
    {
        key: 'key',
        field: 'key',
        name: 'Tag Key',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'tagValue',
        field: 'tagValue',
        name: 'Tag Values',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'aggregate',
        field: 'aggregate',
        name: 'Avg Duration',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'frequency',
        field: 'frequency',
        name: 'Frequency',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'comparison',
        field: 'comparison',
        name: 'Compared To Avg',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'sumdelta',
        field: 'sumdelta',
        name: 'Total Time Lost',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
];
var filterToField = (_a = {},
    _a[SpanOperationBreakdownFilter.Browser] = 'spans.browser',
    _a[SpanOperationBreakdownFilter.Http] = 'spans.http',
    _a[SpanOperationBreakdownFilter.Db] = 'spans.db',
    _a[SpanOperationBreakdownFilter.Resource] = 'spans.resource',
    _a);
export var getTransactionField = function (currentFilter, projects, eventView) {
    var fieldFromFilter = filterToField[currentFilter];
    if (fieldFromFilter) {
        return fieldFromFilter;
    }
    var performanceType = platformAndConditionsToPerformanceType(projects, eventView);
    if (performanceType === PROJECT_PERFORMANCE_TYPE.FRONTEND) {
        return 'measurements.lcp';
    }
    return 'transaction.duration';
};
var getColumnsWithReplacedDuration = function (currentFilter, projects, eventView) {
    var columns = COLUMN_ORDER.map(function (c) { return (__assign({}, c)); });
    var durationColumn = columns.find(function (c) { return c.key === 'aggregate'; });
    if (!durationColumn) {
        return columns;
    }
    var fieldFromFilter = filterToField[currentFilter];
    if (fieldFromFilter) {
        durationColumn.name = 'Avg Span Duration';
        return columns;
    }
    var performanceType = platformAndConditionsToPerformanceType(projects, eventView);
    if (performanceType === PROJECT_PERFORMANCE_TYPE.FRONTEND) {
        durationColumn.name = 'Avg LCP';
        return columns;
    }
    return columns;
};
export function TagValue(props) {
    return <div className="truncate">{props.row.tags_value}</div>;
}
var _TagExplorer = /** @class */ (function (_super) {
    __extends(_TagExplorer, _super);
    function _TagExplorer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = __spreadArray([], __read(_this.state.widths));
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        _this.getColumnOrder = function (columns) {
            var widths = _this.state.widths;
            return columns.map(function (col, i) {
                if (typeof widths[i] === 'number') {
                    return __assign(__assign({}, col), { width: widths[i] });
                }
                return col;
            });
        };
        _this.renderHeadCellWithMeta = function (sortedEventView, tableMeta, columns) {
            return function (column, index) {
                return _this.renderHeadCell(sortedEventView, tableMeta, column, columns[index]);
            };
        };
        _this.handleTagValueClick = function (location, tagKey, tagValue) {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.tag_explorer.tag_value',
                eventName: 'Performance Views: Tag Explorer Value Clicked',
                organization_id: parseInt(organization.id, 10),
            });
            var queryString = decodeScalar(location.query.query);
            var conditions = tokenizeSearch(queryString || '');
            conditions.addTagValues(tagKey, [tagValue]);
            var query = conditions.formatString();
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { query: String(query).trim() }),
            });
        };
        _this.handleCellAction = function (column, tagValue, actionRow) {
            return function (action) {
                var _a;
                var _b = _this.props, eventView = _b.eventView, location = _b.location, organization = _b.organization;
                trackAnalyticsEvent({
                    eventKey: 'performance_views.summary.tag_explorer.cell_action',
                    eventName: 'Performance Views: Tag Explorer Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                });
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                updateQuery(searchConditions, action, __assign(__assign({}, column), { name: actionRow.id }), tagValue);
                browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), (_a = {}, _a[TAGS_CURSOR_NAME] = undefined, _a.query = searchConditions.formatString(), _a)),
                });
            };
        };
        _this.renderBodyCell = function (parentProps, column, dataRow) {
            var value = dataRow[column.key];
            var location = parentProps.location, organization = parentProps.organization, transactionName = parentProps.transactionName;
            if (column.key === 'key') {
                var target_1 = tagsRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: decodeScalar(location.query.project),
                    query: __assign(__assign({}, location.query), { tagKey: dataRow.tags_key }),
                });
                return (<Feature features={['performance-tag-page']} organization={organization}>
          {function (_a) {
                        var hasFeature = _a.hasFeature;
                        if (hasFeature) {
                            return <Link to={target_1}>{dataRow.tags_key}</Link>;
                        }
                        return dataRow.tags_key;
                    }}
        </Feature>);
            }
            var allowActions = [Actions.ADD, Actions.EXCLUDE];
            if (column.key === 'tagValue') {
                var actionRow = __assign(__assign({}, dataRow), { id: dataRow.tags_key });
                return (<CellAction column={column} dataRow={actionRow} handleCellAction={_this.handleCellAction(column, dataRow.tags_value, actionRow)} allowActions={allowActions}>
          <Feature features={['performance-tag-page']} organization={organization}>
            {function (_a) {
                        var hasFeature = _a.hasFeature;
                        if (hasFeature) {
                            return <div className="truncate">{dataRow.tags_value}</div>;
                        }
                        return (<Link to="" onClick={function () {
                                return _this.handleTagValueClick(location, dataRow.tags_key, dataRow.tags_value);
                            }}>
                  <TagValue row={dataRow}/>
                </Link>);
                    }}
          </Feature>
        </CellAction>);
            }
            if (column.key === 'frequency') {
                return <AlignRight>{formatPercentage(dataRow.frequency, 0)}</AlignRight>;
            }
            if (column.key === 'comparison') {
                var localValue = dataRow.comparison;
                var pct = formatPercentage(localValue - 1, 0);
                return (<AlignRight>
          {localValue > 1 ? t('+%s slower', pct) : t('%s faster', pct)}
        </AlignRight>);
            }
            if (column.key === 'aggregate') {
                return (<AlignRight>
          <PerformanceDuration abbreviation milliseconds={dataRow.aggregate}/>
        </AlignRight>);
            }
            if (column.key === 'sumdelta') {
                return (<AlignRight>
          <PerformanceDuration abbreviation milliseconds={dataRow.sumdelta}/>
        </AlignRight>);
            }
            return value;
        };
        _this.renderBodyCellWithData = function (parentProps) {
            return function (column, dataRow) {
                return _this.renderBodyCell(parentProps, column, dataRow);
            };
        };
        return _this;
    }
    _TagExplorer.prototype.onSortClick = function (currentSortKind, currentSortField) {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.summary.tag_explorer.sort',
            eventName: 'Performance Views: Tag Explorer Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    };
    _TagExplorer.prototype.renderHeadCell = function (sortedEventView, tableMeta, column, columnInfo) {
        var _this = this;
        var location = this.props.location;
        var align = fieldAlignment(column.key, column.type, tableMeta);
        var field = { field: column.key, width: column.width };
        function generateSortLink() {
            var _a;
            if (!tableMeta) {
                return undefined;
            }
            var nextEventView = sortedEventView.sortOnField(field, tableMeta);
            var sort = nextEventView.generateQueryStringObject().sort;
            return __assign(__assign({}, location), { query: __assign(__assign({}, location.query), (_a = {}, _a[TAGS_CURSOR_NAME] = undefined, _a.tagSort = sort, _a)) });
        }
        var currentSort = sortedEventView.sortForField(field, tableMeta);
        var canSort = isFieldSortable(field, tableMeta);
        var currentSortKind = currentSort ? currentSort.kind : undefined;
        var currentSortField = currentSort ? currentSort.field : undefined;
        return (<SortLink align={align} title={columnInfo.name} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={function () { return _this.onSortClick(currentSortKind, currentSortField); }}/>);
    };
    _TagExplorer.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var _c = this.props, eventView = _c.eventView, organization = _c.organization, location = _c.location, currentFilter = _c.currentFilter, projects = _c.projects;
        var tagSort = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a.tagSort);
        var cursor = decodeScalar((_b = location.query) === null || _b === void 0 ? void 0 : _b[TAGS_CURSOR_NAME]);
        var tagEventView = eventView.clone();
        tagEventView.fields = COLUMN_ORDER;
        var tagSorts = fromSorts(tagSort);
        var sortedEventView = tagEventView.withSorts(tagSorts.length
            ? tagSorts
            : [
                {
                    field: 'sumdelta',
                    kind: 'desc',
                },
            ]);
        var aggregateColumn = getTransactionField(currentFilter, projects, sortedEventView);
        var adjustedColumns = getColumnsWithReplacedDuration(currentFilter, projects, sortedEventView);
        var columns = this.getColumnOrder(adjustedColumns);
        var columnSortBy = sortedEventView.getSorts();
        return (<SegmentExplorerQuery eventView={sortedEventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={5} cursor={cursor}>
        {function (_a) {
                var isLoading = _a.isLoading, tableData = _a.tableData, pageLinks = _a.pageLinks;
                return (<React.Fragment>
              <GuideAnchor target="tag_explorer">
                <TagsHeader organization={organization} pageLinks={pageLinks}/>
              </GuideAnchor>
              <GridEditable isLoading={isLoading} data={tableData && tableData.data ? tableData.data : []} columnOrder={columns} columnSortBy={columnSortBy} grid={{
                        renderHeadCell: _this.renderHeadCellWithMeta(sortedEventView, (tableData === null || tableData === void 0 ? void 0 : tableData.meta) || {}, adjustedColumns),
                        renderBodyCell: _this.renderBodyCellWithData(_this.props),
                        onResizeColumn: _this.handleResizeColumn,
                    }} location={location}/>
            </React.Fragment>);
            }}
      </SegmentExplorerQuery>);
    };
    return _TagExplorer;
}(React.Component));
function TagsHeader(props) {
    var pageLinks = props.pageLinks, organization = props.organization;
    var handleCursor = function (cursor, pathname, query) {
        var _a;
        trackAnalyticsEvent({
            eventKey: 'performance_views.summary.tag_explorer.change_page',
            eventName: 'Performance Views: Tag Explorer Change Page',
            organization_id: parseInt(organization.id, 10),
        });
        browserHistory.push({
            pathname: pathname,
            query: __assign(__assign({}, query), (_a = {}, _a[TAGS_CURSOR_NAME] = cursor, _a)),
        });
    };
    return (<Header>
      <SectionHeading>
        <div>
          {t('Suspect Tags')}
          <FeatureBadge type="beta" noTooltip/>
        </div>
      </SectionHeading>
      <StyledPagination pageLinks={pageLinks} onCursor={handleCursor} size="small"/>
    </Header>);
}
export var SectionHeading = styled('h4')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  margin: ", " 0;\n  line-height: 1.3;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  margin: ", " 0;\n  line-height: 1.3;\n"])), space(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(1));
var AlignRight = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var Header = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"])), space(1));
var StyledPagination = styled(Pagination)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0 0 0 ", ";\n"], ["\n  margin: 0 0 0 ", ";\n"])), space(1));
export var TagExplorer = _TagExplorer;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=tagExplorer.jsx.map