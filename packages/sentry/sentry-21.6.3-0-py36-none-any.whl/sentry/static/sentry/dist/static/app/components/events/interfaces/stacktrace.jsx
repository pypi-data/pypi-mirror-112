import { __assign, __extends } from "tslib";
import * as React from 'react';
import EventDataSection from 'app/components/events/eventDataSection';
import CrashContent from 'app/components/events/interfaces/crashContent';
import CrashActions from 'app/components/events/interfaces/crashHeader/crashActions';
import CrashTitle from 'app/components/events/interfaces/crashHeader/crashTitle';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import { STACK_TYPE, STACK_VIEW } from 'app/types/stacktrace';
import NoStackTraceMessage from './noStackTraceMessage';
export function isStacktraceNewestFirst() {
    var user = ConfigStore.get('user');
    // user may not be authenticated
    if (!user) {
        return true;
    }
    switch (user.options.stacktraceOrder) {
        case 2:
            return true;
        case 1:
            return false;
        case -1:
        default:
            return true;
    }
}
var defaultProps = {
    hideGuide: false,
};
var StacktraceInterface = /** @class */ (function (_super) {
    __extends(StacktraceInterface, _super);
    function StacktraceInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            stackView: _this.props.data.hasSystemFrames ? STACK_VIEW.APP : STACK_VIEW.FULL,
            newestFirst: isStacktraceNewestFirst(),
        };
        _this.handleChangeNewestFirst = function (_a) {
            var newestFirst = _a.newestFirst;
            _this.setState(function (prevState) { return (__assign(__assign({}, prevState), { newestFirst: newestFirst })); });
        };
        _this.handleChangeStackView = function (_a) {
            var stackView = _a.stackView;
            if (!stackView) {
                return;
            }
            _this.setState(function (prevState) { return (__assign(__assign({}, prevState), { stackView: stackView })); });
        };
        return _this;
    }
    StacktraceInterface.prototype.render = function () {
        var _a;
        var _b = this.props, projectId = _b.projectId, event = _b.event, data = _b.data, hideGuide = _b.hideGuide, type = _b.type;
        var _c = this.state, stackView = _c.stackView, newestFirst = _c.newestFirst;
        var stackTraceNotFound = !((_a = data.frames) !== null && _a !== void 0 ? _a : []).length;
        return (<EventDataSection type={type} title={<CrashTitle title={t('Stack Trace')} hideGuide={hideGuide} newestFirst={newestFirst} onChange={!stackTraceNotFound ? this.handleChangeNewestFirst : undefined}/>} actions={!stackTraceNotFound && (<CrashActions stackView={stackView} platform={event.platform} stacktrace={data} onChange={this.handleChangeStackView}/>)} wrapTitle={false}>
        {stackTraceNotFound ? (<NoStackTraceMessage />) : (<CrashContent projectId={projectId} event={event} stackView={stackView} newestFirst={newestFirst} stacktrace={data} stackType={STACK_TYPE.ORIGINAL}/>)}
      </EventDataSection>);
    };
    StacktraceInterface.defaultProps = defaultProps;
    return StacktraceInterface;
}(React.Component));
export default StacktraceInterface;
//# sourceMappingURL=stacktrace.jsx.map