import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import { Component, Fragment } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import * as qs from 'query-string';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button, { ButtonLabel } from 'app/components/button';
import ButtonBar, { ButtonGrid } from 'app/components/buttonBar';
import DiscoverButton from 'app/components/discoverButton';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import GroupList from 'app/components/issues/groupList';
import Pagination from 'app/components/pagination';
import QueryCount from 'app/components/queryCount';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { QueryResults } from 'app/utils/tokenizeSearch';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import { IssueSortOptions } from 'app/views/issueList/utils';
import { getReleaseParams } from '../../utils';
import EmptyState from '../emptyState';
import { getReleaseEventView } from './chart/utils';
var IssuesType;
(function (IssuesType) {
    IssuesType["NEW"] = "new";
    IssuesType["UNHANDLED"] = "unhandled";
    IssuesType["RESOLVED"] = "resolved";
    IssuesType["ALL"] = "all";
})(IssuesType || (IssuesType = {}));
var IssuesQuery;
(function (IssuesQuery) {
    IssuesQuery["NEW"] = "first-release";
    IssuesQuery["UNHANDLED"] = "error.handled:0";
    IssuesQuery["RESOLVED"] = "is:resolved";
    IssuesQuery["ALL"] = "release";
})(IssuesQuery || (IssuesQuery = {}));
var defaultProps = {
    withChart: false,
};
var Issues = /** @class */ (function (_super) {
    __extends(Issues, _super);
    function Issues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleIssuesTypeSelection = function (issuesType) {
            var location = _this.props.location;
            var issuesTypeQuery = issuesType === IssuesType.ALL
                ? IssuesType.ALL
                : issuesType === IssuesType.NEW
                    ? IssuesType.NEW
                    : issuesType === IssuesType.RESOLVED
                        ? IssuesType.RESOLVED
                        : issuesType === IssuesType.UNHANDLED
                            ? IssuesType.UNHANDLED
                            : '';
            var to = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { issuesType: issuesTypeQuery }) });
            browserHistory.replace(to);
            _this.setState({ issuesType: issuesType });
        };
        _this.handleFetchSuccess = function (groupListState, onCursor) {
            _this.setState({ pageLinks: groupListState.pageLinks, onCursor: onCursor });
        };
        _this.renderEmptyMessage = function () {
            var selection = _this.props.selection;
            var issuesType = _this.state.issuesType;
            var selectedTimePeriod = DEFAULT_RELATIVE_PERIODS[selection.datetime.period];
            var displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : t('given timeframe');
            return (<EmptyState>
        <Fragment>
          {issuesType === IssuesType.NEW &&
                    tct('No new issues for the [timePeriod].', {
                        timePeriod: displayedPeriod,
                    })}
          {issuesType === IssuesType.UNHANDLED &&
                    tct('No unhandled issues for the [timePeriod].', {
                        timePeriod: displayedPeriod,
                    })}
          {issuesType === IssuesType.RESOLVED && t('No resolved issues.')}
          {issuesType === IssuesType.ALL &&
                    tct('No issues for the [timePeriod].', {
                        timePeriod: displayedPeriod,
                    })}
        </Fragment>
      </EmptyState>);
        };
        return _this;
    }
    Issues.prototype.getInitialState = function () {
        var location = this.props.location;
        var query = location.query ? location.query.issuesType : null;
        var issuesTypeState = !query
            ? IssuesType.NEW
            : query.includes(IssuesType.NEW)
                ? IssuesType.NEW
                : query.includes(IssuesType.UNHANDLED)
                    ? IssuesType.UNHANDLED
                    : query.includes(IssuesType.RESOLVED)
                        ? IssuesType.RESOLVED
                        : query.includes(IssuesType.ALL)
                            ? IssuesType.ALL
                            : IssuesType.ALL;
        return {
            issuesType: issuesTypeState,
            count: {
                new: null,
                all: null,
                resolved: null,
                unhandled: null,
            },
        };
    };
    Issues.prototype.componentDidMount = function () {
        this.fetchIssuesCount();
    };
    Issues.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(getReleaseParams({
            location: this.props.location,
            releaseBounds: this.props.releaseBounds,
            defaultStatsPeriod: this.props.defaultStatsPeriod,
            allowEmptyPeriod: this.props.organization.features.includes('release-comparison'),
        }), getReleaseParams({
            location: prevProps.location,
            releaseBounds: prevProps.releaseBounds,
            defaultStatsPeriod: prevProps.defaultStatsPeriod,
            allowEmptyPeriod: prevProps.organization.features.includes('release-comparison'),
        }))) {
            this.fetchIssuesCount();
        }
    };
    Issues.prototype.getDiscoverUrl = function () {
        var _a = this.props, version = _a.version, organization = _a.organization, selection = _a.selection;
        var discoverView = getReleaseEventView(selection, version);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    };
    Issues.prototype.getIssuesUrl = function () {
        var _a = this.props, version = _a.version, organization = _a.organization;
        var issuesType = this.state.issuesType;
        var queryParams = this.getIssuesEndpoint().queryParams;
        var query = new QueryResults([]);
        switch (issuesType) {
            case IssuesType.NEW:
                query.setTagValues('firstRelease', [version]);
                break;
            case IssuesType.UNHANDLED:
                query.setTagValues('release', [version]);
                query.setTagValues('error.handled', ['0']);
                break;
            case IssuesType.RESOLVED:
            case IssuesType.ALL:
            default:
                query.setTagValues('release', [version]);
        }
        return {
            pathname: "/organizations/" + organization.slug + "/issues/",
            query: __assign(__assign({}, queryParams), { limit: undefined, cursor: undefined, query: query.formatString() }),
        };
    };
    Issues.prototype.getIssuesEndpoint = function () {
        var _a = this.props, version = _a.version, organization = _a.organization, location = _a.location, defaultStatsPeriod = _a.defaultStatsPeriod, releaseBounds = _a.releaseBounds;
        var issuesType = this.state.issuesType;
        var queryParams = __assign(__assign({}, getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        })), { limit: 10, sort: IssueSortOptions.FREQ, groupStatsPeriod: 'auto' });
        switch (issuesType) {
            case IssuesType.ALL:
                return {
                    path: "/organizations/" + organization.slug + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: new QueryResults([IssuesQuery.ALL + ":" + version]).formatString() }),
                };
            case IssuesType.RESOLVED:
                return {
                    path: "/organizations/" + organization.slug + "/releases/" + version + "/resolved/",
                    queryParams: __assign(__assign({}, queryParams), { query: '' }),
                };
            case IssuesType.UNHANDLED:
                return {
                    path: "/organizations/" + organization.slug + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: new QueryResults([
                            IssuesQuery.ALL + ":" + version,
                            IssuesQuery.UNHANDLED,
                        ]).formatString() }),
                };
            case IssuesType.NEW:
            default:
                return {
                    path: "/organizations/" + organization.slug + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: new QueryResults([IssuesQuery.NEW + ":" + version]).formatString() }),
                };
        }
    };
    Issues.prototype.fetchIssuesCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, version, issueCountEndpoint, resolvedEndpoint, _b;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, version = _a.version;
                        issueCountEndpoint = this.getIssueCountEndpoint();
                        resolvedEndpoint = "/organizations/" + organization.slug + "/releases/" + version + "/resolved/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(issueCountEndpoint),
                                api.requestPromise(resolvedEndpoint),
                            ]).then(function (_a) {
                                var _b = __read(_a, 2), issueResponse = _b[0], resolvedResponse = _b[1];
                                _this.setState({
                                    count: {
                                        all: issueResponse[IssuesQuery.ALL + ":" + version] || 0,
                                        new: issueResponse[IssuesQuery.NEW + ":" + version] || 0,
                                        resolved: resolvedResponse.length,
                                        unhandled: issueResponse[IssuesQuery.UNHANDLED + " " + IssuesQuery.ALL + ":" + version] ||
                                            0,
                                    },
                                });
                            })];
                    case 2:
                        _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Issues.prototype.getIssueCountEndpoint = function () {
        var _a = this.props, organization = _a.organization, version = _a.version, location = _a.location, releaseBounds = _a.releaseBounds, defaultStatsPeriod = _a.defaultStatsPeriod;
        var issuesCountPath = "/organizations/" + organization.slug + "/issues-count/";
        var params = [
            IssuesQuery.NEW + ":" + version,
            IssuesQuery.ALL + ":" + version,
            IssuesQuery.UNHANDLED + " " + IssuesQuery.ALL + ":" + version,
        ];
        var queryParams = params.map(function (param) { return param; });
        var queryParameters = __assign(__assign({}, getReleaseParams({
            location: location,
            releaseBounds: releaseBounds,
            defaultStatsPeriod: defaultStatsPeriod,
            allowEmptyPeriod: organization.features.includes('release-comparison'),
        })), { query: queryParams });
        return issuesCountPath + "?" + qs.stringify(queryParameters);
    };
    Issues.prototype.render = function () {
        var _this = this;
        var _a = this.state, issuesType = _a.issuesType, count = _a.count, pageLinks = _a.pageLinks, onCursor = _a.onCursor;
        var _b = this.props, organization = _b.organization, queryFilterDescription = _b.queryFilterDescription, withChart = _b.withChart;
        var _c = this.getIssuesEndpoint(), path = _c.path, queryParams = _c.queryParams;
        var hasReleaseComparison = organization.features.includes('release-comparison');
        var issuesTypes = [
            { value: IssuesType.NEW, label: t('New Issues'), issueCount: count.new },
            {
                value: IssuesType.RESOLVED,
                label: t('Resolved Issues'),
                issueCount: count.resolved,
            },
            {
                value: IssuesType.UNHANDLED,
                label: t('Unhandled Issues'),
                issueCount: count.unhandled,
            },
            { value: IssuesType.ALL, label: t('All Issues'), issueCount: count.all },
        ];
        return (<Fragment>
        <ControlsWrapper>
          {hasReleaseComparison ? (<StyledButtonBar active={issuesType} merged>
              {issuesTypes.map(function (_a) {
                    var value = _a.value, label = _a.label, issueCount = _a.issueCount;
                    return (<Button key={value} barId={value} size="small" onClick={function () { return _this.handleIssuesTypeSelection(value); }}>
                  {label}
                  <QueryCount count={issueCount} max={99} hideParens hideIfEmpty={false}/>
                </Button>);
                })}
            </StyledButtonBar>) : (<DropdownControl button={function (_a) {
                    var _b;
                    var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                    return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={t('Filter')} size="small">
                  {(_b = issuesTypes.find(function (i) { return i.value === issuesType; })) === null || _b === void 0 ? void 0 : _b.label}
                </StyledDropdownButton>);
                }}>
              {issuesTypes.map(function (_a) {
                    var value = _a.value, label = _a.label;
                    return (<StyledDropdownItem key={value} onSelect={_this.handleIssuesTypeSelection} data-test-id={"filter-" + value} eventKey={value} isActive={value === issuesType}>
                  {label}
                </StyledDropdownItem>);
                })}
            </DropdownControl>)}

          <OpenInButtonBar gap={1}>
            <Button to={this.getIssuesUrl()} size="small" data-test-id="issues-button">
              {t('Open in Issues')}
            </Button>

            {!hasReleaseComparison && (<GuideAnchor target="release_issues_open_in_discover">
                <DiscoverButton to={this.getDiscoverUrl()} size="small" data-test-id="discover-button">
                  {t('Open in Discover')}
                </DiscoverButton>
              </GuideAnchor>)}
            {!hasReleaseComparison && (<StyledPagination pageLinks={pageLinks} onCursor={onCursor}/>)}
          </OpenInButtonBar>
        </ControlsWrapper>
        <div data-test-id="release-wrapper">
          <GroupList orgId={organization.slug} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} queryFilterDescription={queryFilterDescription} withChart={withChart} narrowGroups renderEmptyMessage={this.renderEmptyMessage} withPagination={false} onFetchSuccess={this.handleFetchSuccess}/>
        </div>
      </Fragment>);
    };
    Issues.defaultProps = defaultProps;
    return Issues;
}(Component));
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n    ", " {\n      overflow: auto;\n    }\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n    ", " {\n      overflow: auto;\n    }\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; }, ButtonGrid);
var OpenInButtonBar = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
var StyledButtonBar = styled(ButtonBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-template-columns: repeat(4, 1fr);\n  ", " {\n    white-space: nowrap;\n    grid-gap: ", ";\n    span:last-child {\n      color: ", ";\n    }\n  }\n  .active {\n    ", " {\n      span:last-child {\n        color: ", ";\n      }\n    }\n  }\n"], ["\n  grid-template-columns: repeat(4, 1fr);\n  ", " {\n    white-space: nowrap;\n    grid-gap: ", ";\n    span:last-child {\n      color: ", ";\n    }\n  }\n  .active {\n    ", " {\n      span:last-child {\n        color: ", ";\n      }\n    }\n  }\n"])), ButtonLabel, space(0.5), function (p) { return p.theme.buttonCount; }, ButtonLabel, function (p) { return p.theme.buttonCountActive; });
var StyledDropdownButton = styled(DropdownButton)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  min-width: 145px;\n"], ["\n  min-width: 145px;\n"])));
var StyledDropdownItem = styled(DropdownItem)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var StyledPagination = styled(Pagination)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
export default withApi(withOrganization(Issues));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=issues.jsx.map