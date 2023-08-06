import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { t } from 'app/locale';
import SelectField from 'app/views/settings/components/forms/selectField';
function StepFifth(_a) {
    var _b, _c;
    var appleStoreOrgs = _a.appleStoreOrgs, stepFifthData = _a.stepFifthData, onSetStepFifthData = _a.onSetStepFifthData;
    return (<StyledSelectField name="organization" label={t('iTunes Organization')} choices={appleStoreOrgs.map(function (appleStoreOrg) { return [
            appleStoreOrg.organizationId,
            appleStoreOrg.name,
        ]; })} placeholder={t('Select organization')} onChange={function (organizationId) {
            var selectedAppleStoreOrg = appleStoreOrgs.find(function (appleStoreOrg) { return appleStoreOrg.organizationId === organizationId; });
            onSetStepFifthData({ org: selectedAppleStoreOrg });
        }} value={(_c = (_b = stepFifthData.org) === null || _b === void 0 ? void 0 : _b.organizationId) !== null && _c !== void 0 ? _c : ''} inline={false} flexibleControlStateSize stacked required/>);
}
export default StepFifth;
var StyledSelectField = styled(SelectField)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=stepFifth.jsx.map