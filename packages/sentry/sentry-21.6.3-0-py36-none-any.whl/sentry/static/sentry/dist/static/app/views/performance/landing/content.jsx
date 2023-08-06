import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import { Component, Fragment } from 'react';
import { browserHistory, withRouter } from 'react-router';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import SearchBar from 'app/components/events/searchBar';
import FeatureBadge from 'app/components/featureBadge';
import * as TeamKeyTransactionManager from 'app/components/performance/teamKeyTransactionsManager';
import { MAX_QUERY_LENGTH } from 'app/constants';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { generateAggregateFields } from 'app/utils/discover/fields';
import { isActiveSuperuser } from 'app/utils/isActiveSuperuser';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import withTeams from 'app/utils/withTeams';
import Charts from '../charts/index';
import { getBackendAxisOptions, getFrontendAxisOptions, getFrontendOtherAxisOptions, getMobileAxisOptions, } from '../data';
import Table from '../table';
import { getTransactionSearchQuery } from '../utils';
import DoubleAxisDisplay from './display/doubleAxisDisplay';
import { BACKEND_COLUMN_TITLES, FRONTEND_OTHER_COLUMN_TITLES, FRONTEND_PAGELOAD_COLUMN_TITLES, MOBILE_COLUMN_TITLES, } from './data';
import { getCurrentLandingDisplay, getDefaultDisplayFieldForPlatform, getDisplayAxes, LANDING_DISPLAYS, LandingDisplayField, LEFT_AXIS_QUERY_KEY, RIGHT_AXIS_QUERY_KEY, } from './utils';
import { BackendCards, FrontendCards } from './vitalsCards';
var LandingContent = /** @class */ (function (_super) {
    __extends(LandingContent, _super);
    function LandingContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLandingDisplayChange = function (field) {
            var _a = _this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, projects = _a.projects;
            var newQuery = __assign({}, location.query);
            delete newQuery[LEFT_AXIS_QUERY_KEY];
            delete newQuery[RIGHT_AXIS_QUERY_KEY];
            var defaultDisplay = getDefaultDisplayFieldForPlatform(projects, eventView);
            var currentDisplay = decodeScalar(location.query.landingDisplay);
            // Transaction op can affect the display and show no results if it is explicitly set.
            var query = decodeScalar(location.query.query, '');
            var searchConditions = tokenizeSearch(query);
            searchConditions.removeTag('transaction.op');
            trackAnalyticsEvent({
                eventKey: 'performance_views.landingv2.display_change',
                eventName: 'Performance Views: Landing v2 Display Change',
                organization_id: parseInt(organization.id, 10),
                change_to_display: field,
                default_display: defaultDisplay,
                current_display: currentDisplay,
                is_default: defaultDisplay === currentDisplay,
            });
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, newQuery), { query: searchConditions.formatString(), landingDisplay: field }),
            });
        };
        _this.renderLandingFrontend = function (isPageload) {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var columnTitles = isPageload
                ? FRONTEND_PAGELOAD_COLUMN_TITLES
                : FRONTEND_OTHER_COLUMN_TITLES;
            var axisOptions = isPageload
                ? getFrontendAxisOptions(organization)
                : getFrontendOtherAxisOptions(organization);
            var _b = getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            return (<Fragment>
        {isPageload && (<FrontendCards eventView={eventView} organization={organization} location={location} projects={projects}/>)}
        <DoubleAxisDisplay eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </Fragment>);
        };
        _this.renderLandingBackend = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var axisOptions = getBackendAxisOptions(organization);
            var _b = getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            var columnTitles = BACKEND_COLUMN_TITLES;
            return (<Fragment>
        <BackendCards eventView={eventView} organization={organization} location={location}/>
        <DoubleAxisDisplay eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </Fragment>);
        };
        _this.renderLandingMobile = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var axisOptions = getMobileAxisOptions(organization);
            var _b = getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            var columnTitles = MOBILE_COLUMN_TITLES;
            return (<Fragment>
        <DoubleAxisDisplay eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </Fragment>);
        };
        _this.renderLandingAll = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, router = _a.router, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            return (<Fragment>
        <Charts eventView={eventView} organization={organization} location={location} router={router}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()}/>
      </Fragment>);
        };
        return _this;
    }
    LandingContent.prototype.getSummaryConditions = function (query) {
        var parsed = tokenizeSearch(query);
        parsed.query = [];
        return parsed.formatString();
    };
    LandingContent.prototype.renderSelectedDisplay = function (display) {
        switch (display) {
            case LandingDisplayField.ALL:
                return this.renderLandingAll();
            case LandingDisplayField.FRONTEND_PAGELOAD:
                return this.renderLandingFrontend(true);
            case LandingDisplayField.FRONTEND_OTHER:
                return this.renderLandingFrontend(false);
            case LandingDisplayField.BACKEND:
                return this.renderLandingBackend();
            case LandingDisplayField.MOBILE:
                return this.renderLandingMobile();
            default:
                throw new Error("Unknown display: " + display);
        }
    };
    LandingContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, eventView = _a.eventView, projects = _a.projects, teams = _a.teams, handleSearch = _a.handleSearch;
        var currentLandingDisplay = getCurrentLandingDisplay(location, projects, eventView);
        var filterString = getTransactionSearchQuery(location, eventView.query);
        var isSuperuser = isActiveSuperuser();
        var userTeams = teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember || isSuperuser;
        });
        return (<Fragment>
        <SearchContainer>
          <SearchBar organization={organization} projectIds={eventView.project} query={filterString} fields={generateAggregateFields(organization, __spreadArray(__spreadArray([], __read(eventView.fields)), [{ field: 'tps()' }]), ['epm()', 'eps()'])} onSearch={handleSearch} maxQueryLength={MAX_QUERY_LENGTH}/>
          <DropdownControl buttonProps={{ prefix: t('Display') }} label={currentLandingDisplay.label}>
            {LANDING_DISPLAYS.filter(function (_a) {
                var isShown = _a.isShown;
                return !isShown || isShown(organization);
            }).map(function (_a) {
                var alpha = _a.alpha, label = _a.label, field = _a.field;
                return (<DropdownItem key={field} onSelect={_this.handleLandingDisplayChange} eventKey={field} data-test-id={field} isActive={field === currentLandingDisplay.field}>
                {label}
                {alpha && <FeatureBadge type="alpha" noTooltip/>}
              </DropdownItem>);
            })}
          </DropdownControl>
        </SearchContainer>
        <Feature organization={organization} features={['team-key-transactions']}>
          {function (_a) {
                var hasFeature = _a.hasFeature;
                return hasFeature ? (<TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={eventView.project.map(String)}>
                {_this.renderSelectedDisplay(currentLandingDisplay.field)}
              </TeamKeyTransactionManager.Provider>) : (_this.renderSelectedDisplay(currentLandingDisplay.field));
            }}
        </Feature>
      </Fragment>);
    };
    return LandingContent;
}(Component));
var SearchContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr min-content;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr min-content;\n  }\n"])), space(2), space(2), function (p) { return p.theme.breakpoints[0]; });
export default withRouter(withTeams(LandingContent));
var templateObject_1;
//# sourceMappingURL=content.jsx.map