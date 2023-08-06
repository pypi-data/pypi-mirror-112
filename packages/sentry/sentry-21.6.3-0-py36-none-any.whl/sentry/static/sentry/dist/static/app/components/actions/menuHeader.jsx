import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import MenuItem from 'app/components/menuItem';
import space from 'app/styles/space';
var MenuHeader = styled(MenuItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-transform: uppercase;\n  font-weight: 600;\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n"], ["\n  text-transform: uppercase;\n  font-weight: 600;\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.innerBorder; }, space(1));
MenuHeader.defaultProps = {
    header: true,
};
export default MenuHeader;
var templateObject_1;
//# sourceMappingURL=menuHeader.jsx.map