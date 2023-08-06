import DurationChart from '../chart/durationChart';
import HistogramChart from '../chart/histogramChart';
import { getAxisOrBackupAxis, getBackupField } from './utils';
export function SingleAxisChart(props) {
    var axis = props.axis, onFilterChange = props.onFilterChange, eventView = props.eventView, organization = props.organization, location = props.location, didReceiveMultiAxis = props.didReceiveMultiAxis, usingBackupAxis = props.usingBackupAxis;
    var backupField = getBackupField(axis);
    function didReceiveMulti(dataCounts) {
        if (!didReceiveMultiAxis) {
            return;
        }
        if (dataCounts[axis.field]) {
            didReceiveMultiAxis(false);
            return;
        }
        if (backupField && dataCounts[backupField]) {
            didReceiveMultiAxis(true);
            return;
        }
    }
    var axisOrBackup = getAxisOrBackupAxis(axis, usingBackupAxis);
    return axis.isDistribution ? (<HistogramChart field={axis.field} eventView={eventView} organization={organization} location={location} onFilterChange={onFilterChange} title={axisOrBackup.label} titleTooltip={axisOrBackup.tooltip} didReceiveMultiAxis={didReceiveMulti} usingBackupAxis={usingBackupAxis} backupField={backupField}/>) : (<DurationChart field={axis.field} eventView={eventView} organization={organization} title={axisOrBackup.label} titleTooltip={axisOrBackup.tooltip} usingBackupAxis={usingBackupAxis} backupField={backupField}/>);
}
//# sourceMappingURL=singleAxisChart.jsx.map