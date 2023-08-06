import { __makeTemplateObject, __rest } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconClose } from 'app/icons/iconClose';
import { t } from 'app/locale';
import space from 'app/styles/space';
var ModalHeader = styled('header')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  margin: -", " -", " ", " -", ";\n\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6 {\n    font-size: 20px;\n    font-weight: 600;\n    margin-bottom: 0;\n    line-height: 1.1;\n  }\n"], ["\n  position: relative;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  margin: -", " -", " ", " -", ";\n\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6 {\n    font-size: 20px;\n    font-weight: 600;\n    margin-bottom: 0;\n    line-height: 1.1;\n  }\n"])), function (p) { return p.theme.border; }, space(3), space(4), space(4), space(4), space(3), space(4));
var CloseButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  right: 0;\n  transform: translate(50%, -50%);\n  border-radius: 50%;\n  background: ", ";\n  height: 24px;\n  width: 24px;\n"], ["\n  position: absolute;\n  top: 0;\n  right: 0;\n  transform: translate(50%, -50%);\n  border-radius: 50%;\n  background: ", ";\n  height: 24px;\n  width: 24px;\n"])), function (p) { return p.theme.background; });
CloseButton.defaultProps = {
    label: t('Close Modal'),
    icon: <IconClose size="10px"/>,
    size: 'zero',
};
var ModalBody = styled('section')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 15px;\n\n  p:last-child {\n    margin-bottom: 0;\n  }\n\n  img {\n    max-width: 100%;\n  }\n"], ["\n  font-size: 15px;\n\n  p:last-child {\n    margin-bottom: 0;\n  }\n\n  img {\n    max-width: 100%;\n  }\n"])));
var ModalFooter = styled('footer')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  display: flex;\n  justify-content: flex-end;\n  padding: ", " ", ";\n  margin: ", " -", " -", ";\n"], ["\n  border-top: 1px solid ", ";\n  display: flex;\n  justify-content: flex-end;\n  padding: ", " ", ";\n  margin: ", " -", " -", ";\n"])), function (p) { return p.theme.border; }, space(3), space(4), space(3), space(4), space(4));
/**
 * Creates a ModalHeader that includes props to enable the close button
 */
var makeClosableHeader = function (closeModal) {
    var ClosableHeader = function (_a) {
        var closeButton = _a.closeButton, children = _a.children, props = __rest(_a, ["closeButton", "children"]);
        return (<ModalHeader {...props}>
        {children}
        {closeButton && <CloseButton onClick={closeModal}/>}
      </ModalHeader>);
    };
    ClosableHeader.displayName = 'Header';
    return ClosableHeader;
};
/**
 * Creates a CloseButton component that is connected to the provided closeModal trigger
 */
var makeCloseButton = function (closeModal) {
    return function (props) {
        return <CloseButton {...props} onClick={closeModal}/>;
    };
};
export { makeClosableHeader, makeCloseButton, ModalBody, ModalFooter };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=components.jsx.map