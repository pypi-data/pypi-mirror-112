import { __extends } from "tslib";
import * as React from 'react';
import GlobalSelectionStore from 'app/stores/globalSelectionStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Higher order component that uses GlobalSelectionStore and provides the
 * active project
 */
function withGlobalSelection(WrappedComponent) {
    var WithGlobalSelection = /** @class */ (function (_super) {
        __extends(WithGlobalSelection, _super);
        function WithGlobalSelection() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = GlobalSelectionStore.get();
            _this.unsubscribe = GlobalSelectionStore.listen(function (selection) {
                if (_this.state !== selection) {
                    _this.setState(selection);
                }
            }, undefined);
            return _this;
        }
        WithGlobalSelection.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithGlobalSelection.prototype.render = function () {
            var _a = this.state, isReady = _a.isReady, selection = _a.selection;
            return (<WrappedComponent selection={selection} isGlobalSelectionReady={isReady} {...this.props}/>);
        };
        WithGlobalSelection.displayName = "withGlobalSelection(" + getDisplayName(WrappedComponent) + ")";
        return WithGlobalSelection;
    }(React.Component));
    return WithGlobalSelection;
}
export default withGlobalSelection;
//# sourceMappingURL=withGlobalSelection.jsx.map