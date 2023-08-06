import { __assign, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Input from 'app/views/settings/components/forms/controls/input';
import GroupByField from './groupByField';
import MetricSelectField from './metricSelectField';
function Queries(_a) {
    var metricMetas = _a.metricMetas, metricTags = _a.metricTags, queries = _a.queries, onRemoveQuery = _a.onRemoveQuery, onAddQuery = _a.onAddQuery, onChangeQuery = _a.onChangeQuery;
    function handleFieldChange(queryIndex, field) {
        var widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            var _a;
            var newQuery = __assign(__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
            onChangeQuery(queryIndex, newQuery);
        };
    }
    return (<Wrapper>
      {queries.map(function (query, queryIndex) {
            return (<Fields displayDeleteButton={queries.length > 1} key={queryIndex}>
            <MetricSelectField metricMetas={metricMetas} metricMeta={query.metricMeta} aggregation={query.aggregation} onChange={function (field, value) { return handleFieldChange(queryIndex, field)(value); }}/>
            <GroupByField metricTags={metricTags} groupBy={query.groupBy} onChange={function (v) { return handleFieldChange(queryIndex, 'groupBy')(v); }}/>
            <Input type="text" name="legend" value={query.legend} placeholder={t('Legend Alias')} onChange={function (event) {
                    return handleFieldChange(queryIndex, 'legend')(event.target.value);
                }} required/>
            {queries.length > 1 && (<Fragment>
                <ButtonDeleteWrapper>
                  <Button onClick={function () {
                        onRemoveQuery(queryIndex);
                    }} size="small">
                    {t('Delete Query')}
                  </Button>
                </ButtonDeleteWrapper>
                <IconDeleteWrapper onClick={function () {
                        onRemoveQuery(queryIndex);
                    }}>
                  <IconDelete aria-label={t('Delete Query')}/>
                </IconDeleteWrapper>
              </Fragment>)}
          </Fields>);
        })}
      <div>
        <Button size="small" icon={<IconAdd isCircled/>} onClick={onAddQuery}>
          {t('Add query')}
        </Button>
      </div>
    </Wrapper>);
}
export default Queries;
var IconDeleteWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 40px;\n  cursor: pointer;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  height: 40px;\n  cursor: pointer;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var Fields = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: ", ";\n    grid-gap: ", ";\n    align-items: center;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: ", ";\n    grid-gap: ", ";\n    align-items: center;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; }, function (p) {
    return p.displayDeleteButton ? '1.3fr 1fr 0.5fr max-content' : '1.3fr 1fr 0.5fr';
}, space(1));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    ", " {\n      :not(:first-child) {\n        border-top: 1px solid ", ";\n        padding-top: ", ";\n      }\n    }\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    ", " {\n      :not(:first-child) {\n        border-top: 1px solid ", ";\n        padding-top: ", ";\n      }\n    }\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; }, Fields, function (p) { return p.theme.border; }, space(2));
var ButtonDeleteWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=queries.jsx.map