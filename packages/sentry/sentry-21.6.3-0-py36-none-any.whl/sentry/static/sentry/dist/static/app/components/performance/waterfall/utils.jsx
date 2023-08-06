import CHART_PALETTE from 'app/constants/chartPalette';
import space from 'app/styles/space';
export var getBackgroundColor = function (_a) {
    var showStriping = _a.showStriping, showDetail = _a.showDetail, theme = _a.theme;
    if (showDetail) {
        return theme.textColor;
    }
    if (showStriping) {
        return theme.backgroundSecondary;
    }
    return theme.background;
};
export function getHatchPattern(_a, primary, alternate) {
    var spanBarHatch = _a.spanBarHatch;
    if (spanBarHatch === true) {
        return "\n      background-image: linear-gradient(135deg,\n        " + alternate + ",\n        " + alternate + " 2.5px,\n        " + primary + " 2.5px,\n        " + primary + " 5px,\n        " + alternate + " 6px,\n        " + alternate + " 8px,\n        " + primary + " 8px,\n        " + primary + " 11px,\n        " + alternate + " 11px,\n        " + alternate + " 14px,\n        " + primary + " 14px,\n        " + primary + " 16.5px,\n        " + alternate + " 16.5px,\n        " + alternate + " 19px,\n        " + primary + " 20px\n      );\n      background-size: 16px 16px;\n    ";
    }
    return null;
}
export var getDurationPillAlignment = function (_a) {
    var durationDisplay = _a.durationDisplay, theme = _a.theme, spanBarHatch = _a.spanBarHatch;
    switch (durationDisplay) {
        case 'left':
            return "right: calc(100% + " + space(0.5) + ");";
        case 'right':
            return "left: calc(100% + " + space(0.75) + ");";
        default:
            return "\n        right: " + space(0.75) + ";\n        color: " + (spanBarHatch === true ? theme.gray300 : theme.white) + ";\n      ";
    }
};
export var getToggleTheme = function (_a) {
    var theme = _a.theme, isExpanded = _a.isExpanded, disabled = _a.disabled, errored = _a.errored;
    var buttonTheme = isExpanded ? theme.button.default : theme.button.primary;
    var errorTheme = theme.button.danger;
    var background = errored
        ? isExpanded
            ? buttonTheme.background
            : errorTheme.background
        : buttonTheme.background;
    var border = errored ? errorTheme.background : buttonTheme.border;
    var color = errored
        ? isExpanded
            ? errorTheme.background
            : buttonTheme.color
        : buttonTheme.color;
    if (disabled) {
        return "\n    background: " + background + ";\n    border: 1px solid " + border + ";\n    color: " + color + ";\n    cursor: default;\n  ";
    }
    return "\n    background: " + background + ";\n    border: 1px solid " + border + ";\n    color: " + color + ";\n  ";
};
export var getDurationDisplay = function (_a) {
    var width = _a.width, left = _a.left;
    var spaceNeeded = 0.3;
    if (left === undefined || width === undefined) {
        return 'inset';
    }
    if (left + width < 1 - spaceNeeded) {
        return 'right';
    }
    if (left > spaceNeeded) {
        return 'left';
    }
    return 'inset';
};
export var getHumanDuration = function (duration) {
    // note: duration is assumed to be in seconds
    var durationMS = duration * 1000;
    return durationMS.toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }) + "ms";
};
export var toPercent = function (value) { return (value * 100).toFixed(3) + "%"; };
// get position of element relative to top/left of document
var getOffsetOfElement = function (element) {
    // left and top are relative to viewport
    var _a = element.getBoundingClientRect(), left = _a.left, top = _a.top;
    // get values that the document is currently scrolled by
    var scrollLeft = window.pageXOffset;
    var scrollTop = window.pageYOffset;
    return { x: left + scrollLeft, y: top + scrollTop };
};
export var rectOfContent = function (element) {
    var _a = getOffsetOfElement(element), x = _a.x, y = _a.y;
    // offsets for the border and any scrollbars (clientLeft and clientTop),
    // and if the element was scrolled (scrollLeft and scrollTop)
    //
    // NOTE: clientLeft and clientTop does not account for any margins nor padding
    var contentOffsetLeft = element.clientLeft - element.scrollLeft;
    var contentOffsetTop = element.clientTop - element.scrollTop;
    return {
        x: x + contentOffsetLeft,
        y: y + contentOffsetTop,
        width: element.scrollWidth,
        height: element.scrollHeight,
    };
};
export var clamp = function (value, min, max) {
    if (value < min) {
        return min;
    }
    if (value > max) {
        return max;
    }
    return value;
};
var getLetterIndex = function (letter) {
    var index = 'abcdefghijklmnopqrstuvwxyz'.indexOf(letter) || 0;
    return index === -1 ? 0 : index;
};
var colorsAsArray = Object.keys(CHART_PALETTE).map(function (key) { return CHART_PALETTE[17][key]; });
export var barColors = {
    default: CHART_PALETTE[17][4],
    transaction: CHART_PALETTE[17][8],
    http: CHART_PALETTE[17][10],
    db: CHART_PALETTE[17][17],
};
export var pickBarColour = function (input) {
    // We pick the color for span bars using the first three letters of the op name.
    // That way colors stay consistent between transactions.
    if (!input || input.length < 3) {
        return CHART_PALETTE[17][4];
    }
    if (barColors[input]) {
        return barColors[input];
    }
    var letterIndex1 = getLetterIndex(input.slice(0, 1));
    var letterIndex2 = getLetterIndex(input.slice(1, 2));
    var letterIndex3 = getLetterIndex(input.slice(2, 3));
    var letterIndex4 = getLetterIndex(input.slice(3, 4));
    return colorsAsArray[(letterIndex1 + letterIndex2 + letterIndex3 + letterIndex4) % colorsAsArray.length];
};
//# sourceMappingURL=utils.jsx.map