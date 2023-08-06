import { __awaiter, __generator, __makeTemplateObject, __read } from "tslib";
import { Fragment, useContext, useEffect, useState } from 'react';
import styled from '@emotion/styled';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import Link from 'app/components/links/link';
import AppStoreConnectContext from 'app/components/projects/appStoreConnectContext';
import { appStoreConnectAlertMessage } from 'app/components/projects/appStoreConnectContext/utils';
import { IconClose, IconRefresh } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { promptIsDismissed } from 'app/utils/promptIsDismissed';
import withApi from 'app/utils/withApi';
var APP_STORE_CONNECT_UPDATES = 'app_store_connect_updates';
function UpdateAlert(_a) {
    var api = _a.api, Wrapper = _a.Wrapper, isCompact = _a.isCompact, project = _a.project, organization = _a.organization, className = _a.className;
    var appStoreConnectContext = useContext(AppStoreConnectContext);
    var _b = __read(useState(false), 2), isDismissed = _b[0], setIsDismissed = _b[1];
    useEffect(function () {
        checkPrompt();
    }, []);
    function checkPrompt() {
        return __awaiter(this, void 0, void 0, function () {
            var prompt;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!project ||
                            !appStoreConnectContext ||
                            !appStoreConnectContext.updateAlertMessage ||
                            isDismissed) {
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, promptsCheck(api, {
                                organizationId: organization.id,
                                projectId: project.id,
                                feature: APP_STORE_CONNECT_UPDATES,
                            })];
                    case 1:
                        prompt = _a.sent();
                        setIsDismissed(promptIsDismissed(prompt));
                        return [2 /*return*/];
                }
            });
        });
    }
    function handleDismiss() {
        if (!project) {
            return;
        }
        promptsUpdate(api, {
            organizationId: organization.id,
            projectId: project.id,
            feature: APP_STORE_CONNECT_UPDATES,
            status: 'dismissed',
        });
        setIsDismissed(true);
    }
    function renderMessage(appStoreConnectValidationData, projectSettingsLink) {
        if (!appStoreConnectValidationData.updateAlertMessage) {
            return null;
        }
        var updateAlertMessage = appStoreConnectValidationData.updateAlertMessage;
        return (<div>
        {updateAlertMessage}
        {isCompact && (<Fragment>
            &nbsp;
            <Link to={updateAlertMessage ===
                    appStoreConnectAlertMessage.appStoreCredentialsInvalid
                    ? projectSettingsLink
                    : projectSettingsLink + "&revalidateItunesSession=true"}>
              {updateAlertMessage ===
                    appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt
                    ? t('We recommend that you revalidate the session in the project settings')
                    : t('Update it in the project settings to reconnect')}
            </Link>
          </Fragment>)}
      </div>);
    }
    function renderActions(projectSettingsLink) {
        if (isCompact) {
            return (<ButtonClose priority="link" title={t('Dismiss')} label={t('Dismiss')} onClick={handleDismiss} icon={<IconClose />}/>);
        }
        return (<Actions>
        <Button priority="link" onClick={handleDismiss}>
          {t('Dismiss')}
        </Button>
        |
        <Button priority="link" to={projectSettingsLink + "&revalidateItunesSession=true"}>
          {t('Update session')}
        </Button>
      </Actions>);
    }
    if (!project ||
        !appStoreConnectContext ||
        !appStoreConnectContext.updateAlertMessage ||
        isDismissed) {
        return null;
    }
    var projectSettingsLink = "/settings/" + organization.slug + "/projects/" + project.slug + "/debug-symbols/?customRepository=" + appStoreConnectContext.id;
    var notice = (<Alert type="warning" icon={<IconRefresh />} className={className}>
      <Content>
        {renderMessage(appStoreConnectContext, projectSettingsLink)}
        {renderActions(projectSettingsLink)}
      </Content>
    </Alert>);
    return Wrapper ? <Wrapper>{notice}</Wrapper> : notice;
}
export default withApi(UpdateAlert);
var Actions = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ButtonClose = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=updateAlert.jsx.map