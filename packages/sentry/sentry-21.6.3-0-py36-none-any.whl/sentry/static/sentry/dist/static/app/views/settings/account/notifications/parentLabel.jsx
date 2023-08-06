import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Avatar from 'app/components/avatar';
import space from 'app/styles/space';
import { getParentKey } from 'app/views/settings/account/notifications/utils';
/** TODO(mgaeta): Infer parentKey from parent. */
var ParentLabel = /** @class */ (function (_super) {
    __extends(ParentLabel, _super);
    function ParentLabel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.render = function () {
            var _a;
            var _b = _this.props, notificationType = _b.notificationType, parent = _b.parent;
            return (<FieldLabel>
        <Avatar {..._a = {},
                _a[getParentKey(notificationType)] = parent,
                _a}/>
        <span>{parent.slug}</span>
      </FieldLabel>);
        };
        return _this;
    }
    return ParentLabel;
}(React.Component));
var FieldLabel = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"], ["\n  display: flex;\n  gap: ", ";\n  line-height: 16px;\n"])), space(0.5));
export default ParentLabel;
var templateObject_1;
//# sourceMappingURL=parentLabel.jsx.map