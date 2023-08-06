import { __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import ActionLink from 'app/components/actions/actionLink';
import MenuItem from 'app/components/menuItem';
import overflowEllipsis from 'app/styles/overflowEllipsis';
function MenuItemActionLink(_a) {
    var className = _a.className, props = __rest(_a, ["className"]);
    return (<MenuItem noAnchor withBorder disabled={props.disabled} className={className}>
      <InnerActionLink {...props}/>
    </MenuItem>);
}
var InnerActionLink = styled(ActionLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  ", "\n  &:hover {\n    color: ", ";\n  }\n\n  .dropdown-menu > li > &,\n  .dropdown-menu > span > li > & {\n    &.disabled:hover {\n      background: ", ";\n      color: #7a8188;\n    }\n  }\n"], ["\n  color: ", ";\n  ", "\n  &:hover {\n    color: ", ";\n  }\n\n  .dropdown-menu > li > &,\n  .dropdown-menu > span > li > & {\n    &.disabled:hover {\n      background: ", ";\n      color: #7a8188;\n    }\n  }\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis, function (p) { return p.theme.textColor; }, function (p) { return p.theme.white; });
export default MenuItemActionLink;
var templateObject_1;
//# sourceMappingURL=menuItemActionLink.jsx.map