import { __assign, __makeTemplateObject, __rest } from "tslib";
import { components } from 'react-select';
import styled from '@emotion/styled';
import SelectControl from 'app/components/forms/selectControl';
import Highlight from 'app/components/highlight';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import SelectField from 'app/views/settings/components/forms/selectField';
function MetricSelectField(_a) {
    var _b, _c;
    var metricMetas = _a.metricMetas, metricMeta = _a.metricMeta, aggregation = _a.aggregation, onChange = _a.onChange;
    var operations = (_b = metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.operations) !== null && _b !== void 0 ? _b : [];
    return (<Wrapper>
      <StyledSelectField name="metric" choices={metricMetas.map(function (metricMetaChoice) { return [
            metricMetaChoice.name,
            metricMetaChoice.name,
        ]; })} placeholder={t('Select metric')} onChange={function (value) {
            var newMetric = metricMetas.find(function (metricMetaChoice) { return metricMetaChoice.name === value; });
            onChange('metricMeta', newMetric);
        }} value={(_c = metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.name) !== null && _c !== void 0 ? _c : ''} components={{
            Option: function (_a) {
                var label = _a.label, optionProps = __rest(_a, ["label"]);
                var selectProps = optionProps.selectProps;
                var inputValue = selectProps.inputValue;
                return (<components.Option label={label} {...optionProps}>
                <Highlight text={inputValue !== null && inputValue !== void 0 ? inputValue : ''}>{label}</Highlight>
              </components.Option>);
            },
        }} styles={{
            control: function (provided) { return (__assign(__assign({}, provided), { borderTopRightRadius: 0, borderBottomRightRadius: 0, borderRight: 'none', boxShadow: 'none' })); },
        }} inline={false} flexibleControlStateSize stacked allowClear/>
      <Tooltip disabled={!!operations.length} title={t('Please select a metric to enable this field')}>
        <SelectControl name="aggregation" placeholder={t('Aggr')} disabled={!operations.length} options={operations.map(function (operation) { return ({
            label: operation === 'count_unique' ? 'unique' : operation,
            value: operation,
        }); })} value={aggregation !== null && aggregation !== void 0 ? aggregation : ''} onChange={function (_a) {
        var value = _a.value;
        return onChange('aggregation', value);
    }} styles={{
            control: function (provided) { return (__assign(__assign({}, provided), { borderTopLeftRadius: 0, borderBottomLeftRadius: 0, boxShadow: 'none' })); },
        }}/>
      </Tooltip>
    </Wrapper>);
}
export default MetricSelectField;
var StyledSelectField = styled(SelectField)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-right: 0;\n  padding-bottom: 0;\n"], ["\n  padding-right: 0;\n  padding-bottom: 0;\n"])));
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=metricSelectField.jsx.map