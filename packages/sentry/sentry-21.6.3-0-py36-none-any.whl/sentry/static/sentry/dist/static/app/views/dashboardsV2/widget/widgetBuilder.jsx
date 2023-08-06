import { __assign, __read, __spreadArray } from "tslib";
import { useEffect, useState } from 'react';
import Alert from 'app/components/alert';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import EventWidget from './eventWidget';
import MetricWidget from './metricWidget';
import { DataSet } from './utils';
function WidgetBuilder(_a) {
    var dashboard = _a.dashboard, onSave = _a.onSave, widget = _a.widget, params = _a.params, location = _a.location, router = _a.router, organization = _a.organization;
    var _b = __read(useState(DataSet.EVENTS), 2), dataSet = _b[0], setDataSet = _b[1];
    var isEditing = !!widget;
    var widgetId = params.widgetId, orgId = params.orgId, dashboardId = params.dashboardId;
    var goBackLocation = {
        pathname: dashboardId
            ? "/organizations/" + orgId + "/dashboard/" + dashboardId + "/"
            : "/organizations/" + orgId + "/dashboards/new/",
        query: __assign(__assign({}, location.query), { dataSet: undefined }),
    };
    useEffect(function () {
        checkDataSet();
    });
    function checkDataSet() {
        var query = location.query;
        var queryDataSet = query === null || query === void 0 ? void 0 : query.dataSet;
        if (!queryDataSet) {
            router.replace({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { dataSet: DataSet.EVENTS }),
            });
            return;
        }
        if (queryDataSet !== DataSet.EVENTS && queryDataSet !== DataSet.METRICS) {
            setDataSet(undefined);
            return;
        }
        if (queryDataSet === DataSet.METRICS) {
            if (dataSet === DataSet.METRICS) {
                return;
            }
            setDataSet(DataSet.METRICS);
            return;
        }
        if (dataSet === DataSet.EVENTS) {
            return;
        }
        setDataSet(DataSet.EVENTS);
    }
    function handleDataSetChange(newDataSet) {
        router.replace({
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), { dataSet: newDataSet }),
        });
    }
    if (!dataSet) {
        return (<Alert type="error" icon={<IconWarning />}>
        {t('Data set not found.')}
      </Alert>);
    }
    function handleAddWidget(newWidget) {
        onSave(__spreadArray(__spreadArray([], __read(dashboard.widgets)), [newWidget]));
    }
    if ((isEditing && !defined(widgetId)) ||
        (isEditing && defined(widgetId) && !dashboard.widgets[widgetId])) {
        return (<Alert type="error" icon={<IconWarning />}>
        {t('Widget not found.')}
      </Alert>);
    }
    function handleUpdateWidget(nextWidget) {
        if (!widgetId) {
            return;
        }
        var nextList = __spreadArray([], __read(dashboard.widgets));
        nextList[widgetId] = nextWidget;
        onSave(nextList);
    }
    function handleDeleteWidget() {
        if (!widgetId) {
            return;
        }
        var nextList = __spreadArray([], __read(dashboard.widgets));
        nextList.splice(widgetId, 1);
        onSave(nextList);
    }
    if (dataSet === DataSet.EVENTS) {
        return (<EventWidget dashboardTitle={dashboard.title} widget={widget} onAdd={handleAddWidget} onUpdate={handleUpdateWidget} onDelete={handleDeleteWidget} onChangeDataSet={handleDataSetChange} goBackLocation={goBackLocation} isEditing={isEditing}/>);
    }
    return (<MetricWidget organization={organization} router={router} location={location} dashboardTitle={dashboard.title} params={params} goBackLocation={goBackLocation} onChangeDataSet={handleDataSetChange}/>);
}
export default WidgetBuilder;
//# sourceMappingURL=widgetBuilder.jsx.map