import { __read, __spreadArray, __values } from "tslib";
import { mountWithTheme } from 'sentry-test/enzyme';
import { generateFieldAsString } from 'app/utils/discover/fields';
import ArithmeticInput from 'app/views/eventsV2/table/arithmeticInput';
describe('ArithmeticInput', function () {
    var wrapper;
    var query;
    var handleQueryChange;
    var numericColumns;
    var columns;
    var operators = ['+', '-', '*', '/'];
    beforeEach(function () {
        query = '';
        handleQueryChange = function (q) {
            query = q;
        };
        numericColumns = [
            { kind: 'field', field: 'transaction.duration' },
            { kind: 'field', field: 'measurements.lcp' },
            { kind: 'field', field: 'spans.http' },
            { kind: 'function', function: ['p50', '', undefined, undefined] },
            {
                kind: 'function',
                function: ['percentile', 'transaction.duration', '0.25', undefined],
            },
            { kind: 'function', function: ['count', '', undefined, undefined] },
        ];
        columns = __spreadArray(__spreadArray([], __read(numericColumns)), [
            // these columns will not be rendered in the dropdown
            { kind: 'field', field: 'transaction' },
            { kind: 'function', function: ['failure_rate', '', undefined, undefined] },
            { kind: 'equation', field: 'transaction.duration+measurements.lcp' },
        ]);
        wrapper = mountWithTheme(<ArithmeticInput name="refinement" key="parameter:text" type="text" required value={query} onUpdate={handleQueryChange} options={columns}/>);
    });
    afterEach(function () {
        wrapper === null || wrapper === void 0 ? void 0 : wrapper.unmount();
    });
    it('can toggle autocomplete dropdown on focus and blur', function () {
        expect(wrapper.find('TermDropdown').props().isOpen).toBeFalsy();
        // focus the input
        wrapper.find('input').simulate('focus');
        expect(wrapper.find('TermDropdown').props().isOpen).toBeTruthy();
        // blur the input
        wrapper.find('input').simulate('blur');
        expect(wrapper.find('TermDropdown').props().isOpen).toBeFalsy();
    });
    it('renders only numeric options in autocomplete', function () {
        wrapper.find('input').simulate('focus');
        var options = wrapper.find('DropdownListItem');
        expect(options).toHaveLength(numericColumns.length + operators.length);
        options.forEach(function (option, i) {
            if (i < numericColumns.length) {
                expect(option.text()).toEqual(generateFieldAsString(numericColumns[i]));
            }
            else {
                expect(option.text()).toEqual(operators[i - numericColumns.length]);
            }
        });
    });
    it('can use keyboard to select an option', function () {
        var e_1, _a, e_2, _b, e_3, _c, e_4, _d;
        var input = wrapper.find('input');
        input.simulate('focus');
        expect(wrapper.find('DropdownListItem .active').exists()).toBeFalsy();
        try {
            for (var numericColumns_1 = __values(numericColumns), numericColumns_1_1 = numericColumns_1.next(); !numericColumns_1_1.done; numericColumns_1_1 = numericColumns_1.next()) {
                var column = numericColumns_1_1.value;
                input.simulate('keydown', { key: 'ArrowDown' });
                expect(wrapper.find('DropdownListItem .active').text()).toEqual(generateFieldAsString(column));
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (numericColumns_1_1 && !numericColumns_1_1.done && (_a = numericColumns_1.return)) _a.call(numericColumns_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        try {
            for (var operators_1 = __values(operators), operators_1_1 = operators_1.next(); !operators_1_1.done; operators_1_1 = operators_1.next()) {
                var operator = operators_1_1.value;
                input.simulate('keydown', { key: 'ArrowDown' });
                expect(wrapper.find('DropdownListItem .active').text()).toEqual(operator);
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (operators_1_1 && !operators_1_1.done && (_b = operators_1.return)) _b.call(operators_1);
            }
            finally { if (e_2) throw e_2.error; }
        }
        // wrap around to the first option again
        input.simulate('keydown', { key: 'ArrowDown' });
        try {
            for (var _e = __values(__spreadArray([], __read(operators)).reverse()), _f = _e.next(); !_f.done; _f = _e.next()) {
                var operator = _f.value;
                input.simulate('keydown', { key: 'ArrowUp' });
                expect(wrapper.find('DropdownListItem .active').text()).toEqual(operator);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (_f && !_f.done && (_c = _e.return)) _c.call(_e);
            }
            finally { if (e_3) throw e_3.error; }
        }
        try {
            for (var _g = __values(__spreadArray([], __read(numericColumns)).reverse()), _h = _g.next(); !_h.done; _h = _g.next()) {
                var column = _h.value;
                input.simulate('keydown', { key: 'ArrowUp' });
                expect(wrapper.find('DropdownListItem .active').text()).toEqual(generateFieldAsString(column));
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (_h && !_h.done && (_d = _g.return)) _d.call(_g);
            }
            finally { if (e_4) throw e_4.error; }
        }
        // the update is buffered until blur happens
        input.simulate('keydown', { key: 'Enter' });
        expect(query).toEqual('');
        input.simulate('blur');
        expect(query).toEqual(generateFieldAsString(numericColumns[0]) + " ");
    });
    it('can use mouse to select an option', function () {
        var input = wrapper.find('input');
        input.simulate('focus');
        // the update is buffered until blur happens
        wrapper.find('DropdownListItem').first().simulate('click');
        input.simulate('blur');
        expect(query).toEqual(generateFieldAsString(numericColumns[0]) + " ");
    });
    it('autocompletes the current term when it is in the front', function () {
        var input = wrapper.find('input');
        input.simulate('focus');
        var value = 'lcp + transaction.duration';
        input.simulate('change', { target: { value: value } });
        var inputElem = input.getDOMNode();
        inputElem.selectionStart = 2;
        inputElem.selectionEnd = 2;
        input.simulate('change');
        var option = wrapper.find('DropdownListItem');
        expect(option).toHaveLength(1);
        expect(option.text()).toEqual(generateFieldAsString({
            kind: 'field',
            field: 'measurements.lcp',
        }));
        option.simulate('click');
        input.simulate('blur');
        expect(query).toEqual("measurements.lcp  + transaction.duration");
    });
    it('autocompletes the current term when it is in the end', function () {
        var input = wrapper.find('input');
        input.simulate('focus');
        var value = 'transaction.duration + lcp';
        input.simulate('change', { target: { value: value } });
        var inputElem = input.getDOMNode();
        inputElem.selectionStart = value.length - 1;
        inputElem.selectionEnd = value.length - 1;
        input.simulate('change');
        var option = wrapper.find('DropdownListItem');
        expect(option).toHaveLength(1);
        var column = numericColumns.find(function (c) { return c.kind === 'field' && c.field.includes('lcp'); });
        expect(option.text()).toEqual(generateFieldAsString(column));
        option.simulate('click');
        input.simulate('blur');
        expect(query).toEqual("transaction.duration + measurements.lcp ");
    });
});
//# sourceMappingURL=arithmeticInput.spec.jsx.map