import { __assign, __extends, __makeTemplateObject } from "tslib";
import 'prism-sentry/index.css';
import * as React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import { analytics } from 'app/utils/analytics';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import FirstEventFooter from './components/firstEventFooter';
import FullIntroduction from './components/fullIntroduction';
var recordAnalyticsDocsClicked = function (_a) {
    var organization = _a.organization, project = _a.project, platform = _a.platform;
    return analytics('onboarding_v2.full_docs_clicked', {
        org_id: organization.id,
        project: project === null || project === void 0 ? void 0 : project.slug,
        platform: platform,
    });
};
var OtherSetup = /** @class */ (function (_super) {
    __extends(OtherSetup, _super);
    function OtherSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFullDocsClick = function () {
            var _a = _this.props, organization = _a.organization, project = _a.project, platform = _a.platform;
            recordAnalyticsDocsClicked({ organization: organization, project: project, platform: platform });
        };
        return _this;
    }
    OtherSetup.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { keyList: null });
    };
    OtherSetup.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [['keyList', "/projects/" + organization.slug + "/" + (project === null || project === void 0 ? void 0 : project.slug) + "/keys/"]];
    };
    OtherSetup.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var keyList = this.state.keyList;
        var currentPlatform = 'other';
        var blurb = (<React.Fragment>
        <p>
          {tct("Prepare the SDK for your language following this [docsLink:guide].", {
                docsLink: <ExternalLink href="https://develop.sentry.dev/sdk/overview/"/>,
            })}
        </p>

        <p>
          {t('Once your SDK is set up, use the following DSN and send your first event!')}
        </p>

        <p>{tct('Here is the DSN: [DSN]', { DSN: <b> {keyList === null || keyList === void 0 ? void 0 : keyList[0].dsn.public}</b> })}</p>
      </React.Fragment>);
        var docs = (<DocsWrapper>
        {blurb}
        {project && (<FirstEventFooter project={project} organization={organization} docsLink="https://develop.sentry.dev/sdk" docsOnClick={this.handleFullDocsClick}/>)}
      </DocsWrapper>);
        var testOnlyAlert = (<Alert type="warning">
        Platform documentation is not rendered in for tests in CI
      </Alert>);
        return (<React.Fragment>
        <FullIntroduction currentPlatform={currentPlatform}/>
        {getDynamicText({
                value: docs,
                fixed: testOnlyAlert,
            })}
      </React.Fragment>);
    };
    return OtherSetup;
}(AsyncComponent));
var DocsWrapper = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
export default withOrganization(withApi(OtherSetup));
var templateObject_1;
//# sourceMappingURL=otherSetup.jsx.map