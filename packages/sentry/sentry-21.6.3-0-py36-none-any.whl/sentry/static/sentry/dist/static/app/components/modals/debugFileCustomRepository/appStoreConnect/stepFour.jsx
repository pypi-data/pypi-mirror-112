import { __assign, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconInfo, IconMobile, IconRefresh } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
function StepFour(_a) {
    var onStartItunesAuthentication = _a.onStartItunesAuthentication, onStartSmsAuthentication = _a.onStartSmsAuthentication, stepFourData = _a.stepFourData, onSetStepFourData = _a.onSetStepFourData;
    return (<Fragment>
      <StyledAlert type="info" icon={<IconInfo />}>
        <AlertContent>
          {t('Did not get a verification code?')}
          <ButtonBar gap={1}>
            <Button size="small" title={t('Get a new verification code')} onClick={function () { return onStartItunesAuthentication(false); }} icon={<IconRefresh />}>
              {t('Resend code')}
            </Button>
            <Button size="small" title={t('Get a text message with a code')} onClick={function () { return onStartSmsAuthentication(); }} icon={<IconMobile />}>
              {t('Text me')}
            </Button>
          </ButtonBar>
        </AlertContent>
      </StyledAlert>
      <Field label={t('Two Factor authentication code')} inline={false} flexibleControlStateSize stacked required>
        <Input type="text" name="two-factor-authentication-code" placeholder={t('Enter your code')} value={stepFourData.authenticationCode} onChange={function (e) {
            return onSetStepFourData(__assign(__assign({}, stepFourData), { authenticationCode: e.target.value }));
        }}/>
      </Field>
    </Fragment>);
}
export default StepFour;
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  span:nth-child(2) {\n    margin: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  span:nth-child(2) {\n    margin: 0;\n  }\n"])));
var AlertContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=stepFour.jsx.map