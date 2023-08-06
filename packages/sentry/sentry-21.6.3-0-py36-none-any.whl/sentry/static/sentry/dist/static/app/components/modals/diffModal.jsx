import { __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import { css } from '@emotion/react';
import IssueDiff from 'app/components/issueDiff';
var DiffModal = function (_a) {
    var className = _a.className, Body = _a.Body, CloseButton = _a.CloseButton, props = __rest(_a, ["className", "Body", "CloseButton"]);
    return (<Body>
    <CloseButton />
    <IssueDiff className={className} {...props}/>
  </Body>);
};
var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  left: 20px;\n  right: 20px;\n  top: 20px;\n  bottom: 20px;\n  display: flex;\n  padding: 0;\n  width: auto;\n\n  [role='document'] {\n    overflow: scroll;\n    height: 100%;\n    display: flex;\n    flex: 1;\n  }\n\n  section {\n    display: flex;\n    width: 100%;\n  }\n"], ["\n  position: absolute;\n  left: 20px;\n  right: 20px;\n  top: 20px;\n  bottom: 20px;\n  display: flex;\n  padding: 0;\n  width: auto;\n\n  [role='document'] {\n    overflow: scroll;\n    height: 100%;\n    display: flex;\n    flex: 1;\n  }\n\n  section {\n    display: flex;\n    width: 100%;\n  }\n"])));
export { modalCss };
export default DiffModal;
var templateObject_1;
//# sourceMappingURL=diffModal.jsx.map