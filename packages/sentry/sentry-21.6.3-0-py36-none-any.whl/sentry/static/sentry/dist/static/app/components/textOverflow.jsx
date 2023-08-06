import { __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import overflowEllipsisLeft from 'app/styles/overflowEllipsisLeft';
var TextOverflow = styled(function (_a) {
    var isParagraph = _a.isParagraph, className = _a.className, children = _a.children;
    var Component = isParagraph ? 'p' : 'div';
    return <Component className={className}>{children}</Component>;
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  width: auto;\n  line-height: 1.1;\n"], ["\n  ", ";\n  width: auto;\n  line-height: 1.1;\n"])), function (p) { return (p.ellipsisDirection === 'right' ? overflowEllipsis : overflowEllipsisLeft); });
TextOverflow.defaultProps = {
    ellipsisDirection: 'right',
    isParagraph: false,
};
export default TextOverflow;
var templateObject_1;
//# sourceMappingURL=textOverflow.jsx.map