import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import { IconInfo } from 'app/icons';
import { tct } from 'app/locale';
var FeedbackAlert = function () { return (<StyledAlert type="info" icon={<IconInfo />}>
    {tct('Got feedback? Email [email:ecosystem-feedback@sentry.io].', {
        email: <a href="mailto:ecosystem-feedback@sentry.io"/>,
    })}
  </StyledAlert>); };
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 20px 0px;\n"], ["\n  margin: 20px 0px;\n"])));
export default FeedbackAlert;
var templateObject_1;
//# sourceMappingURL=feedbackAlert.jsx.map