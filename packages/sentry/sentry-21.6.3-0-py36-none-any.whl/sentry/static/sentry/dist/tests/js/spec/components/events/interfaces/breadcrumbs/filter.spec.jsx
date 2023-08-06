var _a;
import * as React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import Icon from 'app/components/events/interfaces/breadcrumbs/icon';
import Level from 'app/components/events/interfaces/breadcrumbs/level';
import SearchBarActionFilter from 'app/components/events/interfaces/searchBarAction/searchBarActionFilter';
import { IconFire, IconFix, IconLocation, IconSpan, IconSwitch, IconUser } from 'app/icons';
import { BreadcrumbLevelType, BreadcrumbType } from 'app/types/breadcrumbs';
var options = (_a = {},
    _a['Types'] = [
        {
            id: BreadcrumbType.HTTP,
            description: 'HTTP request',
            symbol: <Icon color="green300" icon={IconSwitch} size="xs"/>,
            isChecked: true,
        },
        {
            id: BreadcrumbType.TRANSACTION,
            description: 'Transaction',
            symbol: <Icon color="pink300" icon={IconSpan} size="xs"/>,
            isChecked: true,
        },
        {
            id: BreadcrumbType.UI,
            description: 'User Action',
            symbol: <Icon color="purple300" icon={IconUser} size="xs"/>,
            isChecked: true,
        },
        {
            id: BreadcrumbType.NAVIGATION,
            description: 'Navigation',
            symbol: <Icon color="green300" icon={IconLocation} size="xs"/>,
            isChecked: true,
        },
        {
            id: BreadcrumbType.DEBUG,
            description: 'Debug',
            symbol: <Icon color="purple300" icon={IconFix} size="xs"/>,
            isChecked: true,
        },
        {
            id: BreadcrumbType.ERROR,
            description: 'Error',
            symbol: <Icon color="red300" icon={IconFire} size="xs"/>,
            isChecked: true,
        },
    ],
    _a['Levels'] = [
        {
            id: BreadcrumbLevelType.INFO,
            symbol: <Level level={BreadcrumbLevelType.INFO}/>,
            isChecked: true,
        },
        {
            id: BreadcrumbLevelType.ERROR,
            symbol: <Level level={BreadcrumbLevelType.ERROR}/>,
            isChecked: true,
        },
    ],
    _a);
describe('SearchBarActionFilter', function () {
    var handleFilter;
    beforeEach(function () {
        handleFilter = jest.fn();
    });
    it('default render', function () {
        var wrapper = mountWithTheme(<SearchBarActionFilter options={options} onChange={handleFilter}/>);
        var filterDropdownMenu = wrapper.find('StyledContent');
        // Headers
        var headers = filterDropdownMenu.find('Header');
        expect(headers).toHaveLength(2);
        expect(headers.at(0).text()).toBe('Types');
        expect(headers.at(1).text()).toBe('Levels');
        // Lists
        var lists = filterDropdownMenu.find('List');
        expect(lists).toHaveLength(2);
        expect(lists.at(0).find('StyledListItem')).toHaveLength(6);
        expect(lists.at(1).find('StyledListItem')).toHaveLength(2);
        expect(wrapper).toSnapshot();
    });
    it('Without Options', function () {
        var wrapper = mountWithTheme(<SearchBarActionFilter options={{}} onChange={handleFilter}/>);
        expect(wrapper.find('Header').exists()).toBe(false);
        expect(wrapper.find('StyledListItem').exists()).toBe(false);
    });
    it('With Option Type only', function () {
        var Types = options.Types;
        var wrapper = mountWithTheme(<SearchBarActionFilter options={{ Types: Types }} onChange={handleFilter}/>);
        var filterDropdownMenu = wrapper.find('StyledContent');
        // Header
        var header = filterDropdownMenu.find('Header');
        expect(header).toHaveLength(1);
        expect(header.text()).toBe('Types');
        // List
        var list = filterDropdownMenu.find('List');
        expect(list).toHaveLength(1);
        // List Items
        var listItems = list.find('StyledListItem');
        expect(listItems).toHaveLength(6);
        var firstItem = listItems.at(0);
        expect(firstItem.find('Description').text()).toBe(options.Types[0].description);
        // Check Item
        expect(firstItem.find('[role="checkbox"]').find('CheckboxFancyContent').props().isChecked).toBeTruthy();
        firstItem.simulate('click');
        expect(handleFilter).toHaveBeenCalledTimes(1);
    });
    it('With Option Level only', function () {
        var Levels = options.Levels;
        var wrapper = mountWithTheme(<SearchBarActionFilter options={{ Levels: Levels }} onChange={handleFilter}/>);
        var filterDropdownMenu = wrapper.find('StyledContent');
        // Header
        var header = filterDropdownMenu.find('Header');
        expect(header).toHaveLength(1);
        expect(header.text()).toBe('Levels');
        // List
        var list = filterDropdownMenu.find('List');
        expect(list).toHaveLength(1);
        // List Items
        var listItems = list.find('StyledListItem');
        expect(listItems).toHaveLength(2);
        var firstItem = listItems.at(0);
        expect(firstItem.text()).toBe(options.Levels[0].id);
        // Check Item
        expect(firstItem.find('[role="checkbox"]').find('CheckboxFancyContent').props().isChecked).toBeTruthy();
        firstItem.simulate('click');
        expect(handleFilter).toHaveBeenCalledTimes(1);
    });
});
//# sourceMappingURL=filter.spec.jsx.map