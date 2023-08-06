import { __extends } from "tslib";
import { createRef, PureComponent } from 'react';
import { Observer } from 'mobx-react';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { t } from 'app/locale';
import * as CursorGuideHandler from './cursorGuideHandler';
import * as DividerHandlerManager from './dividerHandlerManager';
import DragManager from './dragManager';
import TraceViewHeader from './header';
import * as ScrollbarManager from './scrollbarManager';
import SpanTree from './spanTree';
import { getTraceContext } from './utils';
var TraceView = /** @class */ (function (_super) {
    __extends(TraceView, _super);
    function TraceView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.traceViewRef = createRef();
        _this.virtualScrollBarContainerRef = createRef();
        _this.minimapInteractiveRef = createRef();
        _this.renderHeader = function (dragProps) { return (<Observer>
      {function () {
                var waterfallModel = _this.props.waterfallModel;
                return (<TraceViewHeader organization={_this.props.organization} minimapInteractiveRef={_this.minimapInteractiveRef} dragProps={dragProps} trace={waterfallModel.parsedTrace} event={waterfallModel.event} virtualScrollBarContainerRef={_this.virtualScrollBarContainerRef} operationNameFilters={waterfallModel.operationNameFilters}/>);
            }}
    </Observer>); };
        return _this;
    }
    TraceView.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, waterfallModel = _a.waterfallModel;
        if (!getTraceContext(waterfallModel.event)) {
            return (<EmptyStateWarning>
          <p>{t('There is no trace for this transaction')}</p>
        </EmptyStateWarning>);
        }
        return (<DragManager interactiveLayerRef={this.minimapInteractiveRef}>
        {function (dragProps) { return (<Observer>
            {function () {
                    var parsedTrace = waterfallModel.parsedTrace;
                    return (<CursorGuideHandler.Provider interactiveLayerRef={_this.minimapInteractiveRef} dragProps={dragProps} trace={parsedTrace}>
                  <DividerHandlerManager.Provider interactiveLayerRef={_this.traceViewRef}>
                    <DividerHandlerManager.Consumer>
                      {function (dividerHandlerChildrenProps) {
                            return (<ScrollbarManager.Provider dividerPosition={dividerHandlerChildrenProps.dividerPosition} interactiveLayerRef={_this.virtualScrollBarContainerRef} dragProps={dragProps}>
                            {_this.renderHeader(dragProps)}
                            <Observer>
                              {function () {
                                    return (<SpanTree traceViewRef={_this.traceViewRef} dragProps={dragProps} organization={organization} waterfallModel={waterfallModel} filterSpans={waterfallModel.filterSpans} spans={waterfallModel.getWaterfall({
                                            viewStart: dragProps.viewWindowStart,
                                            viewEnd: dragProps.viewWindowEnd,
                                        })}/>);
                                }}
                            </Observer>
                          </ScrollbarManager.Provider>);
                        }}
                    </DividerHandlerManager.Consumer>
                  </DividerHandlerManager.Provider>
                </CursorGuideHandler.Provider>);
                }}
          </Observer>); }}
      </DragManager>);
    };
    return TraceView;
}(PureComponent));
export default TraceView;
//# sourceMappingURL=traceView.jsx.map