import { __assign, __awaiter, __generator, __makeTemplateObject, __read } from "tslib";
import { Fragment, useEffect, useState } from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import Alert from 'app/components/alert';
import AlertLink from 'app/components/alertLink';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import LoadingIndicator from 'app/components/loadingIndicator';
import { appStoreConnectAlertMessage } from 'app/components/projects/appStoreConnectContext/utils';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import StepFifth from './stepFifth';
import StepFour from './stepFour';
import StepOne from './stepOne';
import StepThree from './stepThree';
import StepTwo from './stepTwo';
var steps = [
    t('App Store Connect credentials'),
    t('Choose an application'),
    t('Enter iTunes credentials'),
    t('Enter authentication code'),
    t('Choose an organization'),
];
function AppStoreConnect(_a) {
    var Header = _a.Header, Body = _a.Body, Footer = _a.Footer, api = _a.api, initialData = _a.initialData, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, onSubmit = _a.onSubmit, location = _a.location, appStoreConnectContext = _a.appStoreConnectContext;
    var updateAlertMessage = (appStoreConnectContext !== null && appStoreConnectContext !== void 0 ? appStoreConnectContext : {}).updateAlertMessage;
    var _b = __read(useState(location.query.revalidateItunesSession), 2), revalidateItunesSession = _b[0], setRevalidateItunesSession = _b[1];
    var _c = __read(useState(false), 2), isLoading = _c[0], setIsLoading = _c[1];
    var _d = __read(useState(revalidateItunesSession ? 3 : 0), 2), activeStep = _d[0], setActiveStep = _d[1];
    var _e = __read(useState([]), 2), appStoreApps = _e[0], setAppStoreApps = _e[1];
    var _f = __read(useState([]), 2), appleStoreOrgs = _f[0], setAppleStoreOrgs = _f[1];
    var _g = __read(useState(false), 2), useSms = _g[0], setUseSms = _g[1];
    var _h = __read(useState(undefined), 2), sessionContext = _h[0], setSessionContext = _h[1];
    var _j = __read(useState({
        issuer: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectIssuer,
        keyId: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectKey,
        privateKey: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectPrivateKey,
    }), 2), stepOneData = _j[0], setStepOneData = _j[1];
    var _k = __read(useState({
        app: (initialData === null || initialData === void 0 ? void 0 : initialData.appId) && (initialData === null || initialData === void 0 ? void 0 : initialData.appName)
            ? {
                appId: initialData.appId,
                name: initialData.appName,
                bundleId: initialData.bundleId,
            }
            : undefined,
    }), 2), stepTwoData = _k[0], setStepTwoData = _k[1];
    var _l = __read(useState({
        username: initialData === null || initialData === void 0 ? void 0 : initialData.itunesUser,
        password: initialData === null || initialData === void 0 ? void 0 : initialData.itunesPassword,
    }), 2), stepThreeData = _l[0], setStepThreeData = _l[1];
    var _m = __read(useState({
        authenticationCode: undefined,
    }), 2), stepFourData = _m[0], setStepFourData = _m[1];
    var _o = __read(useState({
        org: (initialData === null || initialData === void 0 ? void 0 : initialData.orgId) && (initialData === null || initialData === void 0 ? void 0 : initialData.name)
            ? { organizationId: initialData.orgId, name: initialData.name }
            : undefined,
    }), 2), stepFifthData = _o[0], setStepFifthData = _o[1];
    useEffect(function () {
        if (location.query.revalidateItunesSession && !revalidateItunesSession) {
            setIsLoading(true);
            setRevalidateItunesSession(location.query.revalidateItunesSession);
        }
    }, [location.query]);
    useEffect(function () {
        if (revalidateItunesSession) {
            handleStartItunesAuthentication(false);
            if (activeStep !== 3) {
                setActiveStep(3);
            }
            setIsLoading(false);
            return;
        }
        setIsLoading(false);
    }, [revalidateItunesSession]);
    function checkAppStoreConnectCredentials() {
        return __awaiter(this, void 0, void 0, function () {
            var response, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setIsLoading(true);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/apps/", {
                                method: 'POST',
                                data: {
                                    appconnectIssuer: stepOneData.issuer,
                                    appconnectKey: stepOneData.keyId,
                                    appconnectPrivateKey: stepOneData.privateKey,
                                },
                            })];
                    case 2:
                        response = _a.sent();
                        setAppStoreApps(response.apps);
                        setStepTwoData({ app: response.apps[0] });
                        setIsLoading(false);
                        goNext();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        setIsLoading(false);
                        addErrorMessage(t('We could not establish a connection with App Store Connect. Please check the entered App Store Connect credentials.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function startTwoFactorAuthentication(shouldJumpNext) {
        if (shouldJumpNext === void 0) { shouldJumpNext = false; }
        return __awaiter(this, void 0, void 0, function () {
            var response, organizations, newSessionContext, error_2;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setIsLoading(true);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/2fa/", {
                                method: 'POST',
                                data: {
                                    code: stepFourData.authenticationCode,
                                    useSms: useSms,
                                    sessionContext: sessionContext,
                                },
                            })];
                    case 2:
                        response = _a.sent();
                        organizations = response.organizations, newSessionContext = response.sessionContext;
                        if (shouldJumpNext) {
                            persistData(newSessionContext);
                            return [2 /*return*/];
                        }
                        setSessionContext(newSessionContext);
                        setAppleStoreOrgs(organizations);
                        setStepFifthData({ org: organizations[0] });
                        setIsLoading(false);
                        goNext();
                        return [3 /*break*/, 4];
                    case 3:
                        error_2 = _a.sent();
                        setIsLoading(false);
                        addErrorMessage(t('The two factor authentication failed. Please check the entered code.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function persistData(newSessionContext) {
        return __awaiter(this, void 0, void 0, function () {
            var endpoint, errorMessage, response, error_3;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!stepTwoData.app || !stepFifthData.org || !stepThreeData.username) {
                            return [2 /*return*/];
                        }
                        setIsLoading(true);
                        endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/";
                        errorMessage = t('An error occured while adding the App Store Connect repository.');
                        if (!!initialData) {
                            endpoint = "" + endpoint + initialData.id + "/";
                            errorMessage = t('An error occured while updating the App Store Connect repository.');
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(endpoint, {
                                method: 'POST',
                                data: {
                                    itunesUser: stepThreeData.username,
                                    itunesPassword: stepThreeData.password,
                                    appconnectIssuer: stepOneData.issuer,
                                    appconnectKey: stepOneData.keyId,
                                    appconnectPrivateKey: stepOneData.privateKey,
                                    appName: stepTwoData.app.name,
                                    appId: stepTwoData.app.appId,
                                    bundleId: stepTwoData.app.bundleId,
                                    orgId: stepFifthData.org.organizationId,
                                    orgName: stepFifthData.org.name,
                                    sessionContext: newSessionContext !== null && newSessionContext !== void 0 ? newSessionContext : sessionContext,
                                },
                            })];
                    case 2:
                        response = _a.sent();
                        onSubmit(response);
                        return [3 /*break*/, 4];
                    case 3:
                        error_3 = _a.sent();
                        setIsLoading(false);
                        addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function isFormInvalid() {
        switch (activeStep) {
            case 0:
                return Object.keys(stepOneData).some(function (key) { return !stepOneData[key]; });
            case 1:
                return Object.keys(stepTwoData).some(function (key) { return !stepTwoData[key]; });
            case 2: {
                return Object.keys(stepThreeData).some(function (key) { return !stepThreeData[key]; });
            }
            case 3: {
                return Object.keys(stepFourData).some(function (key) { return !stepFourData[key]; });
            }
            case 4: {
                return Object.keys(stepFifthData).some(function (key) { return !stepFifthData[key]; });
            }
            default:
                return false;
        }
    }
    function goNext() {
        setActiveStep(activeStep + 1);
    }
    function handleStartItunesAuthentication(shouldGoNext) {
        if (shouldGoNext === void 0) { shouldGoNext = true; }
        return __awaiter(this, void 0, void 0, function () {
            var response, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (shouldGoNext) {
                            setIsLoading(true);
                        }
                        if (useSms) {
                            setUseSms(false);
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/start/", {
                                method: 'POST',
                                data: {
                                    itunesUser: stepThreeData.username,
                                    itunesPassword: stepThreeData.password,
                                },
                            })];
                    case 2:
                        response = _b.sent();
                        setSessionContext(response.sessionContext);
                        if (shouldGoNext) {
                            setIsLoading(false);
                            goNext();
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        if (shouldGoNext) {
                            setIsLoading(false);
                        }
                        addErrorMessage(t('The iTunes authentication failed. Please check the entered credentials.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function handleStartSmsAuthentication() {
        return __awaiter(this, void 0, void 0, function () {
            var response, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!useSms) {
                            setUseSms(true);
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/requestSms/", {
                                method: 'POST',
                                data: { sessionContext: sessionContext },
                            })];
                    case 2:
                        response = _b.sent();
                        setSessionContext(response.sessionContext);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage(t('An error occured while sending the SMS. Please try again'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function handleGoBack() {
        var newActiveStep = activeStep - 1;
        switch (newActiveStep) {
            case 3:
                handleStartItunesAuthentication(false);
                setStepFourData({ authenticationCode: undefined });
                break;
            default:
                break;
        }
        setActiveStep(newActiveStep);
    }
    function handleGoNext() {
        switch (activeStep) {
            case 0:
                checkAppStoreConnectCredentials();
                break;
            case 1:
                goNext();
                break;
            case 2:
                handleStartItunesAuthentication();
                break;
            case 3:
                startTwoFactorAuthentication();
                break;
            case 4:
                persistData();
                break;
            default:
                break;
        }
    }
    function renderCurrentStep() {
        switch (activeStep) {
            case 0:
                return <StepOne stepOneData={stepOneData} onSetStepOneData={setStepOneData}/>;
            case 1:
                return (<StepTwo appStoreApps={appStoreApps} stepTwoData={stepTwoData} onSetStepTwoData={setStepTwoData}/>);
            case 2:
                return (<StepThree stepThreeData={stepThreeData} onSetStepOneData={setStepThreeData}/>);
            case 3:
                return (<StepFour stepFourData={stepFourData} onSetStepFourData={setStepFourData} onStartItunesAuthentication={handleStartItunesAuthentication} onStartSmsAuthentication={handleStartSmsAuthentication}/>);
            case 4:
                return (<StepFifth appleStoreOrgs={appleStoreOrgs} stepFifthData={stepFifthData} onSetStepFifthData={setStepFifthData}/>);
            default:
                return (<Alert type="error" icon={<IconWarning />}>
            {t('This step could not be found.')}
          </Alert>);
        }
    }
    function getAlerts() {
        var alerts = [];
        if (revalidateItunesSession) {
            if (!updateAlertMessage && revalidateItunesSession) {
                alerts.push(<StyledAlert type="warning" icon={<IconWarning />}>
            {t('Your iTunes session has already been re-validated.')}
          </StyledAlert>);
            }
            return alerts;
        }
        if (activeStep !== 0) {
            return alerts;
        }
        if (updateAlertMessage === appStoreConnectAlertMessage.appStoreCredentialsInvalid) {
            alerts.push(<StyledAlert type="warning" icon={<IconWarning />}>
          {t('Your App Store Connect credentials are invalid. To reconnect, update your credentials.')}
        </StyledAlert>);
        }
        if (updateAlertMessage === appStoreConnectAlertMessage.iTunesSessionInvalid) {
            alerts.push(<AlertLink withoutMarginBottom icon={<IconWarning />} to={{
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { revalidateItunesSession: true }),
                }}>
          {t('Your iTunes session has expired. To reconnect, revalidate the session.')}
        </AlertLink>);
        }
        if (updateAlertMessage ===
            appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt) {
            alerts.push(<AlertLink withoutMarginBottom icon={<IconWarning />} to={{
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { revalidateItunesSession: true }),
                }}>
          {t('Your iTunes session will likely expire soon. We recommend that you revalidate the session.')}
        </AlertLink>);
        }
        return alerts;
    }
    function renderBodyContent() {
        var alerts = getAlerts();
        return (<Fragment>
        {!!alerts.length && (<Alerts marginBottom={activeStep === 3 ? 1.5 : 3}>
            {alerts.map(function (alert, index) { return (<Fragment key={index}>{alert}</Fragment>); })}
          </Alerts>)}
        {renderCurrentStep()}
      </Fragment>);
    }
    if (initialData && !appStoreConnectContext) {
        return <LoadingIndicator />;
    }
    if (revalidateItunesSession) {
        return (<Fragment>
        <Header closeButton>
          <HeaderContentTitle>{t('Revalidate iTunes session')}</HeaderContentTitle>
        </Header>
        <Body>{renderBodyContent()}</Body>
        <Footer>
          <StyledButton priority="primary" onClick={function () { return startTwoFactorAuthentication(true); }} disabled={isLoading || isFormInvalid()}>
            {t('Revalidate')}
          </StyledButton>
        </Footer>
      </Fragment>);
    }
    return (<Fragment>
      <Header closeButton>
        <HeaderContent>
          <NumericSymbol>{activeStep + 1}</NumericSymbol>
          <HeaderContentTitle>{steps[activeStep]}</HeaderContentTitle>
          <StepsOverview>
            {tct('[currentStep] of [totalSteps]', {
            currentStep: activeStep + 1,
            totalSteps: steps.length,
        })}
          </StepsOverview>
        </HeaderContent>
      </Header>
      <Body>{renderBodyContent()}</Body>
      <Footer>
        <ButtonBar gap={1}>
          {activeStep !== 0 && <Button onClick={handleGoBack}>{t('Back')}</Button>}
          <StyledButton priority="primary" onClick={handleGoNext} disabled={isLoading || isFormInvalid()}>
            {isLoading && (<LoadingIndicatorWrapper>
                <LoadingIndicator mini/>
              </LoadingIndicatorWrapper>)}
            {activeStep + 1 === steps.length
            ? initialData
                ? t('Update')
                : t('Save')
            : steps[activeStep + 1]}
          </StyledButton>
        </ButtonBar>
      </Footer>
    </Fragment>);
}
export default withApi(AppStoreConnect);
var HeaderContent = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(1));
var NumericSymbol = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-radius: 50%;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  font-weight: 700;\n  font-size: ", ";\n  background-color: ", ";\n"], ["\n  border-radius: 50%;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  font-weight: 700;\n  font-size: ", ";\n  background-color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.yellow300; });
var HeaderContentTitle = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: 700;\n  font-size: ", ";\n"], ["\n  font-weight: 700;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var StepsOverview = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  color: ", ";\n  display: flex;\n  justify-content: flex-end;\n"])), function (p) { return p.theme.gray300; });
var LoadingIndicatorWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  height: 100%;\n  position: absolute;\n  width: 100%;\n  top: 0;\n  left: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  height: 100%;\n  position: absolute;\n  width: 100%;\n  top: 0;\n  left: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var StyledButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var Alerts = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"])), space(1.5), function (p) { return space(p.marginBottom); });
var StyledAlert = styled(Alert)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=index.jsx.map