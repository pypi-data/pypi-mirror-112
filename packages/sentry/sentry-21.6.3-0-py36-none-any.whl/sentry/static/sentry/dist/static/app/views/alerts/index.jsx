import { __extends } from "tslib";
import { cloneElement, Component, Fragment, isValidElement } from 'react';
import Feature from 'app/components/acl/feature';
import withOrganization from 'app/utils/withOrganization';
var AlertsContainer = /** @class */ (function (_super) {
    __extends(AlertsContainer, _super);
    function AlertsContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertsContainer.prototype.render = function () {
        var _a = this.props, children = _a.children, organization = _a.organization;
        return (<Feature organization={organization} features={['incidents']}>
        {function (_a) {
                var hasMetricAlerts = _a.hasFeature;
                return (<Fragment>
            {children && isValidElement(children)
                        ? cloneElement(children, {
                            organization: organization,
                            hasMetricAlerts: hasMetricAlerts,
                        })
                        : children}
          </Fragment>);
            }}
      </Feature>);
    };
    return AlertsContainer;
}(Component));
export default withOrganization(AlertsContainer);
//# sourceMappingURL=index.jsx.map