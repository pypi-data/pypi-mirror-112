import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import * as React from 'react';
import * as Sentry from '@sentry/react';
import Alert from 'app/components/alert';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import ButtonBar from 'app/components/buttonBar';
import DiscoverFeature from 'app/components/discover/discoverFeature';
import DiscoverButton from 'app/components/discoverButton';
import * as AnchorLinkManager from 'app/components/events/interfaces/spans/anchorLinkManager';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import * as ScrollbarManager from 'app/components/events/interfaces/spans/scrollbarManager';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { MessageRow } from 'app/components/performance/waterfall/messageRow';
import { DividerSpacer, ScrollbarContainer, VirtualScrollbar, VirtualScrollbarGrip, } from 'app/components/performance/waterfall/miniHeader';
import { pickBarColour, toPercent } from 'app/components/performance/waterfall/utils';
import TimeSince from 'app/components/timeSince';
import { IconInfo } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
import { getDuration } from 'app/utils/formatters';
import getDynamicText from 'app/utils/getDynamicText';
import { filterTrace, reduceTrace } from 'app/utils/performance/quickTrace/utils';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { MetaData } from 'app/views/performance/transactionDetails/styles';
import { SearchContainer, StyledPanel, StyledSearchBar, TraceDetailBody, TraceDetailHeader, TraceViewContainer, TraceViewHeaderContainer, } from './styles';
import TransactionGroup from './transactionGroup';
import { getTraceInfo, isRootTransaction } from './utils';
var TraceDetailsContent = /** @class */ (function (_super) {
    __extends(TraceDetailsContent, _super);
    function TraceDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchQuery: undefined,
            filteredTransactionIds: undefined,
        };
        _this.traceViewRef = React.createRef();
        _this.virtualScrollbarContainerRef = React.createRef();
        _this.handleTransactionFilter = function (searchQuery) {
            _this.setState({ searchQuery: searchQuery || undefined }, _this.filterTransactions);
        };
        _this.filterTransactions = function () { return __awaiter(_this, void 0, void 0, function () {
            var traces, _a, filteredTransactionIds, searchQuery, transformed, fuse, fuseMatches, idMatches;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        traces = this.props.traces;
                        _a = this.state, filteredTransactionIds = _a.filteredTransactionIds, searchQuery = _a.searchQuery;
                        if (!searchQuery || traces === null || traces.length <= 0) {
                            if (filteredTransactionIds !== undefined) {
                                this.setState({
                                    filteredTransactionIds: undefined,
                                });
                            }
                            return [2 /*return*/];
                        }
                        transformed = traces.flatMap(function (trace) {
                            return reduceTrace(trace, function (acc, transaction) {
                                var indexed = [
                                    transaction['transaction.op'],
                                    transaction.transaction,
                                    transaction.project_slug,
                                ];
                                acc.push({
                                    transaction: transaction,
                                    indexed: indexed,
                                });
                                return acc;
                            }, []);
                        });
                        return [4 /*yield*/, createFuzzySearch(transformed, {
                                keys: ['indexed'],
                                includeMatches: true,
                                threshold: 0.6,
                                location: 0,
                                distance: 100,
                                maxPatternLength: 32,
                            })];
                    case 1:
                        fuse = _b.sent();
                        fuseMatches = fuse
                            .search(searchQuery)
                            /**
                             * Sometimes, there can be matches that don't include any
                             * indices. These matches are often noise, so exclude them.
                             */
                            .filter(function (_a) {
                            var matches = _a.matches;
                            return matches.length;
                        })
                            .map(function (_a) {
                            var item = _a.item;
                            return item.transaction.event_id;
                        });
                        idMatches = traces
                            .flatMap(function (trace) {
                            return filterTrace(trace, function (_a) {
                                var event_id = _a.event_id, span_id = _a.span_id;
                                return event_id.includes(searchQuery) || span_id.includes(searchQuery);
                            });
                        })
                            .map(function (transaction) { return transaction.event_id; });
                        this.setState({
                            filteredTransactionIds: new Set(__spreadArray(__spreadArray([], __read(fuseMatches)), __read(idMatches))),
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.isTransactionVisible = function (transaction) {
            var filteredTransactionIds = _this.state.filteredTransactionIds;
            return filteredTransactionIds
                ? filteredTransactionIds.has(transaction.event_id)
                : true;
        };
        return _this;
    }
    TraceDetailsContent.prototype.renderTraceLoading = function () {
        return <LoadingIndicator />;
    };
    TraceDetailsContent.prototype.renderTraceRequiresDateRangeSelection = function () {
        return <LoadingError message={t('Trace view requires a date range selection.')}/>;
    };
    TraceDetailsContent.prototype.renderTraceNotFound = function () {
        return <LoadingError message={t('The trace you are looking for was not found.')}/>;
    };
    TraceDetailsContent.prototype.renderSearchBar = function () {
        return (<SearchContainer>
        <StyledSearchBar defaultQuery="" query={this.state.searchQuery || ''} placeholder={t('Search for transactions')} onSearch={this.handleTransactionFilter}/>
      </SearchContainer>);
    };
    TraceDetailsContent.prototype.renderTraceHeader = function (traceInfo) {
        var _a, _b, _c;
        var meta = this.props.meta;
        return (<TraceDetailHeader>
        <GuideAnchor target="trace_view_guide_breakdown">
          <MetaData headingText={t('Event Breakdown')} tooltipText={t('The number of transactions and errors there are in this trace.')} bodyText={tct('[transactions]  |  [errors]', {
                transactions: tn('%s Transaction', '%s Transactions', (_a = meta === null || meta === void 0 ? void 0 : meta.transactions) !== null && _a !== void 0 ? _a : traceInfo.transactions.size),
                errors: tn('%s Error', '%s Errors', (_b = meta === null || meta === void 0 ? void 0 : meta.errors) !== null && _b !== void 0 ? _b : traceInfo.errors.size),
            })} subtext={tn('Across %s project', 'Across %s projects', (_c = meta === null || meta === void 0 ? void 0 : meta.projects) !== null && _c !== void 0 ? _c : traceInfo.projects.size)}/>
        </GuideAnchor>
        <MetaData headingText={t('Total Duration')} tooltipText={t('The time elapsed between the start and end of this trace.')} bodyText={getDuration(traceInfo.endTimestamp - traceInfo.startTimestamp, 2, true)} subtext={getDynamicText({
                value: <TimeSince date={(traceInfo.endTimestamp || 0) * 1000}/>,
                fixed: '5 days ago',
            })}/>
      </TraceDetailHeader>);
    };
    TraceDetailsContent.prototype.renderTraceWarnings = function () {
        var traces = this.props.traces;
        var _a = (traces !== null && traces !== void 0 ? traces : []).reduce(function (counts, trace) {
            if (isRootTransaction(trace)) {
                counts.roots++;
            }
            else {
                counts.orphans++;
            }
            return counts;
        }, { roots: 0, orphans: 0 }), roots = _a.roots, orphans = _a.orphans;
        var warning = null;
        if (roots === 0 && orphans > 0) {
            warning = (<Alert type="info" icon={<IconInfo size="sm"/>}>
          <ExternalLink href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {t('A root transaction is missing. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </ExternalLink>
        </Alert>);
        }
        else if (roots === 1 && orphans > 0) {
            warning = (<Alert type="info" icon={<IconInfo size="sm"/>}>
          <ExternalLink href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {t('This trace has broken subtraces. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </ExternalLink>
        </Alert>);
        }
        else if (roots > 1) {
            warning = (<Alert type="info" icon={<IconInfo size="sm"/>}>
          <ExternalLink href="https://docs.sentry.io/product/performance/trace-view/#multiple-roots">
            {t('Multiple root transactions have been found with this trace ID.')}
          </ExternalLink>
        </Alert>);
        }
        return warning;
    };
    TraceDetailsContent.prototype.renderInfoMessage = function (_a) {
        var isVisible = _a.isVisible, numberOfHiddenTransactionsAbove = _a.numberOfHiddenTransactionsAbove;
        var messages = [];
        if (isVisible) {
            if (numberOfHiddenTransactionsAbove === 1) {
                messages.push(<span key="stuff">
            {tct('[numOfTransaction] hidden transaction', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
            else if (numberOfHiddenTransactionsAbove > 1) {
                messages.push(<span key="stuff">
            {tct('[numOfTransaction] hidden transactions', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
        }
        if (messages.length <= 0) {
            return null;
        }
        return <MessageRow>{messages}</MessageRow>;
    };
    TraceDetailsContent.prototype.renderLimitExceededMessage = function (traceInfo) {
        var _a;
        var _b = this.props, traceEventView = _b.traceEventView, organization = _b.organization, meta = _b.meta;
        var count = traceInfo.transactions.size;
        var totalTransactions = (_a = meta === null || meta === void 0 ? void 0 : meta.transactions) !== null && _a !== void 0 ? _a : count;
        if (totalTransactions === null || count >= totalTransactions) {
            return null;
        }
        var target = traceEventView.getResultsViewUrlTarget(organization.slug);
        return (<MessageRow>
        {tct('Limited to a view of [count] transactions. To view the full list, [discover].', {
                count: count,
                discover: (<DiscoverFeature>
                {function (_a) {
                        var hasFeature = _a.hasFeature;
                        return (<Link disabled={!hasFeature} to={target}>
                    Open in Discover
                  </Link>);
                    }}
              </DiscoverFeature>),
            })}
      </MessageRow>);
    };
    TraceDetailsContent.prototype.renderTransaction = function (transaction, _a) {
        var _this = this;
        var continuingDepths = _a.continuingDepths, isOrphan = _a.isOrphan, isLast = _a.isLast, index = _a.index, numberOfHiddenTransactionsAbove = _a.numberOfHiddenTransactionsAbove, traceInfo = _a.traceInfo, hasGuideAnchor = _a.hasGuideAnchor;
        var _b = this.props, location = _b.location, organization = _b.organization;
        var children = transaction.children, eventId = transaction.event_id;
        // Add 1 to the generation to make room for the "root trace"
        var generation = transaction.generation + 1;
        var isVisible = this.isTransactionVisible(transaction);
        var accumulated = children.reduce(function (acc, child, idx) {
            var isLastChild = idx === children.length - 1;
            var hasChildren = child.children.length > 0;
            var result = _this.renderTransaction(child, {
                continuingDepths: !isLastChild && hasChildren
                    ? __spreadArray(__spreadArray([], __read(continuingDepths)), [{ depth: generation, isOrphanDepth: isOrphan }]) : continuingDepths,
                isOrphan: isOrphan,
                isLast: isLastChild,
                index: acc.lastIndex + 1,
                numberOfHiddenTransactionsAbove: acc.numberOfHiddenTransactionsAbove,
                traceInfo: traceInfo,
                hasGuideAnchor: false,
            });
            acc.lastIndex = result.lastIndex;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.renderedChildren.push(result.transactionGroup);
            return acc;
        }, {
            renderedChildren: [],
            lastIndex: index,
            numberOfHiddenTransactionsAbove: isVisible
                ? 0
                : numberOfHiddenTransactionsAbove + 1,
        });
        return {
            transactionGroup: (<React.Fragment key={eventId}>
          {this.renderInfoMessage({
                    isVisible: isVisible,
                    numberOfHiddenTransactionsAbove: numberOfHiddenTransactionsAbove,
                })}
          <TransactionGroup location={location} organization={organization} traceInfo={traceInfo} transaction={__assign(__assign({}, transaction), { generation: generation })} continuingDepths={continuingDepths} isOrphan={isOrphan} isLast={isLast} index={index} isVisible={isVisible} hasGuideAnchor={hasGuideAnchor} renderedChildren={accumulated.renderedChildren} barColour={pickBarColour(transaction['transaction.op'])}/>
        </React.Fragment>),
            lastIndex: accumulated.lastIndex,
            numberOfHiddenTransactionsAbove: accumulated.numberOfHiddenTransactionsAbove,
        };
    };
    TraceDetailsContent.prototype.renderTraceView = function (traceInfo) {
        var _this = this;
        var _a;
        var sentryTransaction = (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
        var sentrySpan = sentryTransaction === null || sentryTransaction === void 0 ? void 0 : sentryTransaction.startChild({
            op: 'trace.render',
            description: 'trace-view-content',
        });
        var _b = this.props, location = _b.location, organization = _b.organization, traces = _b.traces, traceSlug = _b.traceSlug;
        if (traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        var accumulator = {
            index: 1,
            numberOfHiddenTransactionsAbove: 0,
            traceInfo: traceInfo,
            transactionGroups: [],
        };
        var _c = traces.reduce(function (acc, trace, index) {
            var isLastTransaction = index === traces.length - 1;
            var hasChildren = trace.children.length > 0;
            var isNextChildOrphaned = !isLastTransaction && traces[index + 1].parent_span_id !== null;
            var result = _this.renderTransaction(trace, __assign(__assign({}, acc), { 
                // if the root of a subtrace has a parent_span_idk, then it must be an orphan
                isOrphan: !isRootTransaction(trace), isLast: isLastTransaction, continuingDepths: !isLastTransaction && hasChildren
                    ? [{ depth: 0, isOrphanDepth: isNextChildOrphaned }]
                    : [], hasGuideAnchor: index === 0 }));
            acc.index = result.lastIndex + 1;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.transactionGroups.push(result.transactionGroup);
            return acc;
        }, accumulator), transactionGroups = _c.transactionGroups, numberOfHiddenTransactionsAbove = _c.numberOfHiddenTransactionsAbove;
        var traceView = (<TraceDetailBody>
        <DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
          <DividerHandlerManager.Consumer>
            {function (_a) {
                var dividerPosition = _a.dividerPosition;
                return (<ScrollbarManager.Provider dividerPosition={dividerPosition} interactiveLayerRef={_this.virtualScrollbarContainerRef}>
                <StyledPanel>
                  <TraceViewHeaderContainer>
                    <ScrollbarManager.Consumer>
                      {function (_a) {
                        var virtualScrollbarRef = _a.virtualScrollbarRef, scrollBarAreaRef = _a.scrollBarAreaRef, onDragStart = _a.onDragStart, onScroll = _a.onScroll;
                        return (<ScrollbarContainer ref={_this.virtualScrollbarContainerRef} style={{
                                // the width of this component is shrunk to compensate for half of the width of the divider line
                                width: "calc(" + toPercent(dividerPosition) + " - 0.5px)",
                            }} onScroll={onScroll}>
                            <div style={{
                                width: 0,
                                height: '1px',
                            }} ref={scrollBarAreaRef}/>
                            <VirtualScrollbar data-type="virtual-scrollbar" ref={virtualScrollbarRef} onMouseDown={onDragStart}>
                              <VirtualScrollbarGrip />
                            </VirtualScrollbar>
                          </ScrollbarContainer>);
                    }}
                    </ScrollbarManager.Consumer>
                    <DividerSpacer />
                  </TraceViewHeaderContainer>
                  <TraceViewContainer ref={_this.traceViewRef}>
                    <AnchorLinkManager.Provider>
                      <TransactionGroup location={location} organization={organization} traceInfo={traceInfo} transaction={{
                        traceSlug: traceSlug,
                        generation: 0,
                        'transaction.duration': traceInfo.endTimestamp - traceInfo.startTimestamp,
                        children: traces,
                        start_timestamp: traceInfo.startTimestamp,
                        timestamp: traceInfo.endTimestamp,
                    }} continuingDepths={[]} isOrphan={false} isLast={false} index={0} isVisible hasGuideAnchor={false} renderedChildren={transactionGroups} barColour={pickBarColour('')}/>
                    </AnchorLinkManager.Provider>
                    {_this.renderInfoMessage({
                        isVisible: true,
                        numberOfHiddenTransactionsAbove: numberOfHiddenTransactionsAbove,
                    })}
                    {_this.renderLimitExceededMessage(traceInfo)}
                  </TraceViewContainer>
                </StyledPanel>
              </ScrollbarManager.Provider>);
            }}
          </DividerHandlerManager.Consumer>
        </DividerHandlerManager.Provider>
      </TraceDetailBody>);
        sentrySpan === null || sentrySpan === void 0 ? void 0 : sentrySpan.finish();
        return traceView;
    };
    TraceDetailsContent.prototype.renderContent = function () {
        var _a = this.props, dateSelected = _a.dateSelected, isLoading = _a.isLoading, error = _a.error, traces = _a.traces;
        if (!dateSelected) {
            return this.renderTraceRequiresDateRangeSelection();
        }
        else if (isLoading) {
            return this.renderTraceLoading();
        }
        else if (error !== null || traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        else {
            var traceInfo = getTraceInfo(traces);
            return (<React.Fragment>
          {this.renderTraceWarnings()}
          {this.renderTraceHeader(traceInfo)}
          {this.renderSearchBar()}
          {this.renderTraceView(traceInfo)}
        </React.Fragment>);
        }
    };
    TraceDetailsContent.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, traceEventView = _a.traceEventView, traceSlug = _a.traceSlug;
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumb organization={organization} location={location} traceSlug={traceSlug}/>
            <Layout.Title data-test-id="trace-header">
              {t('Trace ID: %s', traceSlug)}
            </Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <ButtonBar gap={1}>
              <DiscoverButton to={traceEventView.getResultsViewUrlTarget(organization.slug)}>
                Open in Discover
              </DiscoverButton>
            </ButtonBar>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>{this.renderContent()}</Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    };
    return TraceDetailsContent;
}(React.Component));
export default TraceDetailsContent;
//# sourceMappingURL=content.jsx.map