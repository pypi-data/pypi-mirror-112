export function getAxisOrBackupAxis(axis, usingBackupAxis) {
    var _a;
    var displayedAxis = usingBackupAxis ? (_a = getBackupAxisOption(axis)) !== null && _a !== void 0 ? _a : axis : axis;
    return displayedAxis;
}
export function getBackupAxisOption(axis) {
    return axis.backupOption;
}
export function getBackupAxes(axes, usingBackupAxis) {
    return usingBackupAxis ? axes.map(function (axis) { var _a; return (_a = getBackupAxisOption(axis)) !== null && _a !== void 0 ? _a : axis; }) : axes;
}
export function getBackupField(axis) {
    var backupOption = getBackupAxisOption(axis);
    if (!backupOption) {
        return undefined;
    }
    return backupOption.field;
}
export function getFieldOrBackup(field, backupField) {
    return backupField !== null && backupField !== void 0 ? backupField : field;
}
//# sourceMappingURL=utils.jsx.map