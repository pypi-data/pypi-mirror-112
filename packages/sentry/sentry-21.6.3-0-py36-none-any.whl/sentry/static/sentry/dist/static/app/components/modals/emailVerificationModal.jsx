import * as React from 'react';
import { withRouter } from 'react-router';
import Link from 'app/components/links/link';
import { t, tct } from 'app/locale';
import withApi from 'app/utils/withApi';
import { EmailAddresses } from 'app/views/settings/account/accountEmails';
import TextBlock from 'app/views/settings/components/text/textBlock';
function EmailVerificationModal(_a) {
    var Header = _a.Header, Body = _a.Body, _b = _a.actionMessage, actionMessage = _b === void 0 ? 'taking this action' : _b;
    return (<React.Fragment>
      <Header closeButton>{t('Action Required')}</Header>
      <Body>
        <TextBlock>
          {tct('Please verify your email before [actionMessage], or [link].', {
            actionMessage: actionMessage,
            link: (<Link to="/settings/account/emails/" data-test-id="email-settings-link">
                {t('go to your email settings')}
              </Link>),
        })}
        </TextBlock>
        <EmailAddresses />
      </Body>
    </React.Fragment>);
}
export default withRouter(withApi(EmailVerificationModal));
export { EmailVerificationModal };
//# sourceMappingURL=emailVerificationModal.jsx.map