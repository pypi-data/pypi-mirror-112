import Alert from 'app/components/alert';
import Button from 'app/components/button';
import LoadingError from 'app/components/loadingError';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
function ErrorMessage(_a) {
    var _b, _c;
    var error = _a.error, groupId = _a.groupId, onRetry = _a.onRetry;
    function getErrorMessage(errorCode) {
        switch (errorCode) {
            case 'merged_issues':
                return {
                    title: t('An issue can only contain one fingerprint'),
                    subTitle: t('This issue needs to be fully unmerged before grouping levels can be shown'),
                };
            case 'missing_feature':
                return {
                    title: t('This project does not have the grouping tree feature'),
                };
            case 'no_events':
                return {
                    title: t('This issue has no events'),
                };
            case 'not_hierarchical':
                return {
                    title: t('This issue does not have hierarchical grouping'),
                };
            default:
                return undefined;
        }
    }
    if (typeof error === 'string') {
        return <Alert type="warning">{error}</Alert>;
    }
    if (error.status === 403 && ((_b = error.responseJSON) === null || _b === void 0 ? void 0 : _b.detail)) {
        var _d = error.responseJSON.detail, code = _d.code, message = _d.message;
        var errorMessage = getErrorMessage(code);
        return (<Panel>
        <EmptyMessage size="large" title={(_c = errorMessage === null || errorMessage === void 0 ? void 0 : errorMessage.title) !== null && _c !== void 0 ? _c : message} description={errorMessage === null || errorMessage === void 0 ? void 0 : errorMessage.subTitle} action={code === 'merged_issues' ? (<Button priority="primary" to={"/organizations/sentry/issues/" + groupId + "/merged/?" + location.search}>
                {t('Unmerge issue')}
              </Button>) : undefined}/>
      </Panel>);
    }
    return (<LoadingError message={t('Unable to load grouping levels, please try again later')} onRetry={onRetry}/>);
}
export default ErrorMessage;
//# sourceMappingURL=errorMessage.jsx.map