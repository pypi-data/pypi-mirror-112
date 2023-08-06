import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { IconCollapse, IconExpand, IconFire } from 'app/icons';
import space from 'app/styles/space';
export var DividerContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  min-width: 1px;\n"], ["\n  position: relative;\n  min-width: 1px;\n"])));
export var DividerLine = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background-color: ", ";\n  position: absolute;\n  height: 100%;\n  width: 1px;\n  transition: background-color 125ms ease-in-out;\n  z-index: ", ";\n\n  /* enhanced hit-box */\n  &:after {\n    content: '';\n    z-index: -1;\n    position: absolute;\n    left: -2px;\n    top: 0;\n    width: 5px;\n    height: 100%;\n  }\n\n  &.hovering {\n    background-color: ", ";\n    width: 3px;\n    transform: translateX(-1px);\n    margin-right: -2px;\n\n    cursor: ew-resize;\n\n    &:after {\n      left: -2px;\n      width: 7px;\n    }\n  }\n"], ["\n  background-color: ", ";\n  position: absolute;\n  height: 100%;\n  width: 1px;\n  transition: background-color 125ms ease-in-out;\n  z-index: ", ";\n\n  /* enhanced hit-box */\n  &:after {\n    content: '';\n    z-index: -1;\n    position: absolute;\n    left: -2px;\n    top: 0;\n    width: 5px;\n    height: 100%;\n  }\n\n  &.hovering {\n    background-color: ", ";\n    width: 3px;\n    transform: translateX(-1px);\n    margin-right: -2px;\n\n    cursor: ew-resize;\n\n    &:after {\n      left: -2px;\n      width: 7px;\n    }\n  }\n"])), function (p) { return (p.showDetail ? p.theme.textColor : p.theme.border); }, function (p) { return p.theme.zIndex.traceView.dividerLine; }, function (p) { return p.theme.textColor; });
export var DividerLineGhostContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  width: 100%;\n  height: 100%;\n"], ["\n  position: absolute;\n  width: 100%;\n  height: 100%;\n"])));
var BadgeBorder = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n  margin: ", ";\n  left: -11px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border: 1px solid ", ";\n  border-radius: 50%;\n  z-index: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  position: absolute;\n  margin: ", ";\n  left: -11px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border: 1px solid ", ";\n  border-radius: 50%;\n  z-index: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), space(0.25), function (p) { return p.theme.background; }, space(3), space(3), function (p) { return p.theme[p.borderColor]; }, function (p) { return p.theme.zIndex.traceView.dividerLine; });
export function ErrorBadge() {
    return (<BadgeBorder borderColor="red300">
      <IconFire color="red300" size="xs"/>
    </BadgeBorder>);
}
export function EmbeddedTransactionBadge(_a) {
    var expanded = _a.expanded, onClick = _a.onClick;
    return (<BadgeBorder borderColor="gray500" onClick={function (event) {
            event.stopPropagation();
            event.preventDefault();
            onClick();
        }}>
      {expanded ? (<IconCollapse color="gray500" size="xs"/>) : (<IconExpand color="gray500" size="xs"/>)}
    </BadgeBorder>);
}
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=rowDivider.jsx.map