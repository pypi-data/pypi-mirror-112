import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { ROW_HEIGHT } from 'app/components/performance/waterfall/constants';
export var RowTitleContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: ", "px;\n  position: absolute;\n  left: 0;\n  top: 0;\n  width: 100%;\n  user-select: none;\n"], ["\n  display: flex;\n  align-items: center;\n  height: ", "px;\n  position: absolute;\n  left: 0;\n  top: 0;\n  width: 100%;\n  user-select: none;\n"])), ROW_HEIGHT);
export var RowTitle = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  height: 100%;\n  font-size: ", ";\n  white-space: nowrap;\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  position: relative;\n  height: 100%;\n  font-size: ", ";\n  white-space: nowrap;\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeSmall; });
export var RowTitleContent = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return (p.errored ? p.theme.error : 'inherit'); });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=rowTitle.jsx.map