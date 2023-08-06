import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import * as React from 'react';
import * as ReactRouter from 'react-router';
import { openModal } from 'app/actionCreators/modal';
import { fetchLegacyKeyTransactionsCount } from 'app/actionCreators/performance';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import GridEditable, { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import Pagination from 'app/components/pagination';
import Tooltip from 'app/components/tooltip';
import { IconStar } from 'app/icons';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { isFieldSortable } from 'app/utils/discover/eventView';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { fieldAlignment, getAggregateAlias } from 'app/utils/discover/fields';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import CellAction, { Actions, updateQuery } from 'app/views/eventsV2/table/cellAction';
import TransactionThresholdModal, { modalCss, } from './transactionSummary/transactionThresholdModal';
import { transactionSummaryRouteWithQuery } from './transactionSummary/utils';
import { COLUMN_TITLES } from './data';
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
var Table = /** @class */ (function (_super) {
    __extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
            keyedTransactions: null,
            transaction: undefined,
            transactionThreshold: undefined,
            transactionThresholdMetric: undefined,
        };
        _this.handleCellAction = function (column, dataRow) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization, projects = _a.projects;
                trackAnalyticsEvent({
                    eventKey: 'performance_views.overview.cellaction',
                    eventName: 'Performance Views: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                if (action === Actions.EDIT_THRESHOLD) {
                    var project_threshold_1 = dataRow.project_threshold_config;
                    var transactionName_1 = dataRow.transaction;
                    var projectID_1 = getProjectID(dataRow, projects);
                    openModal(function (modalProps) { return (<TransactionThresholdModal {...modalProps} organization={organization} transactionName={transactionName_1} eventView={eventView} project={projectID_1} transactionThreshold={project_threshold_1[1]} transactionThresholdMetric={project_threshold_1[0]} onApply={function (threshold, metric) {
                            if (threshold !== project_threshold_1[1] ||
                                metric !== project_threshold_1[0]) {
                                _this.setState({
                                    transaction: transactionName_1,
                                    transactionThreshold: threshold,
                                    transactionThresholdMetric: metric,
                                });
                            }
                        }}/>); }, { modalCss: modalCss, backdrop: 'static' });
                    return;
                }
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
        _this.renderPrependCellWithData = function (tableData) {
            var eventView = _this.props.eventView;
            var keyedTransactions = _this.state.keyedTransactions;
            var keyTransactionColumn = eventView
                .getColumns()
                .find(function (col) { return col.name === 'key_transaction'; });
            var teamKeyTransactionColumn = eventView
                .getColumns()
                .find(function (col) { return col.name === 'team_key_transaction'; });
            return function (isHeader, dataRow) {
                if (keyTransactionColumn) {
                    if (isHeader) {
                        var star = (<IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="key-transaction-header"/>);
                        return [_this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, keyTransactionColumn, star)];
                    }
                    else {
                        return [_this.renderBodyCell(tableData, keyTransactionColumn, dataRow)];
                    }
                }
                else if (teamKeyTransactionColumn) {
                    if (isHeader) {
                        var star = (<GuideAnchor target="team_key_transaction_header" position="top" disabled={keyedTransactions === null} // wait for the legacy counts to load
                        >
              <GuideAnchor target="team_key_transaction_existing" position="top" disabled={!keyedTransactions}>
                <IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="team-key-transaction-header"/>
              </GuideAnchor>
            </GuideAnchor>);
                        return [_this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, teamKeyTransactionColumn, star)];
                    }
                    else {
                        return [_this.renderBodyCell(tableData, teamKeyTransactionColumn, dataRow)];
                    }
                }
                return [];
            };
        };
        _this.handleSummaryClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.overview.navigate.summary',
                eventName: 'Performance Views: Overview view summary',
                organization_id: parseInt(organization.id, 10),
            });
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
    Table.prototype.componentDidMount = function () {
        this.fetchKeyTransactionCount();
    };
    Table.prototype.fetchKeyTransactionCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var organization, count, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        organization = this.props.organization;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchLegacyKeyTransactionsCount(organization.slug)];
                    case 2:
                        count = _a.sent();
                        this.setState({ keyedTransactions: count });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        this.setState({ keyedTransactions: null });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Table.prototype.renderBodyCell = function (tableData, column, dataRow) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, location = _a.location;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        var fieldRenderer = getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location });
        var allowActions = [
            Actions.ADD,
            Actions.EXCLUDE,
            Actions.SHOW_GREATER_THAN,
            Actions.SHOW_LESS_THAN,
        ];
        if (organization.features.includes('project-transaction-threshold-override')) {
            allowActions.push(Actions.EDIT_THRESHOLD);
        }
        if (field === 'transaction') {
            var projectID = getProjectID(dataRow, projects);
            var summaryView = eventView.clone();
            if (dataRow['http.method']) {
                summaryView.additionalConditions.setTagValues('http.method', [
                    dataRow['http.method'],
                ]);
            }
            summaryView.query = summaryView.getQueryWithAdditionalConditions();
            var target = transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID: projectID,
            });
            return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
          <Link to={target} onClick={this.handleSummaryClick}>
            {rendered}
          </Link>
        </CellAction>);
        }
        if (field.startsWith('key_transaction')) {
            // don't display per cell actions for key_transaction
            return rendered;
        }
        if (field.startsWith('team_key_transaction')) {
            // don't display per cell actions for team_key_transaction
            return rendered;
        }
        var fieldName = getAggregateAlias(field);
        var value = dataRow[fieldName];
        if (tableMeta[fieldName] === 'integer' && defined(value) && value > 999) {
            return (<Tooltip title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
            {rendered}
          </CellAction>
        </Tooltip>);
        }
        return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
        {rendered}
      </CellAction>);
    };
    Table.prototype.onSortClick = function (currentSortKind, currentSortField) {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.landingv2.transactions.sort',
            eventName: 'Performance Views: Landing Transactions Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    };
    Table.prototype.renderHeadCell = function (tableMeta, column, title) {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
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
        var canSort = isFieldSortable(field, tableMeta);
        var currentSortKind = currentSort ? currentSort.kind : undefined;
        var currentSortField = currentSort ? currentSort.field : undefined;
        var sortLink = (<SortLink align={align} title={title || field.field} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={function () { return _this.onSortClick(currentSortKind, currentSortField); }}/>);
        if (field.field.startsWith('user_misery')) {
            return (<GuideAnchor target="project_transaction_threshold" position="top" disabled={!organization.features.includes('project-transaction-threshold')}>
          {sortLink}
        </GuideAnchor>);
        }
        return sortLink;
    };
    Table.prototype.getSortedEventView = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization;
        return eventView.withSorts(__spreadArray([
            {
                field: organization.features.includes('team-key-transactions')
                    ? 'team_key_transaction'
                    : 'key_transaction',
                kind: 'desc',
            }
        ], __read(eventView.sorts)));
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, setError = _a.setError;
        var _b = this.state, widths = _b.widths, transaction = _b.transaction, transactionThreshold = _b.transactionThreshold, transactionThresholdMetric = _b.transactionThresholdMetric;
        var columnOrder = eventView
            .getColumns()
            // remove key_transactions from the column order as we'll be rendering it
            // via a prepended column
            .filter(function (col) {
            return col.name !== 'key_transaction' &&
                col.name !== 'team_key_transaction' &&
                !col.name.startsWith('count_miserable') &&
                col.name !== 'project_threshold_config';
        })
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return __assign(__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        var sortedEventView = this.getSortedEventView();
        var columnSortBy = sortedEventView.getSorts();
        var prependColumnWidths = ['max-content'];
        return (<div>
        <DiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location} setError={setError} referrer="api.performance.landing-table" transactionName={transaction} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric}>
          {function (_a) {
                var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
                return (<React.Fragment>
              <GridEditable isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                        onResizeColumn: _this.handleResizeColumn,
                        renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                        renderBodyCell: _this.renderBodyCellWithData(tableData),
                        renderPrependColumns: _this.renderPrependCellWithData(tableData),
                        prependColumnWidths: prependColumnWidths,
                    }} location={location}/>
              <Pagination pageLinks={pageLinks}/>
            </React.Fragment>);
            }}
        </DiscoverQuery>
      </div>);
    };
    return Table;
}(React.Component));
export default Table;
//# sourceMappingURL=table.jsx.map