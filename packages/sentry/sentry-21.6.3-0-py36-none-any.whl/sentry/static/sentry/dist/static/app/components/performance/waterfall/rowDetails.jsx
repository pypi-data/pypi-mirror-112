import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
export var ErrorMessageTitle = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
export var ErrorMessageContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: 16px 72px auto;\n  grid-gap: ", ";\n  margin-top: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: 16px 72px auto;\n  grid-gap: ", ";\n  margin-top: ", ";\n"])), space(0.75), space(0.75));
export var ErrorDot = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background-color: ", ";\n  content: '';\n  width: ", ";\n  min-width: ", ";\n  height: ", ";\n  margin-right: ", ";\n  border-radius: 100%;\n  flex: 1;\n"], ["\n  background-color: ", ";\n  content: '';\n  width: ", ";\n  min-width: ", ";\n  height: ", ";\n  margin-right: ", ";\n  border-radius: 100%;\n  flex: 1;\n"])), function (p) { return p.theme.level[p.level]; }, space(1), space(1), space(1), space(1));
export var ErrorLevel = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 80px;\n"], ["\n  width: 80px;\n"])));
export var ErrorTitle = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=rowDetails.jsx.map