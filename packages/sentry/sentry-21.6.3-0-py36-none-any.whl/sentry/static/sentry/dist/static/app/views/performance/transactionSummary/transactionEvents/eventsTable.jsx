import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import * as React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import GridEditable, { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import Pagination from 'app/components/pagination';
import QuestionTooltip from 'app/components/questionTooltip';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { isFieldSortable } from 'app/utils/discover/eventView';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { fieldAlignment, getAggregateAlias, isSpanOperationBreakdownField, SPAN_OP_RELATIVE_BREAKDOWN_FIELD, } from 'app/utils/discover/fields';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import CellAction, { Actions, updateQuery } from 'app/views/eventsV2/table/cellAction';
import { COLUMN_TITLES } from '../../data';
import { generateTraceLink, generateTransactionLink } from '../utils';
import OperationSort from './operationSort';
export function getProjectID(eventData, projects) {
    var projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    var project = projects.find(function (currentProject) { return currentProject.slug === projectSlug; });
    if (!project) {
        return undefined;
    }
    return project.id;
}
var OperationTitle = /** @class */ (function (_super) {
    __extends(OperationTitle, _super);
    function OperationTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OperationTitle.prototype.render = function () {
        var onClick = this.props.onClick;
        return (<div onClick={onClick}>
        <span>{t('operation duration')}</span>
        <StyledIconQuestion size="xs" position="top" title={t("Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once.")}/>
      </div>);
    };
    return OperationTitle;
}(React.Component));
var EventsTable = /** @class */ (function (_super) {
    __extends(EventsTable, _super);
    function EventsTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
                trackAnalyticsEvent({
                    eventKey: 'performance_views.transactionEvents.cellaction',
                    eventName: 'Performance Views: Transaction Events Tab Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                updateQuery(searchConditions, action, column, value);
                ReactRouter.browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { cursor: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        _this.renderBodyCellWithData = function (tableData) {
            return function (column, dataRow) { return _this.renderBodyCell(tableData, column, dataRow); };
        };
        _this.renderHeadCellWithMeta = function (tableMeta) {
            var _a;
            var columnTitles = (_a = _this.props.columnTitles) !== null && _a !== void 0 ? _a : COLUMN_TITLES;
            return function (column, index) {
                return _this.renderHeadCell(tableMeta, column, columnTitles[index]);
            };
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = __spreadArray([], __read(_this.state.widths));
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        return _this;
    }
    EventsTable.prototype.renderBodyCell = function (tableData, column, dataRow) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, transactionName = _a.transactionName;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        var fieldRenderer = getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location, eventView: eventView });
        var allowActions = [
            Actions.ADD,
            Actions.EXCLUDE,
            Actions.SHOW_GREATER_THAN,
            Actions.SHOW_LESS_THAN,
        ];
        if (field === 'id' || field === 'trace') {
            var generateLink = field === 'id' ? generateTransactionLink : generateTraceLink;
            var target = generateLink(transactionName)(organization, dataRow, location.query);
            return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
          <Link to={target}>{rendered}</Link>
        </CellAction>);
        }
        var fieldName = getAggregateAlias(field);
        var value = dataRow[fieldName];
        if (tableMeta[fieldName] === 'integer' && defined(value) && value > 999) {
            return (<Tooltip title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
            {rendered}
          </CellAction>
        </Tooltip>);
        }
        return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
        {rendered}
      </CellAction>);
    };
    EventsTable.prototype.onSortClick = function (currentSortKind, currentSortField) {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.transactionEvents.sort',
            eventName: 'Performance Views: Transaction Events Tab Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    };
    EventsTable.prototype.renderHeadCell = function (tableMeta, column, title) {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, location = _a.location;
        var align = fieldAlignment(column.name, column.type, tableMeta);
        var field = { field: column.name, width: column.width };
        function generateSortLink() {
            if (!tableMeta) {
                return undefined;
            }
            var nextEventView = eventView.sortOnField(field, tableMeta);
            var queryStringObject = nextEventView.generateQueryStringObject();
            return __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { sort: queryStringObject.sort }) });
        }
        var currentSort = eventView.sortForField(field, tableMeta);
        // Event id and Trace id are technically sortable but we don't want to sort them here since sorting by a uuid value doesn't make sense
        var canSort = field.field !== 'id' &&
            field.field !== 'trace' &&
            field.field !== SPAN_OP_RELATIVE_BREAKDOWN_FIELD &&
            isFieldSortable(field, tableMeta);
        var currentSortKind = currentSort ? currentSort.kind : undefined;
        var currentSortField = currentSort ? currentSort.field : undefined;
        if (field.field === SPAN_OP_RELATIVE_BREAKDOWN_FIELD) {
            title = (<OperationSort title={OperationTitle} eventView={eventView} tableMeta={tableMeta} location={location}/>);
        }
        var sortLink = (<SortLink align={align} title={title || field.field} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={function () { return _this.onSortClick(currentSortKind, currentSortField); }}/>);
        return sortLink;
    };
    EventsTable.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, setError = _a.setError;
        var widths = this.state.widths;
        var containsSpanOpsBreakdown = eventView
            .getColumns()
            .find(function (col) {
            return col.name === SPAN_OP_RELATIVE_BREAKDOWN_FIELD;
        });
        var columnOrder = eventView
            .getColumns()
            .filter(function (col) {
            return !containsSpanOpsBreakdown || !isSpanOperationBreakdownField(col.name);
        })
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return __assign(__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        return (<div>
        <DiscoverQuery eventView={eventView} orgSlug={organization.slug} location={location} setError={setError} referrer="api.performance.transaction-events">
          {function (_a) {
                var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
                return (<React.Fragment>
                <GridEditable isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={eventView.getSorts()} grid={{
                        onResizeColumn: _this.handleResizeColumn,
                        renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                        renderBodyCell: _this.renderBodyCellWithData(tableData),
                    }} location={location}/>
                <Pagination pageLinks={pageLinks}/>
              </React.Fragment>);
            }}
        </DiscoverQuery>
      </div>);
    };
    return EventsTable;
}(React.Component));
var StyledIconQuestion = styled(QuestionTooltip)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"], ["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"])));
export default EventsTable;
var templateObject_1;
//# sourceMappingURL=eventsTable.jsx.map