import { createContext } from 'react';
/**
 * Default to undefined to preserve backwards compatibility.
 * The FormField component uses a truthy test to see if it is connected
 * to context or if the control is 'uncontrolled'.
 */
var FormContext = createContext({});
export default FormContext;
//# sourceMappingURL=formContext.jsx.map