import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
function PaginationCaption(_a) {
    var caption = _a.caption;
    return <Wrapper>{caption}</Wrapper>;
}
export default PaginationCaption;
var Wrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(2));
var templateObject_1;
//# sourceMappingURL=paginationCaption.jsx.map