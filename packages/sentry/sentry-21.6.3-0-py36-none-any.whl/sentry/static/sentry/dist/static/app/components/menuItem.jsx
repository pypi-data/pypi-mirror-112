import { __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import Link from 'app/components/links/link';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
var MenuItem = function (_a) {
    var header = _a.header, icon = _a.icon, divider = _a.divider, isActive = _a.isActive, noAnchor = _a.noAnchor, className = _a.className, children = _a.children, props = __rest(_a, ["header", "icon", "divider", "isActive", "noAnchor", "className", "children"]);
    var to = props.to, href = props.href, title = props.title, withBorder = props.withBorder, disabled = props.disabled, onSelect = props.onSelect, eventKey = props.eventKey, allowDefaultEvent = props.allowDefaultEvent, stopPropagation = props.stopPropagation;
    var handleClick = function (e) {
        if (disabled) {
            return;
        }
        if (onSelect) {
            if (allowDefaultEvent !== true) {
                e.preventDefault();
            }
            if (stopPropagation) {
                e.stopPropagation();
            }
            callIfFunction(onSelect, eventKey);
        }
    };
    var renderAnchor = function () {
        var linkProps = {
            onClick: handleClick,
            tabIndex: -1,
            isActive: isActive,
            disabled: disabled,
            withBorder: withBorder,
        };
        if (to) {
            return (<MenuLink to={to} {...linkProps} title={title}>
          {icon && <MenuIcon>{icon}</MenuIcon>}
          {children}
        </MenuLink>);
        }
        if (href) {
            return (<MenuAnchor {...linkProps} href={href}>
          {icon && <MenuIcon>{icon}</MenuIcon>}
          {children}
        </MenuAnchor>);
        }
        return (<MenuTarget role="button" {...linkProps} title={title}>
        {icon && <MenuIcon>{icon}</MenuIcon>}
        {children}
      </MenuTarget>);
    };
    var renderChildren = null;
    if (noAnchor) {
        renderChildren = children;
    }
    else if (header) {
        renderChildren = children;
    }
    else if (!divider) {
        renderChildren = renderAnchor();
    }
    return (<MenuListItem className={className} role="presentation" isActive={isActive} divider={divider} noAnchor={noAnchor} header={header} {...omit(props, ['href', 'title', 'onSelect', 'eventKey', 'to', 'as'])}>
      {renderChildren}
    </MenuListItem>);
};
function getListItemStyles(props) {
    var common = "\n    display: block;\n    padding: " + space(0.5) + " " + space(2) + ";\n    &:focus {\n      outline: none;\n    }\n  ";
    if (props.disabled) {
        return "\n      " + common + "\n      color: " + props.theme.disabled + ";\n      background: transparent;\n      cursor: not-allowed;\n    ";
    }
    if (props.isActive) {
        return "\n      " + common + "\n      color: " + props.theme.white + ";\n      background: " + props.theme.active + ";\n\n      &:hover {\n        color: " + props.theme.black + ";\n      }\n    ";
    }
    return "\n    " + common + "\n\n    &:hover {\n      background: " + props.theme.focus + ";\n    }\n  ";
}
function getChildStyles(props) {
    if (!props.noAnchor) {
        return '';
    }
    return "\n    & a {\n      " + getListItemStyles(props) + "\n    }\n  ";
}
var shouldForwardProp = function (p) {
    return typeof p === 'string' && ['isActive', 'disabled', 'withBorder'].includes(p) === false;
};
var MenuAnchor = styled('a', { shouldForwardProp: shouldForwardProp })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), getListItemStyles);
var MenuListItem = styled('li')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n\n  ", ";\n  ", "\n  ", "\n\n  ", "\n"], ["\n  display: block;\n\n  ", ";\n  ", "\n  ", "\n\n  ", "\n"])), function (p) {
    return p.withBorder &&
        "\n    border-bottom: 1px solid " + p.theme.innerBorder + ";\n\n    &:last-child {\n      border-bottom: none;\n    }\n  ";
}, function (p) {
    return p.divider &&
        "\n    height: 1px;\n    margin: " + space(0.5) + " 0;\n    overflow: hidden;\n    background-color: " + p.theme.innerBorder + ";\n  ";
}, function (p) {
    return p.header &&
        "\n    padding: " + space(0.25) + " " + space(0.5) + ";\n    font-size: " + p.theme.fontSizeSmall + ";\n    line-height: 1.4;\n    color: " + p.theme.gray300 + ";\n  ";
}, getChildStyles);
var MenuTarget = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n  display: flex;\n  align-items: center;\n"], ["\n  ", "\n  display: flex;\n  align-items: center;\n"])), getListItemStyles);
var MenuIcon = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"])), space(1));
var MenuLink = styled(Link, { shouldForwardProp: shouldForwardProp })(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), getListItemStyles);
export default MenuItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=menuItem.jsx.map