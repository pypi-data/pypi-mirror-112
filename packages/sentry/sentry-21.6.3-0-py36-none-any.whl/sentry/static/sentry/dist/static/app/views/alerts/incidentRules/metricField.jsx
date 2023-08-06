import { __assign, __makeTemplateObject, __rest } from "tslib";
import { Fragment } from 'react';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Tooltip from 'app/components/tooltip';
import { t, tct } from 'app/locale';
import { AGGREGATIONS, explodeFieldString, FIELDS, generateFieldAsString, } from 'app/utils/discover/fields';
import { hideParameterSelectorSet, hidePrimarySelectorSet, } from 'app/views/alerts/wizard/options';
import { QueryField } from 'app/views/eventsV2/table/queryField';
import { FieldValueKind } from 'app/views/eventsV2/table/types';
import { generateFieldOptions } from 'app/views/eventsV2/utils';
import FormField from 'app/views/settings/components/forms/formField';
import { errorFieldConfig, getWizardAlertFieldConfig, transactionFieldConfig, } from './constants';
import { PRESET_AGGREGATES } from './presets';
import { Dataset } from './types';
var getFieldOptionConfig = function (_a) {
    var dataset = _a.dataset, alertType = _a.alertType;
    var config;
    var hidePrimarySelector = false;
    var hideParameterSelector = false;
    if (alertType) {
        config = getWizardAlertFieldConfig(alertType, dataset);
        hidePrimarySelector = hidePrimarySelectorSet.has(alertType);
        hideParameterSelector = hideParameterSelectorSet.has(alertType);
    }
    else {
        config = dataset === Dataset.ERRORS ? errorFieldConfig : transactionFieldConfig;
    }
    var aggregations = Object.fromEntries(config.aggregations.map(function (key) {
        // TODO(scttcper): Temporary hack for default value while we handle the translation of user
        if (key === 'count_unique') {
            var agg = AGGREGATIONS[key];
            agg.getFieldOverrides = function () {
                return { defaultValue: 'tags[sentry:user]' };
            };
            return [key, agg];
        }
        return [key, AGGREGATIONS[key]];
    }));
    var fields = Object.fromEntries(config.fields.map(function (key) {
        // XXX(epurkhiser): Temporary hack while we handle the translation of user ->
        // tags[sentry:user].
        if (key === 'user') {
            return ['tags[sentry:user]', 'string'];
        }
        return [key, FIELDS[key]];
    }));
    var measurementKeys = config.measurementKeys;
    return {
        fieldOptionsConfig: { aggregations: aggregations, fields: fields, measurementKeys: measurementKeys },
        hidePrimarySelector: hidePrimarySelector,
        hideParameterSelector: hideParameterSelector,
    };
};
var help = function (_a) {
    var name = _a.name, model = _a.model;
    var aggregate = model.getValue(name);
    var presets = PRESET_AGGREGATES.filter(function (preset) {
        return preset.validDataset.includes(model.getValue('dataset'));
    })
        .map(function (preset) { return (__assign(__assign({}, preset), { selected: preset.match.test(aggregate) })); })
        .map(function (preset, i, list) { return (<Fragment key={preset.name}>
        <Tooltip title={t('This preset is selected')} disabled={!preset.selected}>
          <PresetButton type="button" onClick={function () { return model.setValue(name, preset.default); }} disabled={preset.selected}>
            {preset.name}
          </PresetButton>
        </Tooltip>
        {i + 1 < list.length && ', '}
      </Fragment>); });
    return tct('Choose an aggregate function. Not sure what to select, try a preset: [presets]', { presets: presets });
};
var MetricField = function (_a) {
    var organization = _a.organization, columnWidth = _a.columnWidth, inFieldLabels = _a.inFieldLabels, alertType = _a.alertType, props = __rest(_a, ["organization", "columnWidth", "inFieldLabels", "alertType"]);
    return (<FormField help={help} {...props}>
    {function (_a) {
            var _b;
            var onChange = _a.onChange, value = _a.value, model = _a.model, disabled = _a.disabled;
            var dataset = model.getValue('dataset');
            var _c = getFieldOptionConfig({
                dataset: dataset,
                alertType: alertType,
            }), fieldOptionsConfig = _c.fieldOptionsConfig, hidePrimarySelector = _c.hidePrimarySelector, hideParameterSelector = _c.hideParameterSelector;
            var fieldOptions = generateFieldOptions(__assign({ organization: organization }, fieldOptionsConfig));
            var fieldValue = explodeFieldString(value !== null && value !== void 0 ? value : '');
            var fieldKey = (fieldValue === null || fieldValue === void 0 ? void 0 : fieldValue.kind) === FieldValueKind.FUNCTION
                ? "function:" + fieldValue.function[0]
                : '';
            var selectedField = (_b = fieldOptions[fieldKey]) === null || _b === void 0 ? void 0 : _b.value;
            var numParameters = (selectedField === null || selectedField === void 0 ? void 0 : selectedField.kind) === FieldValueKind.FUNCTION
                ? selectedField.meta.parameters.length
                : 0;
            var parameterColumns = numParameters - (hideParameterSelector ? 1 : 0) - (hidePrimarySelector ? 1 : 0);
            return (<Fragment>
          <StyledQueryField filterPrimaryOptions={function (option) { return option.value.kind === FieldValueKind.FUNCTION; }} fieldOptions={fieldOptions} fieldValue={fieldValue} onChange={function (v) { return onChange(generateFieldAsString(v), {}); }} columnWidth={columnWidth} gridColumns={parameterColumns + 1} inFieldLabels={inFieldLabels} shouldRenderTag={false} disabled={disabled} hideParameterSelector={hideParameterSelector} hidePrimarySelector={hidePrimarySelector}/>
        </Fragment>);
        }}
  </FormField>);
};
var StyledQueryField = styled(QueryField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.columnWidth && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      width: ", "px;\n    "], ["\n      width: ", "px;\n    "])), p.gridColumns * p.columnWidth);
});
var PresetButton = styled(Button)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.disabled && css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n      color: ", ";\n      &:hover,\n      &:focus {\n        color: ", ";\n      }\n    "], ["\n      color: ", ";\n      &:hover,\n      &:focus {\n        color: ", ";\n      }\n    "])), p.theme.textColor, p.theme.textColor);
});
PresetButton.defaultProps = {
    priority: 'link',
    borderless: true,
};
export default MetricField;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=metricField.jsx.map