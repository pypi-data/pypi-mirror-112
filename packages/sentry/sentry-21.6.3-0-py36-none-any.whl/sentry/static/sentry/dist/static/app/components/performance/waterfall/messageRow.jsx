import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { ROW_HEIGHT } from 'app/components/performance/waterfall/constants';
import { Row } from 'app/components/performance/waterfall/row';
import space from 'app/styles/space';
export var MessageRow = styled(Row)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: block;\n  cursor: auto;\n  line-height: ", "px;\n  padding-left: ", ";\n  padding-right: ", ";\n  color: ", ";\n  background-color: ", ";\n  outline: 1px solid ", ";\n  font-size: ", ";\n\n  z-index: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: block;\n  cursor: auto;\n  line-height: ", "px;\n  padding-left: ", ";\n  padding-right: ", ";\n  color: ", ";\n  background-color: ", ";\n  outline: 1px solid ", ";\n  font-size: ", ";\n\n  z-index: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), ROW_HEIGHT, space(1), space(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.zIndex.traceView.rowInfoMessage; }, space(2));
var templateObject_1;
//# sourceMappingURL=messageRow.jsx.map