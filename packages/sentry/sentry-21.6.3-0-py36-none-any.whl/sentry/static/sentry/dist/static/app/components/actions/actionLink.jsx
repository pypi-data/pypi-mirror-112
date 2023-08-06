import { __assign, __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import ActionButton from './button';
import ConfirmableAction from './confirmableAction';
var StyledAction = styled('a')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  ", "\n"])), function (p) { return p.disabled && 'cursor: not-allowed;'; });
var StyledActionButton = styled(ActionButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  ", "\n"])), function (p) { return p.disabled && 'cursor: not-allowed;'; });
export default function ActionLink(_a) {
    var _b;
    var message = _a.message, className = _a.className, title = _a.title, onAction = _a.onAction, type = _a.type, confirmLabel = _a.confirmLabel, disabled = _a.disabled, children = _a.children, shouldConfirm = _a.shouldConfirm, confirmPriority = _a.confirmPriority, props = __rest(_a, ["message", "className", "title", "onAction", "type", "confirmLabel", "disabled", "children", "shouldConfirm", "confirmPriority"]);
    var actionCommonProps = __assign((_b = {}, _b['aria-label'] = title, _b.className = classNames(className, { disabled: disabled }), _b.onClick = disabled ? undefined : onAction, _b.disabled = disabled, _b.children = children, _b), props);
    var action = type === 'button' ? (<StyledActionButton {...actionCommonProps}/>) : (<StyledAction {...actionCommonProps}/>);
    if (shouldConfirm && onAction) {
        return (<ConfirmableAction shouldConfirm={shouldConfirm} priority={confirmPriority} disabled={disabled} message={message} confirmText={confirmLabel} onConfirm={onAction} stopPropagation={disabled}>
        {action}
      </ConfirmableAction>);
    }
    return action;
}
var templateObject_1, templateObject_2;
//# sourceMappingURL=actionLink.jsx.map