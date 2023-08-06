import { __assign, __extends } from "tslib";
import { cloneElement, Component, isValidElement } from 'react';
import withProject from 'app/utils/withProject';
/**
 * Simple Component that takes project from context and passes it as props to children
 *
 * Don't do anything additional (e.g. loader) because not all children require project
 *
 * This is made because some components (e.g. ProjectPluginDetail) takes project as prop
 */
var SettingsProjectProvider = /** @class */ (function (_super) {
    __extends(SettingsProjectProvider, _super);
    function SettingsProjectProvider() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsProjectProvider.prototype.render = function () {
        var _a = this.props, children = _a.children, project = _a.project;
        if (isValidElement(children)) {
            return cloneElement(children, __assign(__assign(__assign({}, this.props), children.props), { project: project }));
        }
        return null;
    };
    return SettingsProjectProvider;
}(Component));
export default withProject(SettingsProjectProvider);
//# sourceMappingURL=settingsProjectProvider.jsx.map