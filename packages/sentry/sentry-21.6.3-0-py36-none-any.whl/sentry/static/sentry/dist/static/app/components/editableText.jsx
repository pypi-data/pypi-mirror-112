import { __makeTemplateObject, __read } from "tslib";
import { useCallback, useEffect, useRef, useState } from 'react';
import * as React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import TextOverflow from 'app/components/textOverflow';
import { IconEdit } from 'app/icons/iconEdit';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import useKeypress from 'app/utils/useKeyPress';
import useOnClickOutside from 'app/utils/useOnClickOutside';
import Input from 'app/views/settings/components/forms/controls/input';
function EditableText(_a) {
    var value = _a.value, onChange = _a.onChange, name = _a.name, errorMessage = _a.errorMessage, successMessage = _a.successMessage, _b = _a.isDisabled, isDisabled = _b === void 0 ? false : _b;
    var _c = __read(useState(false), 2), isEditing = _c[0], setIsEditing = _c[1];
    var _d = __read(useState(value), 2), inputValue = _d[0], setInputValue = _d[1];
    var isEmpty = !inputValue.trim();
    var innerWrapperRef = useRef(null);
    var labelRef = useRef(null);
    var inputRef = useRef(null);
    var enter = useKeypress('Enter');
    var esc = useKeypress('Escape');
    function revertValueAndCloseEditor() {
        if (value !== inputValue) {
            setInputValue(value);
        }
        if (isEditing) {
            setIsEditing(false);
        }
    }
    // check to see if the user clicked outside of this component
    useOnClickOutside(innerWrapperRef, function () {
        if (isEditing) {
            if (isEmpty) {
                displayStatusMessage('error');
                return;
            }
            if (inputValue !== value) {
                onChange(inputValue);
                displayStatusMessage('success');
            }
            setIsEditing(false);
        }
    });
    var onEnter = useCallback(function () {
        if (enter) {
            if (isEmpty) {
                displayStatusMessage('error');
                return;
            }
            if (inputValue !== value) {
                onChange(inputValue);
                displayStatusMessage('success');
            }
            setIsEditing(false);
        }
    }, [enter, inputValue, onChange]);
    var onEsc = useCallback(function () {
        if (esc) {
            revertValueAndCloseEditor();
        }
    }, [esc]);
    useEffect(function () {
        revertValueAndCloseEditor();
    }, [isDisabled, value]);
    // focus the cursor in the input field on edit start
    useEffect(function () {
        if (isEditing) {
            var inputElement = inputRef.current;
            if (defined(inputElement)) {
                inputElement.focus();
            }
        }
    }, [isEditing]);
    useEffect(function () {
        if (isEditing) {
            // if Enter is pressed, save the value and close the editor
            onEnter();
            // if Escape is pressed, revert the value and close the editor
            onEsc();
        }
    }, [onEnter, onEsc, isEditing]); // watch the Enter and Escape key presses
    function displayStatusMessage(status) {
        if (status === 'error') {
            if (errorMessage) {
                addErrorMessage(errorMessage);
            }
            return;
        }
        if (successMessage) {
            addSuccessMessage(successMessage);
        }
    }
    function handleInputChange(event) {
        setInputValue(event.target.value);
    }
    function handleEditClick() {
        setIsEditing(true);
    }
    return (<Wrapper isDisabled={isDisabled} isEditing={isEditing}>
      {isEditing ? (<InputWrapper ref={innerWrapperRef} isEmpty={isEmpty} data-test-id="editable-text-input">
          <StyledInput name={name} ref={inputRef} value={inputValue} onChange={handleInputChange}/>
          <InputLabel>{inputValue}</InputLabel>
        </InputWrapper>) : (<Label onClick={isDisabled ? undefined : handleEditClick} ref={labelRef} data-test-id="editable-text-label">
          <InnerLabel>{inputValue}</InnerLabel>
          {!isDisabled && <IconEdit />}
        </Label>)}
    </Wrapper>);
}
export default EditableText;
var Label = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n  cursor: pointer;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n  cursor: pointer;\n"])), space(1));
var InnerLabel = styled(TextOverflow)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-top: 1px solid transparent;\n  border-bottom: 1px dotted ", ";\n"], ["\n  border-top: 1px solid transparent;\n  border-bottom: 1px dotted ", ";\n"])), function (p) { return p.theme.gray200; });
var InputWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-block;\n  background: ", ";\n  border-radius: ", ";\n  margin: -", " -", ";\n  max-width: calc(100% + ", ");\n"], ["\n  display: inline-block;\n  background: ", ";\n  border-radius: ", ";\n  margin: -", " -", ";\n  max-width: calc(100% + ", ");\n"])), function (p) { return p.theme.gray100; }, function (p) { return p.theme.borderRadius; }, space(0.5), space(1), space(2));
var StyledInput = styled(Input)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  border: none !important;\n  background: transparent;\n  height: auto;\n  min-height: 34px;\n  padding: ", " ", ";\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    box-shadow: none;\n  }\n"], ["\n  border: none !important;\n  background: transparent;\n  height: auto;\n  min-height: 34px;\n  padding: ", " ", ";\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    box-shadow: none;\n  }\n"])), space(0.5), space(1));
var InputLabel = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  height: 0;\n  opacity: 0;\n  white-space: pre;\n  padding: 0 ", ";\n"], ["\n  height: 0;\n  opacity: 0;\n  white-space: pre;\n  padding: 0 ", ";\n"])), space(1));
var Wrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n\n  ", "\n"], ["\n  display: flex;\n\n  ", "\n"])), function (p) {
    return p.isDisabled &&
        "\n      " + InnerLabel + " {\n        border-bottom-color: transparent;\n      }\n    ";
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=editableText.jsx.map