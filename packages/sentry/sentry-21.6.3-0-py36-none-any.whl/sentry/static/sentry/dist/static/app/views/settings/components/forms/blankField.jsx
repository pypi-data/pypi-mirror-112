import { __extends } from "tslib";
import * as React from 'react';
import Field from 'app/views/settings/components/forms/field';
/**
 * This class is meant to hook into `fieldFromConfig`. Like the FieldSeparator
 * class, this doesn't have any fields of its own and is just meant to make
 * forms more flexible.
 */
var BlankField = /** @class */ (function (_super) {
    __extends(BlankField, _super);
    function BlankField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    BlankField.prototype.render = function () {
        return <Field {...this.props}/>;
    };
    return BlankField;
}(React.Component));
export default BlankField;
//# sourceMappingURL=blankField.jsx.map