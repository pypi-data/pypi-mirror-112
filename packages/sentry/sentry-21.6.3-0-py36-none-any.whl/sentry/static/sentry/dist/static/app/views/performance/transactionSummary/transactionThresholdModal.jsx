import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import * as React from 'react';
import { Link } from 'react-router';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import set from 'lodash/set';
import { addErrorMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import FeatureBadge from 'app/components/featureBadge';
import SelectControl from 'app/components/forms/selectControl';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import withApi from 'app/utils/withApi';
import withProjects from 'app/utils/withProjects';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
export var TransactionThresholdMetric;
(function (TransactionThresholdMetric) {
    TransactionThresholdMetric["TRANSACTION_DURATION"] = "duration";
    TransactionThresholdMetric["LARGEST_CONTENTFUL_PAINT"] = "lcp";
})(TransactionThresholdMetric || (TransactionThresholdMetric = {}));
export var METRIC_CHOICES = [
    { label: t('Transaction Duration'), value: 'duration' },
    { label: t('Largest Contentful Paint'), value: 'lcp' },
];
var TransactionThresholdModal = /** @class */ (function (_super) {
    __extends(TransactionThresholdModal, _super);
    function TransactionThresholdModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            threshold: _this.props.transactionThreshold,
            metric: _this.props.transactionThresholdMetric,
            error: null,
        };
        _this.handleApply = function (event) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, closeModal, organization, transactionName, onApply, project, transactionThresholdUrl;
            var _this = this;
            return __generator(this, function (_b) {
                event.preventDefault();
                _a = this.props, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, transactionName = _a.transactionName, onApply = _a.onApply;
                project = this.getProject();
                if (!defined(project)) {
                    return [2 /*return*/];
                }
                transactionThresholdUrl = "/organizations/" + organization.slug + "/project-transaction-threshold-override/";
                api
                    .requestPromise(transactionThresholdUrl, {
                    method: 'POST',
                    includeAllArgs: true,
                    query: {
                        project: project.id,
                    },
                    data: {
                        transaction: transactionName,
                        threshold: this.state.threshold,
                        metric: this.state.metric,
                    },
                })
                    .then(function () {
                    closeModal();
                    if (onApply) {
                        onApply(_this.state.threshold, _this.state.metric);
                    }
                })
                    .catch(function (err) {
                    var _a, _b, _c, _d;
                    _this.setState({
                        error: err,
                    });
                    var errorMessage = (_d = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : (_c = err.responseJSON) === null || _c === void 0 ? void 0 : _c.non_field_errors) !== null && _d !== void 0 ? _d : null;
                    addErrorMessage(errorMessage);
                });
                return [2 /*return*/];
            });
        }); };
        _this.handleFieldChange = function (field) { return function (value) {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                set(newState, field, value);
                return __assign(__assign({}, newState), { errors: undefined });
            });
        }; };
        _this.handleReset = function (event) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, closeModal, organization, transactionName, onApply, project, transactionThresholdUrl;
            var _this = this;
            return __generator(this, function (_b) {
                event.preventDefault();
                _a = this.props, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, transactionName = _a.transactionName, onApply = _a.onApply;
                project = this.getProject();
                if (!defined(project)) {
                    return [2 /*return*/];
                }
                transactionThresholdUrl = "/organizations/" + organization.slug + "/project-transaction-threshold-override/";
                api
                    .requestPromise(transactionThresholdUrl, {
                    method: 'DELETE',
                    includeAllArgs: true,
                    query: {
                        project: project.id,
                    },
                    data: {
                        transaction: transactionName,
                    },
                })
                    .then(function () {
                    var projectThresholdUrl = "/projects/" + organization.slug + "/" + project.slug + "/transaction-threshold/configure/";
                    _this.props.api
                        .requestPromise(projectThresholdUrl, {
                        method: 'GET',
                        includeAllArgs: true,
                        query: {
                            project: project.id,
                        },
                    })
                        .then(function (_a) {
                        var _b = __read(_a, 1), data = _b[0];
                        _this.setState({
                            threshold: data.threshold,
                            metric: data.metric,
                        });
                        closeModal();
                        if (onApply) {
                            onApply(_this.state.threshold, _this.state.metric);
                        }
                    })
                        .catch(function (err) {
                        var _a, _b;
                        var errorMessage = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : null;
                        addErrorMessage(errorMessage);
                    });
                })
                    .catch(function (err) {
                    _this.setState({
                        error: err,
                    });
                });
                return [2 /*return*/];
            });
        }); };
        return _this;
    }
    TransactionThresholdModal.prototype.getProject = function () {
        var _a = this.props, projects = _a.projects, eventView = _a.eventView, project = _a.project;
        if (defined(project)) {
            return projects.find(function (proj) { return proj.id === project; });
        }
        else {
            var projectId_1 = String(eventView.project[0]);
            return projects.find(function (proj) { return proj.id === projectId_1; });
        }
    };
    TransactionThresholdModal.prototype.renderModalFields = function () {
        var _this = this;
        return (<React.Fragment>
        <Field data-test-id="response-metric" label={t('Calculation Method')} inline={false} help={t('This determines which duration metric is used for the Response Time Threshold.')} showHelpInTooltip flexibleControlStateSize stacked required>
          <SelectControl required options={METRIC_CHOICES.slice()} name="responseMetric" label={t('Calculation Method')} value={this.state.metric} onChange={function (option) {
                _this.handleFieldChange('metric')(option.value);
            }}/>
        </Field>
        <Field data-test-id="response-time-threshold" label={t('Response Time Threshold (ms)')} inline={false} help={t('The satisfactory response time for the calculation method defined above. This is used to calculate Apdex and User Misery scores.')} showHelpInTooltip flexibleControlStateSize stacked required>
          <Input type="number" name="threshold" required pattern="[0-9]*(\.[0-9]*)?" onChange={function (event) {
                _this.handleFieldChange('threshold')(event.target.value);
            }} value={this.state.threshold} step={100} min={100}/>
        </Field>
      </React.Fragment>);
    };
    TransactionThresholdModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, organization = _a.organization;
        var project = this.getProject();
        return (<React.Fragment>
        <Header closeButton>
          <h4>
            {t('Transaction Settings')} <FeatureBadge type="alpha"/>
          </h4>
        </Header>
        <Body>
          <Instruction>
            {tct('The changes below will only be applied to this Transaction. To set it at a more global level, go to [projectSettings: Project Settings].', {
                projectSettings: (<Link to={"/settings/" + organization.slug + "/projects/" + (project === null || project === void 0 ? void 0 : project.slug) + "/performance/"}/>),
            })}
          </Instruction>
          {this.renderModalFields()}
        </Body>
        <Footer>
          <ButtonBar gap={1}>
            <Button priority="default" onClick={this.handleReset} data-test-id="reset-all">
              {t('Reset All')}
            </Button>
            <Button label={t('Apply')} priority="primary" onClick={this.handleApply} data-test-id="apply-threshold">
              {t('Apply')}
            </Button>
          </ButtonBar>
        </Footer>
      </React.Fragment>);
    };
    return TransactionThresholdModal;
}(React.Component));
var Instruction = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
export var modalCss = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 100%;\n  max-width: 650px;\n  margin: 70px auto;\n"], ["\n  width: 100%;\n  max-width: 650px;\n  margin: 70px auto;\n"])));
export default withApi(withProjects(TransactionThresholdModal));
var templateObject_1, templateObject_2;
//# sourceMappingURL=transactionThresholdModal.jsx.map