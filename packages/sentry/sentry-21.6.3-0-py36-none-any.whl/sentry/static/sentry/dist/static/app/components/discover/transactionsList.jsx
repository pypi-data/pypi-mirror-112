import { __assign, __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import DiscoverButton from 'app/components/discoverButton';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Pagination from 'app/components/pagination';
import { t } from 'app/locale';
import space from 'app/styles/space';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import BaselineQuery from 'app/utils/performance/baseline/baselineQuery';
import { TrendsEventsDiscoverQuery } from 'app/utils/performance/trends/trendsDiscoverQuery';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import { decodeColumnOrder } from 'app/views/eventsV2/utils';
import { mapShowTransactionToPercentile } from 'app/views/performance/transactionSummary/transactionEvents/utils';
import TransactionsTable from './transactionsTable';
var DEFAULT_TRANSACTION_LIMIT = 5;
var TransactionsList = /** @class */ (function (_super) {
    __extends(TransactionsList, _super);
    function TransactionsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCursor = function (cursor, pathname, query) {
            var _a;
            var cursorName = _this.props.cursorName;
            browserHistory.push({
                pathname: pathname,
                query: __assign(__assign({}, query), (_a = {}, _a[cursorName] = cursor, _a)),
            });
        };
        return _this;
    }
    TransactionsList.prototype.getEventView = function () {
        var _a = this.props, eventView = _a.eventView, selected = _a.selected;
        var sortedEventView = eventView.withSorts([selected.sort]);
        if (selected.query) {
            var query_1 = tokenizeSearch(sortedEventView.query);
            selected.query.forEach(function (item) { return query_1.setTagValues(item[0], [item[1]]); });
            sortedEventView.query = query_1.formatString();
        }
        return sortedEventView;
    };
    TransactionsList.prototype.generateDiscoverEventView = function () {
        var generateDiscoverEventView = this.props.generateDiscoverEventView;
        if (typeof generateDiscoverEventView === 'function') {
            return generateDiscoverEventView();
        }
        return this.getEventView();
    };
    TransactionsList.prototype.generatePerformanceTransactionEventsView = function () {
        var _a;
        var generatePerformanceTransactionEventsView = this.props.generatePerformanceTransactionEventsView;
        return (_a = generatePerformanceTransactionEventsView === null || generatePerformanceTransactionEventsView === void 0 ? void 0 : generatePerformanceTransactionEventsView()) !== null && _a !== void 0 ? _a : this.getEventView();
    };
    TransactionsList.prototype.renderHeader = function () {
        var _a = this.props, organization = _a.organization, selected = _a.selected, options = _a.options, handleDropdownChange = _a.handleDropdownChange, handleOpenAllEventsClick = _a.handleOpenAllEventsClick, handleOpenInDiscoverClick = _a.handleOpenInDiscoverClick, showTransactions = _a.showTransactions, breakdown = _a.breakdown;
        return (<React.Fragment>
        <div>
          <DropdownControl data-test-id="filter-transactions" button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={t('Filter')} size="small">
                {selected.label}
              </StyledDropdownButton>);
            }}>
            {options.map(function (_a) {
                var value = _a.value, label = _a.label;
                return (<DropdownItem data-test-id={"option-" + value} key={value} onSelect={handleDropdownChange} eventKey={value} isActive={value === selected.value}>
                {label}
              </DropdownItem>);
            })}
          </DropdownControl>
        </div>
        {!this.isTrend() &&
                (handleOpenAllEventsClick ? (<GuideAnchor target="release_transactions_open_in_transaction_events">
              <Button onClick={handleOpenAllEventsClick} to={this.generatePerformanceTransactionEventsView().getPerformanceTransactionEventsViewUrlTarget(organization.slug, {
                        showTransactions: mapShowTransactionToPercentile(showTransactions),
                        breakdown: breakdown,
                    })} size="small" data-test-id="transaction-events-open">
                {t('Open All Events')}
              </Button>
            </GuideAnchor>) : (<GuideAnchor target="release_transactions_open_in_discover">
              <DiscoverButton onClick={handleOpenInDiscoverClick} to={this.generateDiscoverEventView().getResultsViewUrlTarget(organization.slug)} size="small" data-test-id="discover-open">
                {t('Open in Discover')}
              </DiscoverButton>
            </GuideAnchor>))}
      </React.Fragment>);
    };
    TransactionsList.prototype.renderTransactionTable = function () {
        var _this = this;
        var _a;
        var _b = this.props, location = _b.location, organization = _b.organization, handleCellAction = _b.handleCellAction, cursorName = _b.cursorName, limit = _b.limit, titles = _b.titles, generateLink = _b.generateLink, baseline = _b.baseline, forceLoading = _b.forceLoading;
        var eventView = this.getEventView();
        var columnOrder = eventView.getColumns();
        var cursor = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        var baselineTransactionName = organization.features.includes('transaction-comparison')
            ? baseline !== null && baseline !== void 0 ? baseline : null
            : null;
        var tableRenderer = function (_a) {
            var isLoading = _a.isLoading, pageLinks = _a.pageLinks, tableData = _a.tableData, baselineData = _a.baselineData;
            return (<React.Fragment>
        <Header>
          {_this.renderHeader()}
          <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
        </Header>
        <TransactionsTable eventView={eventView} organization={organization} location={location} isLoading={isLoading} tableData={tableData} baselineData={baselineData !== null && baselineData !== void 0 ? baselineData : null} columnOrder={columnOrder} titles={titles} generateLink={generateLink} baselineTransactionName={baselineTransactionName} handleCellAction={handleCellAction}/>
      </React.Fragment>);
        };
        if (forceLoading) {
            return tableRenderer({
                isLoading: true,
                pageLinks: null,
                tableData: null,
                baselineData: null,
            });
        }
        if (baselineTransactionName) {
            var orgTableRenderer_1 = tableRenderer;
            tableRenderer = function (_a) {
                var isLoading = _a.isLoading, pageLinks = _a.pageLinks, tableData = _a.tableData;
                return (<BaselineQuery eventView={eventView} orgSlug={organization.slug}>
          {function (baselineQueryProps) {
                        return orgTableRenderer_1({
                            isLoading: isLoading || baselineQueryProps.isLoading,
                            pageLinks: pageLinks,
                            tableData: tableData,
                            baselineData: baselineQueryProps.results,
                        });
                    }}
        </BaselineQuery>);
            };
        }
        return (<DiscoverQuery location={location} eventView={eventView} orgSlug={organization.slug} limit={limit} cursor={cursor} referrer="api.discover.transactions-list">
        {tableRenderer}
      </DiscoverQuery>);
    };
    TransactionsList.prototype.renderTrendsTable = function () {
        var _this = this;
        var _a;
        var _b = this.props, trendView = _b.trendView, location = _b.location, selected = _b.selected, organization = _b.organization, cursorName = _b.cursorName, generateLink = _b.generateLink;
        var sortedEventView = trendView.clone();
        sortedEventView.sorts = [selected.sort];
        sortedEventView.trendType = selected.trendType;
        if (selected.query) {
            var query_2 = tokenizeSearch(sortedEventView.query);
            selected.query.forEach(function (item) { return query_2.setTagValues(item[0], [item[1]]); });
            sortedEventView.query = query_2.formatString();
        }
        var cursor = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        return (<TrendsEventsDiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location} cursor={cursor} limit={5}>
        {function (_a) {
                var isLoading = _a.isLoading, trendsData = _a.trendsData, pageLinks = _a.pageLinks;
                return (<React.Fragment>
            <Header>
              {_this.renderHeader()}
              <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
            </Header>
            <TransactionsTable eventView={sortedEventView} organization={organization} location={location} isLoading={isLoading} tableData={trendsData} baselineData={null} titles={['transaction', 'percentage', 'difference']} columnOrder={decodeColumnOrder([
                        { field: 'transaction' },
                        { field: 'trend_percentage()' },
                        { field: 'trend_difference()' },
                    ])} generateLink={generateLink} baselineTransactionName={null}/>
          </React.Fragment>);
            }}
      </TrendsEventsDiscoverQuery>);
    };
    TransactionsList.prototype.isTrend = function () {
        var selected = this.props.selected;
        return selected.trendType !== undefined;
    };
    TransactionsList.prototype.render = function () {
        return (<React.Fragment>
        {this.isTrend() ? this.renderTrendsTable() : this.renderTransactionTable()}
      </React.Fragment>);
    };
    TransactionsList.defaultProps = {
        cursorName: 'transactionCursor',
        limit: DEFAULT_TRANSACTION_LIMIT,
    };
    return TransactionsList;
}(React.Component));
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"])), space(1));
var StyledDropdownButton = styled(DropdownButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  min-width: 145px;\n"], ["\n  min-width: 145px;\n"])));
var StyledPagination = styled(Pagination)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0 0 0 ", ";\n"], ["\n  margin: 0 0 0 ", ";\n"])), space(1));
export default TransactionsList;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=transactionsList.jsx.map