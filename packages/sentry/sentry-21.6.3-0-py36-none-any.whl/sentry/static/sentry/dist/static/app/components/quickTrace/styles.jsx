import { __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import MenuHeader from 'app/components/actions/menuHeader';
import ExternalLink from 'app/components/links/externalLink';
import MenuItem from 'app/components/menuItem';
import Tag, { Background } from 'app/components/tag';
import Truncate from 'app/components/truncate';
import space from 'app/styles/space';
import { getDuration } from 'app/utils/formatters';
export var SectionSubtext = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
export var QuickTraceContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 24px;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 24px;\n"])));
var nodeColors = function (theme) { return ({
    error: {
        color: theme.white,
        background: theme.red300,
        border: theme.red300,
    },
    warning: {
        color: theme.red300,
        background: theme.background,
        border: theme.red300,
    },
    white: {
        color: theme.textColor,
        background: theme.background,
        border: theme.textColor,
    },
    black: {
        color: theme.background,
        background: theme.textColor,
        border: theme.textColor,
    },
}); };
export var EventNode = styled(Tag)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  span {\n    display: flex;\n    color: ", ";\n  }\n  & ", " {\n    background-color: ", ";\n    border: 1px solid ", ";\n  }\n"], ["\n  span {\n    display: flex;\n    color: ", ";\n  }\n  & " /* sc-selector */, " {\n    background-color: ", ";\n    border: 1px solid ", ";\n  }\n"])), function (p) { return nodeColors(p.theme)[p.type || 'white'].color; }, /* sc-selector */ Background, function (p) { return nodeColors(p.theme)[p.type || 'white'].background; }, function (p) { return nodeColors(p.theme)[p.type || 'white'].border; });
export var TraceConnector = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  width: ", ";\n  border-top: 1px solid ", ";\n"])), space(1), function (p) { return p.theme.textColor; });
/**
 * The DropdownLink component is styled directly with less and the way the
 * elements are laid out within means we can't apply any styles directly
 * using emotion. Instead, we wrap it all inside a span and indirectly
 * style it here.
 */
export var DropdownContainer = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  .dropdown-menu {\n    padding: 0;\n  }\n"], ["\n  .dropdown-menu {\n    padding: 0;\n  }\n"])));
export var DropdownMenuHeader = styled(MenuHeader)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  background: ", ";\n  ", ";\n  padding: ", " ", ";\n"], ["\n  background: ", ";\n  ", ";\n  padding: ", " ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.first && 'border-radius: 2px'; }, space(1), space(1.5));
var StyledMenuItem = styled(MenuItem)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  width: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  width: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return (p.width === 'large' ? '350px' : '200px'); }, function (p) { return p.theme.innerBorder; });
var MenuItemContent = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  width: 100%;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  width: 100%;\n"])));
export function DropdownItem(_a) {
    var children = _a.children, onSelect = _a.onSelect, allowDefaultEvent = _a.allowDefaultEvent, to = _a.to, _b = _a.width, width = _b === void 0 ? 'large' : _b;
    return (<StyledMenuItem to={to} onSelect={onSelect} width={width} allowDefaultEvent={allowDefaultEvent}>
      <MenuItemContent>{children}</MenuItemContent>
    </StyledMenuItem>);
}
export var DropdownItemSubContainer = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n\n  > a {\n    padding-left: 0 !important;\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n\n  > a {\n    padding-left: 0 !important;\n  }\n"])));
export var StyledTruncate = styled(Truncate)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  padding-left: ", ";\n  white-space: nowrap;\n"], ["\n  padding-left: ", ";\n  white-space: nowrap;\n"])), space(1));
export var ErrorNodeContent = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, auto);\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, auto);\n  grid-gap: ", ";\n  align-items: center;\n"])), space(0.25));
export var ExternalDropdownLink = styled(ExternalLink)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: inherit !important;\n  padding: 0 !important;\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  display: inherit !important;\n  padding: 0 !important;\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
export function SingleEventHoverText(_a) {
    var event = _a.event;
    return (<div>
      <Truncate value={event.transaction} maxLength={30} leftTrim trimRegex={/\.|\//g} expandable={false}/>
      <div>
        {getDuration(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)}
      </div>
    </div>);
}
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=styles.jsx.map