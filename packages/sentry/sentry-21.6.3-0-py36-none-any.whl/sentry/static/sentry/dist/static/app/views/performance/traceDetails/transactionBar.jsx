import { __extends } from "tslib";
import * as React from 'react';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Count from 'app/components/count';
import * as AnchorLinkManager from 'app/components/events/interfaces/spans/anchorLinkManager';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import * as ScrollbarManager from 'app/components/events/interfaces/spans/scrollbarManager';
import { ROW_HEIGHT } from 'app/components/performance/waterfall/constants';
import { Row, RowCell, RowCellContainer } from 'app/components/performance/waterfall/row';
import { DurationPill, RowRectangle } from 'app/components/performance/waterfall/rowBar';
import { DividerContainer, DividerLine, DividerLineGhostContainer, ErrorBadge, } from 'app/components/performance/waterfall/rowDivider';
import { RowTitle, RowTitleContainer, RowTitleContent, } from 'app/components/performance/waterfall/rowTitle';
import { ConnectorBar, StyledIconChevron, TOGGLE_BORDER_BOX, TreeConnector, TreeToggle, TreeToggleContainer, } from 'app/components/performance/waterfall/treeConnector';
import { getDurationDisplay, getHumanDuration, toPercent, } from 'app/components/performance/waterfall/utils';
import Tooltip from 'app/components/tooltip';
import { isTraceFullDetailed } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
import { StyledProjectBadge } from './styles';
import TransactionDetail from './transactionDetail';
var MARGIN_LEFT = 0;
var TransactionBar = /** @class */ (function (_super) {
    __extends(TransactionBar, _super);
    function TransactionBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDetail: false,
        };
        _this.transactionRowDOMRef = React.createRef();
        _this.toggleDisplayDetail = function () {
            var transaction = _this.props.transaction;
            if (isTraceFullDetailed(transaction)) {
                _this.setState(function (state) { return ({
                    showDetail: !state.showDetail,
                }); });
            }
        };
        _this.scrollIntoView = function () {
            var element = _this.transactionRowDOMRef.current;
            if (!element) {
                return;
            }
            var boundingRect = element.getBoundingClientRect();
            var offset = boundingRect.top + window.scrollY;
            _this.setState({ showDetail: true }, function () { return window.scrollTo(0, offset); });
        };
        return _this;
    }
    TransactionBar.prototype.getCurrentOffset = function () {
        var transaction = this.props.transaction;
        var generation = transaction.generation;
        return getOffset(generation);
    };
    TransactionBar.prototype.renderConnector = function (hasToggle) {
        var _a = this.props, continuingDepths = _a.continuingDepths, isExpanded = _a.isExpanded, isOrphan = _a.isOrphan, isLast = _a.isLast, transaction = _a.transaction;
        var generation = transaction.generation;
        var eventId = isTraceFullDetailed(transaction)
            ? transaction.event_id
            : transaction.traceSlug;
        if (generation === 0) {
            if (hasToggle) {
                return (<ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingDepths.map(function (_a) {
            var depth = _a.depth, isOrphanDepth = _a.isOrphanDepth;
            if (generation - depth <= 1) {
                // If the difference is less than or equal to 1, then it means that the continued
                // bar is from its direct parent. In this case, do not render a connector bar
                // because the tree connector below will suffice.
                return null;
            }
            var left = -1 * getOffset(generation - depth - 1) - 1;
            return (<ConnectorBar style={{ left: left }} key={eventId + "-" + depth} orphanBranch={isOrphanDepth}/>);
        });
        if (hasToggle && isExpanded) {
            connectorBars.push(<ConnectorBar style={{
                    right: '16px',
                    height: '10px',
                    bottom: isLast ? "-" + ROW_HEIGHT / 2 + "px" : '0',
                    top: 'auto',
                }} key={eventId + "-last"} orphanBranch={false}/>);
        }
        return (<TreeConnector isLast={isLast} hasToggler={hasToggle} orphanBranch={isOrphan}>
        {connectorBars}
      </TreeConnector>);
    };
    TransactionBar.prototype.renderToggle = function (errored) {
        var _a = this.props, isExpanded = _a.isExpanded, transaction = _a.transaction, toggleExpandedState = _a.toggleExpandedState;
        var children = transaction.children, generation = transaction.generation;
        var left = this.getCurrentOffset();
        if (children.length <= 0) {
            return (<TreeToggleContainer style={{ left: left + "px" }}>
          {this.renderConnector(false)}
        </TreeToggleContainer>);
        }
        var isRoot = generation === 0;
        return (<TreeToggleContainer style={{ left: left + "px" }} hasToggler>
        {this.renderConnector(true)}
        <TreeToggle disabled={isRoot} isExpanded={isExpanded} errored={errored} onClick={function (event) {
                event.stopPropagation();
                if (isRoot) {
                    return;
                }
                toggleExpandedState();
            }}>
          <Count value={children.length}/>
          {!isRoot && (<div>
              <StyledIconChevron direction={isExpanded ? 'up' : 'down'}/>
            </div>)}
        </TreeToggle>
      </TreeToggleContainer>);
    };
    TransactionBar.prototype.renderTitle = function (scrollbarManagerChildrenProps) {
        var generateContentSpanBarRef = scrollbarManagerChildrenProps.generateContentSpanBarRef;
        var _a = this.props, organization = _a.organization, transaction = _a.transaction;
        var left = this.getCurrentOffset();
        var errored = isTraceFullDetailed(transaction)
            ? transaction.errors.length > 0
            : false;
        var content = isTraceFullDetailed(transaction) ? (<React.Fragment>
        <Projects orgId={organization.slug} slugs={[transaction.project_slug]}>
          {function (_a) {
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === transaction.project_slug; });
                return (<Tooltip title={transaction.project_slug}>
                <StyledProjectBadge project={project ? project : { slug: transaction.project_slug }} avatarSize={16} hideName/>
              </Tooltip>);
            }}
        </Projects>
        <RowTitleContent errored={errored}>
          <strong>
            {transaction['transaction.op']}
            {' \u2014 '}
          </strong>
          {transaction.transaction}
        </RowTitleContent>
      </React.Fragment>) : (<RowTitleContent errored={false}>
        <strong>{'Trace \u2014 '}</strong>
        {transaction.traceSlug}
      </RowTitleContent>);
        return (<RowTitleContainer ref={generateContentSpanBarRef()}>
        {this.renderToggle(errored)}
        <RowTitle style={{
                left: left + "px",
                width: '100%',
            }}>
          {content}
        </RowTitle>
      </RowTitleContainer>);
    };
    TransactionBar.prototype.renderDivider = function (dividerHandlerChildrenProps) {
        if (this.state.showDetail) {
            // Mock component to preserve layout spacing
            return (<DividerLine showDetail style={{
                    position: 'absolute',
                }}/>);
        }
        var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
        return (<DividerLine ref={addDividerLineRef()} style={{
                position: 'absolute',
            }} onMouseEnter={function () {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseLeave={function () {
                dividerHandlerChildrenProps.setHover(false);
            }} onMouseOver={function () {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={function (event) {
                // we prevent the propagation of the clicks from this component to prevent
                // the span detail from being opened.
                event.stopPropagation();
            }}/>);
    };
    TransactionBar.prototype.renderGhostDivider = function (dividerHandlerChildrenProps) {
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        return (<DividerLineGhostContainer style={{
                width: "calc(" + toPercent(dividerPosition) + " + 0.5px)",
                display: 'none',
            }}>
        <DividerLine ref={addGhostDividerLineRef()} style={{
                right: 0,
            }} className="hovering" onClick={function (event) {
                // the ghost divider line should not be interactive.
                // we prevent the propagation of the clicks from this component to prevent
                // the span detail from being opened.
                event.stopPropagation();
            }}/>
      </DividerLineGhostContainer>);
    };
    TransactionBar.prototype.renderErrorBadge = function () {
        var transaction = this.props.transaction;
        if (!isTraceFullDetailed(transaction) || !transaction.errors.length) {
            return null;
        }
        return <ErrorBadge />;
    };
    TransactionBar.prototype.renderRectangle = function () {
        var _a = this.props, transaction = _a.transaction, traceInfo = _a.traceInfo, barColour = _a.barColour;
        var showDetail = this.state.showDetail;
        // Use 1 as the difference in the event that startTimestamp === endTimestamp
        var delta = Math.abs(traceInfo.endTimestamp - traceInfo.startTimestamp) || 1;
        var startPosition = Math.abs(transaction.start_timestamp - traceInfo.startTimestamp);
        var startPercentage = startPosition / delta;
        var duration = Math.abs(transaction.timestamp - transaction.start_timestamp);
        var widthPercentage = duration / delta;
        return (<RowRectangle spanBarHatch={false} style={{
                backgroundColor: barColour,
                left: "min(" + toPercent(startPercentage || 0) + ", calc(100% - 1px))",
                width: toPercent(widthPercentage || 0),
            }}>
        <DurationPill durationDisplay={getDurationDisplay({
                left: startPercentage,
                width: widthPercentage,
            })} showDetail={showDetail} spanBarHatch={false}>
          {getHumanDuration(duration)}
        </DurationPill>
      </RowRectangle>);
    };
    TransactionBar.prototype.renderHeader = function (_a) {
        var dividerHandlerChildrenProps = _a.dividerHandlerChildrenProps, scrollbarManagerChildrenProps = _a.scrollbarManagerChildrenProps;
        var _b = this.props, hasGuideAnchor = _b.hasGuideAnchor, index = _b.index;
        var showDetail = this.state.showDetail;
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition;
        return (<RowCellContainer showDetail={showDetail}>
        <RowCell data-test-id="transaction-row-title" data-type="span-row-cell" style={{
                width: "calc(" + toPercent(dividerPosition) + " - 0.5px)",
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          <GuideAnchor target="trace_view_guide_row" disabled={!hasGuideAnchor}>
            {this.renderTitle(scrollbarManagerChildrenProps)}
          </GuideAnchor>
        </RowCell>
        <DividerContainer>
          {this.renderDivider(dividerHandlerChildrenProps)}
          {this.renderErrorBadge()}
        </DividerContainer>
        <RowCell data-test-id="transaction-row-duration" data-type="span-row-cell" showStriping={index % 2 !== 0} style={{
                width: "calc(" + toPercent(1 - dividerPosition) + " - 0.5px)",
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          <GuideAnchor target="trace_view_guide_row_details" disabled={!hasGuideAnchor}>
            {this.renderRectangle()}
          </GuideAnchor>
        </RowCell>
        {!showDetail && this.renderGhostDivider(dividerHandlerChildrenProps)}
      </RowCellContainer>);
    };
    TransactionBar.prototype.renderDetail = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, isVisible = _a.isVisible, transaction = _a.transaction;
        var showDetail = this.state.showDetail;
        return (<AnchorLinkManager.Consumer>
        {function (_a) {
                var registerScrollFn = _a.registerScrollFn, scrollToHash = _a.scrollToHash;
                if (!isTraceFullDetailed(transaction)) {
                    return null;
                }
                registerScrollFn("#txn-" + transaction.event_id, _this.scrollIntoView);
                if (!isVisible || !showDetail) {
                    return null;
                }
                return (<TransactionDetail location={location} organization={organization} transaction={transaction} scrollToHash={scrollToHash}/>);
            }}
      </AnchorLinkManager.Consumer>);
    };
    TransactionBar.prototype.render = function () {
        var _this = this;
        var _a = this.props, isVisible = _a.isVisible, transaction = _a.transaction;
        var showDetail = this.state.showDetail;
        return (<Row ref={this.transactionRowDOMRef} visible={isVisible} showBorder={showDetail} cursor={isTraceFullDetailed(transaction) ? 'pointer' : 'default'}>
        <ScrollbarManager.Consumer>
          {function (scrollbarManagerChildrenProps) { return (<DividerHandlerManager.Consumer>
              {function (dividerHandlerChildrenProps) {
                    return _this.renderHeader({
                        dividerHandlerChildrenProps: dividerHandlerChildrenProps,
                        scrollbarManagerChildrenProps: scrollbarManagerChildrenProps,
                    });
                }}
            </DividerHandlerManager.Consumer>); }}
        </ScrollbarManager.Consumer>
        {this.renderDetail()}
      </Row>);
    };
    return TransactionBar;
}(React.Component));
function getOffset(generation) {
    return generation * (TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
}
export default TransactionBar;
//# sourceMappingURL=transactionBar.jsx.map