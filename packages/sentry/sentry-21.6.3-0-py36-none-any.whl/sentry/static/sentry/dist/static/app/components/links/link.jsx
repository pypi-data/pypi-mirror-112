import { __extends, __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import { Link as RouterLink, withRouter } from 'react-router';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
/**
 * A context-aware version of Link (from react-router) that falls
 * back to <a> if there is no router present
 */
var Link = /** @class */ (function (_super) {
    __extends(Link, _super);
    function Link() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Link.prototype.componentDidMount = function () {
        var isRouterPresent = this.props.location;
        if (!isRouterPresent) {
            Sentry.captureException(new Error('The link component was rendered without being wrapped by a <Router />'));
        }
    };
    Link.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, to = _a.to, ref = _a.ref, location = _a.location, props = __rest(_a, ["disabled", "to", "ref", "location"]);
        if (!disabled && location) {
            return <RouterLink to={to} ref={ref} {...props}/>;
        }
        if (typeof to === 'string') {
            return <Anchor href={to} ref={ref} disabled={disabled} {...props}/>;
        }
        return <Anchor href="" ref={ref} {...props} disabled/>;
    };
    return Link;
}(React.Component));
export default withRouter(Link);
var Anchor = styled('a', {
    shouldForwardProp: function (prop) {
        return typeof prop === 'string' && isPropValid(prop) && prop !== 'disabled';
    },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) {
    return p.disabled &&
        "\n  color:" + p.theme.disabled + ";\n  pointer-events: none;\n  :hover {\n    color: " + p.theme.disabled + ";\n  }\n  ";
});
var templateObject_1;
//# sourceMappingURL=link.jsx.map