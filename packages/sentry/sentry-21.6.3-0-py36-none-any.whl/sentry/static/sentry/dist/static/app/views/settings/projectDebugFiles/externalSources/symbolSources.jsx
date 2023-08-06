import { __assign, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import React, { Fragment, useContext, useEffect } from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openDebugFileSourceModal } from 'app/actionCreators/modal';
import ProjectActions from 'app/actions/projectActions';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Alert from 'app/components/alert';
import Link from 'app/components/links/link';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import AppStoreConnectContext from 'app/components/projects/appStoreConnectContext';
import { appStoreConnectAlertMessage } from 'app/components/projects/appStoreConnectContext/utils';
import TextOverflow from 'app/components/textOverflow';
import { DEBUG_SOURCE_TYPES } from 'app/data/debugFileSources';
import { IconRefresh, IconWarning } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import Field from 'app/views/settings/components/forms/field';
import RichListField from 'app/views/settings/components/forms/richListField';
import TextBlock from 'app/views/settings/components/text/textBlock';
import { expandKeys } from './utils';
var dropDownItems = [
    {
        value: 's3',
        label: t(DEBUG_SOURCE_TYPES.s3),
        searchKey: t('aws amazon s3 bucket'),
    },
    {
        value: 'gcs',
        label: t(DEBUG_SOURCE_TYPES.gcs),
        searchKey: t('gcs google cloud storage bucket'),
    },
    {
        value: 'http',
        label: t(DEBUG_SOURCE_TYPES.http),
        searchKey: t('http symbol server ssqp symstore symsrv'),
    },
];
function SymbolSources(_a) {
    var _b;
    var api = _a.api, organization = _a.organization, symbolSources = _a.symbolSources, projectSlug = _a.projectSlug, router = _a.router, location = _a.location;
    var appStoreConnectContext = useContext(AppStoreConnectContext);
    useEffect(function () {
        openDebugFileSourceDialog();
    }, [location.query, appStoreConnectContext]);
    var hasAppConnectStoreFeatureFlag = !!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('app-store-connect'));
    if (hasAppConnectStoreFeatureFlag &&
        !appStoreConnectContext &&
        !dropDownItems.find(function (dropDownItem) { return dropDownItem.value === 'appStoreConnect'; })) {
        dropDownItems.push({
            value: 'appStoreConnect',
            label: t(DEBUG_SOURCE_TYPES.appStoreConnect),
            searchKey: t('apple store connect itunes ios'),
        });
    }
    function getRichListFieldValue() {
        if (!hasAppConnectStoreFeatureFlag ||
            !appStoreConnectContext ||
            !appStoreConnectContext.updateAlertMessage) {
            return { value: symbolSources };
        }
        var symbolSourcesErrors = [];
        var symbolSourcesWarnings = [];
        var symbolSourcesWithErrors = symbolSources.map(function (symbolSource) {
            if (symbolSource.id === appStoreConnectContext.id) {
                var appStoreConnectErrors = [];
                var customRepositoryLink = "/settings/" + organization.slug + "/projects/" + projectSlug + "/debug-symbols/?customRepository=" + symbolSource.id;
                if (appStoreConnectContext.itunesSessionValid &&
                    appStoreConnectContext.appstoreCredentialsValid) {
                    var updateAlertMessage = appStoreConnectContext.updateAlertMessage;
                    if (updateAlertMessage ===
                        appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt) {
                        symbolSourcesWarnings.push(<div>
                {t('Your iTunes session will likely expire soon.')}
                &nbsp;
                {tct('We recommend that you revalidate the session for [link]', {
                                link: (<Link to={customRepositoryLink + "&revalidateItunesSession=true"}>
                      {symbolSource.name}
                    </Link>),
                            })}
              </div>);
                        return __assign(__assign({}, symbolSource), { warning: updateAlertMessage });
                    }
                }
                if (appStoreConnectContext.itunesSessionValid === false) {
                    symbolSourcesErrors.push(tct('Revalidate your iTunes session for [link]', {
                        link: (<Link to={customRepositoryLink + "&revalidateItunesSession=true"}>
                  {symbolSource.name}
                </Link>),
                    }));
                    appStoreConnectErrors.push(t('Revalidate your iTunes session'));
                }
                if (appStoreConnectContext.appstoreCredentialsValid === false) {
                    symbolSourcesErrors.push(tct('Recheck your App Store Credentials for [link]', {
                        link: <Link to={customRepositoryLink}>{symbolSource.name}</Link>,
                    }));
                    appStoreConnectErrors.push(t('Recheck your App Store Credentials'));
                }
                return __assign(__assign({}, symbolSource), { error: !!appStoreConnectErrors.length ? (<Fragment>
              {tn('There was an error connecting to the Apple Store Connect:', 'There were errors connecting to the Apple Store Connect:', appStoreConnectErrors.length)}
              <StyledList symbol="bullet">
                {appStoreConnectErrors.map(function (error, errorIndex) { return (<ListItem key={errorIndex}>{error}</ListItem>); })}
              </StyledList>
            </Fragment>) : undefined });
            }
            return symbolSource;
        });
        return {
            value: symbolSourcesWithErrors,
            errors: symbolSourcesErrors,
            warnings: symbolSourcesWarnings,
        };
    }
    var _c = getRichListFieldValue(), value = _c.value, _d = _c.warnings, warnings = _d === void 0 ? [] : _d, _e = _c.errors, errors = _e === void 0 ? [] : _e;
    function openDebugFileSourceDialog() {
        var customRepository = location.query.customRepository;
        if (!customRepository) {
            return;
        }
        var itemIndex = value.findIndex(function (v) { return v.id === customRepository; });
        var item = value[itemIndex];
        if (!item) {
            return;
        }
        var _warning = item._warning, _error = item._error, sourceConfig = __rest(item, ["_warning", "_error"]);
        openDebugFileSourceModal({
            sourceConfig: sourceConfig,
            sourceType: item.type,
            appStoreConnectContext: appStoreConnectContext,
            onSave: function (updatedItem) {
                return handleSaveModal({ updatedItem: updatedItem, index: itemIndex });
            },
            onClose: handleCloseModal,
        });
    }
    function getRequestMessages(updatedSymbolSourcesQuantity) {
        if (updatedSymbolSourcesQuantity > symbolSources.length) {
            return {
                successMessage: t('Successfully added custom repository'),
                errorMessage: t('An error occurred while adding a new custom repository'),
            };
        }
        if (updatedSymbolSourcesQuantity < symbolSources.length) {
            return {
                successMessage: t('Successfully removed custom repository'),
                errorMessage: t('An error occurred while removing the custom repository'),
            };
        }
        return {
            successMessage: t('Successfully updated custom repository'),
            errorMessage: t('An error occurred while updating the custom repository'),
        };
    }
    function handleSaveModal(_a) {
        var updatedItems = _a.updatedItems, updatedItem = _a.updatedItem, index = _a.index;
        var items = updatedItems !== null && updatedItems !== void 0 ? updatedItems : [];
        if (updatedItem && defined(index)) {
            items = __spreadArray([], __read(symbolSources));
            items.splice(index, 1, updatedItem);
        }
        var symbolSourcesWithoutErrors = items.map(function (item) {
            return omit(item, ['error', 'warning']);
        });
        var _b = getRequestMessages(items.length), successMessage = _b.successMessage, errorMessage = _b.errorMessage;
        var expandedSymbolSourceKeys = symbolSourcesWithoutErrors.map(expandKeys);
        var promise = api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/", {
            method: 'PUT',
            data: {
                symbolSources: JSON.stringify(expandedSymbolSourceKeys),
            },
        });
        promise.catch(function () {
            addErrorMessage(errorMessage);
        });
        promise.then(function (result) {
            ProjectActions.updateSuccess(result);
            addSuccessMessage(successMessage);
        });
        return promise;
    }
    function handleEditModal(repositoryId) {
        router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { customRepository: repositoryId }) }));
    }
    function handleCloseModal() {
        router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { customRepository: undefined, revalidateItunesSession: undefined }) }));
    }
    return (<Fragment>
      {!!warnings.length && (<Alert type="warning" icon={<IconRefresh />} system>
          {tn('Please check the warning related to the following custom repository:', 'Please check the warnings related to the following custom repositories:', warnings.length)}
          <StyledList symbol="bullet">
            {warnings.map(function (warning, index) { return (<ListItem key={index}>{warning}</ListItem>); })}
          </StyledList>
        </Alert>)}
      {!!errors.length && (<Alert type="error" icon={<IconWarning />} system>
          {tn('There was an error connecting to the following custom repository:', 'There were errors connecting to the following custom repositories:', errors.length)}
          <StyledList symbol="bullet">
            {errors.map(function (error, index) { return (<ListItem key={index}>{error}</ListItem>); })}
          </StyledList>
        </Alert>)}
      <Field label={t('Custom Repositories')} help={<Feature features={['organizations:custom-symbol-sources']} hookName="feature-disabled:custom-symbol-sources" organization={organization} renderDisabled={function (p) { return (<FeatureDisabled features={p.features} message={t('Custom repositories are disabled.')} featureName={t('custom repositories')}/>); }}>
            {t('Configures custom repositories containing debug files.')}
          </Feature>} flexibleControlStateSize>
        <StyledRichListField inline={false} addButtonText={t('Add Repository')} name="symbolSources" value={value} onChange={function (updatedItems) {
            handleSaveModal({ updatedItems: updatedItems });
        }} renderItem={function (item) {
            var _a;
            return (<TextOverflow>{(_a = item.name) !== null && _a !== void 0 ? _a : t('<Unnamed Repository>')}</TextOverflow>);
        }} disabled={!organization.features.includes('custom-symbol-sources')} formatMessageValue={false} onEditItem={function (item) { return handleEditModal(item.id); }} onAddItem={function (item, addItem) {
            openDebugFileSourceModal({
                sourceType: item.value,
                onSave: function (updatedData) { return Promise.resolve(addItem(updatedData)); },
            });
        }} removeConfirm={{
            onConfirm: function (item) {
                if (item.type === 'appStoreConnect') {
                    window.location.reload();
                }
            },
            confirmText: t('Remove Repository'),
            message: (<Fragment>
                <TextBlock>
                  <strong>
                    {t('Removing this repository applies instantly to new events.')}
                  </strong>
                </TextBlock>
                <TextBlock>
                  {t('Debug files from this repository will not be used to symbolicate future events. This may create new issues and alert members in your organization.')}
                </TextBlock>
              </Fragment>),
        }} addDropdown={{ items: dropDownItems }}/>
      </Field>
    </Fragment>);
}
export default SymbolSources;
var StyledRichListField = styled(RichListField)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledList = styled(List)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=symbolSources.jsx.map