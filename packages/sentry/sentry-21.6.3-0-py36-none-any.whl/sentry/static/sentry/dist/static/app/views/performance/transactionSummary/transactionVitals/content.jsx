import { __assign, __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import SearchBar from 'app/components/events/searchBar';
import * as Layout from 'app/components/layouts/thirds';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Histogram from 'app/utils/performance/histogram';
import { FILTER_OPTIONS } from 'app/utils/performance/histogram/constants';
import { decodeScalar } from 'app/utils/queryString';
import TransactionHeader, { Tab } from '../header';
import { ZOOM_KEYS } from './constants';
import VitalsPanel from './vitalsPanel';
var VitalsContent = /** @class */ (function (_super) {
    __extends(VitalsContent, _super);
    function VitalsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            delete queryParams.cursor;
            browserHistory.push({
                pathname: location.pathname,
                query: queryParams,
            });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        return _this;
    }
    VitalsContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, transactionName = _a.transactionName, location = _a.location, eventView = _a.eventView, projects = _a.projects, organization = _a.organization;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = decodeScalar(location.query.query, '');
        return (<React.Fragment>
        <TransactionHeader eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={Tab.RealUserMonitoring} hasWebVitals handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <Histogram location={location} zoomKeys={ZOOM_KEYS}>
          {function (_a) {
                var activeFilter = _a.activeFilter, handleFilterChange = _a.handleFilterChange, handleResetView = _a.handleResetView, isZoomed = _a.isZoomed;
                return (<Layout.Body>
                {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
                <Layout.Main fullWidth>
                  <StyledActions>
                    <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={_this.handleSearch}/>
                    <DropdownControl buttonProps={{ prefix: t('Outliers') }} label={activeFilter.label}>
                      {FILTER_OPTIONS.map(function (_a) {
                        var label = _a.label, value = _a.value;
                        return (<DropdownItem key={value} onSelect={function (filterOption) {
                                trackAnalyticsEvent({
                                    eventKey: 'performance_views.vitals.filter_changed',
                                    eventName: 'Performance Views: Change vitals filter',
                                    organization_id: organization.id,
                                    value: filterOption,
                                });
                                handleFilterChange(filterOption);
                            }} eventKey={value} isActive={value === activeFilter.value}>
                          {label}
                        </DropdownItem>);
                    })}
                    </DropdownControl>
                    <Button onClick={function () {
                        trackAnalyticsEvent({
                            eventKey: 'performance_views.vitals.reset_view',
                            eventName: 'Performance Views: Reset vitals view',
                            organization_id: organization.id,
                        });
                        handleResetView();
                    }} disabled={!isZoomed} data-test-id="reset-view">
                      {t('Reset View')}
                    </Button>
                  </StyledActions>
                  <VitalsPanel organization={organization} location={location} eventView={eventView} dataFilter={activeFilter.value}/>
                </Layout.Main>
              </Layout.Body>);
            }}
        </Histogram>
      </React.Fragment>);
    };
    return VitalsContent;
}(React.Component));
var StyledSearchBar = styled(SearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content max-content;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content max-content;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(2), space(3));
export default VitalsContent;
var templateObject_1, templateObject_2;
//# sourceMappingURL=content.jsx.map