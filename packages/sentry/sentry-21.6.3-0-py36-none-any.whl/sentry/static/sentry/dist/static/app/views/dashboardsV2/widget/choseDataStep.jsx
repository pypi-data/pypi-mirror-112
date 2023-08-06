import { t } from 'app/locale';
import RadioField from 'app/views/settings/components/forms/radioField';
import BuildStep from './buildStep';
import { DataSet } from './utils';
var dataSetChoices = [
    [DataSet.EVENTS, t('Events')],
    [DataSet.METRICS, t('Metrics')],
];
function ChooseDataSetStep(_a) {
    var value = _a.value, onChange = _a.onChange;
    return (<BuildStep title={t('Choose your data set')} description={t('Monitor specific events such as errors and transactions or get metric readings on TBD.')}>
      <RadioField name="dataSet" onChange={onChange} value={value} choices={dataSetChoices} inline={false} orientInline hideControlState stacked/>
    </BuildStep>);
}
export default ChooseDataSetStep;
//# sourceMappingURL=choseDataStep.jsx.map