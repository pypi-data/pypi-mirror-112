import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/react';
import space from 'app/styles/space';
var bulletStyle = function (theme) { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-left: ", ";\n  list-style-type: circle;\n  & > li::marker {\n    color: ", ";\n  }\n"], ["\n  padding-left: ", ";\n  list-style-type: circle;\n  & > li::marker {\n    color: ", ";\n  }\n"])), space(3), theme.subText); };
var numericStyle = function (theme, _a) {
    var _b = _a.isSolid, isSolid = _b === void 0 ? false : _b, _c = _a.initialCounterValue, initialCounterValue = _c === void 0 ? 0 : _c;
    return css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  & > li {\n    padding-left: ", ";\n    :before {\n      border-radius: 50%;\n      position: absolute;\n      counter-increment: numberedList;\n      content: counter(numberedList);\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      text-align: center;\n      left: 0;\n      ", "\n    }\n  }\n  counter-reset: numberedList ", ";\n"], ["\n  & > li {\n    padding-left: ", ";\n    :before {\n      border-radius: 50%;\n      position: absolute;\n      counter-increment: numberedList;\n      content: counter(numberedList);\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      text-align: center;\n      left: 0;\n      ", "\n    }\n  }\n  counter-reset: numberedList ", ";\n"])), space(4), isSolid
        ? css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n            width: 24px;\n            height: 24px;\n            font-weight: 500;\n            font-size: ", ";\n            background-color: ", ";\n          "], ["\n            width: 24px;\n            height: 24px;\n            font-weight: 500;\n            font-size: ", ";\n            background-color: ", ";\n          "])), theme.fontSizeSmall, theme.yellow300) : css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n            top: 3px;\n            width: 18px;\n            height: 18px;\n            font-weight: 600;\n            font-size: 10px;\n            border: 1px solid ", ";\n          "], ["\n            top: 3px;\n            width: 18px;\n            height: 18px;\n            font-weight: 600;\n            font-size: 10px;\n            border: 1px solid ", ";\n          "])), theme.gray500), initialCounterValue);
};
export var listSymbol = {
    numeric: 'numeric',
    'colored-numeric': 'colored-numeric',
    bullet: 'bullet',
};
export function getListSymbolStyle(theme, symbol, initialCounterValue) {
    switch (symbol) {
        case 'numeric':
            return numericStyle(theme, { initialCounterValue: initialCounterValue });
        case 'colored-numeric':
            return numericStyle(theme, { isSolid: true, initialCounterValue: initialCounterValue });
        default:
            return bulletStyle(theme);
    }
}
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=utils.jsx.map