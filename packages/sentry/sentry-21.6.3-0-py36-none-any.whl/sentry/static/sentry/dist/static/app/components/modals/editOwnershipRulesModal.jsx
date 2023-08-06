import { __makeTemplateObject, __rest } from "tslib";
import { Fragment } from 'react';
import { css } from '@emotion/react';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import OwnershipModal from 'app/views/settings/project/projectOwnership/editRulesModal';
var EditOwnershipRulesModal = function (_a) {
    var Body = _a.Body, Header = _a.Header, onSave = _a.onSave, props = __rest(_a, ["Body", "Header", "onSave"]);
    return (<Fragment>
      <Header closeButton>{t('Edit Ownership Rules')}</Header>
      <Body>
        <OwnershipModal {...props} onSave={onSave}/>
      </Body>
    </Fragment>);
};
export var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    width: 80%;\n  }\n  [role='document'] {\n    overflow: initial;\n  }\n"], ["\n  @media (min-width: ", ") {\n    width: 80%;\n  }\n  [role='document'] {\n    overflow: initial;\n  }\n"])), theme.breakpoints[0]);
export default EditOwnershipRulesModal;
var templateObject_1;
//# sourceMappingURL=editOwnershipRulesModal.jsx.map