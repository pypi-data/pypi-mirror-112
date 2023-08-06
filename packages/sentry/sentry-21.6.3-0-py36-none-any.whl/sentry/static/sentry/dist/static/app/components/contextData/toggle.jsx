import { __makeTemplateObject, __read } from "tslib";
import { Children, useState } from 'react';
import styled from '@emotion/styled';
import { IconAdd, IconSubtract } from 'app/icons';
function Toggle(_a) {
    var highUp = _a.highUp, wrapClassName = _a.wrapClassName, children = _a.children;
    var _b = __read(useState(false), 2), isExpanded = _b[0], setIsExpanded = _b[1];
    if (Children.count(children) === 0) {
        return null;
    }
    var wrappedChildren = <span className={wrapClassName}>{children}</span>;
    if (highUp) {
        return wrappedChildren;
    }
    return (<span>
      <IconWrapper isExpanded={isExpanded} onClick={function (evt) {
            setIsExpanded(!isExpanded);
            evt.preventDefault();
        }}>
        {isExpanded ? (<IconSubtract size="9px" color="white"/>) : (<IconAdd size="9px" color="white"/>)}
      </IconWrapper>
      {isExpanded && wrappedChildren}
    </span>);
}
export default Toggle;
var IconWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-radius: 2px;\n  background: ", ";\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n  ", "\n"], ["\n  border-radius: 2px;\n  background: ", ";\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n  ", "\n"])), function (p) { return p.theme.white; }, function (p) {
    return p.isExpanded
        ? "\n          background: " + p.theme.gray300 + ";\n          border: 1px solid " + p.theme.gray300 + ";\n          &:hover {\n            background: " + p.theme.gray400 + ";\n          }\n        "
        : "\n          background: " + p.theme.blue300 + ";\n          border: 1px solid " + p.theme.blue300 + ";\n          &:hover {\n            background: " + p.theme.blue200 + ";\n          }\n        ";
});
var templateObject_1;
//# sourceMappingURL=toggle.jsx.map