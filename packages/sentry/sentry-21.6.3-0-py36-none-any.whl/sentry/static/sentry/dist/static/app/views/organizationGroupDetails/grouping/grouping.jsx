import { __assign, __awaiter, __generator, __makeTemplateObject, __read } from "tslib";
import { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import PaginationCaption from 'app/components/pagination/paginationCaption';
import { PanelTable } from 'app/components/panels';
import { DEFAULT_DEBOUNCE_DURATION } from 'app/constants';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import withApi from 'app/utils/withApi';
import RangeSlider from 'app/views/settings/components/forms/controls/rangeSlider';
import ErrorMessage from './errorMessage';
import NewIssue from './newIssue';
function Grouping(_a) {
    var _b, _c;
    var api = _a.api, groupId = _a.groupId, location = _a.location, organization = _a.organization, router = _a.router;
    var _d = location.query, cursor = _d.cursor, level = _d.level;
    var _e = __read(useState(false), 2), isLoading = _e[0], setIsLoading = _e[1];
    var _f = __read(useState(false), 2), isGroupingLevelDetailsLoading = _f[0], setIsGroupingLevelDetailsLoading = _f[1];
    var _g = __read(useState(undefined), 2), error = _g[0], setError = _g[1];
    var _h = __read(useState([]), 2), groupingLevels = _h[0], setGroupingLevels = _h[1];
    var _j = __read(useState(undefined), 2), activeGroupingLevel = _j[0], setActiveGroupingLevel = _j[1];
    var _k = __read(useState([]), 2), activeGroupingLevelDetails = _k[0], setActiveGroupingLevelDetails = _k[1];
    var _l = __read(useState(''), 2), pagination = _l[0], setPagination = _l[1];
    useEffect(function () {
        fetchGroupingLevels();
    }, []);
    useEffect(function () {
        setSecondGrouping();
    }, [groupingLevels]);
    useEffect(function () {
        updateUrlWithNewLevel();
    }, [activeGroupingLevel]);
    useEffect(function () {
        fetchGroupingLevelDetails();
    }, [activeGroupingLevel, cursor]);
    var handleSetActiveGroupingLevel = debounce(function (groupingLevelId) {
        setActiveGroupingLevel(Number(groupingLevelId));
    }, DEFAULT_DEBOUNCE_DURATION);
    function fetchGroupingLevels() {
        return __awaiter(this, void 0, void 0, function () {
            var response, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setIsLoading(true);
                        setError(undefined);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/grouping/levels/")];
                    case 2:
                        response = _a.sent();
                        setIsLoading(false);
                        setGroupingLevels(response.levels);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        setIsLoading(false);
                        setError(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function fetchGroupingLevelDetails() {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var _b, response, xhr, pageLinks, err_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (!groupingLevels.length || !defined(activeGroupingLevel)) {
                            return [2 /*return*/];
                        }
                        setIsGroupingLevelDetailsLoading(true);
                        setError(undefined);
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/grouping/levels/" + activeGroupingLevel + "/new-issues/", {
                                method: 'GET',
                                includeAllArgs: true,
                                query: __assign(__assign({}, location.query), { per_page: 10 }),
                            })];
                    case 2:
                        _b = __read.apply(void 0, [_c.sent(), 3]), response = _b[0], xhr = _b[2];
                        pageLinks = xhr && ((_a = xhr.getResponseHeader) === null || _a === void 0 ? void 0 : _a.call(xhr, 'Link'));
                        setPagination(pageLinks !== null && pageLinks !== void 0 ? pageLinks : '');
                        setActiveGroupingLevelDetails(Array.isArray(response) ? response : [response]);
                        setIsGroupingLevelDetailsLoading(false);
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        setIsGroupingLevelDetailsLoading(false);
                        setError(err_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function updateUrlWithNewLevel() {
        if (!defined(activeGroupingLevel) || level === activeGroupingLevel) {
            return;
        }
        router.replace({
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), { cursor: undefined, level: activeGroupingLevel }),
        });
    }
    function setSecondGrouping() {
        if (!groupingLevels.length) {
            return;
        }
        if (defined(level)) {
            if (!defined(groupingLevels[level])) {
                setError(t('The level you were looking for was not found.'));
                return;
            }
            if (level === activeGroupingLevel) {
                return;
            }
            setActiveGroupingLevel(level);
            return;
        }
        if (groupingLevels.length > 1) {
            setActiveGroupingLevel(Number(groupingLevels[1].id));
            return;
        }
        setActiveGroupingLevel(Number(groupingLevels[0].id));
    }
    if (isLoading) {
        return <LoadingIndicator />;
    }
    if (error) {
        return <ErrorMessage onRetry={fetchGroupingLevels} groupId={groupId} error={error}/>;
    }
    if (!activeGroupingLevelDetails.length) {
        return <LoadingIndicator />;
    }
    var links = parseLinkHeader(pagination);
    var hasMore = ((_b = links.previous) === null || _b === void 0 ? void 0 : _b.results) || ((_c = links.next) === null || _c === void 0 ? void 0 : _c.results);
    var paginationCurrentQuantity = activeGroupingLevelDetails.length;
    return (<Wrapper>
      <Description>
        {t('This issue is an aggregate of multiple events that sentry determined originate from the same root-cause. Use this page to explore more detailed groupings that exist within this issue.')}
      </Description>
      <Content>
        <SliderWrapper>
          {t('Fewer issues')}
          <StyledRangeSlider name="grouping-level" allowedValues={groupingLevels.map(function (groupingLevel) { return Number(groupingLevel.id); })} value={activeGroupingLevel !== null && activeGroupingLevel !== void 0 ? activeGroupingLevel : 0} onChange={handleSetActiveGroupingLevel} showLabel={false}/>
          {t('More issues')}
        </SliderWrapper>
        <div>
          <StyledPanelTable isReloading={isGroupingLevelDetailsLoading} headers={['', t('Events')]}>
            {activeGroupingLevelDetails.map(function (_a) {
            var hash = _a.hash, title = _a.title, metadata = _a.metadata, latestEvent = _a.latestEvent, eventCount = _a.eventCount;
            // XXX(markus): Ugly hack to make NewIssue show the right things.
            return (<NewIssue key={hash} sampleEvent={__assign(__assign({}, latestEvent), { metadata: metadata || latestEvent.metadata, title: title || latestEvent.title })} eventCount={eventCount} organization={organization}/>);
        })}
          </StyledPanelTable>
          <StyledPagination pageLinks={pagination} caption={<PaginationCaption caption={tct('Showing [current] of [total] [result]', {
                result: hasMore
                    ? t('results')
                    : tn('result', 'results', paginationCurrentQuantity),
                current: paginationCurrentQuantity,
                total: hasMore
                    ? paginationCurrentQuantity + "+"
                    : paginationCurrentQuantity,
            })}/>}/>
        </div>
      </Content>
    </Wrapper>);
}
export default withApi(Grouping);
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  display: grid;\n  align-content: flex-start;\n  margin: -", " -", ";\n  padding: ", " ", ";\n"], ["\n  flex: 1;\n  display: grid;\n  align-content: flex-start;\n  margin: -", " -", ";\n  padding: ", " ", ";\n"])), space(3), space(4), space(3), space(4));
var Description = styled('p')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  && {\n    margin-bottom: ", ";\n  }\n"], ["\n  && {\n    margin-bottom: ", ";\n  }\n"])), space(2));
var Content = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(3));
var StyledPanelTable = styled(PanelTable)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-template-columns: 1fr minmax(60px, auto);\n  ", "\n\n  > * {\n    padding: ", " ", ";\n    :nth-child(-n + 2) {\n      padding: ", ";\n    }\n    :nth-child(2n) {\n      display: flex;\n      text-align: right;\n      justify-content: flex-end;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr minmax(80px, auto);\n  }\n"], ["\n  grid-template-columns: 1fr minmax(60px, auto);\n  ", "\n\n  > * {\n    padding: ", " ", ";\n    :nth-child(-n + 2) {\n      padding: ", ";\n    }\n    :nth-child(2n) {\n      display: flex;\n      text-align: right;\n      justify-content: flex-end;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr minmax(80px, auto);\n  }\n"])), function (p) {
    return p.isReloading &&
        "\n      opacity: 0.5;\n      pointer-events: none;\n    ";
}, space(1.5), space(2), space(2), function (p) { return p.theme.breakpoints[3]; });
var StyledPagination = styled(Pagination)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var SliderWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content max-content;\n  justify-content: space-between;\n  align-items: flex-start;\n  position: relative;\n  font-size: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n\n  @media (min-width: 700px) {\n    grid-template-columns: max-content minmax(270px, auto) max-content;\n    align-items: center;\n    justify-content: flex-start;\n    padding-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content max-content;\n  justify-content: space-between;\n  align-items: flex-start;\n  position: relative;\n  font-size: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n\n  @media (min-width: 700px) {\n    grid-template-columns: max-content minmax(270px, auto) max-content;\n    align-items: center;\n    justify-content: flex-start;\n    padding-bottom: 0;\n  }\n"])), space(1.5), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; }, space(2));
var StyledRangeSlider = styled(RangeSlider)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  input {\n    margin-top: 0;\n    margin-bottom: 0;\n  }\n\n  position: absolute;\n  bottom: 0;\n  left: ", ";\n  right: ", ";\n\n  @media (min-width: 700px) {\n    position: static;\n    left: auto;\n    right: auto;\n  }\n"], ["\n  input {\n    margin-top: 0;\n    margin-bottom: 0;\n  }\n\n  position: absolute;\n  bottom: 0;\n  left: ", ";\n  right: ", ";\n\n  @media (min-width: 700px) {\n    position: static;\n    left: auto;\n    right: auto;\n  }\n"])), space(1.5), space(1.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=grouping.jsx.map