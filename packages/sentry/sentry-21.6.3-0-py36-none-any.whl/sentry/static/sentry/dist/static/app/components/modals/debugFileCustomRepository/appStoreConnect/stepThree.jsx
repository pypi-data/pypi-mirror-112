import { __assign } from "tslib";
import { Fragment } from 'react';
import { t } from 'app/locale';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
function StepThree(_a) {
    var stepThreeData = _a.stepThreeData, onSetStepOneData = _a.onSetStepOneData;
    return (<Fragment>
      <Field label={t('Username')} inline={false} flexibleControlStateSize stacked required>
        <Input type="text" name="username" placeholder={t('Username')} onChange={function (e) { return onSetStepOneData(__assign(__assign({}, stepThreeData), { username: e.target.value })); }}/>
      </Field>
      <Field label={t('Password')} inline={false} flexibleControlStateSize stacked required>
        <Input type="password" name="password" placeholder={t('Password')} onChange={function (e) { return onSetStepOneData(__assign(__assign({}, stepThreeData), { password: e.target.value })); }}/>
      </Field>
    </Fragment>);
}
export default StepThree;
//# sourceMappingURL=stepThree.jsx.map