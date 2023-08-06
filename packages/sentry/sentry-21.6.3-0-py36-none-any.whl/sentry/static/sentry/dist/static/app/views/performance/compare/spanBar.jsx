import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { withTheme } from '@emotion/react';
import styled from '@emotion/styled';
import Count from 'app/components/count';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import { isOrphanTreeDepth, unwrapTreeDepth, } from 'app/components/events/interfaces/spans/utils';
import { ROW_HEIGHT, ROW_PADDING } from 'app/components/performance/waterfall/constants';
import { Row, RowCell, RowCellContainer } from 'app/components/performance/waterfall/row';
import { DividerLine, DividerLineGhostContainer, } from 'app/components/performance/waterfall/rowDivider';
import { RowTitle, RowTitleContainer } from 'app/components/performance/waterfall/rowTitle';
import { ConnectorBar, StyledIconChevron, TOGGLE_BORDER_BOX, TreeConnector, TreeToggle, TreeToggleContainer, } from 'app/components/performance/waterfall/treeConnector';
import { getBackgroundColor, getHatchPattern, getHumanDuration, toPercent, } from 'app/components/performance/waterfall/utils';
import { t } from 'app/locale';
import space from 'app/styles/space';
import SpanDetail from './spanDetail';
import { SpanBarRectangle } from './styles';
import { generateCSSWidth, getSpanDescription, getSpanDuration, getSpanID, getSpanOperation, isOrphanDiffSpan, } from './utils';
var SpanBar = /** @class */ (function (_super) {
    __extends(SpanBar, _super);
    function SpanBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDetail: false,
        };
        _this.renderDivider = function (dividerHandlerChildrenProps) {
            var theme = _this.props.theme;
            if (_this.state.showDetail) {
                // Mock component to preserve layout spacing
                return (<DividerLine style={{
                        position: 'relative',
                        backgroundColor: getBackgroundColor({
                            theme: theme,
                            showDetail: true,
                        }),
                    }}/>);
            }
            var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
            return (<DividerLine ref={addDividerLineRef()} style={{
                    position: 'relative',
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
        _this.toggleDisplayDetail = function () {
            _this.setState(function (state) { return ({
                showDetail: !state.showDetail,
            }); });
        };
        return _this;
    }
    SpanBar.prototype.renderSpanTreeConnector = function (_a) {
        var hasToggler = _a.hasToggler;
        var _b = this.props, isLast = _b.isLast, isRoot = _b.isRoot, spanTreeDepth = _b.treeDepth, continuingTreeDepths = _b.continuingTreeDepths, span = _b.span, showSpanTree = _b.showSpanTree;
        var spanID = getSpanID(span);
        if (isRoot) {
            if (hasToggler) {
                return (<ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} key={spanID + "-last"} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingTreeDepths.map(function (treeDepth) {
            var depth = unwrapTreeDepth(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            var left = ((spanTreeDepth - depth) * (TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<ConnectorBar style={{ left: left }} key={spanID + "-" + depth} orphanBranch={isOrphanTreeDepth(treeDepth)}/>);
        });
        if (hasToggler && showSpanTree) {
            // if there is a toggle button, we add a connector bar to create an attachment
            // between the toggle button and any connector bars below the toggle button
            connectorBars.push(<ConnectorBar style={{
                    right: '16px',
                    height: '10px',
                    bottom: isLast ? "-" + ROW_HEIGHT / 2 + "px" : '0',
                    top: 'auto',
                }} key={spanID + "-last"} orphanBranch={false}/>);
        }
        return (<TreeConnector isLast={isLast} hasToggler={hasToggler} orphanBranch={isOrphanDiffSpan(span)}>
        {connectorBars}
      </TreeConnector>);
    };
    SpanBar.prototype.renderSpanTreeToggler = function (_a) {
        var _this = this;
        var left = _a.left;
        var _b = this.props, numOfSpanChildren = _b.numOfSpanChildren, isRoot = _b.isRoot, showSpanTree = _b.showSpanTree;
        var chevron = <StyledIconChevron direction={showSpanTree ? 'up' : 'down'}/>;
        if (numOfSpanChildren <= 0) {
            return (<TreeToggleContainer style={{ left: left + "px" }}>
          {this.renderSpanTreeConnector({ hasToggler: false })}
        </TreeToggleContainer>);
        }
        var chevronElement = !isRoot ? <div>{chevron}</div> : null;
        return (<TreeToggleContainer style={{ left: left + "px" }} hasToggler>
        {this.renderSpanTreeConnector({ hasToggler: true })}
        <TreeToggle disabled={!!isRoot} isExpanded={this.props.showSpanTree} errored={false} onClick={function (event) {
                event.stopPropagation();
                if (isRoot) {
                    return;
                }
                _this.props.toggleSpanTree();
            }}>
          <Count value={numOfSpanChildren}/>
          {chevronElement}
        </TreeToggle>
      </TreeToggleContainer>);
    };
    SpanBar.prototype.renderTitle = function () {
        var _a;
        var _b = this.props, span = _b.span, treeDepth = _b.treeDepth;
        var operationName = getSpanOperation(span) ? (<strong>
        {getSpanOperation(span)}
        {' \u2014 '}
      </strong>) : ('');
        var description = (_a = getSpanDescription(span)) !== null && _a !== void 0 ? _a : (span.comparisonResult === 'matched' ? t('matched') : getSpanID(span));
        var left = treeDepth * (TOGGLE_BORDER_BOX / 2);
        return (<RowTitleContainer>
        {this.renderSpanTreeToggler({ left: left })}
        <RowTitle style={{
                left: left + "px",
                width: '100%',
            }}>
          <span>
            {operationName}
            {description}
          </span>
        </RowTitle>
      </RowTitleContainer>);
    };
    SpanBar.prototype.getSpanBarStyles = function () {
        var _a = this.props, theme = _a.theme, span = _a.span, generateBounds = _a.generateBounds;
        var bounds = generateBounds(span);
        function normalizePadding(width) {
            if (!width) {
                return undefined;
            }
            return "max(1px, " + width + ")";
        }
        switch (span.comparisonResult) {
            case 'matched': {
                var baselineDuration = getSpanDuration(span.baselineSpan);
                var regressionDuration = getSpanDuration(span.regressionSpan);
                if (baselineDuration === regressionDuration) {
                    return {
                        background: {
                            color: undefined,
                            width: normalizePadding(generateCSSWidth(bounds.background)),
                            hatch: true,
                        },
                        foreground: undefined,
                    };
                }
                if (baselineDuration > regressionDuration) {
                    return {
                        background: {
                            // baseline
                            color: theme.textColor,
                            width: normalizePadding(generateCSSWidth(bounds.background)),
                        },
                        foreground: {
                            // regression
                            color: undefined,
                            width: normalizePadding(generateCSSWidth(bounds.foreground)),
                            hatch: true,
                        },
                    };
                }
                // case: baselineDuration < regressionDuration
                return {
                    background: {
                        // regression
                        color: theme.purple200,
                        width: normalizePadding(generateCSSWidth(bounds.background)),
                    },
                    foreground: {
                        // baseline
                        color: undefined,
                        width: normalizePadding(generateCSSWidth(bounds.foreground)),
                        hatch: true,
                    },
                };
            }
            case 'regression': {
                return {
                    background: {
                        color: theme.purple200,
                        width: normalizePadding(generateCSSWidth(bounds.background)),
                    },
                    foreground: undefined,
                };
            }
            case 'baseline': {
                return {
                    background: {
                        color: theme.textColor,
                        width: normalizePadding(generateCSSWidth(bounds.background)),
                    },
                    foreground: undefined,
                };
            }
            default: {
                var _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    };
    SpanBar.prototype.renderComparisonReportLabel = function () {
        var span = this.props.span;
        switch (span.comparisonResult) {
            case 'matched': {
                var baselineDuration = getSpanDuration(span.baselineSpan);
                var regressionDuration = getSpanDuration(span.regressionSpan);
                var label = void 0;
                if (baselineDuration === regressionDuration) {
                    label = <ComparisonLabel>{t('No change')}</ComparisonLabel>;
                }
                if (baselineDuration > regressionDuration) {
                    var duration = getHumanDuration(Math.abs(baselineDuration - regressionDuration));
                    label = (<NotableComparisonLabel>{t('- %s faster', duration)}</NotableComparisonLabel>);
                }
                if (baselineDuration < regressionDuration) {
                    var duration = getHumanDuration(Math.abs(baselineDuration - regressionDuration));
                    label = (<NotableComparisonLabel>{t('+ %s slower', duration)}</NotableComparisonLabel>);
                }
                return label;
            }
            case 'baseline': {
                return <ComparisonLabel>{t('Only in baseline')}</ComparisonLabel>;
            }
            case 'regression': {
                return <ComparisonLabel>{t('Only in this event')}</ComparisonLabel>;
            }
            default: {
                var _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    };
    SpanBar.prototype.renderHeader = function (dividerHandlerChildrenProps) {
        var _this = this;
        var _a, _b;
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        var _c = this.props, spanNumber = _c.spanNumber, span = _c.span;
        var isMatched = span.comparisonResult === 'matched';
        var hideSpanBarColumn = this.state.showDetail && isMatched;
        var spanBarStyles = this.getSpanBarStyles();
        var foregroundSpanBar = spanBarStyles.foreground ? (<ComparisonSpanBarRectangle spanBarHatch={(_a = spanBarStyles.foreground.hatch) !== null && _a !== void 0 ? _a : false} style={{
                backgroundColor: spanBarStyles.foreground.color,
                width: spanBarStyles.foreground.width,
                display: hideSpanBarColumn ? 'none' : 'block',
            }}/>) : null;
        return (<RowCellContainer showDetail={this.state.showDetail}>
        <RowCell data-type="span-row-cell" showDetail={this.state.showDetail} style={{
                width: "calc(" + toPercent(dividerPosition) + " - 0.5px)",
            }} onClick={function () {
                _this.toggleDisplayDetail();
            }}>
          {this.renderTitle()}
        </RowCell>
        {this.renderDivider(dividerHandlerChildrenProps)}
        <RowCell data-type="span-row-cell" showDetail={this.state.showDetail} showStriping={spanNumber % 2 !== 0} style={{
                width: "calc(" + toPercent(1 - dividerPosition) + " - 0.5px)",
            }} onClick={function () {
                _this.toggleDisplayDetail();
            }}>
          <SpanContainer>
            <ComparisonSpanBarRectangle spanBarHatch={(_b = spanBarStyles.background.hatch) !== null && _b !== void 0 ? _b : false} style={{
                backgroundColor: spanBarStyles.background.color,
                width: spanBarStyles.background.width,
                display: hideSpanBarColumn ? 'none' : 'block',
            }}/>
            {foregroundSpanBar}
          </SpanContainer>
          {this.renderComparisonReportLabel()}
        </RowCell>
        {!this.state.showDetail && (<DividerLineGhostContainer style={{
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
          </DividerLineGhostContainer>)}
      </RowCellContainer>);
    };
    SpanBar.prototype.renderDetail = function () {
        if (!this.state.showDetail) {
            return null;
        }
        var _a = this.props, span = _a.span, generateBounds = _a.generateBounds;
        return <SpanDetail span={this.props.span} bounds={generateBounds(span)}/>;
    };
    SpanBar.prototype.render = function () {
        var _this = this;
        return (<Row visible data-test-id="span-row">
        <DividerHandlerManager.Consumer>
          {function (dividerHandlerChildrenProps) { return _this.renderHeader(dividerHandlerChildrenProps); }}
        </DividerHandlerManager.Consumer>
        {this.renderDetail()}
      </Row>);
    };
    return SpanBar;
}(React.Component));
var ComparisonSpanBarRectangle = styled(SpanBarRectangle)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  left: 0;\n  height: 16px;\n  ", "\n"], ["\n  position: absolute;\n  left: 0;\n  height: 16px;\n  ", "\n"])), function (p) { return getHatchPattern(p, p.theme.purple200, p.theme.gray500); });
var ComparisonLabel = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  user-select: none;\n  right: ", ";\n  line-height: ", "px;\n  top: ", "px;\n  font-size: ", ";\n"], ["\n  position: absolute;\n  user-select: none;\n  right: ", ";\n  line-height: ", "px;\n  top: ", "px;\n  font-size: ", ";\n"])), space(1), ROW_HEIGHT - 2 * ROW_PADDING, ROW_PADDING, function (p) { return p.theme.fontSizeExtraSmall; });
var SpanContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  margin-right: 120px;\n"], ["\n  position: relative;\n  margin-right: 120px;\n"])));
var NotableComparisonLabel = styled(ComparisonLabel)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
export default withTheme(SpanBar);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=spanBar.jsx.map