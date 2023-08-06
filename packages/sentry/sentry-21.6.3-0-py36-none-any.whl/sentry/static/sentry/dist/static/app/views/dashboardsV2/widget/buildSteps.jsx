import { __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import List from 'app/components/list';
import space from 'app/styles/space';
function BuildSteps(_a) {
    var children = _a.children;
    return <StyledList symbol="colored-numeric">{children}</StyledList>;
}
export default BuildSteps;
var StyledList = styled(List)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  max-width: 100%;\n\n  @media (min-width: ", ") {\n    max-width: 50%;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  max-width: 100%;\n\n  @media (min-width: ", ") {\n    max-width: 50%;\n  }\n"])), space(4), function (p) { return p.theme.breakpoints[4]; });
var templateObject_1;
//# sourceMappingURL=buildSteps.jsx.map