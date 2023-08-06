import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import GridEditable, { COL_WIDTH_UNDEFINED, } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import { IconAdd } from 'app/icons/iconAdd';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { isFieldSortable } from 'app/utils/discover/eventView';
import { fieldAlignment } from 'app/utils/discover/fields';
import { formatPercentage } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import CellAction, { Actions, updateQuery } from 'app/views/eventsV2/table/cellAction';
import { PerformanceDuration } from '../../utils';
import { TagValue } from '../tagExplorer';
var TAGS_CURSOR_NAME = 'tags_cursor';
var COLUMN_ORDER = [
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
        key: 'count',
        field: 'count',
        name: 'Events',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
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
        key: 'action',
        field: 'action',
        name: '',
        width: -1,
        column: {
            kind: 'field',
        },
    },
];
var TagValueTable = /** @class */ (function (_super) {
    __extends(TagValueTable, _super);
    function TagValueTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.renderHeadCellWithMeta = function (sortedEventView, tableMeta, columns) {
            return function (column, index) {
                return _this.renderHeadCell(sortedEventView, tableMeta, column, columns[index]);
            };
        };
        _this.handleTagValueClick = function (location, tagKey, tagValue) {
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
                var _b = _this.props, eventView = _b.eventView, location = _b.location;
                var searchConditions = tokenizeSearch(eventView.query);
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
            var location = parentProps.location, eventView = parentProps.eventView;
            if (column.key === 'key') {
                return dataRow.tags_key;
            }
            var allowActions = [Actions.ADD, Actions.EXCLUDE];
            if (column.key === 'tagValue') {
                var actionRow = __assign(__assign({}, dataRow), { id: dataRow.tags_key });
                return (<CellAction column={column} dataRow={actionRow} handleCellAction={_this.handleCellAction(column, dataRow.tags_value, actionRow)} allowActions={allowActions}>
          <TagValue row={dataRow}/>
        </CellAction>);
            }
            if (column.key === 'frequency') {
                return <AlignRight>{formatPercentage(dataRow.frequency, 0)}</AlignRight>;
            }
            if (column.key === 'action') {
                var searchConditions = tokenizeSearch(eventView.query);
                var disabled = searchConditions.hasTag(dataRow.tags_key);
                return (<Link disabled={disabled} to="" onClick={function () {
                        return _this.handleTagValueClick(location, dataRow.tags_key, dataRow.tags_value);
                    }}>
          <LinkContainer>
            <IconAdd isCircled/>
            {t('Add to filter')}
          </LinkContainer>
        </Link>);
            }
            if (column.key === 'comparison') {
                var localValue = dataRow.comparison;
                var pct = formatPercentage(localValue - 1, 0);
                return localValue > 1 ? t('+%s slower', pct) : t('%s faster', pct);
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
            if (column.key === 'count') {
                return <AlignRight>{value}</AlignRight>;
            }
            return value;
        };
        _this.renderBodyCellWithData = function (parentProps) {
            return function (column, dataRow) {
                return _this.renderBodyCell(parentProps, column, dataRow);
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
    TagValueTable.prototype.renderHeadCell = function (sortedEventView, tableMeta, column, columnInfo) {
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
        return (<SortLink align={align} title={columnInfo.name} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={function () { }} // TODO(k-fish): Implement sorting
        />);
    };
    TagValueTable.prototype.render = function () {
        var _a = this.props, eventView = _a.eventView, tagKey = _a.tagKey, location = _a.location, isLoading = _a.isLoading, tableData = _a.tableData, aggregateColumn = _a.aggregateColumn;
        var newColumns = __spreadArray([], __read(COLUMN_ORDER)).map(function (c) {
            var newColumn = __assign({}, c);
            if (c.key === 'tagValue') {
                newColumn.name = tagKey;
            }
            if (c.key === 'aggregate') {
                if (aggregateColumn === 'measurements.lcp') {
                    newColumn.name = 'Avg LCP';
                }
            }
            return newColumn;
        });
        return (<StyledPanelTable>
        <GridEditable isLoading={isLoading} data={tableData && tableData.data ? tableData.data : []} columnOrder={newColumns} columnSortBy={[]} grid={{
                renderHeadCell: this.renderHeadCellWithMeta(eventView, tableData ? tableData.meta : {}, newColumns),
                renderBodyCell: this.renderBodyCellWithData(this.props),
                onResizeColumn: this.handleResizeColumn,
            }} location={location}/>
      </StyledPanelTable>);
    };
    return TagValueTable;
}(Component));
export { TagValueTable };
var StyledPanelTable = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  > div {\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n"], ["\n  > div {\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n"])));
var AlignRight = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var LinkContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-end;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-end;\n  align-items: center;\n"])), space(0.5));
export default TagValueTable;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=tagValueTable.jsx.map