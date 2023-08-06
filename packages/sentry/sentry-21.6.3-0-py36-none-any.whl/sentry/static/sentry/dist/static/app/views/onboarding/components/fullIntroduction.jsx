import * as React from 'react';
import { motion } from 'framer-motion';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import Button from 'app/components/button';
import platforms from 'app/data/platforms';
import { t, tct } from 'app/locale';
import SetupIntroduction from './setupIntroduction';
export default function FullIntroduction(_a) {
    var _b, _c;
    var currentPlatform = _a.currentPlatform;
    return (<React.Fragment>
      <SetupIntroduction stepHeaderText={t('Prepare the %s SDK', (_c = (_b = platforms.find(function (p) { return p.id === currentPlatform; })) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '')} platform={currentPlatform}/>
      <motion.p variants={{
            initial: { opacity: 0 },
            animate: { opacity: 1 },
            exit: { opacity: 0 },
        }}>
        {tct("Don't have a relationship with your terminal? [link:Invite your team instead].", {
            link: (<Button priority="link" data-test-id="onboarding-getting-started-invite-members" onClick={openInviteMembersModal}/>),
        })}
      </motion.p>
    </React.Fragment>);
}
//# sourceMappingURL=fullIntroduction.jsx.map