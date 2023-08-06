import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spreadArray, __values } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { fetchOrganizationTags } from 'app/actionCreators/tags';
import Access from 'app/components/acl/access';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t } from 'app/locale';
import IndicatorStore from 'app/stores/indicatorStore';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { metric, trackAnalyticsEvent } from 'app/utils/analytics';
import { isActiveSuperuser } from 'app/utils/isActiveSuperuser';
import RuleNameOwnerForm from 'app/views/alerts/incidentRules/ruleNameOwnerForm';
import Triggers from 'app/views/alerts/incidentRules/triggers';
import TriggersChart from 'app/views/alerts/incidentRules/triggers/chart';
import { getEventTypeFilter } from 'app/views/alerts/incidentRules/utils/getEventTypeFilter';
import hasThresholdValue from 'app/views/alerts/incidentRules/utils/hasThresholdValue';
import { AlertWizardAlertNames } from 'app/views/alerts/wizard/options';
import { getAlertTypeFromAggregateDataset } from 'app/views/alerts/wizard/utils';
import Form from 'app/views/settings/components/forms/form';
import { addOrUpdateRule } from '../actions';
import { createDefaultTrigger } from '../constants';
import RuleConditionsFormForWizard from '../ruleConditionsFormForWizard';
import { AlertRuleThresholdType, Dataset, } from '../types';
var POLLING_MAX_TIME_LIMIT = 3 * 60000;
var isEmpty = function (str) { return str === '' || !defined(str); };
var RuleFormContainer = /** @class */ (function (_super) {
    __extends(RuleFormContainer, _super);
    function RuleFormContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.resetPollingState = function (loadingSlackIndicator) {
            IndicatorStore.remove(loadingSlackIndicator);
            _this.setState({ loading: false, uuid: undefined });
        };
        _this.pollHandler = function (model, quitTime, loadingSlackIndicator) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, onSubmitSuccess, ruleId, uuid, response, status_1, alertRule, error, _b;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (Date.now() > quitTime) {
                            addErrorMessage(t('Looking for that channel took too long :('));
                            this.resetPollingState(loadingSlackIndicator);
                            return [2 /*return*/];
                        }
                        _a = this.props, organization = _a.organization, project = _a.project, onSubmitSuccess = _a.onSubmitSuccess, ruleId = _a.params.ruleId;
                        uuid = this.state.uuid;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/alert-rule-task/" + uuid + "/")];
                    case 2:
                        response = _c.sent();
                        status_1 = response.status, alertRule = response.alertRule, error = response.error;
                        if (status_1 === 'pending') {
                            setTimeout(function () {
                                _this.pollHandler(model, quitTime, loadingSlackIndicator);
                            }, 1000);
                            return [2 /*return*/];
                        }
                        this.resetPollingState(loadingSlackIndicator);
                        if (status_1 === 'failed') {
                            this.handleRuleSaveFailure(error);
                        }
                        if (alertRule) {
                            addSuccessMessage(ruleId ? t('Updated alert rule') : t('Created alert rule'));
                            if (onSubmitSuccess) {
                                onSubmitSuccess(alertRule, model);
                            }
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.handleRuleSaveFailure(t('An error occurred'));
                        this.resetPollingState(loadingSlackIndicator);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        /**
         * Checks to see if threshold is valid given target value, and state of
         * inverted threshold as well as the *other* threshold
         *
         * @param type The threshold type to be updated
         * @param value The new threshold value
         */
        _this.isValidTrigger = function (triggerIndex, trigger, errors, resolveThreshold) {
            var alertThreshold = trigger.alertThreshold;
            var thresholdType = _this.state.thresholdType;
            // If value and/or other value is empty
            // then there are no checks to perform against
            if (!hasThresholdValue(alertThreshold) || !hasThresholdValue(resolveThreshold)) {
                return true;
            }
            // If this is alert threshold and not inverted, it can't be below resolve
            // If this is alert threshold and inverted, it can't be above resolve
            // If this is resolve threshold and not inverted, it can't be above resolve
            // If this is resolve threshold and inverted, it can't be below resolve
            // Since we're comparing non-inclusive thresholds here (>, <), we need
            // to modify the values when we compare. An example of why:
            // Alert > 0, resolve < 1. This means that we want to alert on values
            // of 1 or more, and resolve on values of 0 or less. This is valid, but
            // without modifying the values, this boundary case will fail.
            var isValid = thresholdType === AlertRuleThresholdType.BELOW
                ? alertThreshold - 1 <= resolveThreshold + 1
                : alertThreshold + 1 >= resolveThreshold - 1;
            var otherErrors = errors.get(triggerIndex) || {};
            if (isValid) {
                return true;
            }
            // Not valid... let's figure out an error message
            var isBelow = thresholdType === AlertRuleThresholdType.BELOW;
            var errorMessage = '';
            if (typeof resolveThreshold !== 'number') {
                errorMessage = isBelow
                    ? t('Resolution threshold must be greater than alert')
                    : t('Resolution threshold must be less than alert');
            }
            else {
                errorMessage = isBelow
                    ? t('Alert threshold must be less than resolution')
                    : t('Alert threshold must be greater than resolution');
            }
            errors.set(triggerIndex, __assign(__assign({}, otherErrors), { alertThreshold: errorMessage }));
            return false;
        };
        _this.handleFieldChange = function (name, value) {
            var _a;
            if (['dataset', 'eventTypes', 'timeWindow', 'environment', 'aggregate'].includes(name)) {
                _this.setState((_a = {}, _a[name] = value, _a));
            }
        };
        // We handle the filter update outside of the fieldChange handler since we
        // don't want to update the filter on every input change, just on blurs and
        // searches.
        _this.handleFilterUpdate = function (query) {
            var _a = _this.props, organization = _a.organization, sessionId = _a.sessionId;
            trackAnalyticsEvent({
                eventKey: 'alert_builder.filter',
                eventName: 'Alert Builder: Filter',
                query: query,
                organization_id: organization.id,
                session_id: sessionId,
            });
            _this.setState({ query: query });
        };
        _this.handleSubmit = function (_data, _onSubmitSuccess, _onSubmitError, _e, model) { return __awaiter(_this, void 0, void 0, function () {
            var validRule, triggerErrors, validTriggers, _a, organization, params, rule, onSubmitSuccess, location, sessionId, ruleId, _b, resolveThreshold, triggers, thresholdType, uuid, sanitizedTriggers, loadingIndicator, transaction, sanitizedTriggers_1, sanitizedTriggers_1_1, trigger, _c, _d, action, _f, resp, xhr, err_1, errors, apiErrors;
            var e_1, _g, e_2, _h;
            var _j;
            return __generator(this, function (_k) {
                switch (_k.label) {
                    case 0:
                        validRule = model.validateForm();
                        triggerErrors = this.validateTriggers();
                        validTriggers = Array.from(triggerErrors).length === 0;
                        if (!validTriggers) {
                            this.setState(function (state) { return ({
                                triggerErrors: new Map(__spreadArray(__spreadArray([], __read(triggerErrors)), __read(state.triggerErrors))),
                            }); });
                        }
                        if (!validRule || !validTriggers) {
                            addErrorMessage(t('Alert not valid'));
                            return [2 /*return*/];
                        }
                        _a = this.props, organization = _a.organization, params = _a.params, rule = _a.rule, onSubmitSuccess = _a.onSubmitSuccess, location = _a.location, sessionId = _a.sessionId;
                        ruleId = this.props.params.ruleId;
                        _b = this.state, resolveThreshold = _b.resolveThreshold, triggers = _b.triggers, thresholdType = _b.thresholdType, uuid = _b.uuid;
                        sanitizedTriggers = triggers.filter(function (trigger) { return trigger.label !== 'warning' || !isEmpty(trigger.alertThreshold); });
                        loadingIndicator = IndicatorStore.addMessage(t('Saving your alert rule, hold on...'), 'loading');
                        _k.label = 1;
                    case 1:
                        _k.trys.push([1, 3, , 4]);
                        transaction = metric.startTransaction({ name: 'saveAlertRule' });
                        transaction.setTag('type', 'metric');
                        transaction.setTag('operation', !rule.id ? 'create' : 'edit');
                        try {
                            for (sanitizedTriggers_1 = __values(sanitizedTriggers), sanitizedTriggers_1_1 = sanitizedTriggers_1.next(); !sanitizedTriggers_1_1.done; sanitizedTriggers_1_1 = sanitizedTriggers_1.next()) {
                                trigger = sanitizedTriggers_1_1.value;
                                try {
                                    for (_c = (e_2 = void 0, __values(trigger.actions)), _d = _c.next(); !_d.done; _d = _c.next()) {
                                        action = _d.value;
                                        if (action.type === 'slack') {
                                            transaction.setTag(action.type, true);
                                        }
                                    }
                                }
                                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                                finally {
                                    try {
                                        if (_d && !_d.done && (_h = _c.return)) _h.call(_c);
                                    }
                                    finally { if (e_2) throw e_2.error; }
                                }
                            }
                        }
                        catch (e_1_1) { e_1 = { error: e_1_1 }; }
                        finally {
                            try {
                                if (sanitizedTriggers_1_1 && !sanitizedTriggers_1_1.done && (_g = sanitizedTriggers_1.return)) _g.call(sanitizedTriggers_1);
                            }
                            finally { if (e_1) throw e_1.error; }
                        }
                        transaction.setData('actions', sanitizedTriggers);
                        this.setState({ loading: true });
                        return [4 /*yield*/, addOrUpdateRule(this.api, organization.slug, params.projectId, __assign(__assign(__assign({}, rule), model.getTransformedData()), { triggers: sanitizedTriggers, resolveThreshold: isEmpty(resolveThreshold) ? null : resolveThreshold, thresholdType: thresholdType }), {
                                referrer: (_j = location === null || location === void 0 ? void 0 : location.query) === null || _j === void 0 ? void 0 : _j.referrer,
                                sessionId: sessionId,
                            })];
                    case 2:
                        _f = __read.apply(void 0, [_k.sent(), 3]), resp = _f[0], xhr = _f[2];
                        // if we get a 202 back it means that we have an async task
                        // running to lookup and verify the channel id for Slack.
                        if (xhr && xhr.status === 202) {
                            // if we have a uuid in state, no need to start a new polling cycle
                            if (!uuid) {
                                this.setState({ loading: true, uuid: resp.uuid });
                                this.fetchStatus(model);
                            }
                        }
                        else {
                            IndicatorStore.remove(loadingIndicator);
                            this.setState({ loading: false });
                            addSuccessMessage(ruleId ? t('Updated alert rule') : t('Created alert rule'));
                            if (onSubmitSuccess) {
                                onSubmitSuccess(resp, model);
                            }
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _k.sent();
                        IndicatorStore.remove(loadingIndicator);
                        this.setState({ loading: false });
                        errors = (err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            ? Array.isArray(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                                ? err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON
                                : Object.values(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            : [];
                        apiErrors = errors.length > 0 ? ": " + errors.join(', ') : '';
                        this.handleRuleSaveFailure(t('Unable to save alert%s', apiErrors));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        /**
         * Callback for when triggers change
         *
         * Re-validate triggers on every change and reset indicators when no errors
         */
        _this.handleChangeTriggers = function (triggers, triggerIndex) {
            _this.setState(function (state) {
                var triggerErrors = state.triggerErrors;
                var newTriggerErrors = _this.validateTriggers(triggers, state.thresholdType, state.resolveThreshold, triggerIndex);
                triggerErrors = newTriggerErrors;
                if (Array.from(newTriggerErrors).length === 0) {
                    clearIndicators();
                }
                return { triggers: triggers, triggerErrors: triggerErrors };
            });
        };
        _this.handleThresholdTypeChange = function (thresholdType) {
            var triggers = _this.state.triggers;
            var triggerErrors = _this.validateTriggers(triggers, thresholdType);
            _this.setState(function (state) { return ({
                thresholdType: thresholdType,
                triggerErrors: new Map(__spreadArray(__spreadArray([], __read(triggerErrors)), __read(state.triggerErrors))),
            }); });
        };
        _this.handleResolveThresholdChange = function (resolveThreshold) {
            var triggers = _this.state.triggers;
            var triggerErrors = _this.validateTriggers(triggers, undefined, resolveThreshold);
            _this.setState(function (state) { return ({
                resolveThreshold: resolveThreshold,
                triggerErrors: new Map(__spreadArray(__spreadArray([], __read(triggerErrors)), __read(state.triggerErrors))),
            }); });
        };
        _this.handleDeleteRule = function () { return __awaiter(_this, void 0, void 0, function () {
            var params, orgId, projectId, ruleId, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        orgId = params.orgId, projectId = params.projectId, ruleId = params.ruleId;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/alert-rules/" + ruleId + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        this.goBack();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        addErrorMessage(t('Error deleting rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRuleSaveFailure = function (msg) {
            addErrorMessage(msg);
            metric.endTransaction({ name: 'saveAlertRule' });
        };
        _this.handleCancel = function () {
            _this.goBack();
        };
        return _this;
    }
    RuleFormContainer.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        // SearchBar gets its tags from Reflux.
        fetchOrganizationTags(this.api, organization.slug, [project.id]);
    };
    RuleFormContainer.prototype.getDefaultState = function () {
        var rule = this.props.rule;
        var triggersClone = __spreadArray([], __read(rule.triggers));
        // Warning trigger is removed if it is blank when saving
        if (triggersClone.length !== 2) {
            triggersClone.push(createDefaultTrigger('warning'));
        }
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { dataset: rule.dataset, eventTypes: rule.eventTypes, aggregate: rule.aggregate, query: rule.query || '', timeWindow: rule.timeWindow, environment: rule.environment || null, triggerErrors: new Map(), availableActions: null, triggers: triggersClone, resolveThreshold: rule.resolveThreshold, thresholdType: rule.thresholdType, projects: [this.props.project], owner: rule.owner });
    };
    RuleFormContainer.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        // TODO(incidents): This is temporary until new API endpoints
        // We should be able to just fetch the rule if rule.id exists
        return [
            ['availableActions', "/organizations/" + orgId + "/alert-rules/available-actions/"],
        ];
    };
    RuleFormContainer.prototype.goBack = function () {
        var router = this.props.router;
        var orgId = this.props.params.orgId;
        router.push("/organizations/" + orgId + "/alerts/rules/");
    };
    RuleFormContainer.prototype.fetchStatus = function (model) {
        var _this = this;
        var loadingSlackIndicator = IndicatorStore.addMessage(t('Looking for your slack channel (this can take a while)'), 'loading');
        // pollHandler calls itself until it gets either a success
        // or failed status but we don't want to poll forever so we pass
        // in a hard stop time of 3 minutes before we bail.
        var quitTime = Date.now() + POLLING_MAX_TIME_LIMIT;
        setTimeout(function () {
            _this.pollHandler(model, quitTime, loadingSlackIndicator);
        }, 1000);
    };
    RuleFormContainer.prototype.validateFieldInTrigger = function (_a) {
        var _b;
        var errors = _a.errors, triggerIndex = _a.triggerIndex, field = _a.field, message = _a.message, isValid = _a.isValid;
        // If valid, reset error for fieldName
        if (isValid()) {
            var _c = errors.get(triggerIndex) || {}, _d = field, _validatedField = _c[_d], otherErrors = __rest(_c, [typeof _d === "symbol" ? _d : _d + ""]);
            if (Object.keys(otherErrors).length > 0) {
                errors.set(triggerIndex, otherErrors);
            }
            else {
                errors.delete(triggerIndex);
            }
            return errors;
        }
        if (!errors.has(triggerIndex)) {
            errors.set(triggerIndex, {});
        }
        var currentErrors = errors.get(triggerIndex);
        errors.set(triggerIndex, __assign(__assign({}, currentErrors), (_b = {}, _b[field] = message, _b)));
        return errors;
    };
    /**
     * Validate triggers
     *
     * @return Returns true if triggers are valid
     */
    RuleFormContainer.prototype.validateTriggers = function (triggers, thresholdType, resolveThreshold, changedTriggerIndex) {
        var _this = this;
        var _a, _b;
        if (triggers === void 0) { triggers = this.state.triggers; }
        if (thresholdType === void 0) { thresholdType = this.state.thresholdType; }
        if (resolveThreshold === void 0) { resolveThreshold = this.state.resolveThreshold; }
        var triggerErrors = new Map();
        var requiredFields = ['label', 'alertThreshold'];
        triggers.forEach(function (trigger, triggerIndex) {
            requiredFields.forEach(function (field) {
                // check required fields
                _this.validateFieldInTrigger({
                    errors: triggerErrors,
                    triggerIndex: triggerIndex,
                    isValid: function () {
                        if (trigger.label === 'critical') {
                            return !isEmpty(trigger[field]);
                        }
                        // If warning trigger has actions, it must have a value
                        return trigger.actions.length === 0 || !isEmpty(trigger[field]);
                    },
                    field: field,
                    message: t('Field is required'),
                });
            });
            // Check thresholds
            _this.isValidTrigger(changedTriggerIndex !== null && changedTriggerIndex !== void 0 ? changedTriggerIndex : triggerIndex, trigger, triggerErrors, resolveThreshold);
        });
        // If we have 2 triggers, we need to make sure that the critical and warning
        // alert thresholds are valid (e.g. if critical is above x, warning must be less than x)
        var criticalTriggerIndex = triggers.findIndex(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTriggerIndex = criticalTriggerIndex ^ 1;
        var criticalTrigger = triggers[criticalTriggerIndex];
        var warningTrigger = triggers[warningTriggerIndex];
        var isEmptyWarningThreshold = isEmpty(warningTrigger.alertThreshold);
        var warningThreshold = (_a = warningTrigger.alertThreshold) !== null && _a !== void 0 ? _a : 0;
        var criticalThreshold = (_b = criticalTrigger.alertThreshold) !== null && _b !== void 0 ? _b : 0;
        var hasError = thresholdType === AlertRuleThresholdType.ABOVE
            ? warningThreshold > criticalThreshold
            : warningThreshold < criticalThreshold;
        if (hasError && !isEmptyWarningThreshold) {
            [criticalTriggerIndex, warningTriggerIndex].forEach(function (index) {
                var _a;
                var otherErrors = (_a = triggerErrors.get(index)) !== null && _a !== void 0 ? _a : {};
                triggerErrors.set(index, __assign(__assign({}, otherErrors), { alertThreshold: thresholdType === AlertRuleThresholdType.BELOW
                        ? t('Warning threshold must be greater than critical alert')
                        : t('Warning threshold must be less than critical alert') }));
            });
        }
        return triggerErrors;
    };
    RuleFormContainer.prototype.renderLoading = function () {
        return this.renderBody();
    };
    RuleFormContainer.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, ruleId = _b.ruleId, rule = _b.rule, params = _b.params, onSubmitSuccess = _b.onSubmitSuccess, project = _b.project, userTeamIds = _b.userTeamIds, isCustomMetric = _b.isCustomMetric;
        var _c = this.state, query = _c.query, timeWindow = _c.timeWindow, triggers = _c.triggers, aggregate = _c.aggregate, environment = _c.environment, thresholdType = _c.thresholdType, resolveThreshold = _c.resolveThreshold, loading = _c.loading, eventTypes = _c.eventTypes, dataset = _c.dataset;
        var eventTypeFilter = getEventTypeFilter(this.state.dataset, eventTypes);
        var queryWithTypeFilter = (query + " " + eventTypeFilter).trim();
        var chartProps = {
            organization: organization,
            projects: this.state.projects,
            triggers: triggers,
            query: queryWithTypeFilter,
            aggregate: aggregate,
            timeWindow: timeWindow,
            environment: environment,
            resolveThreshold: resolveThreshold,
            thresholdType: thresholdType,
        };
        var alertType = getAlertTypeFromAggregateDataset({ aggregate: aggregate, dataset: dataset });
        var wizardBuilderChart = (<TriggersChart {...chartProps} header={<ChartHeader>
            <AlertName>{AlertWizardAlertNames[alertType]}</AlertName>
            <AlertInfo>
              {aggregate} | event.type:{eventTypes === null || eventTypes === void 0 ? void 0 : eventTypes.join(',')}
            </AlertInfo>
          </ChartHeader>}/>);
        var ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        var canEdit = isActiveSuperuser() || (ownerId ? userTeamIds.includes(ownerId) : true);
        var triggerForm = function (hasAccess) { return (<Triggers disabled={!hasAccess || !canEdit} projects={_this.state.projects} errors={_this.state.triggerErrors} triggers={triggers} aggregate={aggregate} resolveThreshold={resolveThreshold} thresholdType={thresholdType} currentProject={params.projectId} organization={organization} ruleId={ruleId} availableActions={_this.state.availableActions} onChange={_this.handleChangeTriggers} onThresholdTypeChange={_this.handleThresholdTypeChange} onResolveThresholdChange={_this.handleResolveThresholdChange}/>); };
        var ruleNameOwnerForm = function (hasAccess) { return (<RuleNameOwnerForm disabled={!hasAccess || !canEdit} organization={organization} project={project} userTeamIds={userTeamIds}/>); };
        return (<Access access={['alerts:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<Form apiMethod={ruleId ? 'PUT' : 'POST'} apiEndpoint={"/organizations/" + organization.slug + "/alert-rules/" + (ruleId ? ruleId + "/" : '')} submitDisabled={!hasAccess || loading || !canEdit} initialData={{
                        name: rule.name || '',
                        dataset: rule.dataset,
                        eventTypes: rule.eventTypes,
                        aggregate: rule.aggregate,
                        query: rule.query || '',
                        timeWindow: rule.timeWindow,
                        environment: rule.environment || null,
                        owner: rule.owner,
                    }} saveOnBlur={false} onSubmit={_this.handleSubmit} onSubmitSuccess={onSubmitSuccess} onCancel={_this.handleCancel} onFieldChange={_this.handleFieldChange} extraButton={!!rule.id ? (<Confirm disabled={!hasAccess || !canEdit} message={t('Are you sure you want to delete this alert rule?')} header={t('Delete Alert Rule?')} priority="danger" confirmText={t('Delete Rule')} onConfirm={_this.handleDeleteRule}>
                  <Button type="button" priority="danger">
                    {t('Delete Rule')}
                  </Button>
                </Confirm>) : null} submitLabel={t('Save Rule')}>
            <List symbol="colored-numeric">
              <RuleConditionsFormForWizard api={_this.api} projectSlug={params.projectId} organization={organization} disabled={!hasAccess || !canEdit} thresholdChart={wizardBuilderChart} onFilterSearch={_this.handleFilterUpdate} allowChangeEventTypes={isCustomMetric || dataset === Dataset.ERRORS} alertType={isCustomMetric ? 'custom' : alertType}/>
              <AlertListItem>{t('Set thresholds to trigger alert')}</AlertListItem>
              {triggerForm(hasAccess)}
              <StyledListItem>{t('Add a rule name and team')}</StyledListItem>
              {ruleNameOwnerForm(hasAccess)}
            </List>
          </Form>);
            }}
      </Access>);
    };
    return RuleFormContainer;
}(AsyncComponent));
var StyledListItem = styled(ListItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 0 ", " 0;\n  font-size: ", ";\n"], ["\n  margin: ", " 0 ", " 0;\n  font-size: ", ";\n"])), space(2), space(1), function (p) { return p.theme.fontSizeExtraLarge; });
var AlertListItem = styled(StyledListItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var ChartHeader = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n"], ["\n  padding: ", " ", " 0 ", ";\n"])), space(3), space(3), space(3));
var AlertName = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  color: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, function (p) { return p.theme.textColor; });
var AlertInfo = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  font-family: ", ";\n  font-weight: normal;\n  color: ", ";\n"], ["\n  font-size: ", ";\n  font-family: ", ";\n  font-weight: normal;\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.subText; });
export default RuleFormContainer;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map