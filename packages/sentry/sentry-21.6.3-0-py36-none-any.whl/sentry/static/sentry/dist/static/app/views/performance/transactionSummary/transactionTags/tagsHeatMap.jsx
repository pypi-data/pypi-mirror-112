import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React, { useRef, useState } from 'react';
import ReactDOM from 'react-dom';
import { Popper } from 'react-popper';
import { withTheme } from '@emotion/react';
import styled from '@emotion/styled';
import { truncate } from '@sentry/utils';
import classNames from 'classnames';
import memoize from 'lodash/memoize';
import HeatMapChart from 'app/components/charts/heatMapChart';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { Content } from 'app/components/dropdownControl';
import DropdownMenu from 'app/components/dropdownMenu';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { DropdownContainer, DropdownItem, SectionSubtext, } from 'app/components/quickTrace/styles';
import Truncate from 'app/components/truncate';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { axisLabelFormatter } from 'app/utils/discover/charts';
import getDynamicText from 'app/utils/getDynamicText';
import TagTransactionsQuery from 'app/utils/performance/segmentExplorer/tagTransactionsQuery';
import { decodeScalar } from 'app/utils/queryString';
import { getPerformanceDuration, PerformanceDuration } from '../../utils';
import { eventsRouteWithQuery } from '../transactionEvents/utils';
import { generateTransactionLink } from '../utils';
import { parseHistogramBucketInfo } from './utils';
var findRowKey = function (row) {
    return Object.keys(row).find(function (key) { return key.includes('histogram'); });
};
var VirtualReference = /** @class */ (function () {
    function VirtualReference(element) {
        this.boundingRect = element.getBoundingClientRect();
    }
    VirtualReference.prototype.getBoundingClientRect = function () {
        return this.boundingRect;
    };
    Object.defineProperty(VirtualReference.prototype, "clientWidth", {
        get: function () {
            return this.getBoundingClientRect().width;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(VirtualReference.prototype, "clientHeight", {
        get: function () {
            return this.getBoundingClientRect().height;
        },
        enumerable: false,
        configurable: true
    });
    return VirtualReference;
}());
var getPortal = memoize(function () {
    var portal = document.getElementById('heatmap-portal');
    if (!portal) {
        portal = document.createElement('div');
        portal.setAttribute('id', 'heatmap-portal');
        document.body.appendChild(portal);
    }
    return portal;
});
var TagsHeatMap = function (props) {
    var tableData = props.tableData, isLoading = props.isLoading, organization = props.organization, eventView = props.eventView, location = props.location, tagKey = props.tagKey, transactionName = props.transactionName, aggregateColumn = props.aggregateColumn;
    var chartRef = useRef(null);
    var _a = __read(useState(), 2), chartElement = _a[0], setChartElement = _a[1];
    var _b = __read(useState(), 2), transactionEventView = _b[0], setTransactionEventView = _b[1];
    var _c = __read(useState(false), 2), isMenuOpen = _c[0], setIsMenuOpen = _c[1];
    // TODO(k-fish): Replace with actual theme colors.
    var purples = ['#D1BAFC', '#9282F3', '#6056BA', '#313087', '#021156'];
    var columnNames = new Set();
    var xValues = new Set();
    var rowKey = tableData && tableData.data && tableData.data.length && findRowKey(tableData.data[0]);
    var maxCount = 0;
    var _data = rowKey && tableData && tableData.data
        ? tableData.data.map(function (row) {
            var rawDuration = row[rowKey];
            var x = getPerformanceDuration(rawDuration);
            var y = row.tags_value;
            columnNames.add(y);
            xValues.add(x);
            maxCount = Math.max(maxCount, row.count);
            return [x, y, row.count];
        })
        : null;
    _data &&
        _data.sort(function (a, b) {
            if (a[0] === b[0]) {
                return b[1] - a[1];
            }
            return b[0] - a[0];
        });
    // TODO(k-fish): Cleanup options
    var chartOptions = {
        height: 290,
        animation: false,
        colors: purples,
        tooltip: {},
        yAxis: {
            type: 'category',
            data: Array.from(columnNames),
            splitArea: {
                show: true,
            },
            axisLabel: {
                formatter: function (value) { return truncate(value, 30); },
            },
        },
        xAxis: {
            boundaryGap: true,
            type: 'category',
            splitArea: {
                show: true,
            },
            data: Array.from(xValues),
            axisLabel: {
                show: true,
                showMinLabel: true,
                showMaxLabel: true,
                formatter: function (value) { return axisLabelFormatter(value, 'Count'); },
            },
            axisLine: {},
            axisPointer: {
                show: false,
            },
            axisTick: {
                show: true,
                interval: 0,
                alignWithLabel: true,
            },
        },
        grid: {
            left: space(3),
            right: space(3),
            top: '25px',
            bottom: space(4),
        },
    };
    var visualMaps = [
        {
            min: 0,
            max: maxCount,
            show: false,
            orient: 'horizontal',
            calculable: true,
            inRange: {
                color: purples,
            },
        },
    ];
    var series = [];
    if (_data) {
        series.push({
            seriesName: 'Count',
            dataArray: _data,
            label: {
                show: true,
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)',
                },
            },
        }); // TODO(k-fish): Fix heatmap data typing
    }
    var onOpenMenu = function () {
        setIsMenuOpen(true);
    };
    var onCloseMenu = function () {
        setIsMenuOpen(false);
    };
    var shouldIgnoreMenuClose = function (e) {
        var _a;
        if ((_a = chartRef.current) === null || _a === void 0 ? void 0 : _a.getEchartsInstance().getDom().contains(e.target)) {
            // Ignore the menu being closed if the echart is being clicked.
            return true;
        }
        return false;
    };
    var histogramBucketInfo = tableData &&
        tableData.data &&
        tableData.data.length &&
        parseHistogramBucketInfo(tableData.data[0]);
    return (<StyledPanel>
      <StyledHeaderTitleLegend>
        {t('Heat Map')}
        <QuestionTooltip size="sm" position="top" title={t('This heatmap shows the frequency for each duration across the most common tag values')}/>
      </StyledHeaderTitleLegend>

      <TransitionChart loading={isLoading} reloading={isLoading}>
        <TransparentLoadingMask visible={isLoading}/>
        <DropdownMenu onOpen={onOpenMenu} onClose={onCloseMenu} shouldIgnoreClickOutside={shouldIgnoreMenuClose}>
          {function (_a) {
            var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, actions = _a.actions;
            var onChartClick = function (bucket) {
                var htmlEvent = bucket.event.event;
                // Make a copy of the dims because echarts can remove elements after this click happens.
                // TODO(k-fish): Look at improving this to respond properly to resize events.
                var virtualRef = new VirtualReference(htmlEvent.target);
                setChartElement(virtualRef);
                var newTransactionEventView = eventView.clone();
                newTransactionEventView.fields = [{ field: aggregateColumn }];
                var _a = __read(bucket.value, 2), _ = _a[0], tagValue = _a[1];
                if (histogramBucketInfo && tableData && tableData.data) {
                    var row = tableData.data[bucket.dataIndex];
                    var currentBucketStart = parseInt("" + row[histogramBucketInfo.histogramField], 10);
                    var currentBucketEnd = currentBucketStart + histogramBucketInfo.bucketSize;
                    newTransactionEventView.additionalConditions.setTagValues(aggregateColumn, [">=" + currentBucketStart, "<" + currentBucketEnd]);
                }
                newTransactionEventView.additionalConditions.setTagValues(tagKey, [
                    tagValue,
                ]);
                setTransactionEventView(newTransactionEventView);
                if (!isMenuOpen) {
                    actions.open();
                }
            };
            return (<React.Fragment>
                {ReactDOM.createPortal(<div>
                    {chartElement ? (<Popper referenceElement={chartElement} placement="bottom">
                        {function (_a) {
                            var ref = _a.ref, style = _a.style, placement = _a.placement;
                            return (<StyledDropdownContainer ref={ref} style={style} className="anchor-middle" data-placement={placement}>
                            <StyledDropdownContent {...getMenuProps({
                                className: classNames('dropdown-menu'),
                            })} isOpen={isOpen} alignMenu="right" blendCorner={false}>
                              {transactionEventView ? (<TagTransactionsQuery query={transactionEventView.getQueryWithAdditionalConditions()} location={location} eventView={transactionEventView} orgSlug={organization.slug} limit={4} referrer="api.performance.tag-page">
                                  {function (_a) {
                                        var isTransactionsLoading = _a.isLoading, transactionTableData = _a.tableData;
                                        var moreEventsTarget = isTransactionsLoading
                                            ? null
                                            : eventsRouteWithQuery({
                                                orgSlug: organization.slug,
                                                transaction: transactionName,
                                                projectID: decodeScalar(location.query.project),
                                                query: __assign(__assign({}, transactionEventView.generateQueryStringObject()), { query: transactionEventView.getQueryWithAdditionalConditions() }),
                                            });
                                        return (<React.Fragment>
                                        {isTransactionsLoading ? (<LoadingContainer>
                                            <LoadingIndicator size={40} hideMessage/>
                                          </LoadingContainer>) : (<div>
                                            {!transactionTableData.data.length ? (<Placeholder />) : null}
                                            {__spreadArray([], __read(transactionTableData.data)).slice(0, 3)
                                                    .map(function (row) {
                                                    var target = generateTransactionLink(transactionName)(organization, row, location.query);
                                                    return (<DropdownItem width="small" key={row.id} to={target}>
                                                    <DropdownItemContainer>
                                                      <Truncate value={row.id} maxLength={12}/>
                                                      <SectionSubtext>
                                                        <PerformanceDuration milliseconds={row[aggregateColumn]} abbreviation/>
                                                      </SectionSubtext>
                                                    </DropdownItemContainer>
                                                  </DropdownItem>);
                                                })}
                                            {moreEventsTarget &&
                                                    transactionTableData.data.length > 3 ? (<DropdownItem width="small" to={moreEventsTarget}>
                                                <DropdownItemContainer>
                                                  {t('View all events')}
                                                </DropdownItemContainer>
                                              </DropdownItem>) : null}
                                          </div>)}
                                      </React.Fragment>);
                                    }}
                                </TagTransactionsQuery>) : null}
                            </StyledDropdownContent>
                          </StyledDropdownContainer>);
                        }}
                      </Popper>) : null}
                  </div>, getPortal())}

                {getDynamicText({
                    value: (<HeatMapChart ref={chartRef} visualMaps={visualMaps} series={series} onClick={onChartClick} {...chartOptions}/>),
                    fixed: <Placeholder height="290px" testId="skeleton-ui"/>,
                })}
              </React.Fragment>);
        }}
        </DropdownMenu>
      </TransitionChart>
    </StyledPanel>);
};
var LoadingContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 200px;\n  height: 100px;\n\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  width: 200px;\n  height: 100px;\n\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var DropdownItemContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  flex-direction: row;\n\n  justify-content: space-between;\n"], ["\n  width: 100%;\n  display: flex;\n  flex-direction: row;\n\n  justify-content: space-between;\n"])));
var StyledDropdownContainer = styled(DropdownContainer)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  z-index: ", ";\n"], ["\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.dropdown; });
var StyledDropdownContent = styled(Content)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  right: auto;\n  transform: translate(-50%);\n\n  overflow: visible;\n"], ["\n  right: auto;\n  transform: translate(-50%);\n\n  overflow: visible;\n"])));
var StyledPanel = styled(Panel)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n  margin-bottom: 0;\n  border-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  padding: ", " ", " 0 ", ";\n  margin-bottom: 0;\n  border-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"])), space(3), space(3), space(3));
var StyledHeaderTitleLegend = styled(HeaderTitleLegend)(templateObject_6 || (templateObject_6 = __makeTemplateObject([""], [""])));
export default withTheme(TagsHeatMap);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=tagsHeatMap.jsx.map