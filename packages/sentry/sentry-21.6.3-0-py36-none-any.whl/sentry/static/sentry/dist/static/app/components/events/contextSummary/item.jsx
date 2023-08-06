import { __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import space from 'app/styles/space';
var Item = function (_a) {
    var children = _a.children, icon = _a.icon, className = _a.className;
    return (<Wrapper className={classNames('context-item', className)}>
    {icon}
    {children && <Details>{children}</Details>}
  </Wrapper>);
};
export default Item;
var Details = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  max-width: 100%;\n  min-height: 48px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  max-width: 100%;\n  min-height: 48px;\n"])));
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: 4px 0 4px 40px;\n  display: flex;\n  margin-right: ", ";\n  align-items: center;\n  position: relative;\n  min-width: 0;\n\n  @media (min-width: ", ") {\n    max-width: 25%;\n    border: 0;\n    padding: 0px 0px 0px 42px;\n  }\n"], ["\n  border-top: 1px solid ", ";\n  padding: 4px 0 4px 40px;\n  display: flex;\n  margin-right: ", ";\n  align-items: center;\n  position: relative;\n  min-width: 0;\n\n  @media (min-width: ", ") {\n    max-width: 25%;\n    border: 0;\n    padding: 0px 0px 0px 42px;\n  }\n"])), function (p) { return p.theme.innerBorder; }, space(3), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=item.jsx.map