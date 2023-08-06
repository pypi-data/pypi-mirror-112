import { __assign, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import EditableText from 'app/components/editableText';
import { Title } from 'app/components/layouts/thirds';
import { t } from 'app/locale';
import EventView from 'app/utils/discover/eventView';
import withApi from 'app/utils/withApi';
import { handleUpdateQueryName } from './savedQuery/utils';
var NAME_DEFAULT = t('Untitled query');
/**
 * Allows user to edit the name of the query.
 * By pressing Enter or clicking outside the component, the changes will be saved, if valid.
 */
function EventInputName(_a) {
    var api = _a.api, organization = _a.organization, eventView = _a.eventView, savedQuery = _a.savedQuery;
    function handleChange(nextQueryName) {
        // Do not update automatically if
        // 1) It is a new query
        // 2) The new name is same as the old name
        if (!savedQuery || savedQuery.name === nextQueryName) {
            return;
        }
        // This ensures that we are updating SavedQuery.name only.
        // Changes on QueryBuilder table will not be saved.
        var nextEventView = EventView.fromSavedQuery(__assign(__assign({}, savedQuery), { name: nextQueryName }));
        handleUpdateQueryName(api, organization, nextEventView).then(function (_updatedQuery) {
            // The current eventview may have changes that are not explicitly saved.
            // So, we just preserve them and change its name
            var renamedEventView = eventView.clone();
            renamedEventView.name = nextQueryName;
            browserHistory.push(renamedEventView.getResultsViewUrlTarget(organization.slug));
        });
    }
    var value = eventView.name || NAME_DEFAULT;
    return (<StyledTitle data-test-id={"discover2-query-name-" + value}>
      <EditableText value={value} onChange={handleChange} isDisabled={!eventView.id} errorMessage={t('Please set a name for this query')}/>
    </StyledTitle>);
}
var StyledTitle = styled(Title)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: unset;\n"], ["\n  overflow: unset;\n"])));
export default withApi(EventInputName);
var templateObject_1;
//# sourceMappingURL=eventInputName.jsx.map