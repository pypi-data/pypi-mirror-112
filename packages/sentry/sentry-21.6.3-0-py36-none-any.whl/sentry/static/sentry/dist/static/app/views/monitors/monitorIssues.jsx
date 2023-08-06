import IssueList from 'app/components/issueList';
import { t } from 'app/locale';
var MonitorIssues = function (_a) {
    var orgId = _a.orgId, monitor = _a.monitor;
    return (<IssueList endpoint={"/organizations/" + orgId + "/issues/"} query={{
            query: 'monitor.id:"' + monitor.id + '"',
            project: monitor.project.id,
            limit: 5,
        }} pagination={false} emptyText={t('No issues found')} noBorder noMargin/>);
};
export default MonitorIssues;
//# sourceMappingURL=monitorIssues.jsx.map