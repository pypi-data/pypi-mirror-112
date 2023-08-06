import { __extends } from "tslib";
import * as React from 'react';
import { ThemeProvider } from '@emotion/react';
import AlertStore from 'app/stores/alertStore';
import { lightTheme } from 'app/utils/theme';
import AlertMessage from './alertMessage';
var SystemAlerts = /** @class */ (function (_super) {
    __extends(SystemAlerts, _super);
    function SystemAlerts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.unlistener = AlertStore.listen(function (alerts) { return _this.setState({ alerts: alerts }); }, undefined);
        return _this;
    }
    SystemAlerts.prototype.getInitialState = function () {
        return {
            alerts: AlertStore.getInitialState(),
        };
    };
    SystemAlerts.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    SystemAlerts.prototype.render = function () {
        var className = this.props.className;
        var alerts = this.state.alerts;
        return (<ThemeProvider theme={lightTheme}>
        <div className={className}>
          {alerts.map(function (alert, index) { return (<AlertMessage alert={alert} key={alert.id + "-" + index} system/>); })}
        </div>
      </ThemeProvider>);
    };
    return SystemAlerts;
}(React.Component));
export default SystemAlerts;
//# sourceMappingURL=systemAlerts.jsx.map