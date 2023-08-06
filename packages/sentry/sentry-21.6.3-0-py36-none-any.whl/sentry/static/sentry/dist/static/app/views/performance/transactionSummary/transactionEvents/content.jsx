import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import * as React from 'react';
import { Fragment } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import Alert from 'app/components/alert';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import SearchBar from 'app/components/events/searchBar';
import GlobalSdkUpdateAlert from 'app/components/globalSdkUpdateAlert';
import * as Layout from 'app/components/layouts/thirds';
import LoadingIndicator from 'app/components/loadingIndicator';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { IconFlag } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import { updateQuery } from 'app/views/eventsV2/table/cellAction';
import { getCurrentLandingDisplay, LandingDisplayField } from '../../landing/utils';
import Filter, { filterToSearchConditions } from '../filter';
import TransactionHeader, { Tab } from '../header';
import EventsTable from './eventsTable';
import { getEventsFilterOptions } from './utils';
var EventsPageContent = /** @class */ (function (_super) {
    __extends(EventsPageContent, _super);
    function EventsPageContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
            error: undefined,
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location;
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                // no need to include transaction as its already in the query params
                searchConditions.removeTag('transaction');
                updateQuery(searchConditions, action, column, value);
                browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { cursor: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        return _this;
    }
    EventsPageContent.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<StyledAlert type="error" icon={<IconFlag size="md"/>}>
        {error}
      </StyledAlert>);
    };
    EventsPageContent.prototype.render = function () {
        var _a = this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization, projects = _a.projects, transactionName = _a.transactionName, isLoading = _a.isLoading;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        return (<Fragment>
        <TransactionHeader eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={Tab.Events} hasWebVitals={getCurrentLandingDisplay(location, projects, eventView).field ===
                LandingDisplayField.FRONTEND_PAGELOAD} handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <Layout.Body>
          <StyledSdkUpdatesAlert />
          {this.renderError()}
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main fullWidth>
            {isLoading ? (<LoadingIndicator />) : (<Body {...this.props} setError={this.setError}/>)}
          </Layout.Main>
        </Layout.Body>
      </Fragment>);
    };
    return EventsPageContent;
}(React.Component));
var Body = /** @class */ (function (_super) {
    __extends(Body, _super);
    function Body() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Body.prototype.render = function () {
        var eventView = this.props.eventView;
        var _a = this.props, location = _a.location, organization = _a.organization, transactionName = _a.transactionName, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, eventsDisplayFilterName = _a.eventsDisplayFilterName, onChangeEventsDisplayFilter = _a.onChangeEventsDisplayFilter, setError = _a.setError, webVital = _a.webVital;
        var transactionsListTitles = [
            t('event id'),
            t('user'),
            t('operation duration'),
            t('total duration'),
            t('trace id'),
            t('timestamp'),
        ];
        if (webVital) {
            transactionsListTitles.splice(3, 0, t(webVital));
        }
        var spanOperationBreakdownConditions = filterToSearchConditions(spanOperationBreakdownFilter, location);
        if (spanOperationBreakdownConditions) {
            eventView = eventView.clone();
            eventView.query = (eventView.query + " " + spanOperationBreakdownConditions).trim();
            transactionsListTitles.splice(2, 1, t(spanOperationBreakdownFilter + " duration"));
        }
        return (<React.Fragment>
        <Search {...this.props} onChangeEventsDisplayFilter={onChangeEventsDisplayFilter} eventsDisplayFilterName={eventsDisplayFilterName}/>
        <StyledTable>
          <EventsTable eventView={eventView} organization={organization} location={location} setError={setError} columnTitles={transactionsListTitles} transactionName={transactionName}/>
        </StyledTable>
      </React.Fragment>);
    };
    return Body;
}(React.Component));
var Search = function (props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, spanOperationBreakdownFilter = props.spanOperationBreakdownFilter, onChangeSpanOperationBreakdownFilter = props.onChangeSpanOperationBreakdownFilter, eventsDisplayFilterName = props.eventsDisplayFilterName, onChangeEventsDisplayFilter = props.onChangeEventsDisplayFilter, percentileValues = props.percentileValues;
    var handleSearch = function (query) {
        var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
        // do not propagate pagination when making a new search
        var searchQueryParams = omit(queryParams, 'cursor');
        browserHistory.push({
            pathname: location.pathname,
            query: searchQueryParams,
        });
    };
    var query = decodeScalar(location.query.query, '');
    var eventsFilterOptions = getEventsFilterOptions(spanOperationBreakdownFilter, percentileValues);
    return (<SearchWrapper>
      <Filter organization={organization} currentFilter={spanOperationBreakdownFilter} onChangeFilter={onChangeSpanOperationBreakdownFilter}/>
      <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>
      <LatencyDropdown>
        <DropdownControl buttonProps={{ prefix: t('Percentile') }} label={eventsFilterOptions[eventsDisplayFilterName].label}>
          {Object.entries(eventsFilterOptions).map(function (_a) {
            var _b = __read(_a, 2), name = _b[0], filter = _b[1];
            return (<DropdownItem key={name} onSelect={onChangeEventsDisplayFilter} eventKey={name} data-test-id={name} isActive={eventsDisplayFilterName === name}>
                {filter.label}
              </DropdownItem>);
        })}
        </DropdownControl>
      </LatencyDropdown>
    </SearchWrapper>);
};
var SearchWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"])), space(3));
var StyledAlert = styled(Alert)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1/3;\n  margin: 0;\n"], ["\n  grid-column: 1/3;\n  margin: 0;\n"])));
var StyledSearchBar = styled(SearchBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledTable = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledSdkUpdatesAlert = styled(GlobalSdkUpdateAlert)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var LatencyDropdown = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: ", ";\n  flex-grow: 0;\n"], ["\n  margin-left: ", ";\n  flex-grow: 0;\n"])), space(1));
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
export default EventsPageContent;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=content.jsx.map