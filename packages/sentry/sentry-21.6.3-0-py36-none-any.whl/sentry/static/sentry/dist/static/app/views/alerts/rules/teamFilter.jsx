import { __makeTemplateObject, __read, __spreadArray } from "tslib";
import { useState } from 'react';
import styled from '@emotion/styled';
import Input from 'app/components/forms/input';
import { t } from 'app/locale';
import Filter from './filter';
var ALERT_LIST_QUERY_DEFAULT_TEAMS = ['myteams', 'unassigned'];
export function getTeamParams(team) {
    if (team === undefined) {
        return ALERT_LIST_QUERY_DEFAULT_TEAMS;
    }
    if (team === '') {
        return [];
    }
    if (Array.isArray(team)) {
        return team;
    }
    return [team];
}
function TeamFilter(_a) {
    var teams = _a.teams, selectedTeams = _a.selectedTeams, _b = _a.showStatus, showStatus = _b === void 0 ? false : _b, _c = _a.selectedStatus, selectedStatus = _c === void 0 ? new Set() : _c, handleChangeFilter = _a.handleChangeFilter;
    var _d = __read(useState(), 2), teamFilterSearch = _d[0], setTeamFilterSearch = _d[1];
    var statusOptions = [
        {
            label: t('Unresolved'),
            value: 'open',
            checked: selectedStatus.has('open'),
            filtered: false,
        },
        {
            label: t('Resolved'),
            value: 'closed',
            checked: selectedStatus.has('closed'),
            filtered: false,
        },
    ];
    var additionalOptions = [
        {
            label: t('My Teams'),
            value: 'myteams',
            checked: selectedTeams.has('myteams'),
            filtered: false,
        },
        {
            label: t('Unassigned'),
            value: 'unassigned',
            checked: selectedTeams.has('unassigned'),
            filtered: false,
        },
    ];
    var teamItems = teams.map(function (_a) {
        var id = _a.id, name = _a.name;
        return ({
            label: name,
            value: id,
            filtered: teamFilterSearch
                ? !name.toLowerCase().includes(teamFilterSearch.toLowerCase())
                : false,
            checked: selectedTeams.has(id),
        });
    });
    return (<Filter header={<StyledInput autoFocus placeholder={t('Filter by team name')} onClick={function (event) {
                event.stopPropagation();
            }} onChange={function (event) {
                setTeamFilterSearch(event.target.value);
            }} value={teamFilterSearch || ''}/>} onFilterChange={handleChangeFilter} dropdownSections={__spreadArray(__spreadArray([], __read((showStatus
            ? [
                {
                    id: 'status',
                    label: t('Status'),
                    items: statusOptions,
                },
            ]
            : []))), [
            {
                id: 'teams',
                label: t('Teams'),
                items: __spreadArray(__spreadArray([], __read(additionalOptions)), __read(teamItems)),
            },
        ])}/>);
}
export default TeamFilter;
var StyledInput = styled(Input)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border: none;\n  border-bottom: 1px solid ", ";\n  border-radius: 0;\n"], ["\n  border: none;\n  border-bottom: 1px solid ", ";\n  border-radius: 0;\n"])), function (p) { return p.theme.gray200; });
var templateObject_1;
//# sourceMappingURL=teamFilter.jsx.map