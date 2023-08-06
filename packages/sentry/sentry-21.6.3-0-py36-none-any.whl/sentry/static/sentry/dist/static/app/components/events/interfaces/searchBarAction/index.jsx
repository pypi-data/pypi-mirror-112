import { __makeTemplateObject } from "tslib";
import { Children } from 'react';
import styled from '@emotion/styled';
import SearchBar from 'app/components/searchBar';
import space from 'app/styles/space';
function SearchBarAction(_a) {
    var onChange = _a.onChange, query = _a.query, placeholder = _a.placeholder, filter = _a.filter, className = _a.className;
    return (<Wrapper className={className}>
      {filter}
      <StyledSearchBar onChange={onChange} query={query} placeholder={placeholder} blendWithFilter={!!filter}/>
    </Wrapper>);
}
export default SearchBarAction;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  width: 100%;\n  margin-top: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    grid-gap: 0;\n    grid-template-columns: ", ";\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    width: 400px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  width: 100%;\n  margin-top: ", ";\n  position: relative;\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    grid-gap: 0;\n    grid-template-columns: ", ";\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    width: 400px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), space(2), space(1), function (props) { return props.theme.breakpoints[0]; }, function (p) {
    return p.children && Children.toArray(p.children).length === 1
        ? '1fr'
        : 'max-content 1fr';
}, function (props) { return props.theme.breakpoints[1]; }, function (props) { return props.theme.breakpoints[3]; });
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 100%;\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    ", "\n  }\n"], ["\n  width: 100%;\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    ", "\n  }\n"])), function (props) { return props.theme.breakpoints[0]; }, function (p) {
    return p.blendWithFilter &&
        "\n        .search-input,\n        .search-input:focus {\n          border-top-left-radius: 0;\n          border-bottom-left-radius: 0;\n        }\n      ";
});
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map