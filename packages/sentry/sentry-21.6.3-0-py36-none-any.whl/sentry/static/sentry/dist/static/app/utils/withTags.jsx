import { __assign, __extends, __rest } from "tslib";
import * as React from 'react';
import TagStore from 'app/stores/tagStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * HOC for getting *only* tags from the TagStore.
 */
function withTags(WrappedComponent) {
    var WithTags = /** @class */ (function (_super) {
        __extends(WithTags, _super);
        function WithTags() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                tags: TagStore.getAllTags(),
            };
            _this.unsubscribe = TagStore.listen(function (tags) { return _this.setState({ tags: tags }); }, undefined);
            return _this;
        }
        WithTags.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithTags.prototype.render = function () {
            var _a = this.props, tags = _a.tags, props = __rest(_a, ["tags"]);
            return <WrappedComponent {...__assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        };
        WithTags.displayName = "withTags(" + getDisplayName(WrappedComponent) + ")";
        return WithTags;
    }(React.Component));
    return WithTags;
}
export default withTags;
//# sourceMappingURL=withTags.jsx.map